# Test Infrastructure Specification: `chaewon_ahyeon_research_review`

- **Project**: `chaewon_ahyeon_research_review`
- **Location**: `/home/juke/git/chaewon_ahyeon_research_review`
- **Document Version**: 1.0.0
- **Status**: Official Test Infrastructure Specification (SSOT)
- **Target Suite**: `tests/verify_acceptance_criteria.py`
- **Mandatory Policy**: Strict honorific enforcement — ALWAYS "안채원 선생님", "이아현 선생님", "차지욱 교수님" (NEVER "OO 씨" or 반말).

---

## 1. Test Philosophy & Principles

The test infrastructure of `chaewon_ahyeon_research_review` establishes a rigorous, **opaque-box, requirement-driven verification harness**. It treats all deliverables (research syntheses, literature benchmarks, adversarial critiques, action roadmaps, executive summaries, git repositories) as verifiable operational artifacts subject to deterministic acceptance assertions.

### 1.1 Core Verification Principles
1. **Opaque-Box Verification**: Tests do not assume or inspect internal implementation mechanisms. Instead, they probe observable contract outputs: filesystem artifacts, semantic structure, quantitative figures, bibliographic citations, and policy compliance.
2. **Deterministic Independence**: Each test case is completely self-contained and isolated. Test results do not rely on execution order or persistent side effects.
3. **Genuine & Non-Facade**: Facade tests that trivially pass without evaluating actual criteria are strictly forbidden. Every test performs authentic checks against explicit requirements defined in `ORIGINAL_REQUEST.md` (R1–R4) and `PROJECT.md` (F1–F7).
4. **Progressive Testability**: To support continuous validation throughout milestone execution (M1 through M5), the harness provides a `--progressive` mode. Missing milestone artifacts are diagnosed cleanly as `PENDING` rather than causing unhandled runtime exceptions.
5. **Strict Governance & Culture**: Honorifics and lab communication standards are enforced as hard test invariants. Addressing 안채원 선생님 or 이아현 선생님 with informal address ("씨" or 반말) causes immediate assertion failure.

---

## 2. Feature Inventory Mapping (F1 through F7)

The test suite maps 1:1 against the seven core features specified in `PROJECT.md` and `SCOPE.md`:

| Feature ID | Feature Name | Target Artifact | Requirement | Scope & Verification Focus |
|---|---|---|---|---|
| **F1** | Teams Communication & Mentoring Trace Synthesis | `docs/01_research_synthesis.md` | R1 | 안채원 선생님 & 이아현 선생님 research questions, Teams dialogue traces, 차지욱 교수님 critical feedback, mentoring timeline |
| **F2** | Experimental Data & Infrastructure Extraction | `docs/01_research_synthesis.md` | R1 | KISTI 한강 GH200 scaling, DDP timer profiling, 2.88M samples, 37 subjects pool, 1/64 & 1/1024 non-inferiority ($\Delta > -0.005$) |
| **F3** | Deep Research & Theoretical Foundation | `docs/02_deep_research_literature.md` | R2 | 94-paper foundation survey, 5 baseline citations (Oliveira, Narayanswamy, Banville, Ooi, Truong), 2-axis scaling equations |
| **F4** | Scientific Adversarial Review | `docs/03_adversarial_review.md` | R2 | 5 methodological vulnerability axes (hypothesis, causality/confounders, controls, reconstruction dissociation, statistical rigor) |
| **F5** | Actionable Improvement Items & Prioritized Roadmap | `docs/04_action_items_roadmap.md` | R3 | 3-tier roadmap (Tier 1 Immediate 11/20 NeuroAI, Tier 2 Medium DIVER-2 Aurora, Tier 3 Long Clinical), owners, timelines, metrics |
| **F6** | Git Repository Structuring & Transconnectome Push | `README.md`, `.git`, remote | R4 | Standard layout, executive summary README, `.gitignore` cleanliness, Transconnectome remote configuration |
| **F7** | E2E Acceptance Criteria Verification | `tests/verify_acceptance_criteria.py` | Checklist | Full coverage of R1–R4 criteria, self-verification, 4-tier reporting, JSON export, $\ge 82$ test methods |

---

## 3. Four-Tier Test Architecture & Coverage Thresholds

The acceptance test harness enforces an 82-test minimum contract across four distinct tiers:

```
Total Test Suite: 82 Test Cases
├── Tier 1: Feature Coverage (35 Tests)
│   ├── F1: 5 Tests (Presence, Proposals, Framing, Feedback, Chronology)
│   ├── F2: 5 Tests (HPC Benchmarks, Architecture, 2.88M Exposure, Subject Thresholds, Duration Margins)
│   ├── F3: 5 Tests (Presence, 5 Key Papers, 2-Axis Equations, Modality Transfer, 94-Paper Corpus)
│   ├── F4: 5 Tests (Presence, 5 Vulnerability Axes, Layer Readout, Dissociation Paradox, Confounders)
│   ├── F5: 5 Tests (Presence, Tier 1 11/20, Tier 2 Medium, Tier 3 Long, Schema Attributes)
│   ├── F6: 5 Tests (Git Init, Commit History, Executive README, .gitignore, Remote Config)
│   └── F7: 5 Tests (Checklist Mapping, Self-Verification, Console Summary, JSON Export, Total Count)
├── Tier 2: Boundary & Corner Cases (35 Tests)
│   ├── F1-B: 5 Tests (Ahn Honorifics, Lee Honorifics, Global Student Audit, Verbatim Quotes, Word Count)
│   ├── F2-B: 5 Tests (Subject Bounds, Delta Signs, Throughput Monotonicity, Arithmetic Math, No Placeholders)
│   ├── F3-B: 5 Tests (Year Validity, Real arXiv IDs, Table Schema, Citation Depth, LaTeX Math Syntax)
│   ├── F4-B: 5 Tests (5 Contract Vulnerabilities, Anti-Vagueness, Counter-Evidence, Falsification, Voice)
│   ├── F5-B: 5 Tests (Code Pointers, Metric Targets, 11/20 Deadline Feasibility, Compute Resources, Ordering)
│   ├── F6-B: 5 Tests (Clean Tree, Metadata Isolation, Conventional Commits, File Size Bounds, Remote URL)
│   └── F7-B: 5 Tests (Progressive Handling, Subsuite Filtering, Boolean Exit Codes, Idempotency, Performance)
├── Tier 3: Cross-Feature Interactions (7 Tests)
│   ├── T3-01: F1 ↔ F2 Data Provenance Consistency
│   ├── T3-02: F1 ↔ F4 Adversarial Targets Mentor/Mentee Claims
│   ├── T3-03: F2 ↔ F4 Empirical Metrics Challenged in Review
│   ├── T3-04: F3 ↔ F4 Literature Informs Adversarial Critique
│   ├── T3-05: F4 ↔ F5 Vulnerabilities Map to Action Items
│   ├── T3-06: F5 ↔ F6 README Mirrors Roadmap Priorities
│   └── T3-07: F1..F6 ↔ F7 End-to-End Referencing & Traceability
└── Tier 4: Real-World Acceptance Scenarios (5 Tests)
    ├── S1: Original Request Full Criteria Satisfaction
    ├── S2: Lab Governance & Policy Compliance
    ├── S3: Publication Readiness Audit
    ├── S4: AAAI 2027 NeuroAI Workshop (11/20) Submission Readiness
    └── S5: Transconnectome Distribution & Reproduction Check
```

### Coverage Threshold Summary Table

| Test Tier | Focus & Scope | Designed Count | Minimum Required |
|---|---|---|---|
| **Tier 1** | Feature existence, completeness, and explicit specification coverage | 35 | 35 |
| **Tier 2** | Boundary conditions, numeric intervals, formatting, honorific policies | 35 | 35 |
| **Tier 3** | Pairwise cross-feature consistency, provenance, and mitigation closure | 7 | 7 |
| **Tier 4** | Real-world application scenarios, lab culture, and submission readiness | 5 | 5 |
| **Total** | **Full E2E Acceptance Verification Suite** | **82** | **82** |

---

## 4. Test Runner Specification & CLI Semantics

The test suite is implemented in Python 3 using `unittest` and standard library modules (`pathlib`, `re`, `subprocess`, `argparse`, `json`, `time`), requiring zero external dependencies. It is runnable both directly and through `pytest`.

### 4.1 Invocation Commands

```bash
# 1. Standard execution (Strict Mode: all 82 tests must pass)
python3 tests/verify_acceptance_criteria.py

# 2. Pytest execution
python3 -m pytest tests/verify_acceptance_criteria.py -v

# 3. Progressive execution (Marks unbuilt milestone artifacts as PENDING)
python3 tests/verify_acceptance_criteria.py --progressive

# 4. Filter by Tier (1, 2, 3, or 4)
python3 tests/verify_acceptance_criteria.py --tier 1

# 5. Filter by Feature (F1 through F7)
python3 tests/verify_acceptance_criteria.py --feature F1

# 6. Generate Machine-Readable JSON Audit Report
python3 tests/verify_acceptance_criteria.py --report-json reports/acceptance_results.json
```

### 4.2 CLI Argument Specification

| Flag | Argument | Description |
|---|---|---|
| `--progressive` | None | Enables progressive milestone testing; pending artifacts are reported without fatal exit 1 |
| `--tier` | `{1,2,3,4}` | Restricts execution to the specified tier |
| `--feature` | `{F1,F2,F3,F4,F5,F6,F7}` | Restricts execution to tests mapped to a specific feature |
| `--verbose`, `-v` | None | Displays individual test method execution details and assertions |
| `--report-json` | `<filepath>` | Exports structured execution results and metrics in JSON format |
| `--help`, `-h` | None | Displays CLI argument documentation |

### 4.3 Exit Code Protocol

| Exit Code | Meaning | Condition |
|---|---|---|
| **0** | **SUCCESS** | All executed tests passed cleanly. In progressive mode, all active tests passed and unbuilt milestones are pending. |
| **1** | **FAILURE** | One or more tests failed an assertion (missing data, broken reference, policy violation). |
| **2** | **SYNTAX / CLI ERROR** | Invalid command-line arguments or environmental misconfiguration. |

---

## 5. Diagnostic Error Format & Remediation

When an assertion fails, the test runner produces a structured diagnostic error block specifying the tier, target artifact, expected value, observed value, and concrete remediation steps:

```
======================================================================
FAIL: test_f1_b01_strict_honorifics_chaewon_ahn (TestTier2BoundaryCases)
----------------------------------------------------------------------
[T2-F1B-01] Honorific Policy Violation in docs/01_research_synthesis.md:
- Target Artifact: docs/01_research_synthesis.md
- Expected: '안채원 선생님' (Strict Lab Honorific)
- Actual: Found banned informal address '[비존칭 호칭 결합]'
- Remediation: Ensure proper '안채원 선생님' address and respectful speech (존댓말).
======================================================================
```

---

## 6. Directory Layout & Metadata Compliance

Per project governance guidelines:
- **Project Root**: Contains `README.md`, `TEST_INFRA.md`, `TEST_READY.md`, `PROJECT.md`, `.gitignore`.
- **`docs/`**: Contains core research deliverables (`01_research_synthesis.md`, `02_deep_research_literature.md`, `03_adversarial_review.md`, `04_action_items_roadmap.md`).
- **`tests/`**: Contains test harness (`verify_acceptance_criteria.py`).
- **`.agents/teamwork/`**: Strictly isolated to agent metadata (plans, progress, dispatches, handoffs). **Zero source code, test scripts, or final data files are permitted in `.agents/teamwork/`**.
