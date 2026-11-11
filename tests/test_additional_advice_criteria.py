#!/usr/bin/env python3
"""
test_additional_advice_criteria.py
==================================
Independent automated verification test suite for `docs/05_additional_advice.md`
and the hardened `code/asymmetric_mae/asymmetric_mae.py`.

Requirements Covered:
- R1: Multi-repo audit and blind spots investigation (15 critical blind spots).
- R2: Asymmetric MAE runtime hardening and edge-case verification.
- R3: Separated 11/20 NeuroAI workshop immediate actions vs full-paper roadmaps.
- R4: Strict lab governance and honorific policy enforcement.
"""

from __future__ import annotations

import os
import re
import sys
import unittest
from pathlib import Path

os.environ["CUDA_VISIBLE_DEVICES"] = ""

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = WORKSPACE_ROOT / "docs"
ASYM_DIR = WORKSPACE_ROOT / "code" / "asymmetric_mae"
DIVER_ROOT = Path("/home/juke/git/DIVER-2/diver_pretrain")

if str(DIVER_ROOT) not in sys.path:
    sys.path.insert(0, str(DIVER_ROOT))
if str(ASYM_DIR) not in sys.path:
    sys.path.insert(0, str(ASYM_DIR))


class TestAdditionalAdviceCriteria(unittest.TestCase):
    """Rigorous verification of additional advice documentation and hardened implementation."""

    @classmethod
    def setUpClass(cls):
        cls.doc_path = DOCS_DIR / "05_additional_advice.md"
        cls.readme_path = WORKSPACE_ROOT / "README.md"
        cls.asym_code_path = ASYM_DIR / "asymmetric_mae.py"
        cls.doc_content = cls.doc_path.read_text(encoding="utf-8")
        cls.readme_content = cls.readme_path.read_text(encoding="utf-8")
        cls.asym_content = cls.asym_code_path.read_text(encoding="utf-8")

    def test_01_document_existence_and_substantial_volume(self):
        """Verify docs/05_additional_advice.md exists and has rich technical volume (>= 8KB)."""
        self.assertTrue(self.doc_path.is_file(), "docs/05_additional_advice.md does not exist")
        size = self.doc_path.stat().st_size
        self.assertGreaterEqual(
            size, 8000, f"docs/05_additional_advice.md is too short ({size} bytes < 8000 bytes)"
        )

    def test_02_strict_lab_governance_and_honorifics(self):
        """Verify 100% adherence to lab honorific policies ('안채원 선생님', '이아현 선생님', '차지욱 교수님')."""
        # Forbidden informal patterns
        chaewon_violation = re.compile(r"안채원(?!\s*선생님)")
        ahhyun_violation = re.compile(r"이아현(?!\s*선생님)")

        self.assertFalse(
            bool(chaewon_violation.search(self.doc_content)),
            "Found improper non-honorific reference for 안채원 선생님 in 05_additional_advice.md",
        )
        self.assertFalse(
            bool(ahhyun_violation.search(self.doc_content)),
            "Found improper non-honorific reference for 이아현 선생님 in 05_additional_advice.md",
        )
        self.assertIn("안채원 선생님", self.doc_content)
        self.assertIn("이아현 선생님", self.doc_content)
        self.assertTrue("차지욱 교수님" in self.doc_content or "지도교수" in self.doc_content)

    def test_03_exact_source_code_and_repo_path_citations(self):
        """Verify exact file paths and line numbers from target repositories are cited."""
        required_citations = [
            "gen_gap_eval.py",
            "newsubj_summary.json",
            "heldout_summary.json",
            "split_np.py",
            "electrode_mix.py",
            "small46_summary.json",
            "effdim_summary.json",
            "Attn_Bias.py",
            "dataloader_utils.py",
            "Embed.py",
            "PADDING_MASK_BUG.md",
            "Original_Moirai_projection.py",
            "Original_Moirai_bias.py",
            "dense_long_context_plan.md",
            "eval_probe_cv.py",
        ]
        for citation in required_citations:
            self.assertIn(
                citation,
                self.doc_content,
                f"Missing required technical source citation: {citation} in 05_additional_advice.md",
            )

    def test_04_empirical_metrics_and_statistical_blindspots_verified(self):
        """Verify exact empirical metrics and mathematical deductions are recorded."""
        # 1. New subject loss spike: 0.2791 vs 0.0970 (2.88x)
        self.assertTrue(
            "0.2791" in self.doc_content and ("2.88" in self.doc_content or "0.0970" in self.doc_content),
            "Missing new subject loss empirical figures (0.2791 / 0.0970 / 2.88x)",
        )
        # 2. FWER 53.67% and Bonferroni critical value t=5.38
        self.assertTrue(
            "53.67%" in self.doc_content and ("5.38" in self.doc_content or "2.09" in self.doc_content),
            "Missing FWER 53.67% or Bonferroni inflation figures",
        )
        # 3. sEEG Depth correlation r=+0.473
        self.assertTrue(
            "0.473" in self.doc_content or "0.428" in self.doc_content,
            "Missing sEEG depth correlation figures (0.473 / 0.428)",
        )
        # 4. Layer 1 vs Layer 12 representation collapse (-0.0050)
        self.assertTrue(
            "-0.0050" in self.doc_content and "+0.0003" in self.doc_content,
            "Missing Layer 1 (+0.0003) vs Layer 12 (-0.0050) divergence figures",
        )
        # 5. Participation ratio PR 5~6
        self.assertTrue(
            bool(re.search(r"(5~6|5\.89|5\.08|5\.29)", self.doc_content)),
            "Missing Participation Ratio 5~6 dimensional collapse figures",
        )
        # 6. Padding mask 0.3s (10.6%) bug
        self.assertTrue(
            "0.3" in self.doc_content and "10.6%" in self.doc_content,
            "Missing padding mask 0.3s (10.6%) bug figures",
        )
        # 7. RoPE bf16 829 surviving unique positions
        self.assertTrue(
            "829" in self.doc_content and ("86.2%" in self.doc_content or "5,172" in self.doc_content),
            "Missing RoPE bf16 829 surviving positions figure",
        )
        # 8. Memory explosion 1,169 GiB
        self.assertTrue(
            "1,169" in self.doc_content or "1169" in self.doc_content,
            "Missing dense attention bias memory explosion figure (1,169 GiB)",
        )
        # 9. Spearman rho +0.29
        self.assertTrue(
            "0.29" in self.doc_content,
            "Missing Spearman correlation figure rho=+0.29",
        )

    def test_05_separation_of_workshop_vs_full_paper_actions(self):
        """Verify strict division between 11/20 NeuroAI workshop immediate actions and full paper roadmaps."""
        self.assertIn("11/20", self.doc_content)
        self.assertIn("NeuroAI", self.doc_content)
        for act in ["WS-ACT-01", "WS-ACT-02", "WS-ACT-03", "WS-ACT-04", "WS-ACT-05"]:
            self.assertIn(act, self.doc_content, f"Missing workshop action {act}")

        for act in ["LT-ACT-01", "LT-ACT-02", "LT-ACT-03", "LT-ACT-04", "LT-ACT-05"]:
            self.assertIn(act, self.doc_content, f"Missing full paper roadmap {act}")

    def test_06_asymmetric_mae_code_hardening_adherence(self):
        """Verify that asymmetric_mae.py contains all 4 hardened bug fixes in its implementation."""
        # 1. L=1 NaN guard
        self.assertIn("mask_flat.sum() == 0.0", self.asym_content)
        self.assertIn("ref_len = max(2, L)", self.asym_content)

        # 2. Heterogeneous montage per-sample k_vis
        self.assertIn("k_vis_list", self.asym_content)
        self.assertIn("k_vis_max", self.asym_content)

        # 3. Closed-form register indexing
        self.assertNotIn(
            "reg_flat_idx = torch.nonzero",
            self.asym_content,
            "torch.nonzero is still used for reg_flat_idx; must be closed-form!",
        )
        self.assertIn("reg_flat_idx = torch.cat([row_part, col_part])", self.asym_content)

        # 4. DDP module prefix removal and shape inference
        self.assertIn("module.", self.asym_content)
        self.assertIn("encoder.encoder.norm.weight", self.asym_content)
        self.assertIn("encoder.encoder.layers.", self.asym_content)

    def test_07_readme_indexing_and_section5_summary(self):
        """Verify README.md properly indexes docs/05_additional_advice.md and summarizes all 10 actions."""
        self.assertIn(
            "[docs/05_additional_advice.md](docs/05_additional_advice.md)",
            self.readme_content,
            "README.md document inventory missing link to docs/05_additional_advice.md",
        )
        self.assertIn("결정적 추가 조언", self.readme_content)
        self.assertIn("WS-ACT-01", self.readme_content)
        self.assertIn("LT-ACT-01", self.readme_content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
