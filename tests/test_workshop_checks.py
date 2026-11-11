#!/usr/bin/env python3
"""
test_workshop_checks.py
=======================
Automated unit tests for `code/workshop_checks/` and
`docs/06_student_friendly_guide_and_solutions.md`.
"""
from __future__ import annotations

import os
import re
import sys
import unittest
from pathlib import Path

import numpy as np

os.environ["CUDA_VISIBLE_DEVICES"] = ""

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
CHECKS_DIR = WORKSPACE_ROOT / "code" / "workshop_checks"
SNIPPETS_DIR = CHECKS_DIR / "snippets"
GUIDE_PATH = WORKSPACE_ROOT / "docs" / "06_student_friendly_guide_and_solutions.md"
APPX_PATH = CHECKS_DIR / "outputs" / "appendix_c_neuroprobe_15tasks_fdr.md"

for p in (CHECKS_DIR, SNIPPETS_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from check_n2_subject_balance import cap_per_subject_equally, pearson_r_and_p_df4  # noqa: E402
from check_pr_pc90_and_layers import compute_pr_and_pc90  # noqa: E402
from patch_split_np_fdr import (  # noqa: E402
    T_CRIT_95_DF5,
    T_CRIT_BONF15_DF5,
    benjamini_hochberg_fdr,
    student_t_two_sided_p,
)
from run_all_checks import run_all  # noqa: E402


class TestWorkshopChecksAndGuide(unittest.TestCase):
    """Verify mathematical accuracy, standalone execution, and student-friendly guide compliance."""

    def test_01_student_t_exact_p_values(self):
        self.assertAlmostEqual(student_t_two_sided_p(T_CRIT_95_DF5, df=5), 0.05, places=8)
        self.assertAlmostEqual(student_t_two_sided_p(T_CRIT_BONF15_DF5, df=5), 0.05 / 15.0, places=8)
        self.assertEqual(student_t_two_sided_p(0.0, df=5), 1.0)

    def test_02_benjamini_hochberg_monotonicity(self):
        raw_p = [0.0023, 0.0354, 0.0611, 0.50, 0.94]
        q_vals = benjamini_hochberg_fdr(raw_p)
        self.assertEqual(len(q_vals), 5)
        self.assertTrue(all(0.0 <= q <= 1.0 for q in q_vals))
        self.assertTrue(all(q1 <= q2 + 1e-12 for q1, q2 in zip(q_vals, q_vals[1:])))
        self.assertAlmostEqual(q_vals[0], 0.0023 * 5 / 1, places=8)

    def test_03_equal_per_subject_capping_waterfilling(self):
        # S2_s2 case: Sub26 (54,639) + sub-10_AJILE (13,877) -> exact 50:50 split of 9,757
        alloc = cap_per_subject_equally({"Sub26": 54639, "sub-10": 13877}, 9757)
        self.assertEqual(sum(alloc.values()), 9757)
        self.assertLessEqual(abs(alloc["Sub26"] - alloc["sub-10"]), 1)

        # Edge case where one subject has fewer than half of target
        alloc_asym = cap_per_subject_equally({"ShortSubj": 2000, "LongSubj": 20000}, 9757)
        self.assertEqual(alloc_asym["ShortSubj"], 2000)
        self.assertEqual(alloc_asym["LongSubj"], 7757)

    def test_04_pr_and_pc90_properties(self):
        # Isotropic identity covariance -> PR == D, PC90 == ceil(0.9 * D)
        eye_samples = np.vstack([np.eye(10), -np.eye(10)])
        pr, pc90 = compute_pr_and_pc90(eye_samples, standardize=True)
        self.assertAlmostEqual(pr, 10.0, places=6)
        self.assertGreaterEqual(pc90, 9)

    def test_05_run_all_standalone_and_live_parity(self):
        rep_embedded = run_all(hangang_dir=None, write_outputs=False)
        self.assertEqual(
            rep_embedded["check_1_neuroprobe_15tasks"]["counts_1of64"],
            {"유지": 5, "판정 불가": 10, "깨짐": 0},
        )
        self.assertEqual(
            rep_embedded["check_1_neuroprobe_15tasks"]["counts_1of1024"],
            {"유지": 7, "판정 불가": 8, "깨짐": 0},
        )
        self.assertEqual(rep_embedded["check_5_diver2_bug_demos"]["rope_bf16"]["unique_in_bfloat16"], 829)
        self.assertGreaterEqual(rep_embedded["check_5_diver2_bug_demos"]["neuroprobe_voxel"]["voxel_r_hat"], 1.9)

        hangang_live = Path("/home/juke/git/chaewon-intern-2026fall/hangang")
        if hangang_live.is_dir():
            rep_live = run_all(hangang_dir=hangang_live, write_outputs=False)
            self.assertEqual(
                rep_live["check_1_neuroprobe_15tasks"]["counts_1of64"],
                rep_embedded["check_1_neuroprobe_15tasks"]["counts_1of64"],
            )
            self.assertEqual(
                rep_live["check_1_neuroprobe_15tasks"]["counts_1of1024"],
                rep_embedded["check_1_neuroprobe_15tasks"]["counts_1of1024"],
            )
            self.assertTrue(rep_live["check_2_holdout_vs_newsubj"]["found_missing_div2_in_newsubj_cell_py"])
            r64, p64 = pearson_r_and_p_df4(
                [s["depth_frac"] for s in rep_live["check_3_n2_subject_scaling"]["seeds"]],
                [s["d_64"] for s in rep_live["check_3_n2_subject_scaling"]["seeds"]],
            )
            self.assertGreater(p64, 0.30)  # non-significant at n=6

    def test_06_guide_and_appendix_exist_and_comply_with_honorifics(self):
        self.assertTrue(GUIDE_PATH.is_file(), "Missing 06_student_friendly_guide_and_solutions.md")
        self.assertTrue(APPX_PATH.is_file(), "Missing appendix_c_neuroprobe_15tasks_fdr.md")
        text = GUIDE_PATH.read_text(encoding="utf-8")
        self.assertGreaterEqual(GUIDE_PATH.stat().st_size, 8000)
        self.assertNotIn("—", text, "Guide should avoid em-dashes")
        self.assertFalse(bool(re.search(r"(안채원|이아현)(?!\s*선생님)", text)))
        self.assertIn("안채원 선생님", text)
        self.assertIn("이아현 선생님", text)
        self.assertIn("차지욱 교수님", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
