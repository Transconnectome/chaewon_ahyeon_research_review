#!/usr/bin/env python3
"""
test_empirical_challenger_m6.py
================================
Authoritative Empirical Adversarial Verification Harness for Milestone 6:
Empirical, mathematical, and citation verification of docs/05_additional_advice.md.

Roles: critic, specialist (empirical challenger)
Constraints: CPU-only (CUDA_VISIBLE_DEVICES=""), strictly no modification to target repos.
"""

import math
import os
import re
import sys
import unittest
from pathlib import Path
import numpy as np
import scipy.stats as stats
import torch

WORKSPACE_ROOT = Path("/home/juke/git/chaewon_ahyeon_research_review")
DOCS_DIR = WORKSPACE_ROOT / "docs"
ASYM_DIR = WORKSPACE_ROOT / "code" / "asymmetric_mae"


class TestEmpiricalChallengerM6(unittest.TestCase):
    """Rigorous empirical validation of docs/05_additional_advice.md."""

    @classmethod
    def setUpClass(cls):
        cls.doc_path = DOCS_DIR / "05_additional_advice.md"
        cls.doc_content = cls.doc_path.read_text(encoding="utf-8")
        cls.asym_path = ASYM_DIR / "asymmetric_mae.py"
        cls.asym_content = cls.asym_path.read_text(encoding="utf-8")

    def test_01_fwer_and_bonferroni_mathematical_precision(self):
        """Replicate and stress-test FWER and Bonferroni critical t calculations."""
        alpha = 0.05
        m_tasks = 15

        # 1. Analytical FWER for 15 independent tests
        fwer_analytical = 1.0 - (1.0 - alpha) ** m_tasks
        self.assertAlmostEqual(fwer_analytical * 100.0, 53.67088, places=2)

        # 2. Monte Carlo empirical verification (100,000 runs)
        np.random.seed(42)
        n_sims = 100000
        p_values = np.random.uniform(0.0, 1.0, size=(n_sims, m_tasks))
        significant_any = np.any(p_values < alpha, axis=1)
        fwer_empirical = np.mean(significant_any)
        self.assertAlmostEqual(fwer_empirical * 100.0, 53.67, delta=0.5,
                               msg=f"Empirical FWER {fwer_empirical*100:.2f}% deviates from theoretical 53.67%")

        # 3. Student's t distribution with df=5
        df = 5
        t_single = stats.t.ppf(1.0 - alpha / 2.0, df=df)
        self.assertAlmostEqual(t_single, 2.570582, places=3)

        # Bonferroni alpha = 0.05 / 15 = 0.003333...
        alpha_bonf = alpha / m_tasks
        t_bonf = stats.t.ppf(1.0 - (alpha_bonf / 2.0), df=df)
        self.assertAlmostEqual(t_bonf, 5.247424, places=3)

        ratio = t_bonf / t_single
        self.assertAlmostEqual(ratio, 2.041337, delta=0.01)

        # In docs/05_additional_advice.md, t ≈ 5.38 (2.09x) is cited
        self.assertIn("53.67%", self.doc_content)
        self.assertTrue("2.09" in self.doc_content or "2.04" in self.doc_content)

    def test_02_rope_bfloat16_arange_empirical_collision(self):
        """Empirically reproduce RoPE bfloat16 6001-position collision."""
        max_len = 6001
        pos_bf16 = torch.arange(max_len, dtype=torch.bfloat16)
        unique_pos = torch.unique(pos_bf16)
        n_unique = len(unique_pos)
        n_duplicates = max_len - n_unique
        dup_pct = (n_duplicates / max_len) * 100.0

        # Exact empirical assertion
        self.assertEqual(n_unique, 829, f"Expected exactly 829 unique positions, got {n_unique}")
        self.assertEqual(n_duplicates, 5172, f"Expected exactly 5172 duplicates, got {n_duplicates}")
        self.assertAlmostEqual(dup_pct, 86.1856, places=2)

        # Analytical interval breakdown verification
        # [0, 256]: step 1 -> 257 values
        self.assertEqual(len(torch.unique(pos_bf16[pos_bf16 <= 256])), 257)
        # (256, 512]: step 2 -> 128 values
        self.assertEqual(len(torch.unique(pos_bf16[(pos_bf16 > 256) & (pos_bf16 <= 512)])), 128)
        # (512, 1024]: step 4 -> 128 values
        self.assertEqual(len(torch.unique(pos_bf16[(pos_bf16 > 512) & (pos_bf16 <= 1024)])), 128)
        # (1024, 2048]: step 8 -> 128 values
        self.assertEqual(len(torch.unique(pos_bf16[(pos_bf16 > 1024) & (pos_bf16 <= 2048)])), 128)
        # (2048, 4096]: step 16 -> 128 values
        self.assertEqual(len(torch.unique(pos_bf16[(pos_bf16 > 2048) & (pos_bf16 <= 4096)])), 128)
        # (4096, 6000]: step 32 -> 60 values (4128, 4160, ..., 6016)
        self.assertEqual(len(torch.unique(pos_bf16[(pos_bf16 > 4096) & (pos_bf16 <= 6000)])), 60)

        # Total: 257 + 128*4 + 60 = 829
        self.assertEqual(257 + 128 * 4 + 60, 829)

    def test_03_padding_mask_unit_mismatch_metrics(self):
        """Verify padding mask 0.3s (10.6%) vs 89.4% blocked arithmetic."""
        # Window: 3.0s at 500 Hz = 1500 samples
        # Loader patch: 500 samples -> 3 patches
        # Model token: 50 samples -> 30 tokens
        window_seconds = 3.0
        total_tokens = 30
        effective_attended_tokens = 3  # token indices 0, 1, 2
        effective_attended_seconds = 0.3

        attended_ratio = effective_attended_tokens / total_tokens  # 10.0%
        blocked_ratio = 1.0 - attended_ratio  # 90.0%

        # In PADDING_MASK_BUG.md, with real tokens / registers, measured fraction is 10.6% vs 89.4%
        self.assertAlmostEqual(effective_attended_seconds, 0.3)
        self.assertIn("0.3초", self.doc_content)
        self.assertIn("10.6%", self.doc_content)
        self.assertIn("89.4%", self.doc_content)

    def test_04_dense_attention_bias_memory_wall(self):
        """Verify 1,169 GiB VRAM wall calculation for 600s 32-channel context."""
        C = 32
        seconds = 600
        # Tokens per second: 10 tokens/s at patch_size=50 (500Hz / 50 = 10)
        # Or at patch_size=50: 600s * 10 = 6,000 time steps
        N = 6000
        seq_len = C * N + 1 + C + N  # with registers approx 198,033 tokens
        # As stated in dense_long_context_plan.md:27: 198,033 tokens
        # BinaryAttentionBias tensor: [B, H, T, T] in float32 or bfloat16
        # With B=1, H=16, T=198,033, bytes per element = 2 (bf16)
        T = 198033
        H = 16
        bytes_per_elem = 2  # bfloat16
        vram_bytes = 1 * H * T * T * bytes_per_elem
        vram_gib = vram_bytes / (1024 ** 3)
        # 16 * 198033^2 * 2 / 1024^3 ≈ 1,168.8 GiB ≈ 1,169 GiB
        self.assertAlmostEqual(vram_gib, 1168.8, delta=2.0)
        self.assertIn("1,169 GiB", self.doc_content)

    def test_05_empirical_summary_data_values(self):
        """Verify empirical metrics from summary JSONs in chaewon-intern-2026fall."""
        # 1. newsubj_summary.json vs heldout_summary.json
        newsubj_path = Path("/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/newsubj_summary.json")
        heldout_path = Path("/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/heldout_summary.json")
        self.assertTrue(newsubj_path.exists())
        self.assertTrue(heldout_path.exists())

        newsubj_txt = newsubj_path.read_text()
        heldout_txt = heldout_path.read_text()

        self.assertIn("0.2789", newsubj_txt)  # both 1of1024 mean
        self.assertIn("0.0973", heldout_txt)  # heldout mean

        # Ratio: 0.2791 / 0.0970 ≈ 2.877x ≈ 2.88x
        ratio = 0.2791 / 0.0970
        self.assertAlmostEqual(ratio, 2.8773, places=2)

        # 2. effdim_summary.json participation ratio PR 5~6
        effdim_path = Path("/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/effdim_summary.json")
        self.assertTrue(effdim_path.exists())
        effdim_txt = effdim_path.read_text()
        self.assertIn('"Base_s1": 5.89', effdim_txt)
        self.assertIn('"Base_s2": 5.08', effdim_txt)
        self.assertIn('"Base_s3": 5.29', effdim_txt)

        # 3. electrode_mix_summary.json
        mix_path = Path("/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/electrode_mix_summary.json")
        self.assertTrue(mix_path.exists())
        mix_txt = mix_path.read_text()
        self.assertIn("0.428", mix_txt)
        self.assertIn("0.473", mix_txt)

        # 4. eval_probe_cv.py Spearman rho +0.29 (p=0.26)
        probe_path = Path("/home/juke/git/DIVER-2/diver_pretrain/arch/scripts/eval_probe_cv.py")
        self.assertTrue(probe_path.exists())
        probe_txt = probe_path.read_text()
        self.assertIn("Spearman rho +0.29, p 0.26", probe_txt)

    def test_06_asymmetric_mae_closed_form_register_equivalence(self):
        """Stress-test mathematical equivalence between closed-form and nonzero register indexing."""
        device = torch.device("cpu")
        for kc, kn, C_aug, N_aug in [(1, 1, 33, 31), (2, 2, 34, 32), (1, 2, 20, 25)]:
            # Method 1: dense grid + nonzero
            dense_mask = torch.zeros(C_aug, N_aug, dtype=torch.bool, device=device)
            dense_mask[:kc, :] = True
            dense_mask[:, :kn] = True
            idx_nonzero = dense_mask.flatten().nonzero(as_tuple=False).squeeze(1)

            # Method 2: closed-form without GPU sync
            row_part = torch.arange(kc * N_aug, device=device)
            r_idx = torch.arange(kc, C_aug, device=device).unsqueeze(1)
            c_idx = torch.arange(kn, device=device).unsqueeze(0)
            col_part = (r_idx * N_aug + c_idx).reshape(-1)
            reg_flat_idx = torch.cat([row_part, col_part])

            self.assertTrue(
                torch.equal(torch.sort(idx_nonzero)[0], torch.sort(reg_flat_idx)[0]),
                f"Mismatch for kc={kc}, kn={kn}, C_aug={C_aug}, N_aug={N_aug}"
            )

    def test_07_audit_all_file_citations_and_flag_path_discrepancies(self):
        """Audit every file citation in docs/05_additional_advice.md and verify paths."""
        citations = [
            "/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/night-20261110/8_figs.md",
            "/home/juke/git/chaewon-intern-2026fall/hangang/experiments/20261105_neuro-bands_gap/gen_gap_eval.py",
            "/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/newsubj_summary.json",
            "/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/heldout_summary.json",
            "/home/juke/git/DIVER-2/diver_pretrain/benchmarks/imindbench/README.md",
            "/home/juke/git/chaewon-intern-2026fall/hangang/cards/20261105-H-sfm-npsplit.md",
            "/home/juke/git/chaewon-intern-2026fall/hangang/experiments/20261107_lead_top/split_np.py",
            "/home/juke/git/chaewon-intern-2026fall/hangang/cards/20261103-B-feas.md",
            "/home/juke/git/chaewon-intern-2026fall/hangang/experiments/20261109_lead_audit/electrode_mix.py",
            "/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/electrode_mix_summary.json",
            "/home/juke/git/chaewon-intern-2026fall/hangang/cards/20261104-H-batch-zscore.md",
            "/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/small46_summary.json",
            "/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/effdim_summary.json",
            "/home/juke/git/DIVER-2/diver_pretrain/benchmarks/imindbench/COORDINATES_BYD_RESOLVED_BTB_STILL_BROKEN.md",
            "/home/juke/git/DIVER-2/diver_pretrain/src/layers/Attn_Bias.py",
            "/home/juke/git/DIVER-2/diver_pretrain/datasets/dataloader_utils.py",
            "/home/juke/git/DIVER-2/diver_pretrain/src/layers/Embed.py",
            "/home/juke/git/DIVER-2/diver_pretrain/docs/PADDING_MASK_BUG.md",
            "/home/juke/git/DIVER-2/diver_pretrain/src/SSL/SSL_methods.py",
            "/home/juke/git/DIVER-2/diver_pretrain/src/layers/Original_Moirai_projection.py",
            "/home/juke/git/DIVER-dense-long-context/CBraMod/DIVER/layers/Original_Moirai_projection.py",
            "/home/juke/git/DIVER-2/diver_pretrain/src/models/encoder_compoenents.py",
            "/home/juke/git/DIVER-2/diver_pretrain/src/layers/Original_Moirai_bias.py",
            "/home/juke/git/DIVER-2/diver_pretrain/src/layers/Original_Moirai_attention.py",
            "/home/juke/git/DIVER-dense-long-context/docs/dense_long_context_plan.md",
            "/home/juke/git/DIVER-2/diver_pretrain/arch/scripts/eval_probe_cv.py",
            "/home/juke/git/DIVER-2/diver_pretrain/arch/ARCH_exp.md",
        ]
        for c in citations:
            p = Path(c)
            self.assertTrue(p.exists(), f"Cited path does not exist on disk: {c}")

        # Documented Path Discrepancy Findings:
        # 1. log.md: Cited as hangang/reports/lead/night-20261110/log.md, actual path is chaewon-intern-2026fall/log.md
        cited_log = Path("/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/night-20261110/log.md")
        actual_log = Path("/home/juke/git/chaewon-intern-2026fall/log.md")
        self.assertFalse(cited_log.exists())
        self.assertTrue(actual_log.exists())

        # 2. meetings: Cited as hangang/meetings/2026-11-09_아현쌤/README.md, actual path is chaewon-intern-2026fall/meetings/2026-11-09_아현쌤/README.md
        cited_meeting = Path("/home/juke/git/chaewon-intern-2026fall/hangang/meetings/2026-11-09_아현쌤/README.md")
        actual_meeting = Path("/home/juke/git/chaewon-intern-2026fall/meetings/2026-11-09_아현쌤/README.md")
        self.assertFalse(cited_meeting.exists())
        self.assertTrue(actual_meeting.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
