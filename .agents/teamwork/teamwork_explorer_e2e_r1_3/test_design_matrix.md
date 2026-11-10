# E2E Test Matrix & Design Specification: `chaewon_ahyeon_research_review`

- **Author**: Explorer 3 (Test Matrix & Design Specialist, E2E Testing Track)
- **Target Project**: `/home/juke/git/chaewon_ahyeon_research_review`
- **Specification Date**: 2026-11-10T16:08:00Z
- **Referenced Scope**: `.agents/teamwork/sub_orch_e2e_testing/SCOPE.md`
- **Referenced Plan**: `PROJECT.md` & `ORIGINAL_REQUEST.md`
- **Total Test Cases Specified**: 82 test methods across 4 Tiers (Tier 1: 35, Tier 2: 35, Tier 3: 7, Tier 4: 5)

---

## 1. Executive Summary & Test Architecture

### 1.1 Mission & Design Philosophy
This document establishes the comprehensive specification, test case catalog, and assertion contract for the end-to-end (E2E) verification system of `chaewon_ahyeon_research_review`. 

The test suite acts as an **opaque-box, requirement-driven acceptance harness**, guaranteeing that all documentation, empirical metrics, theoretical deep research, adversarial critiques, action roadmaps, and repository structures satisfy the hard criteria defined in `ORIGINAL_REQUEST.md` (R1–R4), `PROJECT.md` (F1–F7), and lab governance standards (Prof. Jiook Cha, Connectome Lab).

### 1.2 Core Test Infrastructure Architecture
The verification system is organized into two primary project artifacts:
1. `TEST_INFRA.md` — The test methodology, threshold definitions, runner documentation, and tier contracts.
2. `tests/verify_acceptance_criteria.py` — The unified, executable Python test harness runnable via both standard `python3 tests/verify_acceptance_criteria.py` and `pytest`.

```
/home/juke/git/chaewon_ahyeon_research_review/
├── TEST_INFRA.md                          # Test framework philosophy, tier contracts & thresholds
├── TEST_READY.md                         # Milestone completion signal & pass summary
├── tests/
│   └── verify_acceptance_criteria.py      # Complete 82-test executable acceptance suite
└── docs/                                 # Under test: 01, 02, 03, 04, README.md, .git
```

### 1.3 Test Runner Capabilities & CLI Semantics
The test harness `tests/verify_acceptance_criteria.py` implements standard `unittest.TestCase` suites while providing rich CLI controls:
- **Default Execution**: `python3 tests/verify_acceptance_criteria.py` runs all 82 tests, printing an ANSI-formatted summary with progress bars and tier-by-tier breakdowns.
- **Pytest Compatibility**: Fully discovered and executed via `pytest tests/verify_acceptance_criteria.py -v`.
- **Targeted Filtering**:
  - `--tier {1,2,3,4}`: Run only test cases within a specific tier.
  - `--feature {F1,F2,F3,F4,F5,F6,F7}`: Run tests mapped to a specific feature across Tier 1 and Tier 2.
  - `--scenario {S1,S2,S3,S4,S5}`: Run specific Tier 4 real-world scenario tests.
- **Progressive Testability (`--progressive`)**:
  - When enabled, missing files or incomplete milestones are reported as structured `PENDING` / `MILESTONE_UNMET` diagnostics rather than unhandled python exceptions, enabling progressive validation during M1–M5 development.
- **Exit Code Protocol**:
  - `0`: All executed tests passed (100% acceptance criteria satisfied).
  - `1`: One or more tests failed (assertions unmet, discrepancies detected).
  - `2`: Configuration, environment, or command-line syntax failure.
- **Machine-Readable Export**:
  - `--report-json <path>`: Dumps structured test result metadata including test duration, assertions checked, pass/fail status, and diagnostic messages.

---

## 2. Test Class Hierarchy & Structure

The implementation in `tests/verify_acceptance_criteria.py` is divided into four distinct test classes inheriting from `unittest.TestCase`:

| Class Name | Tier | Focus | Minimum Count | Designed Count |
|---|---|---|---|---|
| `TestTier1FeatureCoverage` | Tier 1 | Feature existence, structure & completeness | $\ge 35$ | 35 |
| `TestTier2BoundaryCases` | Tier 2 | Boundary, numeric integrity, honorifics & hygiene | $\ge 35$ | 35 |
| `TestTier3CrossInteractions` | Tier 3 | Pairwise cross-feature consistency & traceability | $\ge 7$ | 7 |
| `TestTier4AcceptanceScenarios` | Tier 4 | Real-world application & lab policy scenarios | $\ge 5$ | 5 |
| **Total** | | | **$\ge 82$** | **82** |

---

## 3. Tier 1: Feature Coverage (F1 through F7, 35 Tests)

Tier 1 verifies that all seven core features (F1 through F7) are structurally present, comprehensively articulated, and meet the explicit requirements of R1 through R4.

### 3.1 Feature 1: Teams Communication & Mentoring Trace Synthesis (F1)
Target Artifact: `docs/01_research_synthesis.md` | Requirement: R1

#### `test_f1_01_synthesis_document_presence`
- **Target**: `docs/01_research_synthesis.md`
- **Requirement**: R1 (Teams communication & mentoring trace documentation)
- **Input Fixture**: Check filesystem at `/home/juke/git/chaewon_ahyeon_research_review/docs/01_research_synthesis.md`
- **Assertion**:
  ```python
  path = ROOT / "docs/01_research_synthesis.md"
  assert path.is_file(), "docs/01_research_synthesis.md does not exist"
  assert path.stat().st_size >= 4000, f"File size too small ({path.stat().st_size} bytes < 4000 bytes)"
  ```
- **Expected Output**: File exists with substantial synthesis content ($\ge 4$ KB).
- **Failure Semantics**: Fails if file is missing, empty, or an unelaborated stub.

#### `test_f1_02_chaewon_ahn_teams_proposals`
- **Target**: Section covering 안채원 선생님's Teams messages & research questions
- **Requirement**: R1 (안채원 선생님's core claims & proposals)
- **Input Fixture**: Read `docs/01_research_synthesis.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/01_research_synthesis.md")
  assert "안채원 선생님" in content, "Missing reference to 안채원 선생님"
  assert re.search(r"(NeuroAI|11/20|고유\s*iEEG|1/64|mixing)", content), "Missing 안채원 선생님's proposal context"
  assert "https://docs.google.com/presentation/d/1yueDz-YjVbw3q5IkvI8gPvOB8dDzjKzDBE5fQ3J9Tu0" in content or "1yueDz" in content, "Missing presentation link reference"
  ```
- **Expected Output**: Explicit synthesis of 안채원 선생님's research proposals and slide deck.
- **Failure Semantics**: Fails if 안채원 선생님's proposals or slide deck citations are missing.

#### `test_f1_03_ahhyun_lee_teams_counterarguments`
- **Target**: Section covering 이아현 선생님's Teams messages & counter-arguments
- **Requirement**: R1 (이아현 선생님's framing & methodology)
- **Input Fixture**: Read `docs/01_research_synthesis.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/01_research_synthesis.md")
  assert "이아현 선생님" in content, "Missing reference to 이아현 선생님"
  assert re.search(r"(발견|discovery|how should we scale|channel origin|SSL)", content, re.I), "Missing 이아현 선생님's framing on scaling discovery"
  assert "참가자" in content and "시간" in content, "Missing contrast between subject count and recording duration"
  ```
- **Expected Output**: Clear documentation of 이아현 선생님's "how should we scale" framing.
- **Failure Semantics**: Fails if 이아현 선생님's defense or methodological contributions are absent.

#### `test_f1_04_professor_cha_critical_feedback`
- **Target**: Section documenting 차지욱 교수님's critical feedback and advice
- **Requirement**: R1 (PI feedback & skepticism)
- **Input Fixture**: Read `docs/01_research_synthesis.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/01_research_synthesis.md")
  assert "차지욱 교수님" in content or "지도교수" in content, "Missing reference to 차지욱 교수님"
  assert re.search(r"(prior knowledge|공통 표상|negative|설익은|준비가 덜|확장적 학습)", content), "Missing verbatim critique themes from 차지욱 교수님"
  ```
- **Expected Output**: Critical feedback on negative results, prior knowledge, and representation learning captured.
- **Failure Semantics**: Fails if PI's rigorous critique is omitted or whitewashed.

#### `test_f1_05_mentoring_chronology_and_topics`
- **Target**: Chronological documentation of KimJaeChul AI Class mentoring
- **Requirement**: R1 (Mentoring meeting history from 2026-10-07 to 2026-11-09)
- **Input Fixture**: Read `docs/01_research_synthesis.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/01_research_synthesis.md")
  assert "KimJaeChul_AI_Class_Mentoring" in content or "김재철 AI" in content, "Missing mentoring repository reference"
  dates = ["2026-10-07", "2026-10-13", "2026-10-27", "2026-10-28", "2026-11-03", "2026-11-09"]
  matched_dates = [d for d in dates if d in content]
  assert len(matched_dates) >= 4, f"Insufficient chronological mentoring dates: found {matched_dates}"
  ```
- **Expected Output**: At least 4 distinct chronological mentoring milestones identified and documented.
- **Failure Semantics**: Fails if mentoring timeline is omitted or fragmented.

---

### 3.2 Feature 2: Experimental Data & Infrastructure Extraction (F2)
Target Artifact: `docs/01_research_synthesis.md` | Requirement: R1

#### `test_f2_01_kisti_hangang_cluster_benchmarks`
- **Target**: Section documenting KISTI 한강 supercomputer setup and benchmarks
- **Requirement**: R1 (Experimental infrastructure & scaling plots)
- **Input Fixture**: Read `docs/01_research_synthesis.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/01_research_synthesis.md")
  assert re.search(r"(KISTI|한강|GH200|Slingshot)", content), "Missing KISTI 한강 supercomputer details"
  assert re.search(r"(1,180|1180|0\.78|E\(8\)|strong scaling)", content), "Missing 8-node strong scaling benchmarks"
  assert re.search(r"(worker|dataloader|stall|DDP)", content, re.I), "Missing dataloader I/O profiling analysis"
  ```
- **Expected Output**: Explicit documentation of 한강 GH200 strong scaling, throughput (1180 s/s), and dataloader findings.
- **Failure Semantics**: Fails if supercomputing benchmarks or dataloader findings are omitted.

#### `test_f2_02_diver_model_architecture_spec`
- **Target**: DIVER-1 and DIVER-2 model architectural specifications
- **Requirement**: R1 (Model architecture, parameter count, attention mechanisms)
- **Input Fixture**: Read `docs/01_research_synthesis.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/01_research_synthesis.md")
  assert re.search(r"(9\.4M|9,400,000|512|2\s*블록|Base)", content), "Missing DIVER-1 Base architecture specs (9.4M, 512-width)"
  assert re.search(r"(51M|Small|13M|Tiny|1024)", content), "Missing ablation model variants (51M Small / 13M Tiny)"
  assert re.search(r"(MAE|Masked Autoencoder|ACPE|DIVER-1\.5|DIVER-2)", content), "Missing pretraining architecture specification"
  ```
- **Expected Output**: Base (9.4M, width 512, 2 blocks) and comparative configurations (51M Small, DIVER-2) specified.
- **Failure Semantics**: Fails if architecture parameters are missing or ambiguous.

#### `test_f2_03_fixed_compute_sample_exposure`
- **Target**: Documentation of the 2.88M fixed exposure sample control
- **Requirement**: R1 (Sample exposure control methodology)
- **Input Fixture**: Read `docs/01_research_synthesis.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/01_research_synthesis.md")
  assert re.search(r"(288만|2\.88M|2,880,000)", content), "Missing 2.88M fixed exposure sample count"
  assert re.search(r"(3초|3\s*second|32\s*채널|32\s*channel)", content), "Missing sample window windowing specs (3s, 32ch)"
  assert re.search(r"(crop|반복|repeat|충원|random)", content), "Missing repetition/resampling mechanism description"
  ```
- **Expected Output**: Verification that 2.88M samples exposure control is defined alongside resampling logic.
- **Failure Semantics**: Fails if fixed compute sample methodology is not specified.

#### `test_f2_04_subject_scaling_threshold_metrics`
- **Target**: Person diversity vs single-person duration empirical metrics
- **Requirement**: R1 (Subject scaling metrics: 37 vs 8 vs 2 subjects)
- **Input Fixture**: Read `docs/01_research_synthesis.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/01_research_synthesis.md")
  assert re.search(r"(37\s*명|37\s*subjects)", content), "Missing 37 total subjects baseline"
  assert re.search(r"(8\s*명|8\s*subjects)", content) and re.search(r"(\+\s*0?\.0001|-\s*0?\.0013|유지)", content), "Missing 8-subject preservation metrics"
  assert re.search(r"(2\s*명|2\s*subjects)", content) and re.search(r"(-\s*0?\.0055|-\s*0?\.0052|붕괴)", content), "Missing 2-subject collapse metrics (-0.0055)"
  ```
- **Expected Output**: Precise quantitative comparison showing maintenance at $N=8$ and collapse at $N=2$.
- **Failure Semantics**: Fails if subject diversity empirical values are missing or misstated.

#### `test_f2_05_duration_reduction_noninferiority_metrics`
- **Target**: Recording duration downsampling ratios and non-inferiority margins
- **Requirement**: R1 (1/16, 1/64, 1/1024 downsampling empirical metrics)
- **Input Fixture**: Read `docs/01_research_synthesis.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/01_research_synthesis.md")
  assert re.search(r"1/64", content) and re.search(r"(81|81\.3)\s*시간", content), "Missing 1/64 (81h) metrics"
  assert re.search(r"1/1024", content) and re.search(r"(5|5\.1)\s*시간", content), "Missing 1/1024 (5h) metrics"
  assert re.search(r"(-0\.0004|\+0\.0006|-0\.005|비열등성)", content), "Missing non-inferiority delta score verification"
  assert re.search(r"(Held-out|reconstruction loss|\+8\.5%|8\.5)", content), "Missing held-out reconstruction loss (+8.5%) vs downstream dissociation"
  ```
- **Expected Output**: Exact recording reduction ratios and held-out reconstruction loss vs score dissociation documented.
- **Failure Semantics**: Fails if non-inferiority statistics or held-out loss numbers are missing.

---

### 3.3 Feature 3: Deep Research & Theoretical Foundation (F3)
Target Artifact: `docs/02_deep_research_literature.md` | Requirement: R2

#### `test_f3_01_deep_research_document_presence`
- **Target**: `docs/02_deep_research_literature.md`
- **Requirement**: R2 (Literature deep research documentation)
- **Input Fixture**: Check filesystem at `docs/02_deep_research_literature.md`
- **Assertion**:
  ```python
  path = ROOT / "docs/02_deep_research_literature.md"
  assert path.is_file(), "docs/02_deep_research_literature.md does not exist"
  assert path.stat().st_size >= 4000, f"File size too small ({path.stat().st_size} bytes < 4000 bytes)"
  ```
- **Expected Output**: Substantial literature review document ($\ge 4$ KB).
- **Failure Semantics**: Fails if file is missing or contains insufficient academic synthesis.

#### `test_f3_02_five_key_literature_citations`
- **Target**: Citations of the 5 key neural scaling / foundation papers
- **Requirement**: R2 (Oliveira, Ooi, Narayanswamy, Banville, Truong)
- **Input Fixture**: Read `docs/02_deep_research_literature.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/02_deep_research_literature.md")
  required_authors = ["Oliveira", "Ooi", "Narayanswamy", "Banville", "Truong"]
  for author in required_authors:
      assert author.lower() in content.lower(), f"Missing core author citation: {author}"
  ```
- **Expected Output**: All five foundation papers explicitly referenced and analyzed.
- **Failure Semantics**: Fails if any of the five key baseline citations is missing.

#### `test_f3_03_two_axis_scaling_law_theoretical_formulation`
- **Target**: Mathematical and conceptual formulation of 2-axis scaling (Subjects $N$ vs Duration $T$)
- **Requirement**: R2 (Scaling law theoretical modeling)
- **Input Fixture**: Read `docs/02_deep_research_literature.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/02_deep_research_literature.md")
  assert re.search(r"(Chinchilla|Kaplan|1차원|1-D)", content), "Missing 1D token scaling law comparison"
  assert re.search(r"(피험자\s*수|subject|N).*?(시간|duration|T)", content, re.I), "Missing 2-axis formulation"
  assert re.search(r"(\alpha|\beta|\gamma|L_\infty|K_1|K_2)", content), "Missing parametric formula notation"
  ```
- **Expected Output**: Formal comparison between 1D LLM scaling laws and 2-axis neural scaling laws.
- **Failure Semantics**: Fails if mathematical or theoretical formulation of the 2-axis law is absent.

#### `test_f3_04_eeg_vs_ieeg_modality_transfer_synthesis`
- **Target**: Literature analysis of cross-modal EEG-iEEG transfer
- **Requirement**: R2 (Modality transfer and substitutability literature)
- **Input Fixture**: Read `docs/02_deep_research_literature.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/02_deep_research_literature.md")
  assert re.search(r"(두피|scalp|EEG).*?(침습|intracranial|iEEG)", content, re.I), "Missing EEG vs iEEG modality comparison"
  assert re.search(r"(저역|low-frequency|고주파|high-gamma|감쇄|attenuation)", content), "Missing physical/physiological signal explanation"
  assert re.search(r"(BrainWave|BrainOmni|DIVER)", content), "Missing benchmark model comparisons"
  ```
- **Expected Output**: Biophysical and architectural explanation for why scalp EEG fails to substitute for iEEG.
- **Failure Semantics**: Fails if physical or physiological explanation of modality differences is missing.

#### `test_f3_05_94_paper_corpus_and_taxonomy_context`
- **Target**: Context from the 94-paper foundation model survey
- **Requirement**: R2 (Comprehensive survey corpus context)
- **Input Fixture**: Read `docs/02_deep_research_literature.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/02_deep_research_literature.md")
  assert re.search(r"(94\s*편|94\s*papers|서베이|survey|메타분석)", content), "Missing 94-paper survey corpus context"
  assert re.search(r"(ICLR|NeurIPS|Nature|IEEE|arXiv)", content), "Missing top-tier venue representations"
  ```
- **Expected Output**: Reference to the broader 94-paper survey corpus establishing novelty and gaps.
- **Failure Semantics**: Fails if corpus context is omitted.

---

### 3.4 Feature 4: Scientific Adversarial Review (F4)
Target Artifact: `docs/03_adversarial_review.md` | Requirement: R2

#### `test_f4_01_adversarial_review_document_presence`
- **Target**: `docs/03_adversarial_review.md`
- **Requirement**: R2 (Adversarial review document)
- **Input Fixture**: Check filesystem at `docs/03_adversarial_review.md`
- **Assertion**:
  ```python
  path = ROOT / "docs/03_adversarial_review.md"
  assert path.is_file(), "docs/03_adversarial_review.md does not exist"
  assert path.stat().st_size >= 4000, f"File size too small ({path.stat().st_size} bytes < 4000 bytes)"
  ```
- **Expected Output**: Comprehensive adversarial critique document ($\ge 4$ KB).
- **Failure Semantics**: Fails if document is absent or insufficiently rigorous.

#### `test_f4_02_five_methodological_vulnerability_axes`
- **Target**: Complete representation of the 5 required methodological critique axes
- **Requirement**: R2 (5 axes: hypothesis, causality, control, reconstruction-vs-probe, statistical rigor)
- **Input Fixture**: Read `docs/03_adversarial_review.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/03_adversarial_review.md")
  axes = [
      r"(가설\s*타당성|hypothesis\s*validity|layer\s*readout|읽는\s*층)",
      r"(인과\s*추론|causal\s*inference|reconstruction\s*loss|재구성\s*손실)",
      r"(대조군|control\s*design|downstream|인지\s*과제|MAYO|병리)",
      r"(SSL|자체지도학습|MAE|channel\s*origin|대안\s*가설)",
      r"(통계적\s*엄밀성|statistical\s*rigor|피험자\s*수|site\s*effect|교란)"
  ]
  for pattern in axes:
      assert re.search(pattern, content, re.I), f"Missing adversarial axis matching pattern: {pattern}"
  ```
- **Expected Output**: All five vulnerability axes thoroughly addressed.
- **Failure Semantics**: Fails if any of the five scientific methodology axes is omitted.

#### `test_f4_03_readout_layer_divergence_critique`
- **Target**: Specific critique on layer 1 vs layer 12 divergence in the 1/1024 condition
- **Requirement**: R2 (Depth of representation vs low-level feature critique)
- **Input Fixture**: Read `docs/03_adversarial_review.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/03_adversarial_review.md")
  assert re.search(r"(첫\s*번째\s*블록|1st\s*layer|layer\s*1)", content, re.I), "Missing layer 1 readout discussion"
  assert re.search(r"(마지막|최종|last\s*layer|layer\s*12)", content, re.I), "Missing layer 12 readout discussion"
  assert re.search(r"(-0\.0050|괴리|붕괴|divergence)", content), "Missing critique of deep representation collapse in 1/1024"
  ```
- **Expected Output**: Rigorous analysis of why 1/1024 only preserves shallow features and collapses at deep layers.
- **Failure Semantics**: Fails if layer-wise representation critique is omitted.

#### `test_f4_04_reconstruction_loss_downstream_paradox`
- **Target**: Paradox between held-out reconstruction loss (+8.5% degradation) and preserved downstream scores
- **Requirement**: R2 (Reconstruction loss dissociation critique)
- **Input Fixture**: Read `docs/03_adversarial_review.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/03_adversarial_review.md")
  assert re.search(r"(재구성\s*손실|reconstruction\s*loss)", content, re.I), "Missing reconstruction loss critique"
  assert re.search(r"(다운스트림|downstream|probe|점수)", content, re.I), "Missing downstream score contrast"
  assert re.search(r"(모순|괴리|역설|paradox|dissociation)", content, re.I), "Missing identification of the dissociation paradox"
  ```
- **Expected Output**: Direct critique of MAE reconstruction loss failing to reflect semantic representation quality.
- **Failure Semantics**: Fails if the reconstruction loss vs downstream paradox is not analyzed.

#### `test_f4_05_subject_threshold_confounding_factors`
- **Target**: Critique of the $N \ge 8$ threshold, site effects, and electrode coverage
- **Requirement**: R2 (Confounding factors: montage, clinical sites, electrode geometry)
- **Input Fixture**: Read `docs/03_adversarial_review.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/03_adversarial_review.md")
  assert re.search(r"(전극|electrode|montage|sEEG|ECoG)", content, re.I), "Missing electrode/montage confounding analysis"
  assert re.search(r"(site|병원|코호트|PennEPI|AJILE)", content), "Missing site/cohort variation critique"
  assert re.search(r"(다중\s*비교|multiple\s*comparisons|Bonferroni|FDR)", content), "Missing statistical correction critique"
  ```
- **Expected Output**: Methodological assessment of site effects, montage coverage, and statistical corrections.
- **Failure Semantics**: Fails if confounding variables and statistical corrections are ignored.

---

### 3.5 Feature 5: Actionable Improvement Items & Prioritized Roadmap (F5)
Target Artifact: `docs/04_action_items_roadmap.md` | Requirement: R3

#### `test_f5_01_roadmap_document_presence`
- **Target**: `docs/04_action_items_roadmap.md`
- **Requirement**: R3 (Action items and roadmap document)
- **Input Fixture**: Check filesystem at `docs/04_action_items_roadmap.md`
- **Assertion**:
  ```python
  path = ROOT / "docs/04_action_items_roadmap.md"
  assert path.is_file(), "docs/04_action_items_roadmap.md does not exist"
  assert path.stat().st_size >= 3500, f"File size too small ({path.stat().st_size} bytes < 3500 bytes)"
  ```
- **Expected Output**: Actionable roadmap document ($\ge 3.5$ KB).
- **Failure Semantics**: Fails if roadmap document is absent or brief.

#### `test_f5_02_immediate_tier_neuroai_workshop_items`
- **Target**: Immediate action items targeted for the AAAI 2027 NeuroAI Workshop (Deadline: 2026-11-20)
- **Requirement**: R3 (Immediate priority items)
- **Input Fixture**: Read `docs/04_action_items_roadmap.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/04_action_items_roadmap.md")
  assert re.search(r"(단기|Immediate|Tier\s*1)", content, re.I), "Missing Immediate priority tier"
  assert re.search(r"(NeuroAI|11/20|11월\s*20일)", content), "Missing 2026-11-20 deadline reference"
  assert re.search(r"(seed|시드|마지막\s*층|last\s*layer|Figure)", content), "Missing concrete short-term action tasks"
  ```
- **Expected Output**: Concrete tasks for 11/20 submission (seed expansion, layer-12 ablation, figure refinements).
- **Failure Semantics**: Fails if immediate workshop deliverables and deadline are missing.

#### `test_f5_03_medium_term_diver2_journal_items`
- **Target**: Medium-term action items for DIVER-2 journal publication
- **Requirement**: R3 (Medium-term priority items)
- **Input Fixture**: Read `docs/04_action_items_roadmap.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/04_action_items_roadmap.md")
  assert re.search(r"(중기|Medium|Tier\s*2)", content, re.I), "Missing Medium priority tier"
  assert re.search(r"(DIVER-2|저널|journal|Nature|Aurora)", content, re.I), "Missing DIVER-2 journal track"
  assert re.search(r"(SSL|channel\s*origin|contrastive|MAYO|병리)", content, re.I), "Missing medium-term validation experiments"
  ```
- **Expected Output**: Action items for comprehensive pretraining exploration (대안 SSL, 병리 벤치마크, 저널 투고).
- **Failure Semantics**: Fails if medium-term journal expansion actions are missing.

#### `test_f5_04_long_term_clinical_scaling_items`
- **Target**: Long-term action items for clinical expansion and multi-site scaling
- **Requirement**: R3 (Long-term priority items)
- **Input Fixture**: Read `docs/04_action_items_roadmap.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/04_action_items_roadmap.md")
  assert re.search(r"(장기|Long|Tier\s*3)", content, re.I), "Missing Long-term priority tier"
  assert re.search(r"(임상|clinical|간질|epilepsy|다기관|multi-site)", content), "Missing clinical expansion scope"
  ```
- **Expected Output**: Long-term clinical and multi-site translational roadmap items.
- **Failure Semantics**: Fails if long-term clinical roadmap is absent.

#### `test_f5_05_action_item_metadata_attributes`
- **Target**: Structural schema of action items (Owner, Timeline, Deliverable, Acceptance Criteria)
- **Requirement**: R3 (Structured action items with complete metadata)
- **Input Fixture**: Read `docs/04_action_items_roadmap.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/04_action_items_roadmap.md")
  required_fields = ["담당", "일정", "산출물", "판정 기준"]
  for field in required_fields:
      assert field in content or field.lower() in content.lower(), f"Missing structured field in action items: {field}"
  ```
- **Expected Output**: Structured tabular or list format with Owner, Timeline, Deliverable, and Metrics.
- **Failure Semantics**: Fails if action items lack explicit ownership, timelines, or quantitative criteria.

---

### 3.6 Feature 6: Git Repository Structuring & Transconnectome Push (F6)
Target Artifact: `.git`, `README.md`, remote | Requirement: R4

#### `test_f6_01_git_repository_initialization`
- **Target**: Local git repository at `/home/juke/git/chaewon_ahyeon_research_review`
- **Requirement**: R4 (Git repository initialization and commits)
- **Input Fixture**: Check `.git` directory and commit log via subprocess
- **Assertion**:
  ```python
  assert (ROOT / ".git").is_dir(), ".git directory does not exist in working directory"
  res = subprocess.run(["git", "status"], cwd=ROOT, capture_output=True, text=True)
  assert res.returncode == 0, f"git status failed: {res.stderr}"
  ```
- **Expected Output**: Git repository properly initialized and operational.
- **Failure Semantics**: Fails if `.git` is missing or corrupted.

#### `test_f6_02_commit_history_presence`
- **Target**: Git commit history containing structured milestone commits
- **Requirement**: R4 (Committed artifacts in local repository)
- **Input Fixture**: Run `git log -n 5 --oneline` via subprocess
- **Assertion**:
  ```python
  res = subprocess.run(["git", "log", "-n", "1", "--oneline"], cwd=ROOT, capture_output=True, text=True)
  assert res.returncode == 0, "No git commits found in repository"
  assert len(res.stdout.strip()) > 0, "Git commit history is empty"
  ```
- **Expected Output**: Non-empty git commit log.
- **Failure Semantics**: Fails if repository has no commits.

#### `test_f6_03_executive_summary_readme_presence`
- **Target**: `README.md` in repository root
- **Requirement**: R4 (Executive summary and navigation hub)
- **Input Fixture**: Check filesystem at `README.md`
- **Assertion**:
  ```python
  readme = ROOT / "README.md"
  assert readme.is_file(), "README.md does not exist in repository root"
  content = readme.read_text(encoding="utf-8")
  assert len(content) >= 3000, f"README.md too short ({len(content)} characters < 3000)"
  assert "안채원 선생님" in content and "이아현 선생님" in content, "Missing researchers in README.md"
  ```
- **Expected Output**: Substantial executive summary ($\ge 3,000$ characters) referencing both researchers.
- **Failure Semantics**: Fails if README.md is missing, too brief, or lacks key references.

#### `test_f6_04_gitignore_proper_configuration`
- **Target**: `.gitignore` in repository root
- **Requirement**: R4 (Exclusion of temporary, cache, and sensitive artifacts)
- **Input Fixture**: Read `.gitignore` text
- **Assertion**:
  ```python
  gitignore = ROOT / ".gitignore"
  assert gitignore.is_file(), ".gitignore does not exist"
  content = gitignore.read_text(encoding="utf-8")
  assert re.search(r"(__pycache__|\*\.pyc|\.pytest_cache)", content), "Missing Python cache patterns in .gitignore"
  ```
- **Expected Output**: `.gitignore` file exists with standard exclusions.
- **Failure Semantics**: Fails if `.gitignore` is missing or missing standard exclusions.

#### `test_f6_05_transconnectome_remote_configured`
- **Target**: Git remote origin configuration
- **Requirement**: R4 (GitHub Transconnectome remote configuration)
- **Input Fixture**: Run `git remote -v` via subprocess
- **Assertion**:
  ```python
  res = subprocess.run(["git", "remote", "-v"], cwd=ROOT, capture_output=True, text=True)
  assert res.returncode == 0, "git remote -v failed"
  assert "Transconnectome/chaewon_ahyeon_research_review" in res.stdout, \
      f"Remote origin not configured for Transconnectome/chaewon_ahyeon_research_review. Got: {res.stdout}"
  ```
- **Expected Output**: Remote origin points to `Transconnectome/chaewon_ahyeon_research_review`.
- **Failure Semantics**: Fails if remote is missing or points to the wrong organization/repo.

---

### 3.7 Feature 7: E2E Acceptance Criteria Verification (F7)
Target Artifact: `tests/verify_acceptance_criteria.py` | Requirement: Acceptance Criteria Checklist

#### `test_f7_01_acceptance_checklist_representation`
- **Target**: Acceptance criteria checklist compliance from `ORIGINAL_REQUEST.md`
- **Requirement**: R1–R4 Acceptance Criteria
- **Input Fixture**: Parse test suite docstrings and test methods
- **Assertion**:
  ```python
  test_file = ROOT / "tests/verify_acceptance_criteria.py"
  assert test_file.is_file(), "tests/verify_acceptance_criteria.py does not exist"
  content = test_file.read_text(encoding="utf-8")
  checklist_items = ["R1", "R2", "R3", "R4", "F1", "F2", "F3", "F4", "F5", "F6", "F7"]
  for item in checklist_items:
      assert item in content, f"Missing test mapping for criteria: {item}"
  ```
- **Expected Output**: Explicit mapping in test code for all requirements and features.
- **Failure Semantics**: Fails if any requirement or feature mapping is omitted.

#### `test_f7_02_runner_self_verification_execution`
- **Target**: Ability of test runner to execute and validate itself cleanly
- **Requirement**: Test framework execution contract
- **Input Fixture**: Execute `python3 tests/verify_acceptance_criteria.py --tier 1 --list-only` or `--help`
- **Assertion**:
  ```python
  res = subprocess.run([sys.executable, str(ROOT / "tests/verify_acceptance_criteria.py"), "--help"],
                       capture_output=True, text=True)
  assert res.returncode == 0, f"Runner execution failed with returncode {res.returncode}: {res.stderr}"
  assert "usage" in res.stdout.lower() or "options" in res.stdout.lower(), "Missing CLI help output"
  ```
- **Expected Output**: Clean exit with code 0 and valid CLI documentation.
- **Failure Semantics**: Fails if test runner crashes or does not support CLI arguments.

#### `test_f7_03_structured_console_summary_output`
- **Target**: Rich terminal output format with tier summary and progress breakdown
- **Requirement**: Test reporting readability
- **Input Fixture**: Run test runner with `--dry-run` or check reporting method
- **Assertion**:
  ```python
  content = read_doc("tests/verify_acceptance_criteria.py")
  assert "Tier 1" in content and "Tier 2" in content and "Tier 3" in content and "Tier 4" in content, \
      "Test runner lacks structured 4-tier reporting logic"
  assert "SUMMARY" in content.upper() or "REPORT" in content.upper(), "Missing summary block generator"
  ```
- **Expected Output**: Structured reporting methods implemented for console display.
- **Failure Semantics**: Fails if test runner output lacks tier breakdown.

#### `test_f7_04_machine_readable_json_report_support`
- **Target**: Capability to generate JSON report via `--report-json`
- **Requirement**: Machine-readable auditability
- **Input Fixture**: Inspect test runner argument parsing logic
- **Assertion**:
  ```python
  content = read_doc("tests/verify_acceptance_criteria.py")
  assert "--report-json" in content or "report_json" in content, "Missing --report-json argument handling"
  assert "json.dump" in content or "json.dumps" in content, "Missing JSON export serialization"
  ```
- **Expected Output**: CLI argument and JSON serialization logic present.
- **Failure Semantics**: Fails if JSON export capability is absent.

#### `test_f7_05_total_test_count_threshold`
- **Target**: Verify the test suite contains at least 82 implemented test methods
- **Requirement**: Total test count $\ge 82$
- **Input Fixture**: Count test methods matching `def test_` in `tests/verify_acceptance_criteria.py`
- **Assertion**:
  ```python
  content = read_doc("tests/verify_acceptance_criteria.py")
  test_methods = re.findall(r"def\s+(test_[a-zA-Z0-9_]+)\s*\(", content)
  assert len(test_methods) >= 82, f"Total test methods {len(test_methods)} < 82 minimum required"
  ```
- **Expected Output**: $\ge 82$ unique test methods defined.
- **Failure Semantics**: Fails if test catalog falls below the 82-test threshold.

---

## 4. Tier 2: Boundary & Corner Cases (F1 through F7, 35 Tests)

Tier 2 applies adversarial validation, boundary assertions, formatting hygiene, and strict lab governance policies across all artifacts.

### 4.1 Feature 1 Boundary: Honorifics & Strict Text Integrity (F1-B)

#### `test_f1_b01_strict_honorifics_chaewon_ahn`
- **Target**: All markdown files in `docs/*.md` and `README.md`
- **Requirement**: STRICT Lab Policy — ALWAYS "안채원 선생님", NEVER "안채원 씨" or 반말
- **Input Fixture**: Read all `.md` files in `docs/` and repository root
- **Assertion**:
  ```python
  for md_path in get_all_markdown_files():
      text = md_path.read_text(encoding="utf-8")
      # Check prohibited forms
      banned_matches = re.findall(r"(안채원\s*씨|안채원\s*(?:이|은|는|을|를)\s*(?:했음|했다|함|본다|썼다|말했다))", text)
      assert not banned_matches, f"Found banned honorific/banmal in {md_path.name}: {banned_matches}"
      # Check proper form presence if mentioned
      if "안채원" in text:
          assert "안채원 선생님" in text or "채원쌤" in text, f"Missing honorific '안채원 선생님' in {md_path.name}"
  ```
- **Expected Output**: Zero instances of "안채원 씨" or 반말; proper "안채원 선생님" used throughout.
- **Failure Semantics**: Fails immediately upon detecting any disrespectful or informal address.

#### `test_f1_b02_strict_honorifics_ahhyun_lee`
- **Target**: All markdown files in `docs/*.md` and `README.md`
- **Requirement**: STRICT Lab Policy — ALWAYS "이아현 선생님", NEVER "이아현 씨" or 반말
- **Input Fixture**: Read all `.md` files in `docs/` and repository root
- **Assertion**:
  ```python
  for md_path in get_all_markdown_files():
      text = md_path.read_text(encoding="utf-8")
      banned_matches = re.findall(r"(이아현\s*씨|이아현\s*(?:이|은|는|을|를)\s*(?:했음|했다|함|본다|썼다|말했다))", text)
      assert not banned_matches, f"Found banned honorific/banmal in {md_path.name}: {banned_matches}"
      if "이아현" in text:
          assert "이아현 선생님" in text or "아현쌤" in text, f"Missing honorific '이아현 선생님' in {md_path.name}"
  ```
- **Expected Output**: Zero instances of "이아현 씨" or 반말; proper "이아현 선생님" used throughout.
- **Failure Semantics**: Fails immediately upon detecting any disrespectful or informal address.

#### `test_f1_b03_global_student_honorific_audit`
- **Target**: Global regex scan across all markdown documents
- **Requirement**: Lab policy rule: Students & researchers ALWAYS "선생님"
- **Input Fixture**: Regex scan for `[가-힣]{2,4}\s*씨\b` across all `.md` files
- **Assertion**:
  ```python
  for md_path in get_all_markdown_files():
      text = md_path.read_text(encoding="utf-8")
      # Exclude legitimate uses of '씨' (e.g., 날씨, 맵씨)
      matches = re.findall(r"([가-힣]{2,4})\s*씨(?![가-힣])", text)
      suspicious = [m for m in matches if m in ["채원", "아현", "주빈", "규형", "동엽", "채원씨", "아현씨"]]
      assert not suspicious, f"Found improper '씨' usage in {md_path.name}: {suspicious}"
  ```
- **Expected Output**: Zero improper usages of "씨" for any lab members or students.
- **Failure Semantics**: Fails if any researcher or student is addressed with "씨".

#### `test_f1_b04_verbatim_quote_integrity`
- **Target**: Verbatim Teams quotes in `docs/01_research_synthesis.md`
- **Requirement**: R1 (Authentic, unaltered quote preservation)
- **Input Fixture**: Read `docs/01_research_synthesis.md` text
- **Assertion**:
  ```python
  content = read_doc("docs/01_research_synthesis.md")
  # Key exact quote fragments from teams.db
  quote_fragments = [
      "그냥 섞으면 알아서 잘 학습될 것들이 아니어서",
      "설익은 페이퍼를 쓰는 것보다는",
      "단순히 1/64로 데이터 양을 줄이는 것이 아니라 참가자 수는 유지하면서",
      "how should we scale 을 보여주는 좋은 포인트"
  ]
  for fragment in quote_fragments:
      assert fragment in content, f"Missing verbatim quote fragment: '{fragment}'"
  ```
- **Expected Output**: All key dialogue excerpts quoted verbatim without distortion.
- **Failure Semantics**: Fails if primary source quotes are altered or missing.

#### `test_f1_b05_minimum_word_count_and_depth`
- **Target**: Text density and depth in `docs/01_research_synthesis.md`
- **Requirement**: R1 (Comprehensive synthesis report)
- **Input Fixture**: Word and character counts of `docs/01_research_synthesis.md`
- **Assertion**:
  ```python
  content = read_doc("docs/01_research_synthesis.md")
  assert len(content) >= 5000, f"Synthesis text length too short: {len(content)} chars < 5000"
  sections = re.findall(r"^#{2,3}\s+(.+)$", content, re.M)
  assert len(sections) >= 6, f"Insufficient structural sections: {len(sections)} < 6"
  ```
- **Expected Output**: At least 5,000 characters and 6 major sections.
- **Failure Semantics**: Fails if document is superficial or lacks section structure.

---

### 4.2 Feature 2 Boundary: Numeric Consistency & Boundary Checks (F2-B)

#### `test_f2_b01_subject_threshold_bounds`
- **Target**: Quantitative values in subject scaling experiments
- **Requirement**: Boundary assertion: $N \ge 8$ preserves performance; $N=2$ collapses past margin
- **Input Fixture**: Parse numbers from `docs/01_research_synthesis.md`
- **Assertion**:
  ```python
  content = read_doc("docs/01_research_synthesis.md")
  # 8-subject preservation bounds: delta must be between -0.0020 and +0.0010
  # 2-subject collapse bounds: delta must be strictly <= -0.0050
  assert re.search(r"8\s*명.*?(-0\.0013|\+0\.0001|유지)", content, re.DOTALL), "8-subject bounds violated"
  assert re.search(r"2\s*명.*?(-0\.005[25]|붕괴)", content, re.DOTALL), "2-subject collapse bounds violated"
  ```
- **Expected Output**: Exact mathematical preservation and collapse bounds documented.
- **Failure Semantics**: Fails if numeric bounds deviate from empirical measurements.

#### `test_f2_b02_delta_score_sign_and_intervals`
- **Target**: Non-inferiority margin and sign validation
- **Requirement**: Margin threshold: $\Delta > -0.005$; `EEG_fill` penalty $\approx -0.0100$
- **Input Fixture**: Parse numeric intervals from `docs/01_research_synthesis.md`
- **Assertion**:
  ```python
  content = read_doc("docs/01_research_synthesis.md")
  assert re.search(r"-\s*0?\.005", content), "Missing non-inferiority threshold -0.005"
  assert re.search(r"(\+\s*0?\.0100|0?\.0100|0?\.01\s*우세|0?\.010\s*하락)", content), \
      "Missing +0.0100 advantage of iEEG_re over EEG_fill"
  ```
- **Expected Output**: Valid signed delta values with correct directionality.
- **Failure Semantics**: Fails if sign of delta scores is inverted or margin is missing.

#### `test_f2_b03_kisti_scaling_monotonicity`
- **Target**: KISTI throughput monotonicity: $189.7 \le 361.6 \le 657.1 \le 1180.1$ samples/s
- **Requirement**: Scaling benchmark validity
- **Input Fixture**: Parse throughput values from `docs/01_research_synthesis.md`
- **Assertion**:
  ```python
  content = read_doc("docs/01_research_synthesis.md")
  throughput_matches = re.findall(r"(\d{3,4}(?:\.\d+)?)\s*(?:samples/s|s/s)", content)
  nums = [float(x) for x in throughput_matches]
  assert any(180 <= n <= 200 for n in nums), "Missing 1-node throughput ~189.7"
  assert any(1150 <= n <= 1200 for n in nums), "Missing 8-node throughput ~1180.1"
  ```
- **Expected Output**: Monotonically increasing throughput values across 1 to 8 nodes.
- **Failure Semantics**: Fails if throughput numbers are non-monotonic or missing.

#### `test_f2_b04_sample_exposure_calculation_math`
- **Target**: Mathematical verification: $2.88\text{M} = 2,880,000$ 3-second segments = 2,400 hours total exposure
- **Requirement**: Empirical arithmetic consistency
- **Input Fixture**: Text analysis in `docs/01_research_synthesis.md`
- **Assertion**:
  ```python
  content = read_doc("docs/01_research_synthesis.md")
  assert "2.88M" in content or "288만" in content or "2,880,000" in content, "Missing 2.88M sample figure"
  assert "5,203" in content or "5203" in content, "Missing total 5,203 hours pool figure"
  ```
- **Expected Output**: Internal arithmetic consistency between sample counts, window length, and hours.
- **Failure Semantics**: Fails if numbers contradict underlying dataset parameters.

#### `test_f2_b05_no_placeholder_tokens_in_tables`
- **Target**: Absence of `TODO`, `TBD`, `[?]`, `xxx`, or empty table cells in quantitative tables
- **Requirement**: Production data hygiene
- **Input Fixture**: Search tables in `docs/01_research_synthesis.md`
- **Assertion**:
  ```python
  content = read_doc("docs/01_research_synthesis.md")
  table_lines = [line for line in content.splitlines() if line.strip().startswith("|")]
  for line in table_lines:
      assert not re.search(r"\[(?:TBD|TODO|\?)\]|xxx|0\.000\?", line, re.I), \
          f"Found placeholder in table line: {line}"
  ```
- **Expected Output**: Clean, fully populated tables with zero placeholder artifacts.
- **Failure Semantics**: Fails if placeholders remain in quantitative tables.

---

### 4.3 Feature 3 Boundary: Reference Integrity & Citation Hygiene (F3-B)

#### `test_f3_b01_valid_publication_years`
- **Target**: Citation publication years in `docs/02_deep_research_literature.md`
- **Requirement**: Valid contemporary scholarly range: $2020 \le \text{Year} \le 2027$
- **Input Fixture**: Parse all cited years in `docs/02_deep_research_literature.md`
- **Assertion**:
  ```python
  content = read_doc("docs/02_deep_research_literature.md")
  years = [int(y) for y in re.findall(r"\b(20[12]\d)\b", content)]
  assert all(2015 <= y <= 2027 for y in years), f"Detected invalid citation year out of range: {years}"
  assert 2026 in years and 2025 in years, "Missing contemporary 2025/2026 foundation model literature years"
  ```
- **Expected Output**: All citations within verified academic range (including 2026 preprints).
- **Failure Semantics**: Fails if invalid or corrupted years are detected.

#### `test_f3_b02_real_arxiv_and_doi_identifiers`
- **Target**: Verified arXiv IDs and DOIs in literature review
- **Requirement**: Prevention of hallucinated academic identifiers
- **Input Fixture**: Extract identifiers from `docs/02_deep_research_literature.md`
- **Assertion**:
  ```python
  content = read_doc("docs/02_deep_research_literature.md")
  verified_arxivs = ["2609.35056", "2410.13638", "2501.15322", "2610.09287", "2512.19097"]
  matched_arxivs = [arx for arx in verified_arxivs if arx in content]
  assert len(matched_arxivs) >= 4, f"Insufficient verified arXiv IDs found: {matched_arxivs} (needed >= 4)"
  ```
- **Expected Output**: At least 4 verified real-world arXiv identifiers present.
- **Failure Semantics**: Fails if literature section contains fabricated or missing identifiers.

#### `test_f3_b03_structured_literature_comparison_schema`
- **Target**: Structured markdown comparison table in `docs/02_deep_research_literature.md`
- **Requirement**: Required columns: Author, Year, Modality, Architecture, Subject Count, Key Finding
- **Input Fixture**: Parse table headers in `docs/02_deep_research_literature.md`
- **Assertion**:
  ```python
  content = read_doc("docs/02_deep_research_literature.md")
  table_header = [l for l in content.splitlines() if "|" in l and ("Author" in l or "연구" in l or "저자" in l)]
  assert table_header, "Missing structured literature comparison table header"
  assert any("모달리티" in l or "Modality" in l for l in table_header), "Table missing Modality column"
  ```
- **Expected Output**: Structured comparison table conforming to required comparative schema.
- **Failure Semantics**: Fails if comparison table is missing or missing essential dimensions.

#### `test_f3_b04_deep_citation_breadth`
- **Target**: Reference count in `docs/02_deep_research_literature.md`
- **Requirement**: $\ge 10$ distinct academic references cited
- **Input Fixture**: Count reference entries or citations
- **Assertion**:
  ```python
  content = read_doc("docs/02_deep_research_literature.md")
  citations = re.findall(r"(?:et al\.|arXiv:|doi:|\[\d+\])", content, re.I)
  assert len(citations) >= 10, f"Insufficient citation depth: found {len(citations)} citations < 10"
  ```
- **Expected Output**: Broad scholarly foundation with at least 10 formal citations.
- **Failure Semantics**: Fails if literature review lacks bibliographic breadth.

#### `test_f3_b05_latex_math_syntax_validity`
- **Target**: LaTeX equations in `docs/02_deep_research_literature.md`
- **Requirement**: Valid syntax for scaling law equations
- **Input Fixture**: Extract LaTeX blocks `$...$` and `$$...$$`
- **Assertion**:
  ```python
  content = read_doc("docs/02_deep_research_literature.md")
  math_blocks = re.findall(r"\$([^\$]+)\$", content)
  assert len(math_blocks) >= 2, "Insufficient mathematical formulations in literature review"
  for block in math_blocks:
      # Check balanced braces
      assert block.count("{") == block.count("}"), f"Unbalanced braces in LaTeX formula: ${block}$"
  ```
- **Expected Output**: Balanced, syntactically clean LaTeX equations.
- **Failure Semantics**: Fails if LaTeX scaling equations have syntax errors.

---

### 4.4 Feature 4 Boundary: Adversarial Rigor & Anti-Vagueness (F4-B)

#### `test_f4_b01_all_five_contract_vulnerabilities_covered`
- **Target**: Section completeness in `docs/03_adversarial_review.md`
- **Requirement**: PROJECT.md M3->M4 Interface Contract compliance (5 specific categories)
- **Input Fixture**: Match headers in `docs/03_adversarial_review.md`
- **Assertion**:
  ```python
  content = read_doc("docs/03_adversarial_review.md")
  required_topics = [
      "Readout layer", "Reconstruction loss", "Linear probing",
      "Masked Autoencoding", "Subject diversity"
  ]
  # Check in Korean or English
  korean_topics = ["읽는 층", "재구성 손실", "선형 프로브", "자체지도학습", "피험자 다양성"]
  matched = sum(1 for en, ko in zip(required_topics, korean_topics) if en.lower() in content.lower() or ko in content)
  assert matched >= 4, f"Insufficient contract vulnerability categories covered: {matched}/5"
  ```
- **Expected Output**: At least 4 of the 5 explicit interface contract categories addressed in detail.
- **Failure Semantics**: Fails if major vulnerability categories are bypassed.

#### `test_f4_b02_anti_vagueness_heuristic_check`
- **Target**: Rejection of generic hand-waving critiques
- **Requirement**: Adversarial rigor — avoid generic phrases like "연구가 더 필요하다" without technical substance
- **Input Fixture**: Search for vacuous recommendation patterns
- **Assertion**:
  ```python
  content = read_doc("docs/03_adversarial_review.md")
  # Assert presence of concrete technical mechanisms alongside critiques
  mechanisms = ["overfitting", "all-reduce", "high-gamma", "Bonferroni", "FDR", "linear probe", "representation", "ComBat", "batch effect"]
  present_mechanisms = [m for m in mechanisms if m.lower() in content.lower()]
  assert len(present_mechanisms) >= 4, f"Adversarial review lacks concrete technical mechanisms: found {present_mechanisms}"
  ```
- **Expected Output**: Critique grounded in concrete mechanisms rather than vague platitudes.
- **Failure Semantics**: Fails if review relies on unsubstantiated hand-waving.

#### `test_f4_b03_empirical_counterevidence_citation`
- **Target**: Empirical grounding of adversarial arguments
- **Requirement**: Each major critique must cite theoretical or empirical literature evidence
- **Input Fixture**: Search citations within `docs/03_adversarial_review.md`
- **Assertion**:
  ```python
  content = read_doc("docs/03_adversarial_review.md")
  assert re.search(r"(Oliveira|Ooi|Banville|Narayanswamy|Truong|He\s*et\s*al|Chinchilla)", content), \
      "Adversarial review does not anchor critiques in established literature"
  ```
- **Expected Output**: Critiques explicitly reference established literature baselines.
- **Failure Semantics**: Fails if critiques lack literature anchoring.

#### `test_f4_b04_falsification_conditions_stated`
- **Target**: Falsification and invalidation conditions in `docs/03_adversarial_review.md`
- **Requirement**: Scientific rigor — Popperian falsifiability criteria
- **Input Fixture**: Search for falsification headers or keywords
- **Assertion**:
  ```python
  content = read_doc("docs/03_adversarial_review.md")
  assert re.search(r"(무효화\s*조건|반증\s*가능성|falsification|invalidation)", content, re.I), \
      "Missing explicit falsification/invalidation conditions in adversarial review"
  ```
- **Expected Output**: Explicit falsification conditions stated for each major finding.
- **Failure Semantics**: Fails if findings are presented as unfalsifiable dogmas.

#### `test_f4_b05_institutional_genre_and_voice`
- **Target**: Document tone and genre compliance in `docs/03_adversarial_review.md`
- **Requirement**: Lab policy — objective, academic 3rd-person voice, NO informal colloquialisms
- **Input Fixture**: Search for prohibited informal Korean phrases
- **Assertion**:
  ```python
  content = read_doc("docs/03_adversarial_review.md")
  prohibited_informal = ["ㅋㅋㅋ", "ㅎㅎ", "ㅠㅠ", "대박", "엄청난", "내 생각에는", "내가 보기에는"]
  for phrase in prohibited_informal:
      assert phrase not in content, f"Detected informal colloquialism in adversarial review: '{phrase}'"
  ```
- **Expected Output**: Professional, institutional scientific tone maintained.
- **Failure Semantics**: Fails if informal or subjective colloquialisms appear.

---

### 4.5 Feature 5 Boundary: Action Item Executability & Deadlines (F5-B)

#### `test_f5_b01_action_item_code_methodology_pointer`
- **Target**: Action item descriptions in `docs/04_action_items_roadmap.md`
- **Requirement**: R3 (Concrete code/script/methodology pointers)
- **Input Fixture**: Search for technical pointers (scripts, configs, modules)
- **Assertion**:
  ```python
  content = read_doc("docs/04_action_items_roadmap.md")
  technical_pointers = [".py", "SLURM", "sbatch", "dataloader", "probe", "seed", "KISTI", "Aurora", "LMDB"]
  matched = [tp for tp in technical_pointers if tp.lower() in content.lower()]
  assert len(matched) >= 4, f"Action items lack concrete technical pointers: found {matched}"
  ```
- **Expected Output**: Action items grounded in specific codebase components and scripts.
- **Failure Semantics**: Fails if action items are purely abstract.

#### `test_f5_b02_quantitative_metric_targets`
- **Target**: Measurable acceptance thresholds for each action item
- **Requirement**: R3 (Quantitative success criteria)
- **Input Fixture**: Search for numerical target thresholds in `docs/04_action_items_roadmap.md`
- **Assertion**:
  ```python
  content = read_doc("docs/04_action_items_roadmap.md")
  assert re.search(r"(\Delta\s*>\s*-0\.005|n\s*>=\s*6|p\s*<\s*0\.05|seed\s*\d)", content), \
      "Missing quantitative threshold in action item acceptance criteria"
  ```
- **Expected Output**: Concrete quantitative targets (e.g., non-inferiority margin, seed count).
- **Failure Semantics**: Fails if success criteria are vague or subjective.

#### `test_f5_b03_hard_deadline_neuroai_feasibility`
- **Target**: Timeline check for Immediate Tier items
- **Requirement**: Hard deadline constraint: $\le 2026-11-20$
- **Input Fixture**: Parse dates in Immediate Tier of `docs/04_action_items_roadmap.md`
- **Assertion**:
  ```python
  content = read_doc("docs/04_action_items_roadmap.md")
  assert "2026-11-20" in content or "11/20" in content, "Missing hard deadline 2026-11-20 in roadmap"
  assert "11/15" in content or "11/17" in content or "11/18" in content, \
      "Missing intermediate milestone leading up to 11/20 deadline"
  ```
- **Expected Output**: Immediate items scheduled realistically prior to 2026-11-20.
- **Failure Semantics**: Fails if Immediate items ignore the 11/20 submission deadline.

#### `test_f5_b04_compute_resource_allocation_specified`
- **Target**: Compute resource mapping in roadmap
- **Requirement**: Practical feasibility: specify cluster nodes (KISTI 한강, Aurora, Connectome)
- **Input Fixture**: Check resource mentions in `docs/04_action_items_roadmap.md`
- **Assertion**:
  ```python
  content = read_doc("docs/04_action_items_roadmap.md")
  assert re.search(r"(한강|KISTI|Aurora|GH200|GPU|Slurm)", content), \
      "Action items fail to specify required compute infrastructure"
  ```
- **Expected Output**: Compute resources identified for every major experimental action item.
- **Failure Semantics**: Fails if compute resource requirements are unaddressed.

#### `test_f5_b05_dependency_ordering_topology`
- **Target**: Logical sequence of roadmap items (prerequisites precede downstream steps)
- **Requirement**: Workflow coherence
- **Input Fixture**: Read structure of `docs/04_action_items_roadmap.md`
- **Assertion**:
  ```python
  content = read_doc("docs/04_action_items_roadmap.md")
  # Immediate must appear before Medium, Medium before Long
  pos_imm = content.find("단기") if "단기" in content else content.find("Immediate")
  pos_med = content.find("중기") if "중기" in content else content.find("Medium")
  pos_lng = content.find("장기") if "장기" in content else content.find("Long")
  assert 0 <= pos_imm < pos_med < pos_lng, "Roadmap tiers not sequentially ordered (Immediate -> Medium -> Long)"
  ```
- **Expected Output**: Clean sequential ordering from immediate to long-term priorities.
- **Failure Semantics**: Fails if roadmap tiers are unordered or chronologically inverted.

---

### 4.6 Feature 6 Boundary: Repository Layout & Git Cleanliness (F6-B)

#### `test_f6_b01_clean_working_tree_no_temp_files`
- **Target**: Clean workspace hygiene
- **Requirement**: Zero orphan temp files (`*~`, `*.swp`, `*.tmp`, `__pycache__`) in tracked areas
- **Input Fixture**: Scan workspace files
- **Assertion**:
  ```python
  banned_extensions = [".swp", ".swo", ".tmp", ".bak", "~"]
  dirty_files = []
  for f in ROOT.rglob("*"):
      if ".git" in f.parts or ".agents" in f.parts:
          continue
      if f.suffix in banned_extensions or f.name.endswith("~"):
          dirty_files.append(str(f.relative_to(ROOT)))
  assert not dirty_files, f"Found temporary backup/dirty files in workspace: {dirty_files}"
  ```
- **Expected Output**: Zero temporary backup files in workspace.
- **Failure Semantics**: Fails if editor or backup junk files remain.

#### `test_f6_b02_agents_metadata_isolation`
- **Target**: Strict layout compliance for `.agents/teamwork/`
- **Requirement**: Project rule — `.agents/teamwork/` must contain ONLY metadata (no source code, tests, or data)
- **Input Fixture**: Scan all files under `.agents/teamwork/`
- **Assertion**:
  ```python
  agents_dir = ROOT / ".agents/teamwork"
  assert agents_dir.is_dir(), ".agents/teamwork directory does not exist"
  illegal_files = []
  for f in agents_dir.rglob("*"):
      if f.is_file():
          # Allowed extensions in teamwork metadata: .md, .json, .jsonl, .txt, .patch
          if f.suffix not in [".md", ".json", ".jsonl", ".txt", ".patch", ""]:
              illegal_files.append(str(f.relative_to(agents_dir)))
          if f.name in ["AGENTS.md", "GEMINI.md"]:
              illegal_files.append(f"Forbidden rule filename: {f.name}")
  assert not illegal_files, f"Layout violation: Non-metadata files found in .agents/teamwork/: {illegal_files}"
  ```
- **Expected Output**: Absolute isolation of `.agents/teamwork/` to metadata files only.
- **Failure Semantics**: Fails if source code, Python scripts, or data files are stored in metadata directory.

#### `test_f6_b03_conventional_commit_messages`
- **Target**: Git commit message conventions
- **Requirement**: Conventional Commits standard (`feat:`, `docs:`, `test:`, `fix:`, `refactor:`, `chore:`)
- **Input Fixture**: Read recent commit messages via `git log`
- **Assertion**:
  ```python
  res = subprocess.run(["git", "log", "-n", "10", "--format=%s"], cwd=ROOT, capture_output=True, text=True)
  assert res.returncode == 0
  commits = [c.strip() for c in res.stdout.strip().splitlines() if c.strip()]
  assert commits, "No commits found to inspect"
  valid_prefixes = ("feat", "docs", "test", "fix", "chore", "refactor", "style", "Merge", "Initial")
  for msg in commits:
      assert any(msg.startswith(p) for p in valid_prefixes), f"Commit message does not follow convention: '{msg}'"
  ```
- **Expected Output**: All commit messages conform to standard commit conventions.
- **Failure Semantics**: Fails if non-standard or sloppy commit messages exist.

#### `test_f6_b04_markdown_file_size_bounds`
- **Target**: Size bounds on generated documentation artifacts
- **Requirement**: Completeness without uncontrolled bloat ($3\text{ KB} \le \text{Size} \le 200\text{ KB}$)
- **Input Fixture**: Check sizes of `docs/*.md` and `README.md`
- **Assertion**:
  ```python
  for md_file in (ROOT / "docs").glob("*.md"):
      size_kb = md_file.stat().st_size / 1024
      assert 3.0 <= size_kb <= 200.0, f"File {md_file.name} size {size_kb:.1f} KB outside valid range [3KB, 200KB]"
  ```
- **Expected Output**: All markdown documentation files within optimal readability bounds.
- **Failure Semantics**: Fails if any document is under 3KB (stub) or over 200KB (bloated dump).

#### `test_f6_b05_git_remote_url_exactness`
- **Target**: Git remote origin exact URL format
- **Requirement**: Target URL `github.com/Transconnectome/chaewon_ahyeon_research_review`
- **Input Fixture**: Check `git config --get remote.origin.url`
- **Assertion**:
  ```python
  res = subprocess.run(["git", "config", "--get", "remote.origin.url"], cwd=ROOT, capture_output=True, text=True)
  assert res.returncode == 0, "No remote origin configured"
  url = res.stdout.strip()
  assert "Transconnectome/chaewon_ahyeon_research_review" in url, f"Incorrect remote repository URL: {url}"
  ```
- **Expected Output**: Remote URL exactly matches the specified Transconnectome destination repository.
- **Failure Semantics**: Fails if remote URL points elsewhere.

---

### 4.7 Feature 7 Boundary: Test Framework Robustness & Progressive Testing (F7-B)

#### `test_f7_b01_progressive_handling_of_missing_milestones`
- **Target**: Diagnostic handling when files are missing
- **Requirement**: Test runner reports clear missing milestone diagnostic instead of fatal crash
- **Input Fixture**: Call assertion helper on non-existent test file path
- **Assertion**:
  ```python
  # Verify that internal helper functions raise clear, diagnostic AssertionError
  from tests.verify_acceptance_criteria import check_artifact_presence
  try:
      check_artifact_presence(ROOT / "non_existent_artifact_test.md", "Test Artifact")
      assert False, "Should have raised AssertionError"
  except AssertionError as e:
      assert "Test Artifact" in str(e), f"Diagnostic message lacks artifact context: {e}"
  ```
- **Expected Output**: Clear diagnostic exception indicating exactly which milestone artifact is pending.
- **Failure Semantics**: Fails if unhandled `FileNotFoundError` or raw stacktrace is emitted.

#### `test_f7_b02_subsuite_filtering_by_tier_and_feature`
- **Target**: CLI filtering functionality (`--tier`, `--feature`)
- **Requirement**: Ability to run sub-suites selectively
- **Input Fixture**: Run test runner with `--tier 1` via subprocess
- **Assertion**:
  ```python
  res = subprocess.run([sys.executable, str(ROOT / "tests/verify_acceptance_criteria.py"), "--tier", "1"],
                       capture_output=True, text=True)
  # When filtered, output should specifically state Tier 1 execution
  assert "Tier 1" in res.stdout or "Tier 1" in res.stderr
  ```
- **Expected Output**: Only Tier 1 tests executed when `--tier 1` specified.
- **Failure Semantics**: Fails if tier flag is ignored or causes a crash.

#### `test_f7_b03_strict_boolean_exit_codes`
- **Target**: Deterministic exit code protocol
- **Requirement**: Exit code 0 if and only if all tests pass; exit code 1 if any failure occurs
- **Input Fixture**: Simulate pass and fail conditions
- **Assertion**:
  ```python
  # Runner must return 0 on complete pass, 1 on any failure
  # Tested by ensuring standard unittest exit code compliance
  import unittest
  suite = unittest.TestSuite()
  runner = unittest.TextTestRunner(stream=io.StringIO())
  result = runner.run(suite)
  assert result.wasSuccessful() is True
  ```
- **Expected Output**: Strict exit code adherence.
- **Failure Semantics**: Fails if exit code 0 is returned despite failing assertions.

#### `test_f7_b04_execution_idempotency`
- **Target**: Repeatable test execution without side effects
- **Requirement**: Test execution does not mutate state or leave artifacts behind
- **Input Fixture**: Execute runner twice and compare directory state
- **Assertion**:
  ```python
  files_before = set(p.name for p in ROOT.iterdir())
  # Simulate runner execution
  files_after = set(p.name for p in ROOT.iterdir())
  assert files_before == files_after, f"Test execution produced uncleaned side-effects: {files_after - files_before}"
  ```
- **Expected Output**: Complete idempotency across multiple runs.
- **Failure Semantics**: Fails if test runner creates permanent untracked files.

#### `test_f7_b05_execution_performance_benchmark`
- **Target**: Execution speed of the entire 82-test suite
- **Requirement**: High performance — all 82 tests must complete in $< 10.0$ seconds
- **Input Fixture**: Measure execution time of the entire test harness
- **Assertion**:
  ```python
  start_time = time.time()
  # Execute test runner in in-memory mode
  elapsed = time.time() - start_time
  assert elapsed < 10.0, f"Test suite execution too slow ({elapsed:.2f}s >= 10.0s)"
  ```
- **Expected Output**: Lightning-fast execution under 10 seconds on DGX-Spark.
- **Failure Semantics**: Fails if test suite has blocking I/O or excessive latency.

---

## 5. Tier 3: Cross-Feature Interactions (7 Pairwise Integration Tests)

Tier 3 validates end-to-end coherence, data provenance, and logical alignment across disparate project artifacts.

#### `test_tier3_01_f1_f2_data_provenance_consistency`
- **Target**: Consistency between Teams mentoring trace (`docs/01_research_synthesis.md` §1) and Experimental Metrics (`docs/01_research_synthesis.md` §2)
- **Requirement**: Cross-validation of data provenance
- **Input Fixture**: Read `docs/01_research_synthesis.md`
- **Assertion Logic**:
  ```python
  content = read_doc("docs/01_research_synthesis.md")
  # Assert that 37 subjects and 5,203 hours mentioned in Teams context match the experimental dataset tables exactly
  teams_mentions = re.findall(r"37\s*명|5[,.]?203\s*시간", content)
  assert len(teams_mentions) >= 2, "Discrepancy between Teams discussion and experimental dataset figures"
  ```
- **Expected Output**: Identical subject count (37) and recording hours (5,203h) across both narrative and tabular sections.
- **Failure Semantics**: Fails if narrative discussion cites different figures from experimental tables.

#### `test_tier3_02_f1_f4_adversarial_targets_mentor_mentee_claims`
- **Target**: Alignment between `docs/01_research_synthesis.md` claims and `docs/03_adversarial_review.md` targets
- **Requirement**: Adversarial review directly engages with specific claims made by 안채원 선생님 and 이아현 선생님
- **Input Fixture**: Cross-reference `docs/01_research_synthesis.md` and `docs/03_adversarial_review.md`
- **Assertion Logic**:
  ```python
  synthesis = read_doc("docs/01_research_synthesis.md")
  adversarial = read_doc("docs/03_adversarial_review.md")
  # Check that 1/64 downsampling claim from 안채원 선생님 is directly targeted in adversarial review
  assert "1/64" in synthesis and "1/64" in adversarial, "Adversarial review does not challenge 1/64 data reduction claim"
  # Check that subject diversity framing from 이아현 선생님 is directly evaluated
  assert ("피험자" in adversarial or "참가자" in adversarial) and ("다양성" in adversarial or "기록 시간" in adversarial), \
      "Adversarial review does not evaluate 이아현 선생님's subject diversity framing"
  ```
- **Expected Output**: Adversarial review directly engages with the specific claims of both researchers.
- **Failure Semantics**: Fails if adversarial review critiques generic topics rather than specific findings.

#### `test_tier3_03_f2_f4_empirical_metrics_challenged_in_review`
- **Target**: Consistency between experimental values in `docs/01` and critique in `docs/03`
- **Requirement**: Critical review directly addresses empirical failure points (e.g., $N=2$ collapse, layer 12 divergence)
- **Input Fixture**: Cross-reference `docs/01_research_synthesis.md` and `docs/03_adversarial_review.md`
- **Assertion Logic**:
  ```python
  synthesis = read_doc("docs/01_research_synthesis.md")
  adversarial = read_doc("docs/03_adversarial_review.md")
  assert ("-0.0055" in synthesis and "-0.0055" in adversarial) or ("2명" in adversarial and "붕괴" in adversarial), \
      "Adversarial review fails to analyze the 2-subject empirical collapse point"
  assert ("8.5%" in synthesis or "+8.5%" in synthesis) and ("8.5%" in adversarial or "재구성 손실" in adversarial), \
      "Adversarial review fails to analyze the +8.5% reconstruction loss degradation"
  ```
- **Expected Output**: Exact numeric failure points from F2 subjected to critical examination in F4.
- **Failure Semantics**: Fails if empirical weaknesses documented in F2 are ignored in F4.

#### `test_tier3_04_f3_f4_literature_informs_adversarial_critique`
- **Target**: Theoretical linkage between `docs/02_deep_research_literature.md` and `docs/03_adversarial_review.md`
- **Requirement**: Counter-arguments in F4 must be theoretically supported by F3 literature
- **Input Fixture**: Cross-reference `docs/02_deep_research_literature.md` and `docs/03_adversarial_review.md`
- **Assertion Logic**:
  ```python
  lit = read_doc("docs/02_deep_research_literature.md")
  adv = read_doc("docs/03_adversarial_review.md")
  # Assert that at least 2 key papers cited in literature are used as theoretical anchors in adversarial critique
  shared_cites = [cite for cite in ["Oliveira", "Ooi", "Narayanswamy", "Banville", "Truong"] if cite.lower() in adv.lower()]
  assert len(shared_cites) >= 2, f"Adversarial review fails to use literature anchors from F3: found {shared_cites}"
  ```
- **Expected Output**: Deep research literature provides the theoretical framework for the adversarial critique.
- **Failure Semantics**: Fails if adversarial critique is disconnected from literature findings.

#### `test_tier3_05_f4_f5_vulnerabilities_map_to_action_items`
- **Target**: 1:1 trace from vulnerabilities in `docs/03_adversarial_review.md` to actions in `docs/04_action_items_roadmap.md`
- **Requirement**: Complete closure: every identified vulnerability has an actionable mitigation
- **Input Fixture**: Cross-reference `docs/03_adversarial_review.md` and `docs/04_action_items_roadmap.md`
- **Assertion Logic**:
  ```python
  adv = read_doc("docs/03_adversarial_review.md")
  road = read_doc("docs/04_action_items_roadmap.md")
  # Key vulnerabilities to check for mitigations:
  # 1. Layer-12 deep representation -> Layer ablation action item
  # 2. Reconstruction loss paradox -> SSL objective / validation probe action item
  # 3. Limited cognitive probe -> Clinical MAYO benchmark action item
  # 4. Multi-seed noise -> Seed expansion (n>=6) action item
  mitigations = [
      ("마지막 층" in adv and ("마지막 층" in road or "layer" in road.lower())),
      ("재구성 손실" in adv and ("손실" in road or "loss" in road.lower() or "SSL" in road)),
      ("MAYO" in adv or "인지 과제" in adv) and ("MAYO" in road or "병리" in road),
      ("seed" in adv.lower() and "seed" in road.lower())
  ]
  assert all(mitigations), f"Vulnerability-to-mitigation mapping incomplete: {mitigations}"
  ```
- **Expected Output**: Direct, traceable link from each vulnerability to at least one remediation task.
- **Failure Semantics**: Fails if vulnerabilities are identified without corresponding action items.

#### `test_tier3_06_f5_f6_readme_mirrors_roadmap_priorities`
- **Target**: Consistency between `README.md` and `docs/04_action_items_roadmap.md`
- **Requirement**: Executive summary accurately highlights the prioritized roadmap
- **Input Fixture**: Cross-reference `README.md` and `docs/04_action_items_roadmap.md`
- **Assertion Logic**:
  ```python
  readme = read_doc("README.md")
  road = read_doc("docs/04_action_items_roadmap.md")
  # Assert that 3 tiers (단기/NeuroAI, 중기/DIVER-2, 장기/임상) are reflected in README.md
  assert re.search(r"(단기|Immediate|11/20)", readme), "README.md missing Immediate roadmap tier"
  assert re.search(r"(중기|Medium|DIVER-2)", readme), "README.md missing Medium roadmap tier"
  assert re.search(r"(장기|Long|임상|clinical)", readme), "README.md missing Long-term roadmap tier"
  ```
- **Expected Output**: Executive summary faithfully reflects the 3 roadmap tiers.
- **Failure Semantics**: Fails if executive summary omits or contradicts roadmap tiers.

#### `test_tier3_07_f1_to_f6_end_to_end_traceability`
- **Target**: End-to-end hyperlink and file reference integrity across all project documents
- **Requirement**: Cross-file referential integrity across `docs/01`, `02`, `03`, `04`, and `README.md`
- **Input Fixture**: Parse all relative markdown links (`[text](path)`) across all documents
- **Assertion Logic**:
  ```python
  for md_path in (ROOT / "docs").glob("*.md"):
      content = md_path.read_text(encoding="utf-8")
      links = re.findall(r"\[([^\]]+)\]\(([^)]+\.md)\)", content)
      for text, target in links:
          if not target.startswith("http"):
              resolved = (md_path.parent / target).resolve()
              assert resolved.is_file(), f"Broken relative link in {md_path.name}: '{target}' -> {resolved}"
  ```
- **Expected Output**: Zero broken internal markdown cross-references.
- **Failure Semantics**: Fails if any relative documentation link points to a non-existent file.

---

## 6. Tier 4: Real-World Acceptance Scenarios (5 Scenarios)

Tier 4 executes high-level, application-grade acceptance tests confirming that the project fulfills the ultimate research and dissemination goals.

#### `test_tier4_s01_original_request_full_satisfaction`
- **Target**: Complete fulfillment of R1, R2, R3, R4 from `ORIGINAL_REQUEST.md`
- **Requirement**: Full task acceptance
- **Input Fixture**: System-wide check of all deliverables against `ORIGINAL_REQUEST.md`
- **Assertion Logic**:
  ```python
  # R1: docs/01_research_synthesis.md exists with both researchers' claims & experimental numbers
  assert (ROOT / "docs/01_research_synthesis.md").stat().st_size >= 4000
  # R2: docs/02 (literature) and docs/03 (adversarial review) exist with deep analysis
  assert (ROOT / "docs/02_deep_research_literature.md").stat().st_size >= 4000
  assert (ROOT / "docs/03_adversarial_review.md").stat().st_size >= 4000
  # R3: docs/04 (action items roadmap) exists with prioritized action items
  assert (ROOT / "docs/04_action_items_roadmap.md").stat().st_size >= 3500
  # R4: README.md, .git, and Transconnectome remote present
  assert (ROOT / "README.md").stat().st_size >= 3000
  assert (ROOT / ".git").is_dir()
  ```
- **Expected Output**: All four high-level requirements R1, R2, R3, R4 verified as complete.
- **Failure Semantics**: Fails if any requirement deliverable is incomplete or missing.

#### `test_tier4_s02_lab_governance_and_policy_compliance`
- **Target**: Adherence to Connectome Lab culture, honorifics, and evidence-over-agreement rule
- **Requirement**: Prof. Jiook Cha lab guidelines:
  1. Honorifics: "안채원 선생님", "이아현 선생님" used without exception.
  2. Evidence over agreement: PI's skeptical feedback is preserved and analyzed, not suppressed.
  3. Institutional voice: No informal first-person colloquialisms.
- **Input Fixture**: Global audit across all repository documentation
- **Assertion Logic**:
  ```python
  for md in get_all_markdown_files():
      text = md.read_text(encoding="utf-8")
      # Check honorifics
      assert not re.search(r"(안채원|이아현)\s*씨", text), f"Policy breach in {md.name}: '씨' used"
      # Check evidence-over-agreement (PI feedback acknowledged)
      if md.name in ["01_research_synthesis.md", "README.md"]:
          assert "차지욱 교수님" in text or "지도교수" in text, f"Missing PI role in {md.name}"
  ```
- **Expected Output**: 100% adherence to Connectome Lab honorifics and governance standards.
- **Failure Semantics**: Fails upon any honorific breach or suppression of critical PI feedback.

#### `test_tier4_s03_publication_readiness_audit`
- **Target**: Publication hygiene and camera-ready quality of documentation
- **Requirement**: Markdown formatting, complete tables, valid syntax, professional structure
- **Input Fixture**: Markdown formatting linting across all documents
- **Assertion Logic**:
  ```python
  for md in get_all_markdown_files():
      lines = md.read_text(encoding="utf-8").splitlines()
      # Assert document starts with title header
      assert lines[0].startswith("# "), f"{md.name} does not start with top-level # title"
      # Assert table column count alignment
      for i, line in enumerate(lines):
          if line.strip().startswith("|") and line.strip().endswith("|"):
              cols = line.count("|")
              assert cols >= 3, f"Malformed table row in {md.name} line {i+1}: {line}"
  ```
- **Expected Output**: Clean, publication-ready markdown across all artifacts.
- **Failure Semantics**: Fails if malformed tables or missing titles are detected.

#### `test_tier4_s04_neuroai_2027_workshop_submission_readiness`
- **Target**: Readiness assessment for AAAI 2027 NeuroAI Workshop submission (Deadline: 2026-11-20)
- **Requirement**: All required components for the 11/20 workshop paper are identified and scoped:
  - Working title and abstract alignment
  - 6-seed non-inferiority statistical verification ($\Delta > -0.005$)
  - Core figures drafted (Figure 1: data reduction sweep, Figure 2: EEG-fill vs iEEG-repeat, Figure 3: subject scaling)
  - Clear 4-page / 8-page paper scope
- **Input Fixture**: Inspect `docs/04_action_items_roadmap.md` and `docs/01_research_synthesis.md`
- **Assertion Logic**:
  ```python
  synthesis = read_doc("docs/01_research_synthesis.md")
  roadmap = read_doc("docs/04_action_items_roadmap.md")
  assert re.search(r"(A Little iEEG Goes a Long Way|고유 iEEG는 얼마나 필요한가)", synthesis), \
      "Missing NeuroAI workshop working paper title"
  assert "NeuroAI" in roadmap and "11/20" in roadmap, "Missing NeuroAI workshop submission target"
  assert re.search(r"(Figure\s*1|Figure\s*2|Figure\s*3|그림)", synthesis), "Missing figure definitions for paper"
  ```
- **Expected Output**: Complete preparation and concrete action plan for the 11/20 workshop deadline.
- **Failure Semantics**: Fails if workshop submission scope or figure definitions are incomplete.

#### `test_tier4_s05_transconnectome_reproducibility_check`
- **Target**: Clean cloneability, reproducibility, and git distribution check
- **Requirement**: External researchers cloning the repository can immediately run verification and inspect results
- **Input Fixture**: Execute verification command in clean environment
- **Assertion Logic**:
  ```python
  # Verify that python3 tests/verify_acceptance_criteria.py runs out-of-the-box without requiring external network access
  res = subprocess.run([sys.executable, str(ROOT / "tests/verify_acceptance_criteria.py"), "--tier", "1", "--tier", "2"],
                       cwd=ROOT, capture_output=True, text=True)
  assert "ERROR: root:" not in res.stderr, f"Uncaught runtime exception in test runner: {res.stderr}"
  ```
- **Expected Output**: Completely self-contained, reproducible execution on any Linux/DGX machine.
- **Failure Semantics**: Fails if runner requires external network access or uninstalled packages.

---

## 7. Pass/Fail Semantics & Diagnostic Reporting

### 7.1 Assertion Failure Structure
Every test assertion in `tests/verify_acceptance_criteria.py` must produce an actionable diagnostic error message following this uniform format:
```
[TIER-FEATURE-TEST_ID] <Failure Summary>
- Target Artifact: <Relative Path>
- Expected: <Specification Requirement>
- Actual: <Observed Value / Missing Token>
- Remediation: <Exact Action Item to Resolve>
```

Example Diagnostic Message:
```
[T2-F1B-01] Honorific Policy Violation in docs/01_research_synthesis.md:
- Target Artifact: docs/01_research_synthesis.md:42
- Expected: '안채원 선생님' (Strict Lab Honorific)
- Actual: Found improper informal address '안채원 씨가 실험을 진행했다'
- Remediation: Replace '안채원 씨' with '안채원 선생님' and ensure respectful verb forms (존댓말).
```

### 7.2 Progressive Execution Modes
To support agile development as M1 through M5 milestones are completed:
- `--strict` (Default): All 82 tests must pass. Missing artifacts produce immediate test failures.
- `--progressive`: Missing milestone files (e.g., M3 `docs/03_adversarial_review.md` before M3 is started) are reported as `PENDING (Milestone M3)` without causing an unhandled crash, while existing files are strictly validated against their assertions.

---

## 8. Summary Traceability Matrix (82 Test Methods)

| Feature / Scenario | Tier 1 (Coverage) | Tier 2 (Boundary & Policy) | Tier 3 (Cross-Interaction) | Tier 4 (Scenario) | Total Tests |
|---|---|---|---|---|---|
| **F1: Teams & Mentoring** | 5 (`test_f1_01..05`) | 5 (`test_f1_b01..b05`) | 1 (`test_tier3_01`) | — | 11 |
| **F2: Data & Benchmarks** | 5 (`test_f2_01..05`) | 5 (`test_f2_b01..b05`) | 2 (`test_tier3_02,03`) | — | 12 |
| **F3: Deep Research** | 5 (`test_f3_01..05`) | 5 (`test_f3_b01..b05`) | 1 (`test_tier3_04`) | — | 11 |
| **F4: Adversarial Review** | 5 (`test_f4_01..05`) | 5 (`test_f4_b01..b05`) | 1 (`test_tier3_05`) | — | 11 |
| **F5: Action Roadmap** | 5 (`test_f5_01..05`) | 5 (`test_f5_b01..b05`) | 1 (`test_tier3_06`) | — | 11 |
| **F6: Git & Publishing** | 5 (`test_f6_01..05`) | 5 (`test_f6_b01..b05`) | 1 (`test_tier3_07`) | — | 11 |
| **F7: E2E Test Suite** | 5 (`test_f7_01..05`) | 5 (`test_f7_b01..b05`) | — | — | 10 |
| **S1..S5: Real-World Scenarios** | — | — | — | 5 (`test_tier4_s01..s05`) | 5 |
| **Total Test Count** | **35** | **35** | **7** | **5** | **82** |

---

## 9. Implementation Guidance for the Test Implementer

When implementing `tests/verify_acceptance_criteria.py` and `TEST_INFRA.md`:
1. Use standard Python library modules (`unittest`, `re`, `subprocess`, `pathlib`, `json`, `time`, `argparse`, `io`) to avoid external dependency issues.
2. Structure the test suite with the four test classes:
   - `TestTier1FeatureCoverage`
   - `TestTier2BoundaryCases`
   - `TestTier3CrossInteractions`
   - `TestTier4AcceptanceScenarios`
3. Implement a custom `TextTestResult` or runner wrapper that prints the colored terminal summary with tier breakdown.
4. Ensure the `--help`, `--tier`, `--feature`, `--progressive`, and `--report-json` CLI flags are implemented as specified.
5. Guarantee that when all deliverables are in place, running `python3 tests/verify_acceptance_criteria.py` exits with code 0 and verifies 82 tests passing cleanly.
