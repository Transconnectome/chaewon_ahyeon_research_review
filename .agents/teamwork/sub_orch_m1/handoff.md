# Handoff Report — Milestone 1 (Research Synthesis & Evidence Documentation)

## 1. Milestone State
- **Status**: **DONE** (Gate Passed on Iteration 1)
- **Target Deliverable**: `/home/juke/git/chaewon_ahyeon_research_review/docs/01_research_synthesis.md`
- **Scope Covered**: Feature Inventory F1 (Teams Communication & Mentoring Trace Synthesis) & F2 (Experimental Data & Infrastructure Extraction)

## 2. Active Subagents
- **Active Subagents**: None (All 9 spawned subagents have completed and are permanently retired)
- **Spawn History**:
  - `explorer_m1_1` (`f22fdfe0`): Chaewon Research Exploration [COMPLETED]
  - `explorer_m1_2` (`52e18387`): Ahyeon Research Exploration [COMPLETED]
  - `explorer_m1_3` (`8c289595`): Teams Mentoring & Plan Blueprint [COMPLETED]
  - `worker_m1` (`be5f087e`): Authoring `docs/01_research_synthesis.md` [COMPLETED]
  - `reviewer_m1_1` (`f0e02bd2`): Structure & Completeness Review [APPROVE]
  - `reviewer_m1_2` (`210cd977`): Empirical & Quotation Review [APPROVE]
  - `challenger_m1_1` (`7a371bb6`): Empirical Data Code Verification [APPROVE]
  - `challenger_m1_2` (`d0a1e594`): Dialogue & Adversarial Verification [APPROVE]
  - `auditor_m1_1` (`33120d20`): Forensic Integrity Audit [CLEAN]

## 3. Pending Decisions
- None. Milestone 1 is fully completed and ready for Milestone 2 handoff.

## 4. Remaining Work (For Successor / Parent Orchestrator)
- Milestone 2 (`docs/02_deep_research_literature.md`): Deep Research & Literature Benchmarking on 94 foundation model papers and 2-axis scaling laws.
- Milestone 3 (`docs/03_adversarial_review.md`): Scientific Adversarial Review building on the 4 debates and challenger attack dossiers identified in Milestone 1.

## 5. Key Artifacts
- **Primary Deliverable**: `/home/juke/git/chaewon_ahyeon_research_review/docs/01_research_synthesis.md` (669 lines, 63KB, 7,365 words)
- **Scope Specification**: `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m1/SCOPE.md`
- **Gate Status**: `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m1/GATE_STATUS.md`
- **Progress Log**: `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m1/progress.md`
- **Briefing**: `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m1/BRIEFING.md`

---

## 6. Observation (핵심 실측 사실 및 조사 결과)
1. **Teams 커뮤니케이션 및 멘토링 전수 복원 (F1)**:
   - 2026-10-26 (인턴십 출범 헌장: 탑 1% 학생의 최고 난도 목표 수행), 10-27, 10-28 (KISTI 한강 멀티노드 셋업), 11-10 (NeuroAI 워크숍 투고 관련 논쟁) 등 전수 로그와 9개 멘토링 회의록 아카이브 완전 복원.
   - 2026-11-10 지도교수 차지욱 교수님의 비판적 회신("negative result", "준비 부족")과 이아현 선생님의 전격적 반론("how should we scale의 핵심 발견", "시간보다 사람") 원문 전수 인용.
2. **4대 핵심 학술 쟁점 실증 기제 (F1, F2)**:
   - **쟁점 1 (Held-out Loss Paradox)**: 37명 동일 피험자 대상 held-out loss는 +8.5% 악화되나, 신규 피험자 대상 held-out loss는 전체 데이터 모델과 -0.06%로 동일함(`newsubj_summary.json`). 이는 데이터 감축이 환자 고유 잡음 암기량(idiosyncrasy)을 제거하고 순수 뇌신경 표상을 보존함을 증명.
   - **쟁점 2 (Layer Readout Divergence)**: 1/1024는 1층 표상은 보존되나 최상위 12층 표상이 -0.0050으로 붕괴하는 반면, 1/64(81.3시간)는 12개 층 전 층에서 표상이 보존됨(0.0000).
   - **쟁점 3 (Data Sampling Asymmetry)**: 부족한 iEEG를 두피 EEG로 메우는 `EEG_fill`은 `iEEG_re` 대비 -0.0100의 명백한 통계적 손실을 발생시키며, 6개 ablation 모두 회복 실패.
   - **쟁점 4 (Subject Diversity Threshold)**: 피험자를 8명으로 분산하면 37명과 동등 유지(+0.0001)되나, 2명으로 축소하면 -0.0055로 붕괴하여 "시간보다 사람(Subjects over Hours)" 법칙 확립.
3. **인프라 및 정량 데이터 테이블 완비 (F2)**:
   - 표 1(고유 iEEG 스윕), 표 2(데이터 샘플링 4대 조건), 표 3(피험자 수 4분면 스윕), 표 4(층별 및 모델 규모별 읽기) 완비.
   - KISTI 한강 GH200 8노드 Strong scaling 실측($E(8)=0.78, 1180.1\text{ s/s}$), DDP All-reduce dataloader stall 타이머 버그 해결(`commit 1600fc2`), LMDB Worker 24 필요성 규명.

---

## 7. Logic Chain (논리 추론 체계)
1. 사전 탐색(3 Explorers)을 통해 안채원 선생님 실측치, 이아현 선생님 DIVER 포트폴리오, Teams 대화 로그를 완전 분리 수집.
2. 3대 보고서를 종합하여 8개 섹션 청사진을 도출하고, 단일 Worker에게 배타적 쓰기 권한을 부여하여 63KB 규모의 학술 synthesis 문서를 작성.
3. 2명의 리뷰어, 2명의 챌린저, 1명의 포렌식 감사관을 병렬 디스패치하여 4개 차원(완전성, 정량적 일치, Teams DB 일치, 호칭 및 무결성)에서 독립 교차 검증 수행.
4. 모든 검증 결과가 만장일치로 통과(Reviewers APPROVE, Challengers APPROVE, Auditor CLEAN, Test suite 38/38 PASS)하여 Gate Pass 확정.

---

## 8. Caveats (한계 및 후속 마일스톤 연계 주의점)
1. **Frozen Linear Probe 편향**: 1/64의 안전성은 주로 Frozen LP에서 입증되었으므로, 전체 미세조정(Full Fine-tuning) 시 과적합 취약성은 M3에서 적대적으로 검증되어야 함.
2. **도메인 편향**: 인지/운동 과제(Neuroprobe, BYD, Pippi) 중심 검증이며, 뇌전증 발작(MAYO) 등 병리적 과제에 대한 추가 확장이 요구됨.
3. **M3 공격 타겟 dossier 전달**: Reviewer 1/2 및 Challenger 1/2가 도출한 4대 공격 벡터(신규 피험자 노이즈 플로어, 2~8명 구간 해상도, 1/1 Base의 0.46 epoch 계산 부족 교란 요인, 고주파 감마 과제 편향)를 M3에 공식 전달.

---

## 9. Conclusion
Milestone 1의 목표인 `docs/01_research_synthesis.md`는 원천 데이터와의 100% 수치 일치, Teams 대화의 원문 복원, 4대 핵심 학술 논쟁의 실증적 규명, 엄격한 연구자 존칭 준수 하에 완벽하게 완수되었습니다.

---

## 10. Verification Method (독립 검증 방법)
- **테스트 스위트 검증**: `python3 tests/verify_acceptance_criteria.py --progressive` (38/38 PASS)
- **호칭 준수 검증**: `grep -n "안채원" docs/01_research_synthesis.md` (10회, 모두 "선생님"), `grep -n "이아현" docs/01_research_synthesis.md` (14회, 모두 "선생님"), `grep -E "씨|반말" docs/01_research_synthesis.md` (0건)
- **원천 데이터 일치 검증**: `hangang/reports/lead/*.json` 및 `teams.db` 직접 쿼리 일치.
