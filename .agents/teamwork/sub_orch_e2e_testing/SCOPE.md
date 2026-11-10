# Scope: E2E Testing Track Orchestrator

## Mission
Design and implement an opaque-box, requirement-driven E2E verification test suite for the `chaewon_ahyeon_research_review` project. Create `TEST_INFRA.md`, build automated validation scripts (`tests/verify_acceptance_criteria.py`), and publish `TEST_READY.md` upon completion.

## Architecture
- Root Files:
  - `TEST_INFRA.md` (Test philosophy, runner, thresholds, tier definitions)
  - `TEST_READY.md` (Signal that test suite is complete with coverage summary)
- Test Implementation: `tests/verify_acceptance_criteria.py`
- Stress / Adversarial Suite: `tests/test_adversarial_challenge.py`
- Test Runner: `python3 tests/verify_acceptance_criteria.py`
- Working Directory: `/home/juke/git/chaewon_ahyeon_research_review`
- State Folder: `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_e2e_testing`

## Feature Inventory to Cover
| # | Feature | Target Artifact | Requirement | Status |
|---|---------|-----------------|-------------|:------:|
| F1 | Teams Communication & Mentoring Trace Synthesis | `docs/01_research_synthesis.md` | R1: 안채원 선생님·이아현 선생님 주장/피드백/논의 정리 | VERIFIED |
| F2 | Experimental Data & Infrastructure Extraction | `docs/01_research_synthesis.md` | R1: KISTI 실측, DIVER-1/2, 2.88M 샘플, 37 피험자 수치 | VERIFIED |
| F3 | Deep Research & Theoretical Foundation | `docs/02_deep_research_literature.md` | R2: 94편 뇌파 파운데이션 모델, 5개 핵심 선행논문 분석 | VERIFIED |
| F4 | Scientific Adversarial Review | `docs/03_adversarial_review.md` | R2: 5대 과학적 방법론 기반 적대적 취약점/반론 검증 | VERIFIED |
| F5 | Actionable Improvement Items & Prioritized Roadmap | `docs/04_action_items_roadmap.md` | R3: 단기(11/20), 중기, 장기 우선순위 액션 아이템 | VERIFIED |
| F6 | Git Repository Structuring & Transconnectome Push | `.git`, `README.md`, remote | R4: Git 초기화, README 작성, Transconnectome 푸시 | VERIFIED |
| F7 | E2E Acceptance Criteria Verification | `tests/verify_acceptance_criteria.py` | Full Acceptance Criteria coverage | VERIFIED |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|:------:|
| E2E-M1 | Test Infrastructure Design | `TEST_INFRA.md` creation with complete 4-tier methodology | none | DONE |
| E2E-M2 | Test Suite Implementation | `tests/verify_acceptance_criteria.py` with Tiers 1-4 (82 tests + 14 stress tests) | E2E-M1 | DONE |
| E2E-M3 | Verification & Ready Signal | Test execution, reviewer approval, auditor clean, publish `TEST_READY.md` | E2E-M2 | DONE |

## Test Tier Specification (Verified Thresholds)
- **Tier 1: Feature Coverage (35 tests total, 5 per feature across F1–F7)**:
  - F1: 안채원 선생님 & 이아현 선생님 synthesis, mentoring minutes, feedback, dates, claims
  - F2: 37 subjects, 5,203h, 2.88M samples, delta scores, KISTI scaling monotonicity, depth electrodes
  - F3: Foundation model literature benchmarks (Oliveira 2026, Ooi 2025, Narayanswamy 2024, Banville 2025, Truong 2026)
  - F4: 5 methodology axes (hypothesis, causality, control, reconstruction vs probe, statistical rigor)
  - F5: Action items with priority tiers (Immediate/Nov 20, Medium/DIVER-2, Long/clinical), owners, timelines
  - F6: Git status, repository structure, README.md executive summary, Transconnectome remote config
  - F7: Full acceptance criteria checklist compliance
- **Tier 2: Boundary & Corner Cases (35 tests total, 5 per feature across F1–F7)**:
  - F1-B: Strict honorific enforcement ("안채원 선생님", "이아현 선생님" mandatory; "씨", "학생", and 반말 globally banned)
  - F2-B: Numeric consistency and strictly increasing KISTI throughput monotonicity ($T_1 < T_2 < T_4 < T_8$)
  - F3-B: Scholarly citation integrity ([1950..2027], contemporary foundation models required)
  - F4-B: Mandatory 100% contract vulnerability coverage (all 5 categories required)
  - F5-B: Action item executability, topological section header ordering (`^#+\s*.*단기`)
  - F6-B: Git commit message conventions, file size checks, clean directory layout
  - F7-B: Test runner handles partially completed milestones gracefully via progressive mode
- **Tier 3: Cross-Feature Combinations (7 pairwise integration tests)**:
  - F1 ↔ F2: Experimental data matches discussion in Teams mentoring traces
  - F1 ↔ F4: Adversarial review targets specific claims made by 안채원 선생님 & 이아현 선생님
  - F2 ↔ F4: Methodological critique directly challenges experimental setup (2.88M samples, 37 subjects)
  - F3 ↔ F4: Deep research literature directly informs the counter-arguments and benchmarks
  - F4 ↔ F5: Every identified vulnerability has at least one corresponding action item in roadmap
  - F5 ↔ F6: README.md executive summary reflects the prioritized roadmap
  - F1..F6 ↔ F7: End-to-end integration across all artifacts with section-anchor handling
- **Tier 4: Real-World Acceptance Scenarios (5 application-level tests)**:
  - S1: Full Acceptance Criteria satisfaction from `ORIGINAL_REQUEST.md`
  - S2: Stakeholder Readability & Policy Compliance (Prof. Jiook Cha lab standards, honorifics)
  - S3: Publication Readiness (Executive summary, artifact integrity, markdown linting)
  - S4: NeuroAI 11/20 submission readiness criteria verification
  - S5: Transconnectome repository distribution & reproduction check
- **Total Test Count**: 82 unique test methods + 14 empirical adversarial challenge tests = 96 tests.
