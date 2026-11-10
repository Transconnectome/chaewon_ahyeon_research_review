# Scope: Milestone 3 — Scientific Adversarial Review

## Mission
안채원 선생님과 이아현 선생님의 연구 결과("A Little iEEG Goes a Long Way", "Subjects over Hours")에 대해 과학적 방법론(가설 타당성, 인과 추론, 대조군 및 실험 설계, 재구성 손실-하류 점수 괴리 역설, 통계적 엄밀성) 관점에서 극한의 비판적 검증과 반론을 수행하는 적대적 리뷰 보고서(`docs/03_adversarial_review.md`)를 작성한다.

## Architecture & Code Layout
- Target Deliverable: `/home/juke/git/chaewon_ahyeon_research_review/docs/03_adversarial_review.md`
- Working Directory: `/home/juke/git/chaewon_ahyeon_research_review`
- State Folder: `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m3`

## Feature Inventory Coverage
- F4: Scientific Adversarial Review

## Inputs & Authoritative Sources
1. Milestone 1 Deliverable:
   - `/home/juke/git/chaewon_ahyeon_research_review/docs/01_research_synthesis.md`
2. Milestone 2 Deliverable:
   - `/home/juke/git/chaewon_ahyeon_research_review/docs/02_deep_research_literature.md`
3. Survey & Milestone Handoffs:
   - `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m1/handoff.md`
   - `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m2/handoff.md`
4. The 5 Methodological Vulnerability Axes:
   - Axis 1: 가설 타당성 (Hypothesis Validity & Falsifiability) — 1/1024 12층 붕괴(-0.0050)와 "시간 불필요" 주장의 내적 모순.
   - Axis 2: 인과 추론 및 교란 요인 (Causal Inference & Confounders) — 피험자 수 vs 전극 커버리지/해부학적 이질성/병원 사이트 효과 교란.
   - Axis 3: 대조군 및 실험 설계 (Experimental Controls & Readout Divergence) — MAE 특이적 현상 가능성, DIVER-1.5 채널 기원 예측 대조군 부재, 3개 인지과제 편향 및 임상 병리 과제 부재.
   - Axis 4: 재구성 손실-하류 점수 괴리 역설 (Reconstruction Loss Paradox) — Held-out loss +8.5% 악화에도 linear probe 유지되는 기전의 착시 가능성 (저주파 스펙트럼 편향).
   - Axis 5: 통계적 엄밀성 및 다중비교 보정 (Statistical Rigor) — Seed n=6 검정력, Neuroprobe 15개 하위과제 다중비교 보정(Bonferroni/FDR), N>=8 임계값의 외삽 한계.
5. Original Request:
   - `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/ORIGINAL_REQUEST.md`

## Milestones (Internal to M3)
1. Explorer -> Worker -> Reviewer -> Challenger -> Auditor cycle.
2. Produce `docs/03_adversarial_review.md`.
3. Verify all Acceptance Criteria for R2 adversarial review are met.

## Honorific Rules
- Students & researchers: ALWAYS "안채원 선생님", "이아현 선생님" + 존댓말 — NEVER "OO 씨" or 반말.
