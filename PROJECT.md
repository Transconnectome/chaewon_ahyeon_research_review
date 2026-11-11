# Project: chaewon_ahyeon_research_review

## Architecture
- **Objective**: 안채원 선생님, 이아현 선생님, 차지욱 교수님의 Teams 기반 연구 성과 및 원천 실험 코드·통계, DIVER-2 파운데이션 모델 아키텍처, 신규 비대칭 MAE 구현을 전수 재검토하고, 딥리서치와 과학적 방법론에 기반한 적대적 리뷰 및 결정적 추가 조언(additional advice)을 도출하여 11/20 NeuroAI 워크숍 투고 및 향후 본 논문 확장을 지원.
- **Data Flow**:
  1. Teams DB (`~/.agents/registry/chavis_teams/teams.db`) & Git Repos (`Transconnectome/chaewon-intern-2026fall`, `DIVER-2`, `DIVER`, `DIVER-dense-long-context`)
  2. Research Synthesis (`docs/01_research_synthesis.md`)
  3. Deep Research & Literature Benchmarking (`docs/02_deep_research_literature.md`)
  4. Scientific Adversarial Review (`docs/03_adversarial_review.md`)
  5. Prioritized Action Items & Roadmap (`docs/04_action_items_roadmap.md`)
  6. Repository Structuring, Executive Summary (`README.md`), and GitHub Transconnectome Publication
  7. In-depth Multi-Repo Audit, Code Hardening & Additional Advice (`docs/05_additional_advice.md`, `code/asymmetric_mae/`, `tests/`)

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| F1 | Teams Communication & Mentoring Trace Synthesis | 안채원 선생님·이아현 선생님의 Teams 메시지, 멘토링 회의록, 교수님 피드백 및 반론 전수 체계화 | M1 | Survey 1, 2, 3 |
| F2 | Experimental Data & Infrastructure Extraction | KISTI 한강 클러스터 실측, DIVER-1/2 아키텍처, 2.88M 샘플 고정 실험, 피험자 다양성 vs 기록 시간 실측 수치 정리 | M1 | Survey 1, 2 |
| F3 | Deep Research & Theoretical Foundation | 94편 뇌파 파운데이션 모델 및 스케일링 법칙(Oliveira, Ooi, Truong, Narayanswamy, Banville) 딥리서치 및 비교 분석 | M2 | Survey 2, 3 |
| F4 | Scientific Adversarial Review | 5대 과학적 방법론(가설 타당성, 인과 추론, 대조군 설계, 재구성 손실-하류 점수 괴리, 통계적 엄밀성) 기반 비판적 검증 | M3 | Survey 1, 2, 3 |
| F5 | Actionable Improvement Items & Prioritized Roadmap | 단기(NeuroAI 워크숍 11/20 마감), 중기(DIVER-2 저널), 장기(임상 확장) 3단계 우선순위 액션 아이템 수립 | M4 | Survey 1, 2, 3 |
| F6 | Git Repository Structuring & Transconnectome Push | 작업 디렉토리 git 초기화, 체계적 디렉토리 구조화, 커밋 및 GitHub Transconnectome 원격 저장소 생성 및 푸시 | M5 | Survey 3 |
| F7 | E2E Acceptance Criteria Verification | 전체 인수 조건(Acceptance Criteria) 자동 검증 및 정합성 테스트 | M5 | Survey 1, 2, 3 |
| F8 | Multi-Repo Audit & Experimental Blind Spots | 5대 실험 사각지대(동일 피험자 2% 분할 데이터 누수 및 미학습 손실 2.88배 폭증, 15개 과제 다중 비교 무보정 FWER 53.67%, 2.88M 샘플 sEEG 심부 비율 r=+0.473 교란, 1/1024 1층 vs 12층 표상 붕괴 및 유효 차원 5~6차원 축퇴, Neuroprobe 56~167 복셀 좌표 왜곡 및 결측 채널 제로필) 규명 | M6 | Survey 2-1, 2-2 |
| F9 | DIVER Architecture Flaws & Asymmetric MAE Hardening | 패딩 마스크 단위 불일치 버그(0.3초/10.6%만 학습), RoPE bf16 256초과 위치 충돌(829개 생존), Dense Attention Bias O(C^2 N^2) 메모리 벽, $L=1$ 단일 패치 NaN 방어, 이종 몽타주 마스크 소멸 방지, closed-form 레지스터 인덱싱, DDP module. prefix 및 형상 역추론 | M6 | Survey 2-2, 2-3 |
| F10 | Critical Additional Advice Document & Executive Summary Integration | `docs/05_additional_advice.md` 작성(워크숍 11/20 마감 전 즉각 조치 5건 및 본 논문 확장 제언 5건 분리, 파일/라인 인용), `README.md` 링크 및 갱신, 검증 테스트 100% 통과 | M6 | Survey 2-1, 2-2, 2-3 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Research Synthesis & Evidence Documentation | F1, F2: 안채원 선생님과 이아현 선생님의 연구 결과, 가설, 데이터, 실험 수치 종합 정리 (`docs/01_research_synthesis.md`) | none | DONE (docs/01_research_synthesis.md, Gate PASS) |
| M2 | Deep Research & Literature Benchmarking | F3: 최신 뇌파/생체신호 파운데이션 모델 및 2축 스케일링 법칙 학술 문헌 딥리서치 (`docs/02_deep_research_literature.md`) | M1 | DONE (docs/02_deep_research_literature.md, Gate PASS) |
| M3 | Scientific Adversarial Review | F4: 5대 과학적 방법론에 기반한 적대적 리뷰 및 취약점/한계점 정밀 검증 (`docs/03_adversarial_review.md`) | M1, M2 | DONE (docs/03_adversarial_review.md, Gate PASS) |
| M4 | Action Items & Prioritized Roadmap | F5: 식별된 취약점을 해소하기 위한 즉각 실행 가능한 단계별 개선 조치 및 로드맵 (`docs/04_action_items_roadmap.md`) | M3 | DONE (docs/04_action_items_roadmap.md, Gate PASS) |
| M5 | Repo Assembly & Transconnectome Publication | F6, F7: 통합 README.md, E2E 검증, Git 커밋 및 GitHub Transconnectome 원격 저장소 푸시 | M1, M2, M3, M4 | DONE (README.md, .gitignore, Git remote pushed, 82/82 E2E pass, 14/14 challenge pass, Gate PASS) |
| M6 | Additional Advice & Asymmetric MAE Hardening | F8, F9, F10: 5대 실험 사각지대 및 DIVER 아키텍처 결함 규명, 비대칭 MAE 엣지 케이스 및 DDP 호환성 강화, `docs/05_additional_advice.md` 작성 및 `README.md` 갱신, 단위/E2E 검증 | M5 | DONE (docs/05_additional_advice.md, asymmetric_mae.py, README.md, 122/122 tests pass, Gate PASS) |

## Interface Contracts
### M1 -> M2, M3
- Input data extracted: 37 subjects, 5,203h iEEG, 2.88M samples fixed, 1/64 (81h) & 1/1024 (5h) non-inferiority ($\Delta > -0.005$), `EEG_fill` vs `iEEG_re` ($-0.0100$ penalty), 37 vs 8 vs 2 subjects (2 subjects drop $-0.0055$), layer 1 vs layer 12 readout divergence, held-out reconstruction loss ($+8.5%$) vs downstream score stability.
- Output file: `docs/01_research_synthesis.md`

### M2 -> M3
- Literature baseline models: Oliveira et al. 2026, Ooi et al. 2025, Narayanswamy et al. 2024, Banville et al. 2025, Truong et al. 2026, BrainWave, DIVER-1.5 ACPE.
- Output file: `docs/02_deep_research_literature.md`

### M3 -> M4
- Categorized vulnerabilities:
  1. Readout layer specificity (layer 1 vs layer 12 divergence in 1/1024).
  2. Reconstruction loss vs Downstream probe dissociation paradox.
  3. Linear probing on restricted 3 cognitive tasks vs clinical pathology tasks.
  4. Masked Autoencoding vs Channel Origin Prediction / Contrastive SSL specificity.
  5. Subject diversity threshold ($N \ge 8$) and site/electrode montage confounding.
- Output file: `docs/03_adversarial_review.md`

### M4 -> M5
- Action items categorized by Priority (Tier 1: Immediate by 11/20, Tier 2: Medium-term DIVER-2, Tier 3: Long-term).
- Output file: `docs/04_action_items_roadmap.md`

### M5 -> M6
- Baseline repository files: `README.md`, `tests/verify_acceptance_criteria.py`, `tests/test_adversarial_challenge.py`, `code/asymmetric_mae/`.

### M6 Deliverables & Contracts
- Implementation files:
  - `code/asymmetric_mae/asymmetric_mae.py` (L=1 NaN guard, per-sample k_vis heterogeneous montage guard, closed-form register indexing, DDP module. prefix removal and width/depth auto-inference)
  - `tests/test_asymmetric_mae_smoke.py` (Extended tests for L=1, heterogeneous montage, DDP compat, closed-form register equivalence)
  - `docs/05_additional_advice.md` (Comprehensive Additional Advice document with exact file/line citations and separated workshop vs paper actions)
  - `README.md` (Updated with Section 5 Additional Advice integration)

## Code Layout
```
/home/juke/git/chaewon_ahyeon_research_review/
├── README.md                          # 종합 보고서 및 총괄 요약
├── docs/
│   ├── 01_research_synthesis.md       # R1: 연구 결과 및 원천 자료 체계적 요약
│   ├── 02_deep_research_literature.md # R2-1: 최신 학술 문헌 딥리서치 및 비교 분석
│   ├── 03_adversarial_review.md       # R2-2: 과학적 방법론 기반 적대적 리뷰
│   ├── 04_action_items_roadmap.md     # R3: 개선 액션 아이템 및 단계별 로드맵
│   └── 05_additional_advice.md        # R3-New: 심층 맹점 규명 및 결정적 추가 조언
├── code/
│   └── asymmetric_mae/                # 신규 비대칭 MAE 구현 및 래퍼
│       ├── asymmetric_mae.py
│       └── run_asym_mae_wrapper.py
├── tests/
│   ├── verify_acceptance_criteria.py  # 인수 조건 자동 검증 테스트
│   ├── test_adversarial_challenge.py  # 적대적 스트레스 테스트
│   ├── test_asymmetric_mae_smoke.py   # 비대칭 MAE 단위/스모크 테스트
│   └── test_additional_advice_criteria.py # 신규 추가 조언 및 맹점 검증 테스트
├── .gitignore                         # Git 제외 설정
└── .agents/teamwork/                  # 오케스트레이션 및 에이전트 메타데이터
```
