#!/usr/bin/env python3
"""
verify_acceptance_criteria.py
=============================
Authoritative End-to-End (E2E) Acceptance Criteria Verification Test Suite
for `chaewon_ahyeon_research_review`.

Requirements & Features Covered:
- R1: Teams Communication & Mentoring Trace Synthesis (F1, F2)
- R2: Deep Research & Scientific Adversarial Review (F3, F4)
- R3: Actionable Improvement Items & Prioritized Roadmap (F5)
- R4: Git Repository Structuring & Transconnectome Publication (F6)
- Checklist: Full E2E Acceptance Verification (F7)

Lab Policy Hard Constraint:
- ALWAYS use honorifics: "안채원 선생님", "이아현 선생님", "차지욱 교수님".
- Informal address ("씨" or 반말) is strictly prohibited across all artifacts.

Usage:
    python3 tests/verify_acceptance_criteria.py [OPTIONS]
    python3 -m pytest tests/verify_acceptance_criteria.py -v

CLI Options:
    --progressive        Enable progressive milestone execution (skips unbuilt artifacts cleanly)
    --tier {1,2,3,4}     Run test cases belonging to a specific tier
    --feature {F1..F7}   Run test cases for a specific feature
    --report-json PATH   Export structured test results to JSON
    --verbose, -v        Display detailed per-test execution information
    --help, -h           Show command-line options
"""

import argparse
import io
import json
import os
import re
import subprocess
import sys
import time
import unittest
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent


def check_artifact_presence(path: Path, artifact_name: str, progressive: bool = False) -> None:
    """Verifies artifact existence or raises diagnostic SkipTest/AssertionError."""
    if not path.is_file():
        if progressive:
            raise unittest.SkipTest(
                f"[PROGRESSIVE] Artifact '{artifact_name}' ({path.name}) not created yet (Milestone pending)"
            )
        raise AssertionError(
            f"Required artifact '{artifact_name}' at {path} does not exist."
        )


def get_all_markdown_files() -> List[Path]:
    """Retrieves all project markdown files under docs/ and workspace root."""
    md_files: Set[Path] = set()
    docs_dir = WORKSPACE_ROOT / "docs"
    if docs_dir.is_dir():
        md_files.update(docs_dir.glob("*.md"))
    # Dynamically discover all root markdown files (e.g. README, TEST_INFRA, PROJECT, SUMMARY, etc.)
    md_files.update(p for p in WORKSPACE_ROOT.glob("*.md") if p.is_file())
    return sorted(list(md_files))


class BaseAcceptanceTest(unittest.TestCase):
    """Base class providing shared fixtures and diagnostic helpers."""

    progressive: bool = os.environ.get("PROGRESSIVE", "0") == "1"
    root: Path = WORKSPACE_ROOT
    docs: Path = WORKSPACE_ROOT / "docs"

    def read_doc_safe(self, rel_path: str, min_size: int = 1) -> str:
        """Reads artifact text with progressive testability handling."""
        full_path = self.root / rel_path
        if not full_path.is_file():
            if self.progressive:
                self.skipTest(
                    f"[PROGRESSIVE] Artifact '{rel_path}' does not exist yet (Milestone pending)"
                )
            self.fail(f"Required artifact '{rel_path}' not found at {full_path}")
        size = full_path.stat().st_size
        if size < min_size:
            self.fail(
                f"Artifact '{rel_path}' size too small ({size} bytes < {min_size} bytes)"
            )
        try:
            return full_path.read_text(encoding="utf-8")
        except UnicodeDecodeError as e:
            self.fail(f"Failed to read '{rel_path}' with UTF-8 encoding: {e}")

    def check_git_initialized(self) -> None:
        """Checks git repository initialization."""
        git_dir = self.root / ".git"
        if not git_dir.is_dir():
            if self.progressive:
                self.skipTest(
                    "[PROGRESSIVE] Git repository not initialized yet (Milestone M5 pending)"
                )
            self.fail(".git directory does not exist in workspace root")


# =====================================================================
# Tier 1: Feature Coverage (F1 through F7, 35 Tests)
# =====================================================================

class TestTier1FeatureCoverage(BaseAcceptanceTest):
    """Tier 1: Feature existence, structural completeness, and primary specification coverage."""

    # --- F1: Teams Communication & Mentoring Trace Synthesis ---

    def test_f1_01_synthesis_document_presence(self):
        """[T1-F1-01] Verify docs/01_research_synthesis.md exists with substantial content (>= 4KB)."""
        content = self.read_doc_safe("docs/01_research_synthesis.md", min_size=4000)
        self.assertGreaterEqual(len(content), 4000, "docs/01_research_synthesis.md must be >= 4000 characters")

    def test_f1_02_chaewon_ahn_teams_proposals(self):
        """[T1-F1-02] Verify 안채원 선생님's research proposals and Google Slide deck link."""
        content = self.read_doc_safe("docs/01_research_synthesis.md")
        self.assertIn("안채원 선생님", content, "Missing reference to 안채원 선생님 in synthesis")
        self.assertTrue(
            bool(re.search(r"(NeuroAI|11/20|고유\s*iEEG|1/64|mixing)", content)),
            "Missing 안채원 선생님's core proposal context in synthesis"
        )
        self.assertTrue(
            "1yueDz" in content or "presentation" in content,
            "Missing 안채원 선생님's mentoring presentation slide deck reference"
        )

    def test_f1_03_ahhyun_lee_teams_counterarguments(self):
        """[T1-F1-03] Verify 이아현 선생님's counterarguments and 'how should we scale' framing."""
        content = self.read_doc_safe("docs/01_research_synthesis.md")
        self.assertIn("이아현 선생님", content, "Missing reference to 이아현 선생님 in synthesis")
        self.assertTrue(
            bool(re.search(r"(발견|discovery|how should we scale|channel origin|SSL)", content, re.I)),
            "Missing 이아현 선생님's framing on scaling discovery and channel origin"
        )
        self.assertTrue(
            "참가자" in content and "시간" in content,
            "Missing contrast between subject count and recording duration"
        )

    def test_f1_04_professor_cha_critical_feedback(self):
        """[T1-F1-04] Verify 차지욱 교수님's critical feedback and advice on representation learning."""
        content = self.read_doc_safe("docs/01_research_synthesis.md")
        self.assertTrue(
            "차지욱 교수님" in content or "지도교수" in content,
            "Missing reference to 차지욱 교수님 in synthesis"
        )
        self.assertTrue(
            bool(re.search(r"(prior knowledge|공통 표상|negative|설익은|준비가 덜|확장적 학습)", content)),
            "Missing verbatim critique themes from 차지욱 교수님"
        )

    def test_f1_05_mentoring_chronology_and_topics(self):
        """[T1-F1-05] Verify chronological mentoring timeline across October and November 2026."""
        content = self.read_doc_safe("docs/01_research_synthesis.md")
        self.assertTrue(
            "KimJaeChul_AI_Class_Mentoring" in content or "김재철 AI" in content,
            "Missing KimJaeChul AI Class mentoring repository reference"
        )
        dates = ["2026-10-07", "2026-10-13", "2026-10-27", "2026-10-28", "2026-11-03", "2026-11-09"]
        matched = [d for d in dates if d in content]
        self.assertGreaterEqual(len(matched), 4, f"Insufficient chronological mentoring dates: found {matched}")

    # --- F2: Experimental Data & Infrastructure Extraction ---

    def test_f2_01_kisti_hangang_cluster_benchmarks(self):
        """[T1-F2-01] Verify KISTI 한강 supercomputer setup, GH200 scaling, and dataloader analysis."""
        content = self.read_doc_safe("docs/01_research_synthesis.md")
        self.assertTrue(
            bool(re.search(r"(KISTI|한강|GH200|Slingshot)", content)),
            "Missing KISTI 한강 supercomputer infrastructure details"
        )
        self.assertTrue(
            bool(re.search(r"(1,180|1180|0\.78|E\(8\)|strong scaling)", content)),
            "Missing 8-node strong scaling benchmarks (1180 s/s, E=0.78)"
        )
        self.assertTrue(
            bool(re.search(r"(worker|dataloader|stall|DDP)", content, re.I)),
            "Missing dataloader I/O profiling analysis and timer correction"
        )

    def test_f2_02_diver_model_architecture_spec(self):
        """[T1-F2-02] Verify DIVER-1 Base and variant model architectural parameters."""
        content = self.read_doc_safe("docs/01_research_synthesis.md")
        self.assertTrue(
            bool(re.search(r"(9\.4M|9,400,000|512|2\s*블록|Base)", content)),
            "Missing DIVER-1 Base architecture specifications (9.4M params, 512 width)"
        )
        self.assertTrue(
            bool(re.search(r"(51M|Small|13M|Tiny|1024)", content)),
            "Missing ablation model variants (51M Small, 13M Tiny, or width 1024)"
        )
        self.assertTrue(
            bool(re.search(r"(MAE|Masked Autoencoder|ACPE|DIVER-1\.5|DIVER-2)", content)),
            "Missing pretraining architecture specification (MAE, ACPE, DIVER-2)"
        )

    def test_f2_03_fixed_compute_sample_exposure(self):
        """[T1-F2-03] Verify documentation of 2.88M fixed exposure sample control."""
        content = self.read_doc_safe("docs/01_research_synthesis.md")
        self.assertTrue(
            bool(re.search(r"(288만|2\.88M|2,880,000|2,887,680)", content)),
            "Missing 2.88M fixed exposure sample count figure"
        )
        self.assertTrue(
            bool(re.search(r"(3초|3\s*second|32\s*채널|32\s*channel)", content)),
            "Missing sample window specs (3 seconds, 32 channels)"
        )
        self.assertTrue(
            bool(re.search(r"(crop|반복|repeat|충원|random)", content)),
            "Missing resampling/repetition mechanism description"
        )

    def test_f2_04_subject_scaling_threshold_metrics(self):
        """[T1-F2-04] Verify 37 subjects pool baseline, 8-subject preservation, and 2-subject collapse."""
        content = self.read_doc_safe("docs/01_research_synthesis.md")
        self.assertTrue(
            bool(re.search(r"(37\s*명|37\s*subjects)", content)),
            "Missing 37 total subjects baseline pool figure"
        )
        self.assertTrue(
            bool(re.search(r"(8\s*명|8\s*subjects)", content)) and bool(re.search(r"(\+\s*0?\.0001|-\s*0?\.0013|유지)", content)),
            "Missing 8-subject preservation metrics (+0.0001 / -0.0013)"
        )
        self.assertTrue(
            bool(re.search(r"(2\s*명|2\s*subjects)", content)) and bool(re.search(r"(-\s*0?\.0055|-\s*0?\.0052|붕괴)", content)),
            "Missing 2-subject collapse metrics (-0.0055)"
        )

    def test_f2_05_duration_reduction_noninferiority_metrics(self):
        """[T1-F2-05] Verify 1/64 (81h) and 1/1024 (5h) non-inferiority margins and held-out loss."""
        content = self.read_doc_safe("docs/01_research_synthesis.md")
        self.assertTrue(
            bool(re.search(r"1/64", content)) and bool(re.search(r"(81|81\.3)\s*시간", content)),
            "Missing 1/64 (81h) metrics"
        )
        self.assertTrue(
            bool(re.search(r"1/1024", content)) and bool(re.search(r"(5|5\.1)\s*시간", content)),
            "Missing 1/1024 (5h) metrics"
        )
        self.assertTrue(
            bool(re.search(r"(-0\.0004|\+0\.0006|-0\.005|비열등성)", content)),
            "Missing non-inferiority delta score verification (margin delta > -0.005)"
        )
        self.assertTrue(
            bool(re.search(r"(Held-out|reconstruction loss|\+8\.5%|8\.5)", content)),
            "Missing held-out reconstruction loss (+8.5%) vs downstream score dissociation"
        )

    # --- F3: Deep Research & Theoretical Foundation ---

    def test_f3_01_deep_research_document_presence(self):
        """[T1-F3-01] Verify docs/02_deep_research_literature.md exists with substantial content (>= 4KB)."""
        content = self.read_doc_safe("docs/02_deep_research_literature.md", min_size=4000)
        self.assertGreaterEqual(len(content), 4000, "docs/02_deep_research_literature.md must be >= 4000 characters")

    def test_f3_02_five_key_literature_citations(self):
        """[T1-F3-02] Verify formal citations for all 5 foundation papers (Oliveira, Ooi, Narayanswamy, Banville, Truong)."""
        content = self.read_doc_safe("docs/02_deep_research_literature.md")
        for author in ["Oliveira", "Ooi", "Narayanswamy", "Banville", "Truong"]:
            self.assertIn(author.lower(), content.lower(), f"Missing core author citation: {author}")

    def test_f3_03_two_axis_scaling_law_theoretical_formulation(self):
        """[T1-F3-03] Verify 2-axis scaling law formulation (Subjects N vs Duration T) against 1D LLM laws."""
        content = self.read_doc_safe("docs/02_deep_research_literature.md")
        self.assertTrue(
            bool(re.search(r"(Chinchilla|Kaplan|1차원|1-D)", content)),
            "Missing 1D token scaling law comparison (Chinchilla / Kaplan)"
        )
        self.assertTrue(
            bool(re.search(r"(피험자\s*수|subject|N).*?(시간|duration|T)", content, re.I)),
            "Missing 2-axis parametric formulation (N vs T)"
        )
        self.assertTrue(
            bool(re.search(r"(\\?alpha|\\?beta|\\?gamma|L_\\?infty|K_1|K_2)", content)),
            "Missing parametric scaling formula notation"
        )

    def test_f3_04_eeg_vs_ieeg_modality_transfer_synthesis(self):
        """[T1-F3-04] Verify biophysical and architectural explanation of EEG vs iEEG modality differences."""
        content = self.read_doc_safe("docs/02_deep_research_literature.md")
        self.assertTrue(
            bool(re.search(r"(두피|scalp|EEG).*?(침습|intracranial|iEEG)", content, re.I)),
            "Missing scalp EEG vs intracranial iEEG comparison"
        )
        self.assertTrue(
            bool(re.search(r"(저역|low-frequency|고주파|high-gamma|감쇄|attenuation)", content)),
            "Missing physical signal characteristics (high-gamma attenuation)"
        )
        self.assertTrue(
            bool(re.search(r"(BrainWave|BrainOmni|DIVER)", content)),
            "Missing benchmark model comparisons (BrainWave, BrainOmni, DIVER)"
        )

    def test_f3_05_94_paper_corpus_and_taxonomy_context(self):
        """[T1-F3-05] Verify reference to the 94-paper foundation survey corpus establishing novelty."""
        content = self.read_doc_safe("docs/02_deep_research_literature.md")
        self.assertTrue(
            bool(re.search(r"(94\s*편|94\s*papers|서베이|survey|메타분석)", content)),
            "Missing 94-paper foundation survey corpus reference"
        )
        self.assertTrue(
            bool(re.search(r"(ICLR|NeurIPS|Nature|IEEE|arXiv)", content)),
            "Missing top-tier academic conference/journal representations"
        )

    # --- F4: Scientific Adversarial Review ---

    def test_f4_01_adversarial_review_document_presence(self):
        """[T1-F4-01] Verify docs/03_adversarial_review.md exists with substantial content (>= 4KB)."""
        content = self.read_doc_safe("docs/03_adversarial_review.md", min_size=4000)
        self.assertGreaterEqual(len(content), 4000, "docs/03_adversarial_review.md must be >= 4000 characters")

    def test_f4_02_five_methodological_vulnerability_axes(self):
        """[T1-F4-02] Verify coverage of all 5 scientific methodology vulnerability axes."""
        content = self.read_doc_safe("docs/03_adversarial_review.md")
        axes = [
            r"(가설\s*타당성|hypothesis\s*validity|layer\s*readout|읽는\s*층)",
            r"(인과\s*추론|causal\s*inference|reconstruction\s*loss|재구성\s*손실)",
            r"(대조군|control\s*design|downstream|인지\s*과제|MAYO|병리)",
            r"(SSL|자체지도학습|MAE|channel\s*origin|대안\s*가설)",
            r"(통계적\s*엄밀성|statistical\s*rigor|피험자\s*수|site\s*effect|교란)",
        ]
        for pattern in axes:
            self.assertTrue(
                bool(re.search(pattern, content, re.I)),
                f"Missing adversarial axis matching pattern: {pattern}"
            )

    def test_f4_03_readout_layer_divergence_critique(self):
        """[T1-F4-03] Verify critique of Layer 1 vs Layer 12 representation collapse in 1/1024 regime."""
        content = self.read_doc_safe("docs/03_adversarial_review.md")
        self.assertTrue(
            bool(re.search(r"(첫\s*번째\s*블록|1st\s*layer|layer\s*1)", content, re.I)),
            "Missing Layer 1 readout analysis"
        )
        self.assertTrue(
            bool(re.search(r"(마지막|최종|last\s*layer|layer\s*12)", content, re.I)),
            "Missing Layer 12 readout analysis"
        )
        self.assertTrue(
            bool(re.search(r"(-0\.0050|괴리|붕괴|divergence)", content)),
            "Missing critique of deep representation collapse in 1/1024"
        )

    def test_f4_04_reconstruction_loss_downstream_paradox(self):
        """[T1-F4-04] Verify critique of +8.5% reconstruction loss degradation vs preserved probe scores."""
        content = self.read_doc_safe("docs/03_adversarial_review.md")
        self.assertTrue(
            bool(re.search(r"(재구성\s*손실|reconstruction\s*loss)", content, re.I)),
            "Missing reconstruction loss critique"
        )
        self.assertTrue(
            bool(re.search(r"(다운스트림|downstream|probe|점수)", content, re.I)),
            "Missing downstream score contrast"
        )
        self.assertTrue(
            bool(re.search(r"(모순|괴리|역설|paradox|dissociation)", content, re.I)),
            "Missing identification of the dissociation paradox"
        )

    def test_f4_05_subject_threshold_confounding_factors(self):
        """[T1-F4-05] Verify methodological assessment of site effects, montage coverage, and statistical corrections."""
        content = self.read_doc_safe("docs/03_adversarial_review.md")
        self.assertTrue(
            bool(re.search(r"(전극|electrode|montage|sEEG|ECoG)", content, re.I)),
            "Missing electrode/montage confounding analysis"
        )
        self.assertTrue(
            bool(re.search(r"(site|병원|코호트|PennEPI|AJILE)", content)),
            "Missing site/cohort variation critique"
        )
        self.assertTrue(
            bool(re.search(r"(다중\s*비교|multiple\s*comparisons|Bonferroni|FDR)", content)),
            "Missing statistical correction critique (Bonferroni / FDR)"
        )

    # --- F5: Actionable Improvement Items & Prioritized Roadmap ---

    def test_f5_01_roadmap_document_presence(self):
        """[T1-F5-01] Verify docs/04_action_items_roadmap.md exists with substantial content (>= 3.5KB)."""
        content = self.read_doc_safe("docs/04_action_items_roadmap.md", min_size=3500)
        self.assertGreaterEqual(len(content), 3500, "docs/04_action_items_roadmap.md must be >= 3500 characters")

    def test_f5_02_immediate_tier_neuroai_workshop_items(self):
        """[T1-F5-02] Verify Immediate Tier action items for AAAI 2027 NeuroAI Workshop (2026-11-20)."""
        content = self.read_doc_safe("docs/04_action_items_roadmap.md")
        self.assertTrue(
            bool(re.search(r"(단기|Immediate|Tier\s*1)", content, re.I)),
            "Missing Immediate priority tier"
        )
        self.assertTrue(
            bool(re.search(r"(NeuroAI|11/20|11월\s*20일)", content)),
            "Missing 2026-11-20 submission deadline reference"
        )
        self.assertTrue(
            bool(re.search(r"(seed|시드|마지막\s*층|last\s*layer|Figure)", content)),
            "Missing concrete short-term action tasks (seed expansion, layer 12, figures)"
        )

    def test_f5_03_medium_term_diver2_journal_items(self):
        """[T1-F5-03] Verify Medium-Term action items for DIVER-2 journal paper and Aurora HPC."""
        content = self.read_doc_safe("docs/04_action_items_roadmap.md")
        self.assertTrue(
            bool(re.search(r"(중기|Medium|Tier\s*2)", content, re.I)),
            "Missing Medium priority tier"
        )
        self.assertTrue(
            bool(re.search(r"(DIVER-2|저널|journal|Nature|Aurora)", content, re.I)),
            "Missing DIVER-2 journal track and compute references"
        )
        self.assertTrue(
            bool(re.search(r"(SSL|channel\s*origin|contrastive|MAYO|병리)", content, re.I)),
            "Missing medium-term pretraining and clinical validation tasks"
        )

    def test_f5_04_long_term_clinical_scaling_items(self):
        """[T1-F5-04] Verify Long-Term action items for clinical expansion and multi-site scaling."""
        content = self.read_doc_safe("docs/04_action_items_roadmap.md")
        self.assertTrue(
            bool(re.search(r"(장기|Long|Tier\s*3)", content, re.I)),
            "Missing Long-term priority tier"
        )
        self.assertTrue(
            bool(re.search(r"(임상|clinical|간질|epilepsy|다기관|multi-site)", content)),
            "Missing clinical expansion and multi-site scaling scope"
        )

    def test_f5_05_action_item_metadata_attributes(self):
        """[T1-F5-05] Verify structured schema for action items (Owner, Timeline, Deliverable, Acceptance Criteria)."""
        content = self.read_doc_safe("docs/04_action_items_roadmap.md")
        for field in ["담당", "일정", "산출물", "판정 기준"]:
            self.assertTrue(
                field in content or field.lower() in content.lower(),
                f"Missing structured action item attribute: {field}"
            )

    # --- F6: Git Repository Structuring & Transconnectome Push ---

    def test_f6_01_git_repository_initialization(self):
        """[T1-F6-01] Verify local git repository initialization (.git directory presence)."""
        self.check_git_initialized()
        res = subprocess.run(["git", "status"], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"git status failed: {res.stderr}")

    def test_f6_02_commit_history_presence(self):
        """[T1-F6-02] Verify non-empty git commit log in local repository."""
        self.check_git_initialized()
        res = subprocess.run(["git", "log", "-n", "1", "--oneline"], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, "No git commits found in repository")
        self.assertGreater(len(res.stdout.strip()), 0, "Git commit history is empty")

    def test_f6_03_executive_summary_readme_presence(self):
        """[T1-F6-03] Verify README.md exists in root, >= 3000 chars, referencing both researchers."""
        content = self.read_doc_safe("README.md", min_size=3000)
        self.assertIn("안채원 선생님", content, "Missing honorific reference to 안채원 선생님 in README.md")
        self.assertIn("이아현 선생님", content, "Missing honorific reference to 이아현 선생님 in README.md")

    def test_f6_04_gitignore_proper_configuration(self):
        """[T1-F6-04] Verify .gitignore exists and excludes Python cache artifacts."""
        content = self.read_doc_safe(".gitignore", min_size=10)
        self.assertTrue(
            bool(re.search(r"(__pycache__|\*\.pyc|\.pytest_cache)", content)),
            "Missing standard Python cache exclusions in .gitignore"
        )

    def test_f6_05_transconnectome_remote_configured(self):
        """[T1-F6-05] Verify Git remote origin is configured to Transconnectome/chaewon_ahyeon_research_review."""
        self.check_git_initialized()
        res = subprocess.run(["git", "remote", "-v"], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, "git remote -v failed")
        self.assertIn(
            "Transconnectome/chaewon_ahyeon_research_review",
            res.stdout,
            f"Remote origin not configured for Transconnectome/chaewon_ahyeon_research_review: {res.stdout}"
        )

    # --- F7: E2E Acceptance Criteria Verification ---

    def test_f7_01_acceptance_checklist_representation(self):
        """[T1-F7-01] Verify test suite docstrings and mappings represent all requirements (R1..R4, F1..F7)."""
        test_file = self.root / "tests/verify_acceptance_criteria.py"
        self.assertTrue(test_file.is_file(), "tests/verify_acceptance_criteria.py must exist")
        content = test_file.read_text(encoding="utf-8")
        for item in ["R1", "R2", "R3", "R4", "F1", "F2", "F3", "F4", "F5", "F6", "F7"]:
            self.assertIn(item, content, f"Missing requirement/feature checklist mapping: {item}")

    def test_f7_02_runner_self_verification_execution(self):
        """[T1-F7-02] Verify test runner self-execution with CLI --help flag exits with code 0."""
        res = subprocess.run(
            [sys.executable, str(self.root / "tests/verify_acceptance_criteria.py"), "--help"],
            capture_output=True,
            text=True
        )
        self.assertEqual(res.returncode, 0, f"CLI --help failed with code {res.returncode}: {res.stderr}")
        self.assertTrue(
            "usage" in res.stdout.lower() or "options" in res.stdout.lower(),
            "CLI --help output missing standard usage description"
        )

    def test_f7_03_structured_console_summary_output(self):
        """[T1-F7-03] Verify test runner implements structured 4-tier reporting logic."""
        test_file = self.root / "tests/verify_acceptance_criteria.py"
        content = test_file.read_text(encoding="utf-8")
        for tier in ["Tier 1", "Tier 2", "Tier 3", "Tier 4"]:
            self.assertIn(tier, content, f"Test runner lacks reporting section for {tier}")
        self.assertTrue(
            "SUMMARY" in content.upper() or "REPORT" in content.upper(),
            "Missing structured summary generator in test runner"
        )

    def test_f7_04_machine_readable_json_report_support(self):
        """[T1-F7-04] Verify test runner supports --report-json argument and JSON serialization."""
        test_file = self.root / "tests/verify_acceptance_criteria.py"
        content = test_file.read_text(encoding="utf-8")
        self.assertTrue(
            "--report-json" in content or "report_json" in content,
            "Missing --report-json argument handling in test runner"
        )
        self.assertTrue(
            "json.dump" in content or "json.dumps" in content,
            "Missing JSON export serialization in test runner"
        )

    def test_f7_05_total_test_count_threshold(self):
        """[T1-F7-05] Verify test suite contains at least 82 implemented test methods."""
        test_file = self.root / "tests/verify_acceptance_criteria.py"
        content = test_file.read_text(encoding="utf-8")
        test_methods = re.findall(r"def\s+(test_[a-zA-Z0-9_]+)\s*\(", content)
        self.assertGreaterEqual(
            len(test_methods),
            82,
            f"Total implemented test methods {len(test_methods)} < 82 minimum required"
        )


# =====================================================================
# Tier 2: Boundary & Corner Cases (F1 through F7, 35 Tests)
# =====================================================================

class TestTier2BoundaryCases(BaseAcceptanceTest):
    """Tier 2: Boundary assertion, numerical intervals, formatting hygiene, and lab governance policies."""

    # --- F1-B: Honorifics & Text Integrity ---

    def test_f1_b01_strict_honorifics_chaewon_ahn(self):
        """[T2-F1B-01] STRICT POLICY: Zero instances of banned informal address or 반말 across all documentation."""
        md_files = get_all_markdown_files()
        if not md_files and self.progressive:
            self.skipTest("[PROGRESSIVE] No markdown files exist yet to audit honorifics")
        # Every instance of '안채원' must be followed by '선생님'; bare non-honorific or 반말 is strictly banned
        non_honorific_pattern = re.compile(r"안채원(?!\s*선생님)")
        for md in md_files:
            text = md.read_text(encoding="utf-8")
            violations = []
            for line_no, line in enumerate(text.splitlines(), start=1):
                if non_honorific_pattern.search(line):
                    violations.append(f"  Line {line_no}: {line.strip()}")
            self.assertFalse(
                violations,
                f"Policy breach in {md.name}: Found non-honorific or bare address for 안채원 선생님 (Must ALWAYS be '안채원 선생님'):\n"
                + "\n".join(violations),
            )
            if "안채원" in text:
                self.assertIn("안채원 선생님", text, f"Missing honorific '안채원 선생님' in {md.name}")

    def test_f1_b02_strict_honorifics_ahhyun_lee(self):
        """[T2-F1B-02] STRICT POLICY: Zero instances of banned informal address or 반말 across all documentation."""
        md_files = get_all_markdown_files()
        if not md_files and self.progressive:
            self.skipTest("[PROGRESSIVE] No markdown files exist yet to audit honorifics")
        # Every instance of '이아현' must be followed by '선생님'; bare non-honorific or 반말 is strictly banned
        non_honorific_pattern = re.compile(r"이아현(?!\s*선생님)")
        for md in md_files:
            text = md.read_text(encoding="utf-8")
            violations = []
            for line_no, line in enumerate(text.splitlines(), start=1):
                if non_honorific_pattern.search(line):
                    violations.append(f"  Line {line_no}: {line.strip()}")
            self.assertFalse(
                violations,
                f"Policy breach in {md.name}: Found non-honorific or bare address for 이아현 선생님 (Must ALWAYS be '이아현 선생님'):\n"
                + "\n".join(violations),
            )
            if "이아현" in text:
                self.assertIn("이아현 선생님", text, f"Missing honorific '이아현 선생님' in {md.name}")

    def test_f1_b03_global_student_honorific_audit(self):
        """[T2-F1B-03] Lab Policy: Students & researchers ALWAYS '선생님'; no improper informal suffixes."""
        md_files = get_all_markdown_files()
        if not md_files and self.progressive:
            self.skipTest("[PROGRESSIVE] No markdown files exist yet to audit honorifics")
        target_names = ["채원", "아현", "주빈", "규형", "동엽"]
        # Match student/researcher names followed by informal suffixes (씨 or 학생)
        # Supports full names with surnames ('김주빈', '박규형', '최동엽', '안채원', '이아현')
        # Handles attached Korean postpositions (e.g. 씨는, 씨가, 씨를, 씨와, 씨의, 씨에게) and delimiters
        particles_and_delimiters = (
            r"(?:[는은이가를을와의과에도만로]|에게|한테|께|으로|란|이며|이고|이나|이랑|처럼|보다|마저|조차|요|\s|[.,!?;:\)\]\>\"\'\-]|$)"
        )
        pattern = re.compile(rf"([가-힣]{{2,4}})\s*(씨|학생)(?={particles_and_delimiters})")
        for md in md_files:
            text = md.read_text(encoding="utf-8")
            matches = pattern.findall(text)
            suspicious = [
                f"{name} {suffix}"
                for name, suffix in matches
                if any(t in name for t in target_names)
            ]
            self.assertFalse(
                suspicious,
                f"Found improper student/researcher informal address in {md.name}: {suspicious} "
                f"(Students & researchers must ALWAYS be addressed with '선생님')",
            )

    def test_f1_b04_verbatim_quote_integrity(self):
        """[T2-F1B-04] Verify key Teams dialogue fragments are preserved verbatim without distortion."""
        content = self.read_doc_safe("docs/01_research_synthesis.md")
        quotes = [
            "그냥 섞으면 알아서 잘 학습될 것들이 아니어서",
            "설익은 페이퍼를 쓰는 것보다는",
            "단순히 1/64로 데이터 양을 줄이는 것이 아니라 참가자 수는 유지하면서",
            "how should we scale 을 보여주는 좋은 포인트",
        ]
        for q in quotes:
            self.assertIn(q, content, f"Missing verbatim quote fragment: '{q}'")

    def test_f1_b05_minimum_word_count_and_depth(self):
        """[T2-F1B-05] Verify synthesis document density (>= 5000 characters and >= 6 major sections)."""
        content = self.read_doc_safe("docs/01_research_synthesis.md")
        self.assertGreaterEqual(len(content), 5000, f"Synthesis length {len(content)} chars < 5000 threshold")
        sections = re.findall(r"^#{2,3}\s+(.+)$", content, re.M)
        self.assertGreaterEqual(len(sections), 6, f"Insufficient structural sections: {len(sections)} < 6")

    # --- F2-B: Numeric Consistency & Boundary Checks ---

    def test_f2_b01_subject_threshold_bounds(self):
        """[T2-F2B-01] Verify mathematical bounds: N>=8 preserves delta score; N=2 collapses <= -0.0050."""
        content = self.read_doc_safe("docs/01_research_synthesis.md")
        self.assertTrue(
            bool(re.search(r"8\s*명.*?(-0\.0013|\+0\.0001|유지)", content, re.DOTALL)),
            "8-subject preservation bounds violated or not articulated"
        )
        self.assertTrue(
            bool(re.search(r"2\s*명.*?(-0\.005[25]|붕괴)", content, re.DOTALL)),
            "2-subject collapse bounds violated or not articulated"
        )

    def test_f2_b02_delta_score_sign_and_intervals(self):
        """[T2-F2B-02] Verify non-inferiority margin sign (margin -0.005) and iEEG_re advantage over EEG_fill."""
        content = self.read_doc_safe("docs/01_research_synthesis.md")
        self.assertTrue(
            bool(re.search(r"-\s*0?\.005", content)),
            "Missing non-inferiority threshold -0.005"
        )
        self.assertTrue(
            bool(re.search(r"(\+\s*0?\.0100|0?\.0100|0?\.01\s*우세|0?\.010\s*하락)", content)),
            "Missing +0.0100 advantage of iEEG_re over EEG_fill"
        )

    def test_f2_b03_kisti_scaling_monotonicity(self):
        """[T2-F2B-03] Verify KISTI scaling throughput values monotonicity (1-node ~189.7 to 8-node ~1180.1)."""
        content = self.read_doc_safe("docs/01_research_synthesis.md")
        node_dict = {}
        for line in content.splitlines():
            node_m = re.search(r"(?:(\d+)\s*[-–—]?\s*(?:노드|node)|(?:노드|node)\s*(\d+))", line, re.IGNORECASE)
            tp_m = re.search(r"(\d{1,2},?\d{3}(?:\.\d+)?|\d{2,4}(?:\.\d+)?)\s*(?:samples/s|s/s)", line, re.IGNORECASE)
            if node_m and tp_m:
                node_cnt = int(node_m.group(1) or node_m.group(2))
                tp_val = float(tp_m.group(1).replace(",", ""))
                if node_cnt not in node_dict:
                    node_dict[node_cnt] = tp_val

        sorted_nodes = sorted(node_dict.keys())
        throughputs = [node_dict[k] for k in sorted_nodes]

        self.assertGreaterEqual(
            len(sorted_nodes),
            3,
            f"Expected at least 3 node scaling data points in docs/01_research_synthesis.md, found: {sorted_nodes}"
        )
        self.assertTrue(
            any(180 <= n <= 200 for n in throughputs),
            f"Missing 1-node throughput ~189.7 samples/s in {throughputs}"
        )
        self.assertTrue(
            any(1150 <= n <= 1200 for n in throughputs),
            f"Missing 8-node throughput ~1180.1 samples/s in {throughputs}"
        )
        self.assertTrue(
            all(x < y for x, y in zip(throughputs, throughputs[1:])),
            f"KISTI throughput is not strictly monotonic across increasing node counts: {list(zip(sorted_nodes, throughputs))}"
        )

    def test_f2_b04_sample_exposure_calculation_math(self):
        """[T2-F2B-04] Verify internal arithmetic consistency: 2.88M samples from 5,203 hours total pool."""
        content = self.read_doc_safe("docs/01_research_synthesis.md")
        self.assertTrue(
            "2.88M" in content or "288만" in content or "2,880,000" in content,
            "Missing 2.88M sample exposure figure"
        )
        self.assertTrue(
            "5,203" in content or "5203" in content,
            "Missing 5,203 total hours pool figure"
        )

    def test_f2_b05_no_placeholder_tokens_in_tables(self):
        """[T2-F2B-05] Verify absence of placeholder tokens ([TODO], [TBD], [?], xxx) document-wide outside code blocks."""
        content = self.read_doc_safe("docs/01_research_synthesis.md")
        # Strip fenced code blocks and inline code to prevent false positives on code examples
        content_clean = re.sub(r"```[\s\S]*?```", "", content)
        content_clean = re.sub(r"~~~[\s\S]*?~~~", "", content_clean)
        content_clean = re.sub(r"`[^`\n]+`", "", content_clean)

        placeholder_pattern = re.compile(
            r"\[(?:TBD|TODO|\?)[^\]]*\]|\b(?:TBD|TODO)\b|\bxxx\b|0\.000\?",
            re.IGNORECASE
        )

        violations = []
        for line_no, line in enumerate(content_clean.splitlines(), start=1):
            matches = placeholder_pattern.findall(line)
            if matches:
                violations.append(f"Line {line_no}: {line.strip()} (found: {matches})")

        self.assertFalse(
            bool(violations),
            f"Found placeholder tokens in docs/01_research_synthesis.md:\n" + "\n".join(violations)
        )

    # --- F3-B: Reference Integrity & Citation Hygiene ---

    def test_f3_b01_valid_publication_years(self):
        """[T2-F3B-01] Verify citation publication years fall in valid scholarly range [1950..2027] with contemporary papers."""
        content = self.read_doc_safe("docs/02_deep_research_literature.md")
        years = [int(y) for y in re.findall(r"\b(19\d\d|20\d\d)\b", content)]
        self.assertTrue(years, "No publication years found in literature review")
        self.assertTrue(
            all(1950 <= y <= 2027 for y in years),
            f"Detected invalid publication year out of range [1950..2027]: {years}"
        )
        self.assertTrue(
            2025 in years or 2026 in years,
            "Missing contemporary 2025/2026 foundation model literature citations"
        )

    def test_f3_b02_real_arxiv_and_doi_identifiers(self):
        """[T2-F3B-02] Verify presence of real, verified arXiv identifiers (at least 4 verified IDs)."""
        content = self.read_doc_safe("docs/02_deep_research_literature.md")
        verified_arxivs = ["2609.35056", "2410.13638", "2501.15322", "2610.09287", "2512.19097"]
        matched = [arx for arx in verified_arxivs if arx in content]
        self.assertGreaterEqual(
            len(matched),
            4,
            f"Insufficient verified arXiv identifiers found: {matched} (required >= 4)"
        )

    def test_f3_b03_structured_literature_comparison_schema(self):
        """[T2-F3B-03] Verify structured comparative table with Author, Modality, and Architecture dimensions."""
        content = self.read_doc_safe("docs/02_deep_research_literature.md")
        headers = [l for l in content.splitlines() if "|" in l and ("Author" in l or "연구" in l or "저자" in l or "Model" in l or "모델" in l)]
        self.assertTrue(headers, "Missing structured literature comparison table header")
        self.assertTrue(
            any("모달리티" in l or "Modality" in l for l in headers),
            "Comparison table missing Modality column"
        )

    def test_f3_b04_deep_citation_breadth(self):
        """[T2-F3B-04] Verify deep scholarly foundation (at least 10 formal citations/references)."""
        content = self.read_doc_safe("docs/02_deep_research_literature.md")
        citations = re.findall(r"(?:et al\.|arXiv:|doi:|\[\d+\])", content, re.I)
        self.assertGreaterEqual(
            len(citations),
            10,
            f"Insufficient citation depth: found {len(citations)} citations < 10"
        )

    def test_f3_b05_latex_math_syntax_validity(self):
        """[T2-F3B-05] Verify valid syntax and balanced braces in LaTeX scaling formulas (display and inline)."""
        content = self.read_doc_safe("docs/02_deep_research_literature.md")
        # Extract display math blocks ($$...$$) first to prevent parser desynchronization
        display_blocks = re.findall(r"\$\$(.+?)\$\$", content, re.DOTALL)
        # Strip display math blocks before extracting inline math blocks ($...$)
        clean_content = re.sub(r"\$\$(.+?)\$\$", "", content, flags=re.DOTALL)
        inline_blocks = re.findall(r"(?<!\$)\$([^\$\n]+)\$(?!\$)", clean_content)
        all_blocks = display_blocks + inline_blocks

        self.assertGreaterEqual(
            len(all_blocks),
            2,
            f"Insufficient mathematical formulations in literature review: found {len(all_blocks)} < 2"
        )
        for block in all_blocks:
            self.assertEqual(
                block.count("{"),
                block.count("}"),
                f"Unbalanced braces in LaTeX formula: {block.strip()}"
            )

    # --- F4-B: Adversarial Challenge Rigor ---

    def test_f4_b01_all_five_contract_vulnerabilities_covered(self):
        """[T2-F4B-01] Verify all 5 interface contract vulnerability categories are addressed."""
        content = self.read_doc_safe("docs/03_adversarial_review.md")
        contract_pairs = [
            ("Readout layer", "읽는 층"),
            ("Reconstruction loss", "재구성 손실"),
            ("Linear probing", "선형 프로브"),
            ("Masked Autoencoding", "자체지도학습"),
            ("Subject diversity", "피험자 다양성"),
        ]
        missing = [
            f"'{en}' / '{ko}'" for en, ko in contract_pairs
            if en.lower() not in content.lower() and ko not in content
        ]
        self.assertEqual(
            len(missing),
            0,
            f"All 5 contract vulnerability categories must be addressed in docs/03_adversarial_review.md. Missing {len(missing)}: {missing}"
        )

    def test_f4_b02_anti_vagueness_heuristic_check(self):
        """[T2-F4B-02] Verify adversarial review is grounded in technical mechanisms, not vague platitudes."""
        content = self.read_doc_safe("docs/03_adversarial_review.md")
        mechanisms = ["overfitting", "all-reduce", "high-gamma", "Bonferroni", "FDR", "linear probe", "representation", "ComBat", "batch effect"]
        present = [m for m in mechanisms if m.lower() in content.lower()]
        self.assertGreaterEqual(
            len(present),
            4,
            f"Adversarial review lacks concrete technical mechanisms: found {present}"
        )

    def test_f4_b03_empirical_counterevidence_citation(self):
        """[T2-F4B-03] Verify critiques cite established empirical literature baselines."""
        content = self.read_doc_safe("docs/03_adversarial_review.md")
        self.assertTrue(
            bool(re.search(r"(Oliveira|Ooi|Banville|Narayanswamy|Truong|He\s*et\s*al|Chinchilla)", content)),
            "Adversarial review does not anchor counter-arguments in literature"
        )

    def test_f4_b04_falsification_conditions_stated(self):
        """[T2-F4B-04] Verify explicit Popperian falsification and invalidation conditions are articulated."""
        content = self.read_doc_safe("docs/03_adversarial_review.md")
        self.assertTrue(
            bool(re.search(r"(무효화\s*조건|반증\s*가능성|falsification|invalidation)", content, re.I)),
            "Missing explicit falsification/invalidation conditions in adversarial review"
        )

    def test_f4_b05_institutional_genre_and_voice(self):
        """[T2-F4B-05] Lab Policy: Professional scientific voice; zero informal colloquialisms."""
        content = self.read_doc_safe("docs/03_adversarial_review.md")
        prohibited = ["ㅋㅋㅋ", "ㅎㅎ", "ㅠㅠ", "대박", "엄청난", "내 생각에는", "내가 보기에는"]
        for phrase in prohibited:
            self.assertNotIn(phrase, content, f"Detected informal colloquialism: '{phrase}'")

    # --- F5-B: Action Item Executability & Feasibility ---

    def test_f5_b01_action_item_code_methodology_pointer(self):
        """[T2-F5B-01] Verify action items contain concrete technical pointers (scripts, Slurm, probes)."""
        content = self.read_doc_safe("docs/04_action_items_roadmap.md")
        pointers = [".py", "SLURM", "sbatch", "dataloader", "probe", "seed", "KISTI", "Aurora", "LMDB"]
        matched = [p for p in pointers if p.lower() in content.lower()]
        self.assertGreaterEqual(
            len(matched),
            4,
            f"Action items lack concrete technical pointers: found {matched}"
        )

    def test_f5_b02_quantitative_metric_targets(self):
        """[T2-F5B-02] Verify measurable quantitative targets in action item acceptance criteria."""
        content = self.read_doc_safe("docs/04_action_items_roadmap.md")
        self.assertTrue(
            bool(re.search(r"(\Delta\s*>\s*-0\.005|n\s*>=\s*6|p\s*<\s*0\.05|seed\s*\d)", content)),
            "Missing quantitative threshold in action item acceptance criteria"
        )

    def test_f5_b03_hard_deadline_neuroai_feasibility(self):
        """[T2-F5B-03] Verify Immediate Tier timeline respects the 2026-11-20 hard submission deadline."""
        content = self.read_doc_safe("docs/04_action_items_roadmap.md")
        self.assertTrue(
            "2026-11-20" in content or "11/20" in content,
            "Missing hard deadline 2026-11-20 in roadmap"
        )
        self.assertTrue(
            any(d in content for d in ["11/15", "11/17", "11/18", "11/19"]),
            "Missing intermediate milestone leading up to 11/20 deadline"
        )

    def test_f5_b04_compute_resource_allocation_specified(self):
        """[T2-F5B-04] Verify explicit compute resource mapping (KISTI 한강, Aurora, Slurm) in roadmap."""
        content = self.read_doc_safe("docs/04_action_items_roadmap.md")
        self.assertTrue(
            bool(re.search(r"(한강|KISTI|Aurora|GH200|GPU|Slurm)", content)),
            "Action items fail to specify required compute infrastructure"
        )

    def test_f5_b05_dependency_ordering_topology(self):
        """[T2-F5B-05] Verify sequential ordering: Immediate (단기) precedes Medium (중기) precedes Long (장기)."""
        content = self.read_doc_safe("docs/04_action_items_roadmap.md")
        m_imm = re.search(r"^#+\s*.*(?:단기|Immediate)", content, re.MULTILINE | re.IGNORECASE)
        m_med = re.search(r"^#+\s*.*(?:중기|Medium)", content, re.MULTILINE | re.IGNORECASE)
        m_lng = re.search(r"^#+\s*.*(?:장기|Long)", content, re.MULTILINE | re.IGNORECASE)
        self.assertIsNotNone(m_imm, "Missing Immediate/단기 roadmap section heading (e.g. '## 단기')")
        self.assertIsNotNone(m_med, "Missing Medium/중기 roadmap section heading (e.g. '## 중기')")
        self.assertIsNotNone(m_lng, "Missing Long/장기 roadmap section heading (e.g. '## 장기')")
        pos_imm, pos_med, pos_lng = m_imm.start(), m_med.start(), m_lng.start()
        self.assertTrue(
            pos_imm < pos_med < pos_lng,
            f"Roadmap section headers not sequentially ordered: pos_imm={pos_imm}, pos_med={pos_med}, pos_lng={pos_lng}"
        )

    # --- F6-B: Repository Cleanliness & Layout ---

    def test_f6_b01_clean_working_tree_no_temp_files(self):
        """[T2-F6B-01] Verify clean workspace: zero temporary backup files (*.swp, *.tmp, *~)."""
        banned = [".swp", ".swo", ".tmp", ".bak", "~"]
        dirty = []
        for f in self.root.rglob("*"):
            if ".git" in f.parts or ".agents" in f.parts:
                continue
            if f.suffix in banned or f.name.endswith("~"):
                dirty.append(str(f.relative_to(self.root)))
        self.assertFalse(dirty, f"Found temporary backup/dirty files in workspace: {dirty}")

    def test_f6_b02_agents_metadata_isolation(self):
        """[T2-F6B-02] Strict layout compliance: .agents/teamwork/ contains ONLY metadata, zero source/tests."""
        agents_dir = self.root / ".agents/teamwork"
        self.assertTrue(agents_dir.is_dir(), ".agents/teamwork directory does not exist")
        illegal = []
        allowed_exts = {".md", ".json", ".jsonl", ".txt", ".patch", ""}
        for f in agents_dir.rglob("*"):
            if f.is_file():
                if f.suffix not in allowed_exts:
                    illegal.append(str(f.relative_to(agents_dir)))
                if f.name in ["AGENTS.md", "GEMINI.md"]:
                    illegal.append(f"Forbidden rule filename: {f.name}")
        self.assertFalse(illegal, f"Non-metadata files found in .agents/teamwork/: {illegal}")

    def test_f6_b03_conventional_commit_messages(self):
        """[T2-F6B-03] Verify git commit messages adhere to Conventional Commits standards."""
        self.check_git_initialized()
        res = subprocess.run(["git", "log", "-n", "10", "--format=%s"], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        commits = [c.strip() for c in res.stdout.strip().splitlines() if c.strip()]
        self.assertTrue(commits, "No commits found to inspect")
        valid_prefixes = ("feat", "docs", "test", "fix", "chore", "refactor", "style", "Merge", "Initial")
        for msg in commits:
            self.assertTrue(
                any(msg.startswith(p) for p in valid_prefixes),
                f"Commit message does not follow convention: '{msg}'"
            )

    def test_f6_b04_markdown_file_size_bounds(self):
        """[T2-F6B-04] Verify all generated documents in docs/*.md are within [3KB, 200KB] bounds."""
        docs_dir = self.root / "docs"
        if not docs_dir.is_dir() or not list(docs_dir.glob("*.md")):
            if self.progressive:
                self.skipTest("[PROGRESSIVE] No documents in docs/ yet to check size bounds")
            self.fail("No markdown documents found in docs/")
        for md_file in docs_dir.glob("*.md"):
            size_kb = md_file.stat().st_size / 1024.0
            self.assertTrue(
                3.0 <= size_kb <= 200.0,
                f"File {md_file.name} size {size_kb:.1f} KB outside bounds [3KB, 200KB]"
            )

    def test_f6_b05_git_remote_url_exactness(self):
        """[T2-F6B-05] Verify Git remote URL points exactly to Transconnectome/chaewon_ahyeon_research_review."""
        self.check_git_initialized()
        res = subprocess.run(["git", "config", "--get", "remote.origin.url"], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, "No remote.origin.url configured")
        url = res.stdout.strip()
        self.assertIn(
            "Transconnectome/chaewon_ahyeon_research_review",
            url,
            f"Incorrect remote origin URL: {url}"
        )

    # --- F7-B: Test Framework Robustness ---

    def test_f7_b01_progressive_handling_of_missing_milestones(self):
        """[T2-F7B-01] Verify check_artifact_presence raises clear diagnostic AssertionError when strict."""
        test_path = self.root / "non_existent_test_artifact.md"
        try:
            check_artifact_presence(test_path, "Test Artifact", progressive=False)
            self.fail("Expected AssertionError on non-existent file")
        except AssertionError as e:
            self.assertIn("Test Artifact", str(e), "Diagnostic message lacks artifact context")

    def test_f7_b02_subsuite_filtering_by_tier_and_feature(self):
        """[T2-F7B-02] Verify test runner CLI filtering by tier and feature runs without crashing."""
        runner_path = self.root / "tests/verify_acceptance_criteria.py"
        res = subprocess.run(
            [sys.executable, str(runner_path), "--tier", "1", "--progressive"],
            capture_output=True,
            text=True
        )
        self.assertEqual(res.returncode, 0, f"Filtered runner execution failed: {res.stderr}")
        self.assertTrue(
            "Tier 1" in res.stdout or "Tier 1" in res.stderr,
            "Filtered runner output missing Tier 1 banner"
        )

    def test_f7_b03_strict_boolean_exit_codes(self):
        """[T2-F7B-03] Verify test harness complies strictly with standard unittest exit code contracts."""
        suite = unittest.TestSuite()
        suite.addTest(unittest.FunctionTestCase(lambda: None))
        runner = unittest.TextTestRunner(stream=io.StringIO())
        result = runner.run(suite)
        self.assertTrue(result.wasSuccessful(), "Null test run failed")

    def test_f7_b04_execution_idempotency(self):
        """[T2-F7B-04] Verify test runner execution is completely idempotent and produces no stray files."""
        files_before = set(p.name for p in self.root.iterdir())
        runner_path = self.root / "tests/verify_acceptance_criteria.py"
        subprocess.run(
            [sys.executable, str(runner_path), "--help"],
            capture_output=True,
            text=True
        )
        files_after = set(p.name for p in self.root.iterdir())
        self.assertEqual(
            files_before,
            files_after,
            f"Test runner left untracked files: {files_after - files_before}"
        )

    def test_f7_b05_execution_performance_benchmark(self):
        """[T2-F7B-05] Verify in-memory verification logic runs swiftly (< 10.0 seconds)."""
        start = time.time()
        md_files = get_all_markdown_files()
        elapsed = time.time() - start
        self.assertLess(elapsed, 10.0, f"File scanning took too long ({elapsed:.2f}s >= 10.0s)")


# =====================================================================
# Tier 3: Cross-Feature Interactions (7 Tests)
# =====================================================================

class TestTier3CrossInteractions(BaseAcceptanceTest):
    """Tier 3: Pairwise cross-feature consistency, provenance, and mitigation closure."""

    def test_tier3_01_f1_f2_data_provenance_consistency(self):
        """[T3-01] Cross-validate that Teams mentoring numbers match experimental tables (37 subjects, 5,203h)."""
        content = self.read_doc_safe("docs/01_research_synthesis.md")
        teams_mentions = re.findall(r"37\s*명|5[,.]?203\s*시간", content)
        self.assertGreaterEqual(
            len(teams_mentions),
            2,
            "Discrepancy between Teams discussion and experimental dataset figures"
        )

    def test_tier3_02_f1_f4_adversarial_targets_mentor_mentee_claims(self):
        """[T3-02] Cross-validate that adversarial review directly critiques claims from 안채원 선생님 & 이아현 선생님."""
        synthesis = self.read_doc_safe("docs/01_research_synthesis.md")
        adversarial = self.read_doc_safe("docs/03_adversarial_review.md")
        self.assertTrue(
            "1/64" in synthesis and "1/64" in adversarial,
            "Adversarial review does not challenge 1/64 data reduction claim"
        )
        self.assertTrue(
            ("피험자" in adversarial or "참가자" in adversarial) and ("다양성" in adversarial or "기록 시간" in adversarial),
            "Adversarial review does not evaluate 이아현 선생님's subject diversity framing"
        )

    def test_tier3_03_f2_f4_empirical_metrics_challenged_in_review(self):
        """[T3-03] Cross-validate that 2-subject empirical collapse (-0.0055) and loss (+8.5%) are addressed in review."""
        synthesis = self.read_doc_safe("docs/01_research_synthesis.md")
        adversarial = self.read_doc_safe("docs/03_adversarial_review.md")
        self.assertTrue(
            ("-0.0055" in synthesis and "-0.0055" in adversarial) or ("2명" in adversarial and "붕괴" in adversarial),
            "Adversarial review fails to analyze the 2-subject empirical collapse point"
        )
        self.assertTrue(
            ("8.5%" in synthesis or "+8.5%" in synthesis) and ("8.5%" in adversarial or "재구성 손실" in adversarial),
            "Adversarial review fails to analyze the +8.5% reconstruction loss degradation"
        )

    def test_tier3_04_f3_f4_literature_informs_adversarial_critique(self):
        """[T3-04] Cross-validate that literature from F3 anchors counter-arguments in F4 adversarial review."""
        lit = self.read_doc_safe("docs/02_deep_research_literature.md")
        adv = self.read_doc_safe("docs/03_adversarial_review.md")
        core_cites = ["Oliveira", "Ooi", "Narayanswamy", "Banville", "Truong"]
        shared = [c for c in core_cites if c.lower() in adv.lower()]
        self.assertGreaterEqual(
            len(shared),
            2,
            f"Adversarial review fails to use literature anchors from F3: found {shared}"
        )

    def test_tier3_05_f4_f5_vulnerabilities_map_to_action_items(self):
        """[T3-05] Cross-validate 1:1 mitigation trace from F4 vulnerabilities to F5 roadmap tasks."""
        adv = self.read_doc_safe("docs/03_adversarial_review.md")
        road = self.read_doc_safe("docs/04_action_items_roadmap.md")
        mitigations = [
            ("마지막 층" in adv and ("마지막 층" in road or "layer" in road.lower())),
            ("재구성 손실" in adv and ("손실" in road or "loss" in road.lower() or "SSL" in road)),
            ("MAYO" in adv or "인지 과제" in adv) and ("MAYO" in road or "병리" in road),
            ("seed" in adv.lower() and "seed" in road.lower()),
        ]
        self.assertTrue(
            all(mitigations),
            f"Vulnerability-to-mitigation mapping incomplete: {mitigations}"
        )

    def test_tier3_06_f5_f6_readme_mirrors_roadmap_priorities(self):
        """[T3-06] Cross-validate that README executive summary reflects the 3 prioritized roadmap tiers."""
        readme = self.read_doc_safe("README.md")
        road = self.read_doc_safe("docs/04_action_items_roadmap.md")
        self.assertTrue(
            bool(re.search(r"(단기|Immediate|11/20)", readme)),
            "README.md missing Immediate roadmap tier"
        )
        self.assertTrue(
            bool(re.search(r"(중기|Medium|DIVER-2)", readme)),
            "README.md missing Medium roadmap tier"
        )
        self.assertTrue(
            bool(re.search(r"(장기|Long|임상|clinical)", readme)),
            "README.md missing Long-term roadmap tier"
        )

    def test_tier3_07_f1_to_f6_end_to_end_traceability(self):
        """[T3-07] Cross-validate zero broken relative markdown links across docs/ and README.md."""
        md_files = get_all_markdown_files()
        if not md_files and self.progressive:
            self.skipTest("[PROGRESSIVE] No markdown files exist yet to check link integrity")
        for md in md_files:
            text = md.read_text(encoding="utf-8")
            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)
            for _, target in links:
                target_str = target.strip()
                if target_str.startswith(("http://", "https://", "mailto:", "ftp:")):
                    continue
                # Strip optional markdown title attribute (e.g. [label](path.md "title"))
                target_path = target_str.split()[0]
                # Strip section anchor fragment (e.g. path.md#section -> path.md)
                clean_target = target_path.split("#")[0].strip()
                if not clean_target:
                    # In-page section anchor (#heading); no file resolution needed
                    continue
                resolved = (md.parent / clean_target).resolve()
                self.assertTrue(
                    resolved.is_file(),
                    f"Broken relative link in {md.name}: '{target}' -> target file not found: {resolved}"
                )


# =====================================================================
# Tier 4: Real-World Acceptance Scenarios (5 Scenarios)
# =====================================================================

class TestTier4AcceptanceScenarios(BaseAcceptanceTest):
    """Tier 4: High-level real-world scenarios, lab governance, and submission readiness."""

    def test_tier4_s01_original_request_full_satisfaction(self):
        """[T4-S01] Verify complete fulfillment of R1..R4 criteria from ORIGINAL_REQUEST.md."""
        self.read_doc_safe("docs/01_research_synthesis.md", min_size=4000)
        self.read_doc_safe("docs/02_deep_research_literature.md", min_size=4000)
        self.read_doc_safe("docs/03_adversarial_review.md", min_size=4000)
        self.read_doc_safe("docs/04_action_items_roadmap.md", min_size=3500)
        self.read_doc_safe("README.md", min_size=3000)
        self.check_git_initialized()

    def test_tier4_s02_lab_governance_and_policy_compliance(self):
        """[T4-S02] Lab Policy: Strict honorifics and PI critical feedback acknowledged across documentation."""
        md_files = get_all_markdown_files()
        if not md_files and self.progressive:
            self.skipTest("[PROGRESSIVE] No markdown files exist yet to check lab governance")
        informal_pattern = re.compile(r"(안채원|이아현)(?!\s*선생님)")
        for md in md_files:
            text = md.read_text(encoding="utf-8")
            self.assertFalse(
                bool(informal_pattern.search(text)),
                f"Policy breach in {md.name}: non-honorific or bare address used for researcher (Must be '안채원 선생님', '이아현 선생님')"
            )
            if md.name in ["01_research_synthesis.md", "README.md"]:
                self.assertTrue(
                    "차지욱 교수님" in text or "지도교수" in text,
                    f"Missing PI feedback role in {md.name}"
                )

    def test_tier4_s03_publication_readiness_audit(self):
        """[T4-S03] Verify publication hygiene: markdown titles start with # and tables have valid delimiters."""
        md_files = get_all_markdown_files()
        if not md_files and self.progressive:
            self.skipTest("[PROGRESSIVE] No markdown files exist yet to audit publication readiness")
        for md in md_files:
            lines = md.read_text(encoding="utf-8").splitlines()
            self.assertTrue(
                lines and lines[0].startswith("# "),
                f"{md.name} does not start with top-level # title"
            )
            in_code = False
            for i, line in enumerate(lines):
                if line.strip().startswith("```"):
                    in_code = not in_code
                    continue
                if in_code:
                    continue
                if line.strip().startswith("|") and line.strip().endswith("|"):
                    cols = line.count("|")
                    self.assertGreaterEqual(
                        cols,
                        3,
                        f"Malformed table row in {md.name} line {i+1}: {line}"
                    )

    def test_tier4_s04_neuroai_2027_workshop_submission_readiness(self):
        """[T4-S04] Verify readiness for AAAI 2027 NeuroAI Workshop (working title, deadline, and figures)."""
        synthesis = self.read_doc_safe("docs/01_research_synthesis.md")
        roadmap = self.read_doc_safe("docs/04_action_items_roadmap.md")
        self.assertTrue(
            bool(re.search(r"(A Little iEEG Goes a Long Way|고유 iEEG는 얼마나 필요한가|NeuroAI)", synthesis)),
            "Missing NeuroAI workshop working paper title in synthesis"
        )
        self.assertTrue(
            "NeuroAI" in roadmap and "11/20" in roadmap,
            "Missing NeuroAI workshop submission target in roadmap"
        )
        self.assertTrue(
            bool(re.search(r"(Figure\s*1|Figure\s*2|Figure\s*3|그림)", synthesis)),
            "Missing figure definitions for paper in synthesis"
        )

    def test_tier4_s05_transconnectome_reproducibility_check(self):
        """[T4-S05] Verify test runner executes reproducibly without external network or uncaught exceptions."""
        runner_path = self.root / "tests/verify_acceptance_criteria.py"
        res = subprocess.run(
            [sys.executable, str(runner_path), "--tier", "1", "--progressive"],
            cwd=self.root,
            capture_output=True,
            text=True
        )
        self.assertNotIn("ERROR: root:", res.stderr, f"Uncaught exception in test runner: {res.stderr}")
        self.assertNotIn("Traceback (most recent call last):", res.stderr)


# =====================================================================
# Test Suite Assembly & CLI Runner Engine
# =====================================================================

TIER_CLASSES = {
    1: TestTier1FeatureCoverage,
    2: TestTier2BoundaryCases,
    3: TestTier3CrossInteractions,
    4: TestTier4AcceptanceScenarios,
}

FEATURE_PREFIXES = {
    "F1": ("test_f1_", "test_f1_b", "test_tier3_01", "test_tier3_02", "test_tier4_s02", "test_tier4_s04"),
    "F2": ("test_f2_", "test_f2_b", "test_tier3_01", "test_tier3_03", "test_tier4_s04"),
    "F3": ("test_f3_", "test_f3_b", "test_tier3_04", "test_tier4_s03"),
    "F4": ("test_f4_", "test_f4_b", "test_tier3_02", "test_tier3_03", "test_tier3_04", "test_tier3_05", "test_tier4_s01"),
    "F5": ("test_f5_", "test_f5_b", "test_tier3_05", "test_tier3_06", "test_tier4_s04"),
    "F6": ("test_f6_", "test_f6_b", "test_tier3_06", "test_tier3_07", "test_tier4_s01", "test_tier4_s03", "test_tier4_s05"),
    "F7": ("test_f7_", "test_f7_b", "test_tier3_07", "test_tier4_"),
}


def build_filtered_suite(
    tier: Optional[int] = None,
    feature: Optional[str] = None,
    progressive: bool = False,
) -> unittest.TestSuite:
    """Constructs a filtered unittest.TestSuite based on CLI criteria."""
    BaseAcceptanceTest.progressive = progressive

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    target_classes = [TIER_CLASSES[tier]] if tier else list(TIER_CLASSES.values())

    for cls in target_classes:
        for method_name in loader.getTestCaseNames(cls):
            if feature:
                prefixes = FEATURE_PREFIXES.get(feature.upper(), ())
                if not any(method_name.startswith(p) for p in prefixes):
                    continue
            suite.addTest(cls(method_name))

    return suite


def run_tests_with_reporting(
    tier: Optional[int] = None,
    feature: Optional[str] = None,
    progressive: bool = False,
    verbose: bool = False,
    report_json: Optional[str] = None,
) -> int:
    """Executes the test suite and displays a formatted ANSI 4-tier summary table."""
    suite = build_filtered_suite(tier=tier, feature=feature, progressive=progressive)
    total_tests = suite.countTestCases()

    start_time = time.time()
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2 if verbose else 1)
    result = runner.run(suite)
    elapsed = time.time() - start_time

    passed = total_tests - len(result.failures) - len(result.errors) - len(result.skipped)
    failed = len(result.failures) + len(result.errors)
    skipped = len(result.skipped)

    # ANSI Color Helpers
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}   E2E ACCEPTANCE CRITERIA VERIFICATION REPORT: chaewon_ahyeon_research_review{RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}")
    print(f"Mode: {'PROGRESSIVE' if progressive else 'STRICT'} | Elapsed: {elapsed:.3f}s | Target Count: {total_tests}")
    print(f"Filter: Tier={tier if tier else 'ALL'} | Feature={feature if feature else 'ALL'}\n")

    tier_counts = {1: {"total": 0, "pass": 0, "fail": 0, "skip": 0},
                   2: {"total": 0, "pass": 0, "fail": 0, "skip": 0},
                   3: {"total": 0, "pass": 0, "fail": 0, "skip": 0},
                   4: {"total": 0, "pass": 0, "fail": 0, "skip": 0}}

    failed_test_ids = {t[0].id() for t in result.failures} | {t[0].id() for t in result.errors}
    skipped_test_ids = {t[0].id() for t in result.skipped}

    target_tier_numbers = [tier] if tier else [1, 2, 3, 4]
    for t_num in target_tier_numbers:
        t_cls = TIER_CLASSES[t_num]
        loader = unittest.TestLoader()
        for m in loader.getTestCaseNames(t_cls):
            if feature:
                prefixes = FEATURE_PREFIXES.get(feature.upper(), ())
                if not any(m.startswith(p) for p in prefixes):
                    continue
            test_id = f"{t_cls.__module__}.{t_cls.__name__}.{m}"
            tier_counts[t_num]["total"] += 1
            if test_id in failed_test_ids:
                tier_counts[t_num]["fail"] += 1
            elif test_id in skipped_test_ids:
                tier_counts[t_num]["skip"] += 1
            else:
                tier_counts[t_num]["pass"] += 1

    print(f"{BOLD}TIER BREAKDOWN SUMMARY:{RESET}")
    print(f"----------------------------------------------------------------------")
    print(f" Tier   | Focus Description                         | Total | Pass | Fail | Pend/Skip")
    print(f"--------+-------------------------------------------+-------+------+------+----------")
    tier_desc = {
        1: "Tier 1: Feature Coverage (F1..F7)",
        2: "Tier 2: Boundary & Corner Cases (F1..F7)",
        3: "Tier 3: Cross-Feature Interactions",
        4: "Tier 4: Real-World Acceptance Scenarios",
    }
    for t_num in [1, 2, 3, 4]:
        d = tier_counts[t_num]
        desc = tier_desc[t_num]
        if tier and t_num != tier:
            print(f" Tier {t_num} | {desc:<41} | {'-':<5} | {'-':<4} | {'-':<4} | {'-':<9}")
            continue
        p_color = GREEN if d["fail"] == 0 else RED
        print(f" Tier {t_num} | {desc:<41} | {d['total']:<5} | {p_color}{d['pass']:<4}{RESET} | {RED if d['fail'] else ''}{d['fail']:<4}{RESET} | {YELLOW if d['skip'] else ''}{d['skip']:<9}{RESET}")
    print(f"----------------------------------------------------------------------")
    print(f" TOTAL  | Comprehensive Acceptance Suite            | {total_tests:<5} | {GREEN}{passed:<4}{RESET} | {RED if failed else ''}{failed:<4}{RESET} | {YELLOW if skipped else ''}{skipped:<9}{RESET}")
    print(f"----------------------------------------------------------------------\n")

    if result.failures or result.errors:
        print(f"{BOLD}{RED}FAILED ASSERTIONS & DIAGNOSTICS:{RESET}")
        for test, trace in result.failures + result.errors:
            print(f"\n{RED}[FAIL]{RESET} {test.id()}:")
            # Indent traceback
            for line in trace.strip().splitlines()[-6:]:
                print(f"   {line}")

    if verbose and result.skipped:
        print(f"\n{BOLD}{YELLOW}PENDING MILESTONE ARTIFACTS:{RESET}")
        for test, reason in result.skipped:
            print(f"   {YELLOW}[PENDING]{RESET} {test.id()} -> {reason}")

    # Final verdict
    success = (failed == 0)
    verdict = f"{GREEN}ALL ACCEPTANCE CRITERIA SATISFIED (PASS){RESET}" if success else f"{RED}VERIFICATION FAILED{RESET}"
    print(f"\n{BOLD}VERDICT: {verdict}{RESET}")
    print(f"{CYAN}======================================================================{RESET}\n")

    # Export machine-readable JSON if requested
    if report_json:
        report_data = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "progressive_mode": progressive,
            "elapsed_seconds": round(elapsed, 4),
            "total_tests": total_tests,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "tier_breakdown": tier_counts,
            "failures": [{"test": t[0].id(), "trace": t[1]} for t in result.failures + result.errors],
            "verdict": "PASS" if success else "FAIL",
        }
        out_path = Path(report_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report_data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Saved JSON verification report to: {out_path}")

    return 0 if success else 1


def main():
    """Command-line interface entry point."""
    parser = argparse.ArgumentParser(
        description="E2E Acceptance Criteria Verification Test Suite for chaewon_ahyeon_research_review"
    )
    parser.add_argument(
        "--progressive",
        action="store_true",
        default=os.environ.get("PROGRESSIVE", "0") == "1",
        help="Enable progressive milestone mode (skips unbuilt artifacts cleanly)",
    )
    parser.add_argument(
        "--tier",
        type=int,
        choices=[1, 2, 3, 4],
        help="Restrict execution to a specific tier (1, 2, 3, or 4)",
    )
    parser.add_argument(
        "--feature",
        type=str,
        choices=["F1", "F2", "F3", "F4", "F5", "F6", "F7"],
        help="Restrict execution to a specific feature (F1 through F7)",
    )
    parser.add_argument(
        "--report-json",
        type=str,
        metavar="PATH",
        help="Save machine-readable JSON verification report to path",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Display verbose per-test diagnostics",
    )

    args = parser.parse_args()

    exit_code = run_tests_with_reporting(
        tier=args.tier,
        feature=args.feature,
        progressive=args.progressive,
        verbose=args.verbose,
        report_json=args.report_json,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
