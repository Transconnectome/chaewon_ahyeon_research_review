# Comprehensive Specification Mining Report: E2E Testing Track

- **Project**: `chaewon_ahyeon_research_review`
- **Track**: E2E Testing Track (Iteration 1)
- **Author**: Explorer 1 (Specification Miner)
- **Date**: 2026-11-10T16:15:00Z
- **State Folder**: `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_spec_miner_e2e_r1_1`
- **Mandatory Constraint**: Strict honorific enforcement across all documentation — ALWAYS "안채원 선생님", "이아현 선생님", "차지욱 교수님" (NEVER "OO 씨" or 반말).

---

## 1. Executive Summary & Authoritative Sources

This specification mining report defines the full behavioral requirements, invariants, mathematical and statistical formulas, acceptance criteria, domain metrics, and edge cases for the `chaewon_ahyeon_research_review` project. It provides the authoritative foundation for the test design matrix, test runner (`tests/verify_acceptance_criteria.py`), and test infrastructure (`TEST_INFRA.md`).

### Authoritative Specification Sources Probed:
1. `ORIGINAL_REQUEST.md`: Approved User Request & Acceptance Criteria (SSOT).
2. `PROJECT.md`: Project Architecture, Feature Inventory (F1–F7), Milestone Dependencies, and Code Layout.
3. `SCOPE.md` (`sub_orch_e2e_testing/SCOPE.md`): 4-Tier Test Hierarchy & Minimum Thresholds (>=82 test cases).
4. `~/.agents/registry/chavis_teams/teams.db`: Raw Microsoft Teams chat messages between 차지욱 교수님, 이아현 선생님, and 안채원 선생님.
5. `Transconnectome/KimJaeChul_AI_Class_Mentoring`: Official mentoring minutes and logs (`students/2026-2_ChaewonAhn/`).
6. `Transconnectome/DIVER-2` (`pretrain/hangang-fake-scaling` & `docs/scaling-plan`): Supercomputing benchmarks, DDP profiling corrections, and scaling plans.
7. `Transconnectome/chaewon-intern-2026fall`: `hangang/reports/paper_skeleton.md`, `scaling_literature/SUBJECT_AXIS_REPORT.md`, `log.md`.
8. Shared Agent Context (`~/.agents/context/core.md`): Honorific rules, Trinity provider contracts, and institutional communication standards.

---

## 2. Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| F1.1 | F1 Synthesis | Teams Communication & Archive Mining | 안채원 선생님과 이아현 선생님의 Teams 1:1 대화 및 채널 논의, 멘토링 회의록 체계적 수집 및 요약 | `teams.db`, `KimJaeChul_AI_Class_Mentoring` | `docs/01_research_synthesis.md` (§1) | 파일 누락 시 경고, 비어있는 섹션 방지 | `ORIGINAL_REQUEST.md`, `teams.db` |
| F1.2 | F1 Synthesis | Dialectical Debate & Feedback Synthesis | 차지욱 교수님의 비판적 회신("준비 부족 음성 결과")과 이아현 선생님의 적극적 옹호 및 재해석("How to scale 발견")의 변증법적 기록 | Teams 메시지 원문 (`1794295206799` 등) | `docs/01_research_synthesis.md` (§1.3) | 축약/왜곡 금지, 원문 인용 및 맥락 보존 | `teams.db`, Survey 1 Handoff |
| F1.3 | F1 Synthesis | Strict Honorific Enforcement | 문서 및 코드 내 안채원 선생님, 이아현 선생님에 대한 존칭 준수 ("OO 씨", 반말 절대 금지) | 텍스트 전체 | 무결한 존칭 ("안채원 선생님", "이아현 선생님") | "씨" 또는 반말 발견 시 테스트 즉시 실패 | Global Rules, `ORIGINAL_REQUEST.md` |
| F2.1 | F2 Empirical | KISTI 한강 슈퍼컴퓨터 Scaling 실측 | 한강 6호기 GH200 1~8노드 Strong Scaling 효율 ($E(8)=0.78$) 및 처리량 (1,180.1 samples/s) 실측 정리 | Slurm 로그 (`job 1154165`), `HANGANG_2026-10-28.md` | `docs/01_research_synthesis.md` (§2.1) | Aurora PV Tile 대비 비교 수치 누락 시 오류 | `DIVER-2`, Survey 2 Handoff |
| F2.2 | F2 Empirical | DDP Profiling Timer 결함 교정 | PyTorch DDP all-reduce 동기화로 인한 dataloader stall 오표기 규명 및 타임스탬프 차분 기반 프로파일링 정립 | `DIVER_STEP_TIMERS`, `job 1154230` | `docs/01_research_synthesis.md` (§2.2) | I/O 대기율 누락 시 오류 | `DIVER-2`, Survey 2 Handoff |
| F2.3 | F2 Empirical | iEEG Subsampling & Data Saturation | 37명/5,203h iEEG 데이터에서 2.88M step 고정 하 1/64(81h) 및 1/1024(5h) 비열등성 ($\Delta > -0.005$) 실측 수치화 | 6-seed 짝 비교, `paper_skeleton.md` | `docs/01_research_synthesis.md` (§2.3) | 신뢰구간 및 df 미명시 시 오류 | `chaewon-intern-2026fall` |
| F2.4 | F2 Empirical | Multimodal Non-Substitutability | 부족분을 EEG로 메우는 `EEG_fill`의 성능 손실($-0.0100$) vs `iEEG_re` 반복의 성능 보존($+0.0100$) 실측 | 6-seed 짝 비교, Base vs Fill vs Re | `docs/01_research_synthesis.md` (§2.4) | 음양 부호 오류 시 테스트 실패 | `chaewon-intern-2026fall` |
| F2.5 | F2 Empirical | Subject Diversity vs Duration Threshold | 동일 81h/5h 조건에서 8명 분산(성능 유지, $\Delta=+.0001$) vs 2명 집중(성능 붕괴, $\Delta=-.0055$) 실측 | 6-seed 비교, `subjfix46_summary.json` | `docs/01_research_synthesis.md` (§2.5) | 2명 조건 붕괴 수치 누락 시 오류 | `chaewon-intern-2026fall` |
| F2.6 | F2 Empirical | Layer-wise Readout Divergence | 1/64는 1층 및 12층 모두 유지되나, 1/1024는 1층 유지($+.0006$) 및 12층 붕괴($-.0050$)되는 심층 표현 결함 실측 | `bigscar_rdall.py`, `d2rdall_summary.json` | `docs/01_research_synthesis.md` (§2.6) | 층별 상호작용 누락 시 불완전 | `chaewon-intern-2026fall` |
| F2.7 | F2 Empirical | Reconstruction Loss Dissociation Paradox | 1/1024에서 held-out reconstruction loss가 $+8.5\%$ 악화됨에도 downstream linear probe 점수가 유지되는 괴리 실측 | `curve6_gap_summary.json`, `job 1247125` | `docs/01_research_synthesis.md` (§2.7) | 새 피험자 loss ($-0.1\%$) 미기재 시 오류 | `chaewon-intern-2026fall` |
| F3.1 | F3 Literature | 94-Paper Foundation Model Meta-Survey | 뇌파 파운데이션 모델 94편 전수 조사 및 파라메트릭 스케일링 법칙 적합 부재 현황 규명 | `ephys-foundation-model-plan` | `docs/02_deep_research_literature.md` (§1) | 문헌 메타데이터 부재 시 오류 | `DIVER-2`, Survey 3 Handoff |
| F3.2 | F3 Literature | 5 Key Baseline Papers Benchmarking | Oliveira(2026), Narayanswamy(2024), Banville(2025), Ooi(2025), Truong(2026) 핵심 비교 분석 | arXiv / Nature 논문 원문 | `docs/02_deep_research_literature.md` (§2) | 저자/연도/한계점 누락 시 오류 | `SUBJECT_AXIS_REPORT.md` |
| F3.3 | F3 Literature | 2-Axis Neural Scaling Law Formalization | Oliveira형 분리식 ($L=A H^{-\alpha} + B S^{-\beta} + L_\infty$) vs Ooi형 딥러닝 확장식 ($L=E + K_1 S^{-\beta} + K_2 (S \cdot H)^{-\gamma}$) 모델링 | 수식 정의, 가설 $H_0: K_1=0$ | `docs/02_deep_research_literature.md` (§3) | 수식 표기 오류 시 테스트 실패 | `SUBJECT_AXIS_REPORT.md` |
| F3.4 | F3 Literature | Registry v8 Controlled Experiment Triad | C1 PennEPI(총량 고정 배분), C2 6개 데이터셋(병원 다양성), C3 RAM(1인당 시간 고정 피험자 스윕) 3대 대조군 설계 | Registry v8 TSV 메타데이터 | `docs/02_deep_research_literature.md` (§4) | 코호트 인원/시간 오류 시 오류 | `SUBJECT_AXIS_REPORT.md` |
| F4.1 | F4 Adversarial | Adversarial Review: Hypothesis Validity | "사전 지식 없는 무작위 믹싱의 실패" 비판에 대한 방어 논리 및 Scaling 축으로서의 가치 검증 | 차지욱 교수님 피드백, DIVER-1.5 | `docs/03_adversarial_review.md` (§1) | 단순 반론 나열 시 불인정 | `PROJECT.md`, Survey 1 Handoff |
| F4.2 | F4 Adversarial | Adversarial Review: Causal Inference & Confounding | sEEG depth vs ECoG grid 전극 비율(6.9~26.3%), 병원/사이트 배치 효과, SWEC 대역폭 교란 요인 인과성 검증 | 전극 믹스 감사 (`job 1243386`) | `docs/03_adversarial_review.md` (§2) | 전극 교란 반증 수치 누락 시 오류 | `chaewon-intern-2026fall` |
| F4.3 | F4 Adversarial | Adversarial Review: Control Group Rigor | Untrained(.6039), Hand-crafted feature(.5954), EEG-only(.6212), Base(.6363) 간 엄밀한 대조군 검증 | 통계표 (`Table 2`, `paper_skeleton.md`) | `docs/03_adversarial_review.md` (§3) | 베이스라인 점수 불일치 시 오류 | `chaewon-intern-2026fall` |
| F4.4 | F4 Adversarial | Adversarial Review: Dissociation Paradox Critique | MAE 재구성 손실(+8.5%)과 선형 프로브 점수 유지 간의 괴리가 단순 저주파 특징 과적합인지에 대한 비판적 규명 | Held-out vs New subject loss | `docs/03_adversarial_review.md` (§4) | 외우기(memorization) 수치 누락 시 오류 | `chaewon-intern-2026fall` |
| F4.5 | F4 Adversarial | Adversarial Review: Statistical Rigor | Paired seed(n=6), 95% t-CI, 비열등성 마진($\Delta > -0.005$), 다중 비교 보정(FWER/FDR) 엄밀성 검증 | 통계 요약 JSON | `docs/03_adversarial_review.md` (§5) | 신뢰구간 하한 계산 오류 시 오류 | `chaewon-intern-2026fall` |
| F5.1 | F5 Roadmap | Tier 1 Immediate Roadmap (Nov 20, 2026) | AAAI 2027 NeuroAI 워크숍 마감(11/20) 대비 4쪽 논문 완료, seed 6 보강, 마지막 층 한계 명시, 전극 교란 반증 | 마감일자, 우선 과제 목록 | `docs/04_action_items_roadmap.md` (§1) | 모호한 "연구 필요" 서술 시 오류 | `PROJECT.md`, `paper_skeleton.md` |
| F5.2 | F5 Roadmap | Tier 2 Medium-Term Roadmap (DIVER-2) | Aurora 슈퍼컴퓨터(25,000h, 12월 만료) C1~C3 본실험, 204M 대형 모델 검증, Ooi형 외삽 검증 | Aurora 일정, C1~C3 매니페스트 | `docs/04_action_items_roadmap.md` (§2) | 구체적 실행자/기한 누락 시 오류 | `PROJECT.md`, `DIVER-2` |
| F5.3 | F5 Roadmap | Tier 3 Long-Term Roadmap (Clinical Pathology) | MAYO 발작 감지 벤치마크 착수, Full Fine-tuning 과적합 방지 정규화, 임상 모니터링 실증 확장 | MAYO 데이터셋, 임상 파이프라인 | `docs/04_action_items_roadmap.md` (§3) | 마일스톤 연계 누락 시 오류 | `PROJECT.md` |
| F6.1 | F6 Structuring | Repository Structure & Hygiene | 작업 디렉토리 `~/git/chaewon_ahyeon_research_review` git 초기화 및 표준 디렉토리 구조 확립 | Git repo, `.gitignore` | `.git`, `docs/`, `tests/` | 고아 파일 또는 잘못된 위치 저장 시 오류 | `PROJECT.md` § Code Layout |
| F6.2 | F6 Structuring | Unified Executive Summary (`README.md`) | R1~R4 및 F1~F7을 포괄하는 국문/영문 종합 요약 보고서 작성 | `docs/01`~`04` 산출물 | `README.md` | 핵심 수치 또는 기여 누락 시 오류 | `PROJECT.md`, `ORIGINAL_REQUEST.md` |
| F6.3 | F6 Structuring | Transconnectome Remote Publication | GitHub `Transconnectome/chaewon_ahyeon_research_review` 원격 저장소 생성, 커밋 및 푸시 | `gh` CLI, `snuconnectome` 인증 | GitHub Remote Repo | 푸시 실패 또는 권한 오류 시 오류 | `ORIGINAL_REQUEST.md` R4 |
| F7.1 | F7 Verification | E2E Acceptance Criteria Verification Suite | 전체 요구사항 및 인수 조건을 검증하는 독립 실행형 파이썬 테스트 스위트 | `verify_acceptance_criteria.py` | Exit Code 0 / 1, 테스트 리포트 | 테스트 실패 또는 문법 에러 시 Exit 1 | `PROJECT.md`, `SCOPE.md` |
| F7.2 | F7 Verification | Test Infrastructure Specification | 테스트 철학, 4-tier 분류 체계, 합격 기준, 실행 지침 문서화 | `SCOPE.md` | `TEST_INFRA.md` | 최소 테스트 수(82개) 미달 시 오류 | `SCOPE.md` |
| F7.3 | F7 Verification | Test Readiness Signal | 테스트 인프라 완성, 전 테스트 통과 검증 및 준비 완료 선언 | 테스트 실행 결과 | `TEST_READY.md` | 실패한 테스트 존재 시 생성 불가 | `SCOPE.md` |

---

## 3. Edge Cases

| # | Feature | Input / Condition | Observed / Required Behavior |
|---|---------|-------------------|-----------------------------|
| E1 | F1.3 Honorifics | 텍스트 내 이름 뒤에 존칭 없이 접미사 '씨'를 결합하거나, 비존댓말("했다", "한다" 등의 학생 평가체) 등장 | 검증 스위트 즉각 FAILED 처리. 오직 "안채원 선생님", "이아현 선생님" 및 "OO 선생님" 존칭만 허용 |
| E2 | F2.3 Subsampling | 1/1024 조건에서 Base 대비 점수 변화가 양수($+.0006$)로 나오는 역전 현상 | 사전학습 이득(+0.0336) 범위 내의 무작위 변동으로 해석하며, "점수가 더 좋아졌다"가 아니라 "비열등(하한 > -0.005)하게 유지된다"로 기술 |
| E3 | F2.4 Modality Mix | `EEG_fill`과 `EEG_add`의 결과 혼동 (부족분 대체 vs 기존 유지 후 추가) | `EEG_fill`은 $-0.0100$ 명백한 손실, `EEG_add`는 $-0.0010$ 비열등(공짜 추가이나 무이득)으로 엄밀히 구분하여 기술 |
| E4 | F2.5 Person Diversity | 2명 피험자 조건에서 성능 하락($-0.0055$)의 원인이 전극 종류(심부 전극 부족)라는 가설 | 2명 조건의 모든 seed가 심부 depth 전극(6.9~26.3%)을 포함하고 있으며 전극 비율과 성능 손실 간 상관이 없음을 반증 데이터로 제시 |
| E5 | F2.6 Readout Layer | 1/1024 모델 평가 시 1번째 블록(Layer 1)만 평가하는 경우 | 1층에서는 $+.0006$으로 비열등하나, 12층(Layer 12)에서는 $-.0050$으로 붕괴함을 반드시 병기하여 저수준 시계열 특징 보존 vs 심층 의미 표상 붕괴를 분리 |
| E6 | F2.7 Dissociation | Held-out reconstruction loss가 $+8.5\%$ 악화되었는데 하류 성능은 유지되는 현상 | 같은 피험자의 held-out에서는 loss가 $+8.5\%$ 증가하지만, 완전 신규 피험자(new subjects)에서는 loss 차이가 $-0.1\%$로 나타남을 명시하여 환자별 스타일 외우기(memorization)로 규명 |
| E7 | F3.2 Literature | Truong et al.(2026)의 피험자 수 scaling 해석 시 50명 미만 구간 포함 | ~50명 미만에서는 곡선이 평평(onset)하므로, 50명 미만에서만 적합하여 "피험자 효과 없음"으로 결론짓는 것은 잘못된 피팅 조건임을 명시 |
| E8 | F3.3 Scaling Laws | Oliveira형 vs Ooi형 피험자 스케일링 법칙 적합 시 $L_\infty=0$ 경계해 발생 | $L_\infty=0$ 경계에 붙은 해는 지수 $\beta$를 왜곡(0.07~1.99로 28배 편차)하므로, 단일 지수 대신 95% 신뢰구간 및 외삽 검증 오차로 비교 |
| E9 | F4.2 Confounding | Neuroprobe 벤치마크 내 피험자(BTB)가 사전학습 데이터와 중복될 위험 | BTB(5명, 7.9GB)는 사전학습 데이터셋에서 완전히 배제되었으며, Sub10은 BTB가 아니라 사설 grid/strip(66ch)임을 확인하여 데이터 누수 배제 |
| E10 | F4.5 Multi-testing | 15개 하류 세부 과제별 다중 비교 시 우연한 통과 발생 가능성 | 3대 벤치마크 평균(`rule3`)을 1차 기준으로 삼고, 세부 과제별 판정 시 "유지", "깨짐", "판정 불가(CI 경계 걸침)"를 엄격히 구분 |
| E11 | F5.1 Roadmap | 11/20 NeuroAI 워크숍 제출 논문에서 ×4 긴 학습(256 epoch) 포함 여부 | 11/10 실측 결과 x4clean(job 1247049)에서 후반 loss 상승 이상(+.005~.009)이 관찰되었으므로, ×4는 판정에서 제외하고 한계점으로 처리 |
| E12 | F6.1 Hygiene | `.agents/teamwork/` 내부에 소스 코드, 테스트 파일, 데이터 파일이 배치되는 경우 | 레이아웃 위반으로 감지. `.agents/teamwork/`는 오직 에이전트 메타데이터만 허용하며 코드는 루트 `tests/`, 문서는 `docs/`에 배치 |
| E13 | F6.3 Git Push | GitHub `Transconnectome` 조직에 동일한 이름의 원격 저장소가 이미 존재하는 경우 | 원격 저장소 상태를 확인하고, 충돌 없이 안전하게 최신 커밋을 동기화하거나 remote URL을 정확히 바인딩 |
| E14 | F7.1 Progressive | 프로젝트 마일스톤이 진행 중(M1~M4 미완료)일 때 E2E 테스트 실행 시 crash | 미완료 마일스톤에 대해 비정상 크래시(AttributeError, FileNotFoundError 등)가 아닌 명확한 Assertion / Skip / Pending 처리 및 점진적 통과 지원 |

---

## 4. Comprehensive Feature Specifications (F1 through F7)

### Feature 1: Teams Communication & Mentoring Trace Synthesis (F1)
- **Authoritative Requirement**: `ORIGINAL_REQUEST.md` R1, `PROJECT.md` F1, M1.
- **Target Artifact**: `docs/01_research_synthesis.md` (§1).
- **Core Components**:
  1. **Mentoring Background**: 김재철 AI 클래스 인턴십(2026-10-26~) 멘토링 체계, 이아현 선생님의 1:1 전담 지도, `Transconnectome/KimJaeChul_AI_Class_Mentoring` 저장소 구축.
  2. **Experimental Milestones**: 2026-10-28 KISTI 한강 멀티노드 셋업 보고, 2026-11-03 한강 속도 1.72배 단축, 2026-11-08 1/64 유지 및 EEG 혼합 손실 발견, 2026-11-09 종합 슬라이드 미팅.
  3. **The Dialectical Debate (핵심 논쟁)**:
     - **차지욱 교수님의 비판 (2026-11-10T08:18:09Z)**:
       > "그냥 섞으면 알아서 잘 학습될 것들이 아니어서 놀랍지 않은 결과... 공통 표상을 학습하지 못하고 있다는 것을 다 잘 알고 있음... iEEG 효과 미미도 놀라운 negative results 아님... 설익은 페이퍼를 쓰는 것보다는 의미있는 발견을 먼저 하는게 좋을 것..."
     - **이아현 선생님의 옹호 및 반론 (2026-11-10T14:52:02Z)**:
       > "negative result 가 아니라 발견... 참가자 수는 유지하면서 한 명당 데이터를 1/64로 줄였을 때... 참가자를 줄이면 harmful 하지만 참가자당 시간을 줄였을 때는 그렇지 않음... DIVER-1.5 channel origin prediction과 합치... how should we scale을 보여주는 좋은 포인트..."
  4. **Strict Honorific Invariant**: "안채원 선생님", "이아현 선생님" 존칭 준수. "씨", 반말, 평가적 하대 금지.

### Feature 2: Experimental Data & Infrastructure Extraction (F2)
- **Authoritative Requirement**: `ORIGINAL_REQUEST.md` R1, `PROJECT.md` F2, M1.
- **Target Artifact**: `docs/01_research_synthesis.md` (§2).
- **Domain Metrics & Invariants**:
  1. **HPC Strong Scaling**: KISTI 국가슈퍼컴퓨팅센터 6호기 「한강」(Slurm, GH200 4장/노드, Slingshot).
     - 1노드: 189.7 samples/s ($E=1.00$)
     - 2노드: 361.6 samples/s ($E=0.95$)
     - 4노드: 657.1 samples/s ($E=0.87$)
     - 8노드: 1,180.1 samples/s ($E=0.78$)
     - 한강 GH200 1노드 처리량 = Aurora ALCF PVC Tile 12개 노드의 약 3.8배.
  2. **DDP Timer Profiling 결함 해결**: PyTorch DDP all-reduce 특성상 dataloader stall이 backward/opt_step으로 전가되는 결함 수정. iEEG의 cold cache I/O 대기율 15.6% 실측 및 worker 16 튜닝.
  3. **Data Volume & Subsampling**:
     - 원천 데이터: iEEG 37명 (사설 25명 + AJILE 12명), 5,203시간, 624,365개 30초 레코드 (344,994 채널·h).
     - 고정 학습량: 2,887,680 (2.88M) 샘플 고정.
     - 1/64 (81.3h, 9,757 레코드): $\Delta\text{score} = -0.0004 [-0.0019, +0.0012]$ (비열등, 마진 $\Delta > -0.005$).
     - 1/256 (20.3h, 2,438 레코드): $\Delta\text{score} = -0.0010 [-0.0031, +0.0012]$ (비열등).
     - 1/1024 (5.1h, 613 레코드): $\Delta\text{score} = +0.0006 [-0.0012, +0.0024]$ (비열등).
     - 반감 기울기: 기록 절반당 $+0.00001 [-0.00021, +0.00022]$ (0과 구별 불가).
     - 미학습 모델(.6039) 대비 Base 사전학습 이득: $+0.0336 [+0.0255, +0.0417]$. 1/64는 이 이득의 98.9% 보존.
  4. **Modality Mixing Contrast**:
     - `EEG_fill`: iEEG 12.5% 남기고 EEG 채움 $\rightarrow$ Base 대비 $-0.0103 [-0.0147, -0.0059]$ 급락.
     - `iEEG_re`: iEEG 12.5% 단순 반복 $\rightarrow$ `EEG_fill` 대비 $+0.0100 [+0.0074, +0.0125]$ 우세.
     - `EEG_add`: iEEG 100% 유지 + EEG 추가 $\rightarrow$ `iEEG_re×2` 대비 $-0.0010 [-0.0029, +0.0008]$ 비열등 (무해하나 무이득).
  5. **Subject Diversity vs Duration**:
     - 81h (9,757 레코드): 8명 분산 $\Delta = +0.0001 [-0.0012, +0.0014]$ (유지) vs 2명 집중 $\Delta = -0.0055 [-0.0101, -0.0010]$ (붕괴).
     - 5h (613 레코드): 8명 분산 $\Delta = -0.0013 [-0.0047, +0.0020]$ (유지) vs 2명 집중 $\Delta = -0.0052 [-0.0099, -0.0005]$ (붕괴).
  6. **Readout Layer & Model Capacity**:
     - 1/64: 1층 $\Delta = -0.0004$, 12층 $\Delta = -0.0000$ (전 층 유지).
     - 1/1024: 1층 $\Delta = +0.0006$ (유지), 12층 Base $\Delta = -0.0029$ (판정 불가), Small(51M) $\Delta = -0.0050 [-0.0072, -0.0028]$ (붕괴).
  7. **Reconstruction vs Downstream Dissociation**:
     - 동일 피험자 Held-out reconstruction loss: 1/64 $+0.1\%$, 1/256 $+1.8\%$, 1/1024 $+8.5\% [+7.7, +9.2\%]$ 악화.
     - 신규 피험자(New subjects, Pippi/BYD) reconstruction loss: 1/1024 $-0.1\% [-1.3, +1.2\%]$ (전체 모델과 동등).

### Feature 3: Deep Research & Theoretical Foundation (F3)
- **Authoritative Requirement**: `ORIGINAL_REQUEST.md` R2, `PROJECT.md` F3, M2.
- **Target Artifact**: `docs/02_deep_research_literature.md`.
- **Literature Benchmark Taxonomy**:
  1. **94-Paper Meta-Analysis**: 기존 생체신호 모델 중 피험자 다양성 축과 시간 축을 분리한 parametric scaling law를 적합한 연구는 전무.
  2. **5 Key Papers Comparison**:
     - **Oliveira et al. (2026, arXiv:2609.35056)**: 두피 EEG CTNet 분류. 1인당 trial $\times$ 피험자 독립 스윕. $L = A N_t^{-\alpha} + B N_s^{-\beta} + L_\infty$. 한계: $\beta$가 0.07~1.99로 28배 편차 발생, $L_\infty=0$ 경계해 왜곡.
     - **Narayanswamy et al. (2024, LSM, arXiv:2410.13638)**: 스마트워치 센서. $L = a C^b + c$. 총 시간이 같으면 loss 유사. 한계: 사람 축 적합 없이 compute 축만 분석, 손목 센서의 낮은 다양성.
     - **Banville et al. (2025, Meta, arXiv:2501.15322)**: 다중 피험자 vs 단일 피험자. 한계: 사람 축 적합 포기(24 vs 48명 t-test p=0.49), 학습한 사람(seen subjects)으로 평가하여 다양성 효과 차폐.
     - **Ooi et al. (2025, Nature 644:731)**: fMRI phenotype 회귀. $r = K_0 \sqrt{1 / (1 + K_1/N + K_2/(NT))}$. 짧을 때는 총량($NT$), 길어지면 피험자 수($N$)가 병목.
     - **Truong et al. (2026, arXiv:2610.09287)**: 두피 EEG 10~1,863명. 50명 미만 평평(onset), 50명 초과 구간에서 $\log_2 S$ 선형 증가.
  3. **Mathematical Scaling Formalization**:
     - 가설 검정: $H_0: K_1 = 0$ ("피험자 다양성은 총 연산량과 독립적인 효과를 갖지 않는다").
     - 외삽 검증 프로토콜: 120h, 240h에서 적합 후 480h 외삽 예측 오차 비교.
  4. **Registry v8 Triad Design**:
     - **C1 (총량 고정 배분)**: PennEPI (103명, 중앙값 176h). 120/240/480h 3단계 스윕.
     - **C2 (병원/데이터셋 다양성)**: 6개 코호트(FR1, SWS, CCEP, PennEPI, SWEC, UMN) 48명 1인당 30 ch-h 고정.
     - **C3 (1인당 시간 고정 피험자 스윕)**: RAM(FR1+catFR1 고유 377명) 20, 40, 80, 140, 200명 스윕.

### Feature 4: Scientific Adversarial Review (F4)
- **Authoritative Requirement**: `ORIGINAL_REQUEST.md` R2, `PROJECT.md` F4, M3.
- **Target Artifact**: `docs/03_adversarial_review.md`.
- **5 Methodological Vulnerability Axes**:
  1. **가설 타당성 (Hypothesis Validity)**:
     - 반론: "사전 지식 없는 단순 데이터 혼합은 실패하는 것이 당연하며, 이는 준비 부족을 알리는 음성 결과(negative result)에 불과하다" (차지욱 교수님 논점).
     - 방어 및 입증: 총 compute를 엄밀히 통제한 상태에서 단순 데이터 감축이 아닌 "피험자 수 보존 vs 개인당 시간 감축"을 분리하여 스케일링 가이드라인("How to scale")을 제시한 양성 발견.
  2. **인과 추론 및 교란 요인 (Causal Inference & Confounders)**:
     - 반론: 피험자 2명 조건의 성능 붕괴($-0.0055$)는 피험자 수가 적어서가 아니라 심부 전극(sEEG depth)이나 특정 해부학적 뇌 영역이 결측되었기 때문일 수 있다.
     - 방어 및 입증: 전극 믹스 전수 감사(`job 1243386`) 결과, 2명 조건의 모든 seed가 심부 depth 전극(6.9~26.3%)을 포함하고 있으며, depth 비율과 손실 간 상관이 없음을 실측하여 반증.
  3. **대조군 및 실험 설계 (Control Groups & Ablation)**:
     - 반론: 다운스트림 벤치마크 점수 유지가 모델 학습이 아니라 단순 데이터셋 자체의 손쉬운 난이도나 손특징(hand-crafted feature) 덕분일 수 있다.
     - 방어 및 입증: Untrained 모델(.6039), Hand-crafted feature(.5954) 대비 Base(.6363) 및 1/64(.6359)의 명백한 성능 우위($+0.0336$)를 입증하여 사전학습의 고유 기여 확립.
  4. **재구성 손실과 하류 점수 괴리 역설 (Reconstruction vs Probe Dissociation)**:
     - 반론: 1/1024에서 held-out loss가 $+8.5\%$ 악화되는데 downstream probe가 유지되는 것은 probe가 저주파/저차원 특징에 과적합되었거나 모델이 환자별 스타일을 외웠음을 의미한다.
     - 방어 및 입증: 완전 신규 피험자(New subjects)에 대한 loss 차이는 $-0.1\%$로 나타나, $+8.5\%$ 증가는 동일 환자의 미세 신호 외우기(memorization)에 불과하며 일반화 표상 품질은 손상되지 않았음을 실측(`job 1247125`).
  5. **통계적 엄밀성 (Statistical Rigor)**:
     - 반론: 단일 seed나 좁은 표본으로 인한 가짜 비열등성 판정 위험.
     - 방어 및 입증: 6개 random seed 짝 비교(df=5), 사전 등록된 비열등성 마진($\Delta > -0.005$, 사전학습 효과의 15% 이내 손실 허용), 95% t-신뢰구간 산출.

### Feature 5: Actionable Improvement Items & Prioritized Roadmap (F5)
- **Authoritative Requirement**: `ORIGINAL_REQUEST.md` R3, `PROJECT.md` F5, M4.
- **Target Artifact**: `docs/04_action_items_roadmap.md`.
- **3-Tier Action Item Structure**:
  1. **Tier 1: 즉각 실행 과제 (Immediate, AAAI 2027 NeuroAI 워크숍 마감 2026-11-20)**:
     - Task 1.1: 4쪽 논문 뼈대 완성 (`paper_skeleton.md` 기반 본문 작성).
     - Task 1.2: 1/32 seed 4–6 재학습 run 반영 및 Figure 3 (a,b,c) 최종 렌더링.
     - Task 1.3: 1/1024의 12층 붕괴($-.0050$) 및 Full Fine-tuning 과적합(epoch ~7 검증 loss 상승)을 한계점(Limitations) 섹션에 정직하게 명시.
     - Task 1.4: 전극 종류(depth 6.9~26.3%) 감사 수치를 반영하여 "전극 부재 가설" 반증 박스 추가.
  2. **Tier 2: 중기 실행 과제 (Medium-Term, DIVER-2 저널 논문 & Aurora HPC)**:
     - Task 2.1: Aurora 슈퍼컴퓨터(25,000시간, 12월 만료) 자원을 활용한 C1(PennEPI 103명), C2(6개 병원), C3(RAM 377명) 본실험 완수.
     - Task 2.2: 204M(폭 1024) 및 12개 층 대형 모델에서의 1/64 비열등성 재현성 검증.
     - Task 2.3: Oliveira형 vs Ooi형 딥러닝 확장식 외삽 오차 비교를 통한 최종 스케일링 법칙 함수형 확정.
  3. **Tier 3: 장기 실행 과제 (Long-Term, 임상 확장 및 파운데이션 모델 생태계)**:
     - Task 3.1: MAYO 클리닉 간질 발작파 감지 벤치마크를 통한 병리적 진단 과제 검증.
     - Task 3.2: DIVER-1.5의 Channel Origin Prediction(채널 출처 예측) 및 Contrastive SSL과의 비교를 통한 MAE 고유 특성 분리.
     - Task 3.3: 병원 간 데이터 공유 제한을 극복하는 "소표본 다수 환자" 연합 학습(Federated Pretraining) 프로토콜 개발.

### Feature 6: Git Repository Structuring & Transconnectome Push (F6)
- **Authoritative Requirement**: `ORIGINAL_REQUEST.md` R4, `PROJECT.md` F6, M5.
- **Target Artifacts**:
  - `README.md` (종합 총괄 요약)
  - `docs/01_research_synthesis.md`
  - `docs/02_deep_research_literature.md`
  - `docs/03_adversarial_review.md`
  - `docs/04_action_items_roadmap.md`
  - `tests/verify_acceptance_criteria.py`
  - `.git` 저장소 초기화, 커밋, 및 GitHub `Transconnectome/chaewon_ahyeon_research_review` 원격 저장소 푸시.
- **Invariants**:
  - `README.md`는 경영진/교수님 보고용 총괄 요약본으로서 연구 배경, 핵심 발견, 5대 취약점, 3단계 로드맵, 검증 결과를 모두 포괄해야 함.
  - `.agents/teamwork/` 내에는 오직 에이전트 메타데이터만 존재해야 함. 소스/문서/테스트는 지정된 루트/docs/tests 디렉토리에 배치.

### Feature 7: E2E Acceptance Criteria Verification (F7)
- **Authoritative Requirement**: `PROJECT.md` F7, `SCOPE.md`.
- **Target Artifacts**: `TEST_INFRA.md`, `tests/verify_acceptance_criteria.py`, `TEST_READY.md`.
- **Execution Contract**: `python3 tests/verify_acceptance_criteria.py` (Exit code 0 = PASS, Exit code 1 = FAIL).
- **Test Hierarchy**: 4 Tiers, 최소 82개 이상의 테스트 케이스 구현.

---

## 5. E2E Testing Track 4-Tier Test Requirements Matrix

To ensure that the test design specialist (Explorer 3) and test implementer have unambiguous, mathematically verifiable assertion targets, this section details the requirements for all 4 tiers:

### Tier 1: Feature Coverage (>=5 tests per feature, >=35 tests total)
1. **F1 Tests (Teams & Mentoring Synthesis)**:
   - `test_f1_presence_of_research_synthesis_doc`: `docs/01_research_synthesis.md` 파일 존재 및 5KB 이상 크기 확인.
   - `test_f1_chaewon_ahn_mentoring_history`: 안채원 선생님 김재철 AI 클래스 인턴십, 10/26~11/10 타임라인 기술 확인.
   - `test_f1_ahyeon_lee_mentoring_and_diver`: 이아현 선생님 DIVER-1/1.5/2 역할 및 멘토링 주도성 기술 확인.
   - `test_f1_prof_cha_critique_quoted`: 차지욱 교수님의 11/10 비판 메시지("준비 부족", "음성 결과") 인용 및 분석 확인.
   - `test_f1_ahyeon_counterargument_recorded`: 이아현 선생님의 11/10 반론("발견", "how should we scale") 인용 및 분석 확인.
2. **F2 Tests (Empirical Extraction)**:
   - `test_f2_hangang_supercomputer_metrics`: 한강 GH200 1~8노드 실측치(1,180.1 samples/s, $E(8)=0.78$) 확인.
   - `test_f2_ddp_timer_anomaly_resolution`: DDP all-reduce dataloader stall 타이머 버그 및 해결책 기술 확인.
   - `test_f2_subsampling_non_inferiority`: 1/64(81h) 및 1/1024(5h) 비열등성($\Delta > -0.005$) 실측 수치 확인.
   - `test_f2_eeg_fill_vs_ieeg_re_penalty`: `EEG_fill` vs `iEEG_re` 비교 수치($+0.0100$) 확인.
   - `test_f2_subject_diversity_threshold`: 8명 분산(유지) vs 2명 집중($-0.0055$ 붕괴) 실측 수치 확인.
3. **F3 Tests (Deep Research & Literature)**:
   - `test_f3_presence_of_literature_doc`: `docs/02_deep_research_literature.md` 파일 존재 및 크기 확인.
   - `test_f3_94_paper_meta_survey`: 94편 뇌파 파운데이션 모델 전수 분석 및 스케일링 법칙 부재 규명 확인.
   - `test_f3_five_core_paper_citations`: Oliveira, Narayanswamy, Banville, Ooi, Truong 5개 논문 인용 및 비교표 확인.
   - `test_f3_mathematical_scaling_formalization`: Oliveira형 vs Ooi형 딥러닝 확장식 수식 표기 확인.
   - `test_f3_registry_v8_triad_design`: C1(PennEPI), C2(6개 데이터셋), C3(RAM 377명) 3대 대조 설계 확인.
4. **F4 Tests (Adversarial Review)**:
   - `test_f4_presence_of_adversarial_doc`: `docs/03_adversarial_review.md` 파일 존재 및 크기 확인.
   - `test_f4_axis1_hypothesis_validity`: 가설 타당성 및 음성 결과 비판 방어 논리 확인.
   - `test_f4_axis2_causal_confounding`: 전극 믹스(depth 6.9~26.3%) 및 사이트 효과 인과성 검증 확인.
   - `test_f4_axis3_control_group_design`: 미학습(.6039), 손특징(.5954), EEG 전용(.6212), Base(.6363) 대조 확인.
   - `test_f4_axis4_dissociation_paradox`: 재구성 손실(+8.5%)과 다운스트림 유지 간 괴리 분석 확인.
5. **F5 Tests (Action Items Roadmap)**:
   - `test_f5_presence_of_roadmap_doc`: `docs/04_action_items_roadmap.md` 파일 존재 및 크기 확인.
   - `test_f5_tier1_immediate_neuroai_deadline`: Tier 1 즉각 실행 과제(11/20 NeuroAI 워크숍 마감) 확인.
   - `test_f5_tier2_medium_diver2_aurora`: Tier 2 중기 과제(DIVER-2, Aurora HPC 12월 만료) 확인.
   - `test_f5_tier3_long_clinical_pathology`: Tier 3 장기 과제(MAYO 임상 발작파 벤치마크) 확인.
   - `test_f5_action_items_executability`: 각 액션 아이템별 실행자(Owner), 기한(Timeline), 산출물(Deliverable) 명시 확인.
6. **F6 Tests (Repo Structuring & Publishing)**:
   - `test_f6_readme_executive_summary`: `README.md` 파일 존재 및 종합 보고서 내용 충실도 확인.
   - `test_f6_standard_directory_layout`: `docs/`, `tests/` 표준 디렉토리 구조 준수 확인.
   - `test_f6_git_initialization_status`: 로컬 `.git` 저장소 초기화 및 커밋 이력 확인.
   - `test_f6_transconnectome_remote_config`: 원격 저장소 URL(`Transconnectome/chaewon_ahyeon_research_review`) 설정 확인.
   - `test_f6_no_orphan_metadata_in_src`: 소스 디렉토리 오염 방지 및 `.gitignore` 유효성 확인.
7. **F7 Tests (Acceptance Criteria & Test Suite)**:
   - `test_f7_test_infra_doc_exists`: `TEST_INFRA.md` 파일 존재 확인.
   - `test_f7_test_ready_doc_exists`: `TEST_READY.md` 파일 존재 확인.
   - `test_f7_runner_executable`: `tests/verify_acceptance_criteria.py` 파이썬 실행 가능 여부 확인.
   - `test_f7_acceptance_criteria_checklist`: `ORIGINAL_REQUEST.md` 체크리스트 8개 항목 전수 매핑 확인.
   - `test_f7_exit_code_zero_on_success`: 검증 통과 시 Exit Code 0 반환 확인.

### Tier 2: Boundary & Corner Cases (>=5 tests per feature, >=35 tests total)
1. **F1-B (Strict Honorific Enforcement)**:
   - `test_f1_b_no_chaewon_ssi`: 문서 전체에서 안채원 연구자의 이름 뒤에 접미사 '씨'가 붙은 형태 미존재 검증.
   - `test_f1_b_no_ahyeon_ssi`: 문서 전체에서 이아현 연구자의 이름 뒤에 접미사 '씨'가 붙은 형태 미존재 검증.
   - `test_f1_b_mandatory_chaewon_seonsaengnim`: "안채원 선생님" 정규 존칭 표현 빈도 검증 ($\ge 5$회).
   - `test_f1_b_mandatory_ahyeon_seonsaengnim`: "이아현 선생님" 정규 존칭 표현 빈도 검증 ($\ge 5$회).
   - `test_f1_b_no_disrespectful_speech`: 학생에 대한 비존댓말("했다", "본다" 등 평가절하 서술) 미존재 검증.
2. **F2-B (Numeric Boundary & Consistency)**:
   - `test_f2_b_non_inferiority_margin_sign`: 비열등성 기준 마진($\Delta > -0.005$)의 음수 부호 및 하한 검증.
   - `test_f2_b_two_subject_drop_sign`: 2명 피험자 조건 손실($-0.0055$)의 음수 부호 및 붕괴 판정 일관성 검증.
   - `test_f2_b_eeg_fill_penalty_magnitude`: `EEG_fill` 손실($-0.0100$)과 `iEEG_re` 간의 차이 정확성 검증.
   - `test_f2_b_subject_count_min_threshold`: 피험자 수 임계치($N \ge 8$) 경계 조건 서술 검증.
   - `test_f2_b_readout_layer_12_collapse`: Layer 12 Small 모델 붕괴($-0.0050$)와 Layer 1 유지($+.0006$) 대비 검증.
3. **F3-B (Literature Reference Integrity)**:
   - `test_f3_b_doi_arxiv_presence`: 핵심 5편 논문의 정확한 식별자(arXiv:2609.35056, arXiv:2410.13638, arXiv:2501.15322, Nature 644, arXiv:2610.09287) 검증.
   - `test_f3_b_no_hallucinated_citations`: 허위 논문 인용 및 미확인 플레이스홀더 부재 검증.
   - `test_f3_b_truong_onset_threshold`: Truong onset(50명) 미만에서의 적합 오류 지적 서술 검증.
   - `test_f3_b_oliveira_beta_instability`: Oliveira 지수 $\beta$의 극단적 불안정성(0.07~1.99, 28배) 기술 검증.
   - `test_f3_b_ram_cohort_deduplication`: RAM 코호트 중복(148명) 제거 후 고유 377명 산출 정밀성 검증.
4. **F4-B (Adversarial Challenge Rigor)**:
   - `test_f4_b_all_five_vulnerabilities_covered`: 5대 취약점 카테고리가 누락 없이 항목별로 검증되었는지 확인.
   - `test_f4_b_electrode_confound_refuted`: 전극 깊이(6.9~26.3%) 감사 수치와 반증 논리 구체성 검증.
   - `test_f4_b_memorization_distinction`: 동일 피험자 loss(+8.5%) vs 신규 피험자 loss(-0.1%) 분리 검증.
   - `test_f4_b_within_session_leakage_noted`: Within-session 디코딩 평가의 잠재적 누수 한계 서술 검증.
   - `test_f4_b_full_finetuning_overfitting_noted`: Full Fine-tuning 시 epoch ~7 과적합 현상 명시 검증.
5. **F5-B (Action Item Executability)**:
   - `test_f5_b_no_vague_study_needed`: "추가 연구가 필요하다" 식의 모호한 서술 배제 및 구체적 검증 지표 존재 확인.
   - `test_f5_b_timeline_feasibility`: 11/20 마감(Tier 1)과 12월 Aurora 만료(Tier 2)의 실현 가능한 일정 정합성 검증.
   - `test_f5_b_measurable_acceptance_criteria`: 액션 아이템마다 정량적 통과 기준(예: seed 6 짝 t-test) 명시 검증.
   - `test_f5_b_x4_training_instability_action`: x4 긴 학습(256 epoch) 불안정 현상에 대한 명확한 배제/보완 계획 검증.
   - `test_f5_b_clinical_task_extension_plan`: MAYO 간질 벤치마크 착수에 대한 구체적 프로토콜 기술 검증.
6. **F6-B (Git & Layout Hygiene)**:
   - `test_f6_b_no_code_in_agents_metadata`: `.agents/teamwork/` 내 `.py`, `.sh`, `.c` 소스 파일 미존재 검증.
   - `test_f6_b_git_commit_convention`: Git 커밋 메시지 컨벤션 준수 여부 검증.
   - `test_f6_b_file_size_thresholds`: 각 보고서 파일이 최소 본문 길이를 충족하는지 검증 (모두 > 3KB).
   - `test_f6_b_markdown_lint_cleanliness`: 마크다운 헤더 계층 및 깨진 링크 부재 검증.
   - `test_f6_b_transconnectome_org_binding`: Git remote가 올바른 `Transconnectome` 조직을 가리키는지 검증.
7. **F7-B (Runner Robustness & Graceful Degradation)**:
   - `test_f7_b_progressive_testability`: 산출물이 부분적으로 작성된 상태에서도 에러로 중단되지 않고 진행 상황을 보고하는지 검증.
   - `test_f7_b_clear_failure_messages`: 실패한 테스트가 발생했을 때 정확한 원인과 누락 파일을 출력하는지 검증.
   - `test_f7_b_no_external_network_dependency`: 단위/기능 테스트가 외부 네트워크 호출 없이 로컬 결정론적으로 동작하는지 검증.
   - `test_f7_b_execution_time_budget`: 전체 테스트 스위트 실행 시간이 30초 이내로 완료되는지 검증.
   - `test_f7_b_reproducible_environment`: 표준 `python3` 라이브러리(unittest 등)만으로 구동 가능한지 검증.

### Tier 3: Cross-Feature Combinations (>=7 pairwise integration tests)
1. `test_tier3_f1_f2_experimental_trace_consistency`: F1의 Teams 멘토링 회의록(11/9 슬라이드)과 F2의 실험 수치(2.88M, 1/64, -0.0055 등) 간 완전한 수치 일치 검증.
2. `test_tier3_f1_f4_debate_to_adversarial_mapping`: F1의 차지욱 교수님 비판("음성 결과")이 F4의 적대적 리뷰 제1축(가설 타당성)에 직접 매핑되어 비판-반론 구조를 형성하는지 검증.
3. `test_tier3_f2_f4_empirical_to_methodology_defense`: F2의 2명 피험자 붕괴 수치($-0.0055$)가 F4의 인과 추론 및 전극 교란 반증(depth 6.9~26.3%)에 정합하게 활용되는지 검증.
4. `test_tier3_f3_f4_literature_to_adversarial_critique`: F3의 Truong onset(50명) 및 Ooi fMRI 모델이 F4의 피험자 다양성 가설 검증의 이론적 토대로 활용되는지 검증.
5. `test_tier3_f4_f5_vulnerability_to_roadmap_coverage`: F4에서 식별된 5대 취약점(Layer 12 붕괴, 재구성 괴리, 전극 교란 등) 각각에 대해 F5 로드맵에 대응 액션 아이템이 1:1 이상 존재하는지 검증.
6. `test_tier3_f5_f6_roadmap_to_readme_synthesis`: F5의 우선순위 액션 아이템 요약이 F6의 `README.md` 총괄 로드맵 섹션에 완벽히 반영되어 있는지 검증.
7. `test_tier3_f1_through_f6_to_f7_e2e_integration`: F1부터 F6까지의 모든 산출물(`docs/01`~`04`, `README.md`, `.git`)이 F7의 테스트 스위트에 의해 종단간(E2E) 누락 없이 통합 검증되는지 확인.

### Tier 4: Real-World Acceptance Scenarios (>=5 application-level tests)
1. `test_tier4_s1_full_acceptance_criteria_satisfaction`: `ORIGINAL_REQUEST.md`에 명시된 8대 인수 조건 체크리스트 전수 통과 검증.
2. `test_tier4_s2_lab_policy_and_honorific_compliance`: 서울대학교 인지신경과학 연구실(Connectome Lab) 및 차지욱 교수님 운영 가이드라인(학생 대상 존칭, 증거 기반 분석) 준수 검증.
3. `test_tier4_s3_publication_readiness_audit`: `README.md` 및 `docs/` 문서들의 학술적 완결성, 수치 신뢰구간 표기 무결성, 오탈자 및 마크다운 포맷 검증.
4. `test_tier4_s4_neuroai_workshop_nov20_readiness`: 2026-11-20 마감인 AAAI 2027 NeuroAI 워크숍 제출 요건(4쪽 분량, 메인 Figure 3 패널 구성, 핵심 발견 서술) 충족도 검증.
5. `test_tier4_s5_transconnectome_reproduction_check`: GitHub Transconnectome 원격 저장소 배포 및 타 연구자의 독립적 클론/재현 가능성 검증.

---

## 6. Summary of Verification Minimums

- **Tier 1 (Feature Coverage)**: 7 features $\times$ 5 tests = **35 tests**
- **Tier 2 (Boundary & Corner Cases)**: 7 features $\times$ 5 tests = **35 tests**
- **Tier 3 (Cross-Feature Integrations)**: **7 tests**
- **Tier 4 (Real-World Acceptance Scenarios)**: **5 tests**
- **Grand Total**: $35 + 35 + 7 + 5 =$ **82 tests minimum**.
