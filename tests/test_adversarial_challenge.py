#!/usr/bin/env python3
"""
test_adversarial_challenge.py
=============================
Authoritative Adversarial Challenge & Stress Harness for tests/verify_acceptance_criteria.py.

This harness empirically verifies:
1. False Positives (Type I: harness passes bad/corrupted data or missing invariants)
2. False Negatives (Type II: harness fails on valid variations, pre-2015 citations, anchors)
3. Honorific Policy Enforcement (catches '안채원 씨', '이아현 씨', student surnames, 반말, root files)
4. Determinism & Flakiness (multi-run reproducibility, idempotency)
"""

import copy
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

# Dynamically import verify_acceptance_criteria
SPEC = importlib.util.spec_from_file_location(
    "verify_acceptance_criteria",
    WORKSPACE_ROOT / "tests/verify_acceptance_criteria.py"
)
verify_mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verify_mod)


class AdversarialTestChallenge(unittest.TestCase):
    """Adversarially challenge the acceptance test suite against corruptions and edge cases."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="adv_test_")
        self.addCleanup(lambda: shutil.rmtree(self.temp_dir, ignore_errors=True))

    def run_sub_test(self, test_cls, method_name, root_override=None):
        """Runs a single test method from verify_acceptance_criteria with isolated state."""
        orig_root = verify_mod.WORKSPACE_ROOT
        orig_base_root = verify_mod.BaseAcceptanceTest.root
        orig_base_docs = verify_mod.BaseAcceptanceTest.docs
        orig_prog = verify_mod.BaseAcceptanceTest.progressive

        try:
            if root_override:
                verify_mod.WORKSPACE_ROOT = root_override
                verify_mod.BaseAcceptanceTest.root = root_override
                verify_mod.BaseAcceptanceTest.docs = root_override / "docs"

            instance = test_cls(method_name)
            result = unittest.TestResult()
            instance.run(result)
            return result
        finally:
            verify_mod.WORKSPACE_ROOT = orig_root
            verify_mod.BaseAcceptanceTest.root = orig_base_root
            verify_mod.BaseAcceptanceTest.docs = orig_base_docs
            verify_mod.BaseAcceptanceTest.progressive = orig_prog

    # =========================================================================
    # 1. HONORIFIC ENFORCEMENT CHALLENGES
    # =========================================================================

    def test_challenge_honorific_ahn_chaewon_ssi_detected(self):
        """Verify harness properly fails when '안채원 씨' is injected into docs/01_research_synthesis.md."""
        temp_root = Path(self.temp_dir)
        temp_docs = temp_root / "docs"
        temp_docs.mkdir(parents=True, exist_ok=True)

        orig_content = (WORKSPACE_ROOT / "docs/01_research_synthesis.md").read_text(encoding="utf-8")
        corrupted_content = orig_content + "\n\n안채원 씨가 제안한 데이터 감축 모델...\n"
        (temp_docs / "01_research_synthesis.md").write_text(corrupted_content, encoding="utf-8")

        result = self.run_sub_test(
            verify_mod.TestTier2BoundaryCases,
            "test_f1_b01_strict_honorifics_chaewon_ahn",
            root_override=temp_root
        )
        self.assertEqual(len(result.failures), 1, "Harness MUST fail when '안채원 씨' is present")
        self.assertIn("안채원 씨", str(result.failures[0][1]))

    def test_challenge_honorific_lee_ahhyun_ssi_detected(self):
        """Verify harness properly fails when '이아현 씨' is injected into docs/01_research_synthesis.md."""
        temp_root = Path(self.temp_dir)
        temp_docs = temp_root / "docs"
        temp_docs.mkdir(parents=True, exist_ok=True)

        orig_content = (WORKSPACE_ROOT / "docs/01_research_synthesis.md").read_text(encoding="utf-8")
        corrupted_content = orig_content + "\n\n이아현 씨의 반론에 따르면...\n"
        (temp_docs / "01_research_synthesis.md").write_text(corrupted_content, encoding="utf-8")

        result = self.run_sub_test(
            verify_mod.TestTier2BoundaryCases,
            "test_f1_b02_strict_honorifics_ahhyun_lee",
            root_override=temp_root
        )
        self.assertEqual(len(result.failures), 1, "Harness MUST fail when '이아현 씨' is present")
        self.assertIn("이아현 씨", str(result.failures[0][1]))

    def test_challenge_honorific_student_surname_bypass_vulnerability(self):
        """HARDENED: Verify test_f1_b03 detects informal student address with surname prefixes and postpositions."""
        temp_root = Path(self.temp_dir)
        temp_docs = temp_root / "docs"
        temp_docs.mkdir(parents=True, exist_ok=True)

        orig_content = (WORKSPACE_ROOT / "docs/01_research_synthesis.md").read_text(encoding="utf-8")
        # Injected with 3-syllable full student name + 씨
        corrupted_content = orig_content + "\n\n김주빈 씨와 박규형 씨, 최동엽 씨가 참여하였다.\n"
        (temp_docs / "01_research_synthesis.md").write_text(corrupted_content, encoding="utf-8")

        result = self.run_sub_test(
            verify_mod.TestTier2BoundaryCases,
            "test_f1_b03_global_student_honorific_audit",
            root_override=temp_root
        )
        self.assertEqual(
            len(result.failures),
            1,
            "Harness MUST detect student full names with surnames ('김주빈 씨', '박규형 씨', '최동엽 씨')"
        )
        self.assertIn("김주빈", str(result.failures[0][1]))

    def test_challenge_honorific_banmal_leak_vulnerability(self):
        """HARDENED: Verify test_f1_b01/b02 detects bare non-honorific or 반말 even if honorific appears elsewhere."""
        temp_root = Path(self.temp_dir)
        temp_docs = temp_root / "docs"
        temp_docs.mkdir(parents=True, exist_ok=True)

        orig_content = (WORKSPACE_ROOT / "docs/01_research_synthesis.md").read_text(encoding="utf-8")
        # Injected bare non-honorific banmal statement
        corrupted_content = orig_content + "\n\n안채원은 이 데이터를 직접 정리했다. 이아현은 분석을 맡았다.\n"
        (temp_docs / "01_research_synthesis.md").write_text(corrupted_content, encoding="utf-8")

        res_ahn = self.run_sub_test(
            verify_mod.TestTier2BoundaryCases,
            "test_f1_b01_strict_honorifics_chaewon_ahn",
            root_override=temp_root
        )
        res_lee = self.run_sub_test(
            verify_mod.TestTier2BoundaryCases,
            "test_f1_b02_strict_honorifics_ahhyun_lee",
            root_override=temp_root
        )
        self.assertEqual(
            len(res_ahn.failures),
            1,
            "Harness MUST catch bare non-honorific address for 안채원 선생님 ('안채원은')"
        )
        self.assertIn("안채원", str(res_ahn.failures[0][1]))
        self.assertEqual(
            len(res_lee.failures),
            1,
            "Harness MUST catch bare non-honorific address for 이아현 선생님 ('이아현은')"
        )
        self.assertIn("이아현", str(res_lee.failures[0][1]))

    def test_challenge_honorific_untracked_root_file_vulnerability(self):
        """HARDENED: Verify get_all_markdown_files dynamically audits all root markdown files (e.g. SUMMARY.md)."""
        temp_root = Path(self.temp_dir)
        temp_docs = temp_root / "docs"
        temp_docs.mkdir(parents=True, exist_ok=True)

        orig_content = (WORKSPACE_ROOT / "docs/01_research_synthesis.md").read_text(encoding="utf-8")
        (temp_docs / "01_research_synthesis.md").write_text(orig_content, encoding="utf-8")

        # Create a new root file with blatant policy breach
        (temp_root / "SUMMARY.md").write_text("# Summary\n안채원 씨와 이아현 씨의 연구 요약본이다.\n", encoding="utf-8")

        result = self.run_sub_test(
            verify_mod.TestTier2BoundaryCases,
            "test_f1_b01_strict_honorifics_chaewon_ahn",
            root_override=temp_root
        )
        self.assertEqual(
            len(result.failures),
            1,
            "Harness MUST discover custom root markdown files (e.g. SUMMARY.md) and fail on honorific violation"
        )
        self.assertIn("SUMMARY.md", str(result.failures[0][1]))

    # =========================================================================
    # 2. FALSE POSITIVE CHALLENGES (Harness passes bad / incomplete data)
    # =========================================================================

    def test_challenge_false_positive_corrupted_subject_numbers(self):
        """Verify harness detects when critical 37-subject baseline is missing or corrupted."""
        temp_root = Path(self.temp_dir)
        temp_docs = temp_root / "docs"
        temp_docs.mkdir(parents=True, exist_ok=True)

        orig_content = (WORKSPACE_ROOT / "docs/01_research_synthesis.md").read_text(encoding="utf-8")
        # Replace 37 subjects with 99 subjects
        corrupted = orig_content.replace("37명", "99명").replace("37 subjects", "99 subjects").replace("37", "99")
        (temp_docs / "01_research_synthesis.md").write_text(corrupted, encoding="utf-8")

        result = self.run_sub_test(
            verify_mod.TestTier1FeatureCoverage,
            "test_f2_04_subject_scaling_threshold_metrics",
            root_override=temp_root
        )
        self.assertEqual(len(result.failures), 1, "Harness MUST fail when 37 subjects figure is corrupted")

    def test_challenge_false_positive_kisti_monotonicity_vacuum(self):
        """HARDENED: Verify test_f2_b03 detects non-monotonic throughput scaling across KISTI nodes."""
        temp_root = Path(self.temp_dir)
        temp_docs = temp_root / "docs"
        temp_docs.mkdir(parents=True, exist_ok=True)

        # Content has 190 and 1180, but middle is degraded (non-monotonic)
        non_monotonic_content = (
            "# Synthesis\n"
            "1노드 189.7 samples/s\n"
            "2노드 50.0 samples/s (degraded!)\n"
            "4노드 20.0 samples/s (collapsed!)\n"
            "8노드 1180.1 samples/s\n"
        )
        (temp_docs / "01_research_synthesis.md").write_text(non_monotonic_content, encoding="utf-8")

        result = self.run_sub_test(
            verify_mod.TestTier2BoundaryCases,
            "test_f2_b03_kisti_scaling_monotonicity",
            root_override=temp_root
        )
        self.assertEqual(
            len(result.failures),
            1,
            "Harness MUST detect non-monotonic throughput scaling across KISTI nodes"
        )
        self.assertIn("monotonic", str(result.failures[0][1]).lower())

    def test_challenge_false_positive_partial_adversarial_vulnerabilities(self):
        """HARDENED: Verify test_f4_b01 strictly requires all 5 interface contract vulnerability categories."""
        temp_root = Path(self.temp_dir)
        temp_docs = temp_root / "docs"
        temp_docs.mkdir(parents=True, exist_ok=True)

        # Has only 4 of the 5 vulnerabilities (completely omits Linear Probing / 선형 프로브)
        four_vulns_content = (
            "# Adversarial Review\n"
            "1. Readout layer 읽는 층 괴리\n"
            "2. Reconstruction loss 재구성 손실 역설\n"
            "3. Masked Autoencoding 자체지도학습 한계\n"
            "4. Subject diversity 피험자 다양성 편향\n"
        )
        (temp_docs / "03_adversarial_review.md").write_text(four_vulns_content, encoding="utf-8")

        result = self.run_sub_test(
            verify_mod.TestTier2BoundaryCases,
            "test_f4_b01_all_five_contract_vulnerabilities_covered",
            root_override=temp_root
        )
        self.assertEqual(
            len(result.failures),
            1,
            "Harness MUST fail when only 4 of 5 vulnerabilities are present"
        )
        self.assertIn("Linear probing", str(result.failures[0][1]))

    def test_challenge_false_positive_broken_link_with_anchor_bypassed(self):
        """HARDENED: Verify test_tier3_07 detects broken relative markdown links even when #anchor is appended."""
        temp_root = Path(self.temp_dir)
        temp_docs = temp_root / "docs"
        temp_docs.mkdir(parents=True, exist_ok=True)

        # File contains a link to a completely non-existent file, but with an anchor tag
        (temp_docs / "01_research_synthesis.md").write_text(
            "# Synthesis\n[Broken Link](does_not_exist_file.md#target_section)\n",
            encoding="utf-8"
        )

        result = self.run_sub_test(
            verify_mod.TestTier3CrossInteractions,
            "test_tier3_07_f1_to_f6_end_to_end_traceability",
            root_override=temp_root
        )
        self.assertEqual(
            len(result.failures),
            1,
            "Harness MUST detect broken relative link even with anchor fragment"
        )
        self.assertIn("does_not_exist_file.md", str(result.failures[0][1]))

    def test_challenge_false_positive_placeholders_outside_tables_bypassed(self):
        """HARDENED: Verify test_f2_b05 detects placeholder tokens ([TODO], [TBD], xxx) anywhere in document body."""
        temp_root = Path(self.temp_dir)
        temp_docs = temp_root / "docs"
        temp_docs.mkdir(parents=True, exist_ok=True)

        body_placeholder_content = (
            "# Synthesis\n"
            "Here is the text with [TODO: replace with actual cluster numbers] and [TBD].\n\n"
            "| Node | Throughput |\n"
            "|---|---|\n"
            "| 1 | 189.7 |\n"
        )
        (temp_docs / "01_research_synthesis.md").write_text(body_placeholder_content, encoding="utf-8")

        result = self.run_sub_test(
            verify_mod.TestTier2BoundaryCases,
            "test_f2_b05_no_placeholder_tokens_in_tables",
            root_override=temp_root
        )
        self.assertEqual(
            len(result.failures),
            1,
            "Harness MUST detect placeholder tokens [TODO] / [TBD] outside code blocks"
        )
        self.assertIn("TODO", str(result.failures[0][1]))

    # =========================================================================
    # 3. FALSE NEGATIVE CHALLENGES (Harness falsely rejects valid documents)
    # =========================================================================

    def test_challenge_false_negative_pre_2015_scholarly_citation(self):
        """HARDENED: Verify test_f3_b01 permits valid foundational pre-2015 scholarly citations (range 1950..2027)."""
        temp_root = Path(self.temp_dir)
        temp_docs = temp_root / "docs"
        temp_docs.mkdir(parents=True, exist_ok=True)

        valid_content = (
            "# Deep Research Literature\n"
            "Oliveira et al. (2026), Ooi et al. (2025).\n"
            "We also build upon the foundational representation learning method of Mikolov et al. (2013).\n"
        )
        (temp_docs / "02_deep_research_literature.md").write_text(valid_content, encoding="utf-8")

        result = self.run_sub_test(
            verify_mod.TestTier2BoundaryCases,
            "test_f3_b01_valid_publication_years",
            root_override=temp_root
        )
        self.assertEqual(
            len(result.failures),
            0,
            f"Harness MUST NOT falsely reject valid historical scholarly citation (1950..2027): {result.failures}"
        )

    def test_challenge_false_negative_roadmap_ordering_sentence(self):
        """HARDENED: Verify test_f5_b05 uses section header matching rather than naive full-text find()."""
        temp_root = Path(self.temp_dir)
        temp_docs = temp_root / "docs"
        temp_docs.mkdir(parents=True, exist_ok=True)

        valid_content = (
            "# Action Items Roadmap\n"
            "본 문서는 장기적 비전과 중기적 과제, 그리고 단기적 실행 항목을 종합한다.\n\n"
            "## 1. 단기 과제 (Immediate)\n"
            "## 2. 중기 과제 (Medium)\n"
            "## 3. 장기 과제 (Long)\n"
        )
        (temp_docs / "04_action_items_roadmap.md").write_text(valid_content, encoding="utf-8")

        result = self.run_sub_test(
            verify_mod.TestTier2BoundaryCases,
            "test_f5_b05_dependency_ordering_topology",
            root_override=temp_root
        )
        self.assertEqual(
            len(result.failures),
            0,
            f"Harness MUST NOT falsely reject valid roadmap due to naive substring search on intro sentence: {result.failures}"
        )

    def test_challenge_false_negative_display_math_desync(self):
        """HARDENED: Verify test_f3_b05 strips display math ($$) to prevent delimiter desynchronization."""
        temp_root = Path(self.temp_dir)
        temp_docs = temp_root / "docs"
        temp_docs.mkdir(parents=True, exist_ok=True)

        # LaTeX display math block followed by Korean prose containing an unmatched brace in prose
        valid_content = (
            "# Lit\n"
            "$$\n"
            "L(N, T) = K_1 N^{-\\alpha} + K_2 T^{-\\beta}\n"
            "$$\n"
            "그리고 본 연구의 수식 모델 {설명 은 다음과 같다: $a = b$\n"
        )
        (temp_docs / "02_deep_research_literature.md").write_text(valid_content, encoding="utf-8")

        result = self.run_sub_test(
            verify_mod.TestTier2BoundaryCases,
            "test_f3_b05_latex_math_syntax_validity",
            root_override=temp_root
        )
        self.assertEqual(
            len(result.failures),
            0,
            f"Harness MUST NOT falsely reject valid LaTeX math when display math ($$) is present: {result.failures}"
        )

    # =========================================================================
    # 4. TIER 4 FEATURE FILTER EXCLUSION CHALLENGE
    # =========================================================================

    def test_challenge_feature_filtering_tier4_exclusion(self):
        """HARDENED: Verify CLI --feature F1..F7 maps relevant Tier 4 acceptance scenario tests."""
        for feat in ["F1", "F2", "F3", "F4", "F5", "F6", "F7"]:
            suite = verify_mod.build_filtered_suite(feature=feat, progressive=True)
            tier4_in_suite = [t.id() for t in suite if "TestTier4AcceptanceScenarios" in t.id()]
            self.assertGreater(
                len(tier4_in_suite),
                0,
                f"Feature {feat} MUST include relevant Tier 4 scenario tests (found: {tier4_in_suite})"
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
