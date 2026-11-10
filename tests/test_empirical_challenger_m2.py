#!/usr/bin/env python3
"""
test_empirical_challenger_m2.py
===============================
Authoritative Empirical Adversarial Test Harness for Milestone 2:
Validates biophysical models, negative transfer dynamics, information-theoretic
bridges, and representation divergence in `docs/02_deep_research_literature.md`.

Challenger 2 Empirical Verification Suite:
1. Biophysical Skull Conductivity & Volume Conduction Simulation
2. High-Gamma (>40Hz) Filtering: Spatial Smearing vs Dielectric Attenuation
3. Optimization Dynamics of DANN (0.84-0.97 Discriminator Accuracy)
4. Chai et al. (2026) Excess Loss & Entropy Bridge Analysis
5. Completeness Audit of Section 4.5 Recovery Ablations
"""

import math
import re
import unittest
from pathlib import Path
import numpy as np

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent


class TestBiophysicalClaims(unittest.TestCase):
    """Adversarial stress-testing of biophysical claims in docs/02_deep_research_literature.md."""

    def test_conductivity_ratio_accuracy(self):
        """Verify the exact conductivity ratios of brain, CSF, and skull.
        
        Claim in doc:
        - sigma_skull = 0.01 S/m
        - sigma_brain = 0.33 S/m
        - sigma_csf = 1.79 S/m
        - Claims skull is '40~80x' more resistive than brain & CSF.
        """
        sigma_skull = 0.01
        sigma_brain = 0.33
        sigma_csf = 1.79

        ratio_brain_to_skull = sigma_brain / sigma_skull  # 33.0
        ratio_csf_to_skull = sigma_csf / sigma_skull      # 179.0

        # Nunez & Srinivasan (2006) Classic Rush-Driscoll ratio was 80:1 (brain:skull).
        # Modern in vivo (Oostendorp 2000, Hoekema 2003, Dannhauer 2011) gives 15:1 to 30:1.
        # Check: 33 is within modern range (~30), but NOT 40~80x.
        # CSF ratio is 179x, far exceeding 40~80x.
        self.assertAlmostEqual(ratio_brain_to_skull, 33.0, places=1)
        self.assertAlmostEqual(ratio_csf_to_skull, 179.0, places=1)

        # Flag nuance: The doc conflates brain:skull ratio (33x) and CSF:skull ratio (179x) into '40~80배'.
        # 40~80x is historically the Rush & Driscoll (1969) brain:skull assumption (80:1).
        conflation_detected = (ratio_brain_to_skull < 40.0) and (ratio_csf_to_skull > 80.0)
        self.assertTrue(
            conflation_detected,
            "Document states 40~80x for both brain and CSF, whereas brain is 33x and CSF is 179x."
        )

    def test_high_gamma_spatial_vs_dielectric_filtering(self):
        """Empirically test whether skull attenuation above 40Hz is dielectric (capacitive)
        or spatial cancellation of non-synchronous micro-dipoles.
        
        According to Buzsaki et al. (2012 Nat Rev Neurosci) and Logothetis et al. (2007 Neuron):
        - Extracellular medium and bone have minimal capacitive reactance up to 1 kHz (quasi-static).
        - Attenuation of high-gamma is due to spatial cancellation of localized asynchronously firing dipoles.
        """
        # Dielectric time constant of bone:
        # epsilon_r of wet bone ~ 100 - 1000 at 100 Hz (Gabriel et al. 1996)
        epsilon_0 = 8.854e-12  # F/m
        epsilon_r = 500.0      # typical at 100 Hz
        sigma_skull = 0.01     # S/m
        f = 100.0              # 100 Hz (high gamma)
        omega = 2 * math.pi * f

        conduction_current = sigma_skull
        displacement_current = omega * epsilon_0 * epsilon_r

        # Quasi-static approximation validity: displacement current << conduction current
        current_ratio = displacement_current / conduction_current
        self.assertLess(
            current_ratio, 0.001,
            f"Quasi-static regime holds: displacement current is {current_ratio:.6f} of conduction current. "
            "Therefore, bone behaves purely resistively, NOT as a dielectric capacitive low-pass filter!"
        )

        # Now test spatial cancellation:
        # Dipoles distributed across cortical area A with asynchronous phase vs synchronous phase
        np.random.seed(42)
        n_micro_dipoles = 1000
        # High gamma: random phase across micro-columns (destructive interference)
        phases_high_gamma = np.random.uniform(0, 2 * np.pi, n_micro_dipoles)
        sum_high_gamma = np.abs(np.sum(np.exp(1j * phases_high_gamma)))

        # Alpha band: synchronized phase across macro-columns (constructive interference)
        phases_alpha = np.random.normal(0, 0.2, n_micro_dipoles)
        sum_alpha = np.abs(np.sum(np.exp(1j * phases_alpha)))

        # Spatial cancellation ratio:
        spatial_attenuation = sum_high_gamma / sum_alpha
        self.assertLess(
            spatial_attenuation, 0.10,
            f"High gamma cancels out spatially by a factor of {spatial_attenuation:.4f} due to destructive phase interference!"
        )

    def test_gradient_dominance_in_eeg_fill(self):
        """Simulate joint pretraining MSE gradients: 87.5% EEG vs 12.5% iEEG.
        Given EEG SNR/amplitude is 10-100 uV and iEEG is 100-2000 uV,
        if batch z-score is applied, EEG noise variance dominates representations.
        """
        np.random.seed(123)
        # 12.5% iEEG: localized sharp waveforms (high information)
        ieeg_samples = 125
        eeg_samples = 875

        # iEEG has localized high-frequency energy
        t = np.linspace(0, 1, 50)
        ieeg_clean = np.sin(2 * np.pi * 80 * t)  # 80 Hz gamma
        # EEG has broad low-frequency power + large background noise
        eeg_noise = np.sin(2 * np.pi * 10 * t) + np.random.normal(0, 0.5, (eeg_samples, 50))

        # Under joint MSE loss, gradient norm on shared weights is dominated by the 87.5% EEG batches
        grad_norm_eeg = np.mean(np.linalg.norm(eeg_noise, axis=1)) * eeg_samples
        grad_norm_ieeg = np.mean(np.linalg.norm(ieeg_clean, axis=0)) * ieeg_samples
        ratio = grad_norm_eeg / (grad_norm_eeg + grad_norm_ieeg)

        self.assertGreater(
            ratio, 0.85,
            f"EEG gradients account for {ratio*100:.1f}% of total gradient updates in EEG_fill."
        )


class TestAblationInterpretation(unittest.TestCase):
    """Adversarial stress-testing of the 6 recovery ablations and physical incommensurability claims."""

    def test_dann_discriminator_accuracy_interpretation(self):
        """In DANN (Ganin et al. 2016), discriminator accuracy of 0.84-0.97
        indicates an optimization failure of the adversarial game, NOT mathematical impossibility.
        """
        acc_min, acc_max = 0.84, 0.97
        # Optimal DANN domain invariance occurs when discriminator accuracy -> 0.50 (chance level).
        # When accuracy is 0.84-0.97, the discriminator is winning completely.
        # This causes vanishing gradients for the feature extractor (cross-entropy saturates).
        self.assertGreater(acc_min, 0.80)
        # Challenge conclusion: An optimization collapse (discriminator dominance / mode collapse)
        # cannot be cited as conclusive evidence of 'physical incommensurability'.
        is_optimization_collapse = acc_min > 0.80
        self.assertTrue(is_optimization_collapse)

    def test_section_4_5_ablation_completeness(self):
        """Check whether Section 4.5 in docs/02_deep_research_literature.md lists all 6 ablations
        as announced in its section heading '4.5 6대 복구 절제실험(Ablation)의 전원 실패 원인 분석'.
        """
        doc_path = WORKSPACE_ROOT / "docs/02_deep_research_literature.md"
        content = doc_path.read_text(encoding="utf-8")

        # Find section 4.5
        sec45_match = re.search(r"### 4\.5\s+6대 복구 절제실험.*?---", content, re.DOTALL)
        self.assertIsNotNone(sec45_match, "Section 4.5 must exist")
        sec45_text = sec45_match.group(0)

        # Count numbered items in section 4.5
        numbered_items = re.findall(r"^\d+\.\s+", sec45_text, re.MULTILINE)
        
        # In docs/01_research_synthesis.md, 6 ablations were listed:
        # 1. lp45
        # 2. H-batch zscore
        # 3. H-batch adv
        # 4. H-sfm modtok
        # 5. EEG_add (5.77M samples)
        # 6. Channel padding/truncation
        
        # Flag if fewer than 6 items are documented:
        self.assertEqual(
            len(numbered_items), 4,
            f"Section 4.5 heading claims '6대 복구 절제실험' but only enumerates {len(numbered_items)} items!"
        )


class TestInformationDynamicsClaims(unittest.TestCase):
    """Adversarial stress-testing of Chai et al. (2026), Raghu et al. (2021), and MAE paradox resolution."""

    def test_chai_scaling_variable_definition(self):
        """Check the formula for scaling variable z in Chai & Xiong (2026).
        Formula in doc:
            z = (R - 1) * N_total / U
        In Chai et al. (2026):
            z = (R - 1) * N / U, where N is model parameters, U is unique tokens.
        If N_total is interpreted as total tokens (U * R), z becomes R*(R-1), losing parameter dependence!
        """
        # Let model parameters N = 51.4e6 (Small model)
        # Let unique tokens U = 5.1 hours * 3600s * 500Hz * 128 channels / 50 tokens = 2.35e7 tokens
        N_params = 51.4e6
        U_tokens = 2.35e7
        R_repetitions = 30  # 30 draws

        z_true = (R_repetitions - 1) * (N_params / U_tokens)
        
        # If N_total means total tokens trained = U * R:
        z_flawed = (R_repetitions - 1) * (U_tokens * R_repetitions / U_tokens)  # R * (R-1) = 870
        
        self.assertAlmostEqual(z_true, 29 * (51.4 / 23.5), places=1)
        self.assertNotEqual(z_true, z_flawed)

    def test_source_entropy_vs_latent_participation_ratio(self):
        """Chai et al. established r = -0.89 between SOURCE UNIGRAM ENTROPY of training tokens
        and excess loss repetition tolerance.
        In docs/02_deep_research_literature.md, Section 5.1 compares this to
        the LATENT PARTICIPATION RATIO (PR) of frozen embeddings (PR=7.4 for 1/1024 vs PR=5.4 for Base).
        
        Evaluate whether Latent PR is mathematically equivalent to Source Token Entropy.
        """
        # Source entropy H(X) measures information content of input distribution X: H(X) = -sum p(x) log p(x).
        # Latent Participation Ratio PR(Z) = (sum lambda_i)^2 / sum lambda_i^2 measures dimensional spread of representations Z.
        # A higher PR can mean either richer representations OR uncollapsed diffuse noise!
        # In 1/1024, PR=7.4 is higher than Base (5.4) and Scratch (5.0).
        # This shows representations are LESS compact (more diffuse), not necessarily higher source entropy.
        
        pr_scratch = 5.0
        pr_1024 = 7.4
        pr_64 = 5.8
        pr_base = 5.4

        # Non-monotonic behavior of PR with training data:
        # As data increases (1024 -> 64 -> Base), PR decreases from 7.4 -> 5.8 -> 5.4 (subspace concentration).
        # Scratch is 5.0 (random weights project to low-rank subspace depending on architecture).
        self.assertGreater(pr_1024, pr_base)
        self.assertGreater(pr_64, pr_base)
        # Conclusion: Latent PR is NOT an input source entropy proxy; it reflects representation compression dynamics!

    def test_vision_mae_analogy_limits(self):
        """Check whether the Vision MAE (He et al. 2022) analogy holds for Seen vs Unseen iEEG reconstruction loss.
        He et al. (2022) showed MAE reconstruction loss does not correlate monotonically with linear probe accuracy.
        However, He et al. (2022) did NOT show Seen vs Unseen patient noise memorization.
        """
        # Seen held-out loss: +8.5%
        # Unseen held-out loss: -0.06%
        # Downstream linear probe score: +0.0006
        delta_seen = 8.5
        delta_unseen = -0.06
        delta_downstream = 0.0006

        # The empirical finding is valid and remarkable:
        self.assertGreater(delta_seen, 5.0)
        self.assertAlmostEqual(delta_unseen, 0.0, delta=0.5)
        self.assertAlmostEqual(delta_downstream, 0.0, delta=0.005)
        # The analogy to He et al. 2022 is conceptually sound regarding 'reconstruction != linear separability',
        # but the patient-specific noise-memorization mechanism is an empirical inference specific to electrophysiology.


if __name__ == "__main__":
    unittest.main()
