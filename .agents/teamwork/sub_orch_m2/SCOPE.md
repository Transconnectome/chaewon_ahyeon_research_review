# Scope: Milestone 2 — Deep Research & Scholarly Literature Benchmarking

## Mission
최신 학술 문헌(94편 뇌파 파운데이션 모델 및 2축 스케일링 법칙 핵심 문헌들)을 딥리서치하여 안채원 선생님과 이아현 선생님의 연구 결과("A Little iEEG Goes a Long Way", "Subjects over Hours")와 엄밀하게 비교·대조하는 학술 벤치마킹 보고서(`docs/02_deep_research_literature.md`)를 작성한다.

## Architecture & Code Layout
- Target Deliverable: `/home/juke/git/chaewon_ahyeon_research_review/docs/02_deep_research_literature.md`
- Working Directory: `/home/juke/git/chaewon_ahyeon_research_review`
- State Folder: `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m2`
- Status: **DONE (Gate PASS)**

## Feature Inventory Coverage
- F3: Deep Research & Theoretical Foundation [DONE]

## Inputs & Authoritative Sources
1. Milestone 1 Output:
   - `/home/juke/git/chaewon_ahyeon_research_review/docs/01_research_synthesis.md`
2. Core Literature Base (Survey 2 & 3 handoffs):
   - Oliveira et al. (2026, arXiv:2609.35056): Scalp EEG 2-axis scaling ($L = A N_t^{-\alpha} + B N_s^{-\beta} + L_\infty$), $\beta$ instability (0.07~1.99).
   - Narayanswamy et al. (2024, Google LSM, arXiv:2410.13638): Equal total hours yields equal loss.
   - Banville et al. (2025, Meta, arXiv:2501.15322): Subject-specific layers, lack of subject scaling axis.
   - Ooi et al. (2025, Nature 644:731): fMRI phenotype scaling ($r = K_0 \sqrt{1/(1 + K_1/N + K_2/(NT))}$), bottleneck transition from $NT$ to $N$.
   - Truong et al. (2026, arXiv:2610.09287): Scalp EEG 10->1,863 subjects, onset threshold at ~50 subjects.
   - Chai (2026): Entropy proxy ($r=-0.89$ with repetition tolerance).
   - DIVER-1 (arXiv:2512.19097) & DIVER-1.5 (ACPE + channel origin prediction).
   - BrainWave, BrainOmni (multimodal mixing confounders).
   - 94-paper survey in `~/git/ephys-foundation-model-plan/submissions/2026/20261010-yahyunee-diver2-scaling-survey/`.
3. Original Request:
   - `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/ORIGINAL_REQUEST.md`

## Milestones (Internal to M2)
| # | Step | Role / Subagent | Status | Deliverable |
|---|------|-----------------|--------|-------------|
| 1 | Exploration (2-Axis Scaling) | explorer_m2_1 | DONE | explorer_m2_1/handoff.md |
| 2 | Exploration (94-Paper Corpus) | explorer_m2_2 | DONE | explorer_m2_2/handoff.md |
| 3 | Exploration (Information Dynamics) | explorer_m2_3 | DONE | explorer_m2_3/handoff.md |
| 4 | Worker Implementation | worker_m2_1 | DONE | docs/02_deep_research_literature.md (51KB) |
| 5 | Reviewer 1 (Scholarly Completeness) | reviewer_m2_1 | APPROVE | reviewer_m2_1/handoff.md |
| 6 | Reviewer 2 (Mathematical Rigor) | reviewer_m2_2 | APPROVE | reviewer_m2_2/handoff.md |
| 7 | Challenger 1 (Scaling Equations) | challenger_m2_1 | APPROVE | challenger_m2_1/handoff.md |
| 8 | Challenger 2 (Biophysics & Dynamics) | challenger_m2_2 | APPROVE | challenger_m2_2/handoff.md |
| 9 | Forensic Auditor (Anti-Cheating) | auditor_m2_1 | CLEAN | auditor_m2_1/handoff.md |
| 10 | Milestone Gate Evaluation | Sub-Orchestrator | **PASS** | GATE_STATUS.md |

## Honorific Rules
- Students & researchers: ALWAYS "안채원 선생님", "이아현 선생님" + 존댓말 — NEVER "OO 씨" or 반말.
