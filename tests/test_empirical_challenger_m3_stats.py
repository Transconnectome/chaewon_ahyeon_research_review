#!/usr/bin/env python3
"""
test_empirical_challenger_m3_stats.py
=====================================
Authoritative Empirical Adversarial Test Harness for Milestone 3 (Challenger 1):
Mathematical and Statistical Simulation of Claims in docs/03_adversarial_review.md.

Empirically verifies:
1. Non-central t-distribution power curves (n=6, df=5: power drops from ~71% to ~38% at Delta=-0.002).
2. Family-wise error rate (FWER) for k=15 tests at alpha=0.05 (1 - 0.95^15 = 53.67%).
3. Bonferroni corrected critical t-value (t_crit ~ 5.247) and CI lower bound collapse to -0.0106.
4. Epoch calculations for Base (0.461 epochs) and 1/64 (29.52 epochs) under 2.88M sample budget.
5. Strict Lab Governance Honorifics Compliance across all documentation.
"""

import math
import re
import unittest
from pathlib import Path
import numpy as np
import scipy.stats as stats

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent


class TestStatisticalPowerAndInferenceSimulations(unittest.TestCase):
    """Empirical simulation and stress-testing of statistical claims in Axis 5 of docs/03_adversarial_review.md."""

    def test_non_central_t_power_curve_collapse(self):
        """Verify non-central t power drops from ~71.3% at Delta=0 to ~37.8% at Delta=-0.002 (n=6, df=5).
        
        Analytical formulation:
        One-sided non-inferiority test: H0: mu_diff <= -delta vs H1: mu_diff > -delta
        delta_margin = 0.005, alpha = 0.05, n = 6, df = 5
        SE = 0.001945
        Critical value t_crit = t.ppf(1 - alpha, df=5) = 2.0150
        Non-centrality parameter: nc = (Delta_true + delta_margin) / SE
        Power = 1 - nct.cdf(t_crit, df=5, nc)
        """
        n = 6
        df = n - 1
        delta_margin = 0.005
        se = 0.001945
        alpha = 0.05

        t_crit = stats.t.ppf(1.0 - alpha, df)
        self.assertAlmostEqual(t_crit, 2.015048, places=4)

        # 1. At Delta_true = 0.0000 (fully equal)
        nc_zero = (0.0000 + delta_margin) / se
        self.assertAlmostEqual(nc_zero, 2.570694, places=3)
        power_zero = 1.0 - stats.nct.cdf(t_crit, df, nc_zero)
        beta_zero = 1.0 - power_zero
        self.assertAlmostEqual(power_zero * 100.0, 71.27, delta=0.5,
                               msg="Power at Delta=0 must be ~71.3%")
        self.assertAlmostEqual(beta_zero * 100.0, 28.73, delta=0.5,
                               msg="Type II error at Delta=0 must be ~28.7%")

        # 2. At Delta_true = -0.0020 (within non-inferiority margin)
        nc_minus_002 = (-0.0020 + delta_margin) / se
        self.assertAlmostEqual(nc_minus_002, 1.542416, places=3)
        power_minus_002 = 1.0 - stats.nct.cdf(t_crit, df, nc_minus_002)
        beta_minus_002 = 1.0 - power_minus_002
        self.assertAlmostEqual(power_minus_002 * 100.0, 37.80, delta=0.5,
                               msg="Power at Delta=-0.002 must drop to ~37.8%")
        self.assertAlmostEqual(beta_minus_002 * 100.0, 62.20, delta=0.5,
                               msg="Type II error at Delta=-0.002 must inflate to ~62.2%")

        # 3. Monotonic power degradation check across full curve
        deltas = [0.0, -0.001, -0.002, -0.003, -0.004]
        powers = [1.0 - stats.nct.cdf(t_crit, df, (d + delta_margin) / se) for d in deltas]
        for i in range(len(powers) - 1):
            self.assertGreater(powers[i], powers[i+1], "Power curve must strictly decrease as Delta degrades")

    def test_family_wise_error_rate_k15(self):
        """Verify FWER for k=15 independent tests at alpha=0.05 is 53.67%, and for k=17 is 58.19%."""
        alpha = 0.05
        k15 = 15
        fwer_15 = 1.0 - ((1.0 - alpha) ** k15)
        self.assertAlmostEqual(fwer_15 * 100.0, 53.67088, places=2,
                               msg="FWER for k=15 must be 53.67%")

        k17 = 17
        fwer_17 = 1.0 - ((1.0 - alpha) ** k17)
        self.assertAlmostEqual(fwer_17 * 100.0, 58.1880, places=2,
                               msg="FWER for k=17 must be 58.19%")

    def test_bonferroni_critical_t_and_ci_lower_bound_collapse(self):
        """Verify Bonferroni critical t is 5.2474 (2.04x inflation) and CI lower bound collapses to -0.0106."""
        alpha = 0.05
        k = 15
        df = 5
        se = 0.001945
        delta_hat = -0.0004  # Observed empirical delta for 1/64 condition

        # Bonferroni corrected two-sided alpha
        alpha_bonf = alpha / k
        alpha_half_bonf = alpha_bonf / 2.0

        t_crit_single = stats.t.ppf(1.0 - alpha / 2.0, df)
        self.assertAlmostEqual(t_crit_single, 2.570582, places=4)

        t_crit_bonf = stats.t.ppf(1.0 - alpha_half_bonf, df)
        self.assertAlmostEqual(t_crit_bonf, 5.247424, places=3,
                               msg="Bonferroni critical t for df=5, k=15 must be ~5.2474")

        # Ratio of critical values
        ratio = t_crit_bonf / t_crit_single
        self.assertAlmostEqual(ratio, 2.0413, delta=0.05,
                               msg="Critical t inflation ratio must be ~2.04x")

        # Confidence interval lower bound
        ci_low_bonf = delta_hat - (t_crit_bonf * se)
        self.assertAlmostEqual(ci_low_bonf, -0.010606, places=4,
                               msg="Bonferroni CI lower bound must collapse to -0.0106")

        # Check margin collapse factor
        margin = -0.005
        collapse_factor = ci_low_bonf / margin
        self.assertAlmostEqual(collapse_factor, 2.121, delta=0.1,
                               msg="CI lower bound must exceed non-inferiority margin by ~2.1x")

    def test_epoch_calculations_and_undertraining_confounder(self):
        """Verify compute budget epoch calculations for Base and 1/64 models."""
        total_samples = 2880000
        base_hours = 5203.2
        hours_1_64 = 81.3

        # Interpretation A: 3.0s window slices (actual training slice length in DIVER)
        window_seconds_3s = 3.0
        total_training_hours_3s = (total_samples * window_seconds_3s) / 3600.0
        self.assertAlmostEqual(total_training_hours_3s, 2400.0, places=2)

        epochs_base_3s = total_training_hours_3s / base_hours
        self.assertAlmostEqual(epochs_base_3s, 0.46125, places=3,
                               msg="Base model under-training must be 0.461 epochs")

        epochs_1_64_3s = total_training_hours_3s / hours_1_64
        self.assertAlmostEqual(epochs_1_64_3s, 29.5203, places=2,
                               msg="1/64 model exposure must be 29.52 epochs")

        # Interpretation B: 30.0s recording segments (stored corpus segment length)
        segment_seconds_30s = 30.0
        total_training_hours_30s = (total_samples * segment_seconds_30s) / 3600.0
        self.assertAlmostEqual(total_training_hours_30s, 24000.0, places=2)

        repeats_base_30s = total_training_hours_30s / base_hours
        self.assertAlmostEqual(repeats_base_30s, 4.6125, places=2,
                               msg="Base model 30s segment repeat factor must be 4.61")

        repeats_1_64_30s = total_training_hours_30s / hours_1_64
        self.assertAlmostEqual(repeats_1_64_30s, 295.203, places=1,
                               msg="1/64 model 30s segment repeat factor must be 295.2")


class TestGovernanceHonorificsCompliance(unittest.TestCase):
    """Audit strict lab governance and honorific policy compliance."""

    def test_all_markdown_documents_strict_honorifics(self):
        """Verify zero informal addresses or missing honorifics across docs/."""
        doc_files = list((WORKSPACE_ROOT / "docs").glob("*.md"))
        self.assertGreaterEqual(len(doc_files), 3, "At least 3 milestone documents must exist")

        unhonorific_ahn = re.compile(r"안채원(?!\s*선생님)")
        unhonorific_lee = re.compile(r"이아현(?!\s*선생님)")
        unhonorific_cha = re.compile(r"차지욱(?!\s*교수님)")
        informal_ssi = re.compile(r"([가-힣]{2,4})\s*씨")

        violations = []
        for doc in doc_files:
            text = doc.read_text(encoding="utf-8")
            for idx, line in enumerate(text.splitlines(), 1):
                if unhonorific_ahn.search(line):
                    violations.append(f"{doc.name}:{idx} 안채원 without '선생님': {line}")
                if unhonorific_lee.search(line):
                    violations.append(f"{doc.name}:{idx} 이아현 without '선생님': {line}")
                if unhonorific_cha.search(line):
                    violations.append(f"{doc.name}:{idx} 차지욱 without '교수님': {line}")
                m = informal_ssi.search(line)
                if m:
                    violations.append(f"{doc.name}:{idx} informal '씨' detected: {line}")

        self.assertEqual(len(violations), 0, f"Found governance violations: {violations}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
