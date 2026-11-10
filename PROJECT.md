# Project: chaewon_ahyeon_research_review

## Architecture
- **Objective**: 안채원 선생님과 이아현 선생님의 Teams 기반 연구 성과를 분석하고, 최신 학술 문헌 딥리서치와 과학적 방법론에 기반한 적대적 리뷰(adversarial review)를 수행하여 연구의 한계와 개선 여지를 분석하고, 구체적·우선순위화된 액션 아이템을 도출하여 Git 저장소에 커밋 및 GitHub Transconnectome 조직에 업로드.
- **Data Flow**:
  1. Teams DB (`~/.agents/registry/chavis_teams/teams.db`) & Git Repos (`Transconnectome/chaewon-intern-2026fall`, `DIVER-2`, `KimJaeChul_AI_Class_Mentoring`)
  2. Research Synthesis (`docs/01_research_synthesis.md`)
  3. Deep Research & Literature Benchmarking (`docs/02_deep_research_literature.md`)
  4. Scientific Adversarial Review (`docs/03_adversarial_review.md`)
  5. Prioritized Action Items & Roadmap (`docs/04_action_items_roadmap.md`)
  6. Repository Structuring, Executive Summary (`README.md`), and GitHub Transconnectome Publication

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

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Research Synthesis & Evidence Documentation | F1, F2: 안채원 선생님과 이아현 선생님의 연구 결과, 가설, 데이터, 실험 수치 종합 정리 (`docs/01_research_synthesis.md`) | none | DONE (docs/01_research_synthesis.md, Gate PASS) |
| M2 | Deep Research & Literature Benchmarking | F3: 최신 뇌파/생체신호 파운데이션 모델 및 2축 스케일링 법칙 학술 문헌 딥리서치 (`docs/02_deep_research_literature.md`) | M1 | DONE (docs/02_deep_research_literature.md, Gate PASS) |
| M3 | Scientific Adversarial Review | F4: 5대 과학적 방법론에 기반한 적대적 리뷰 및 취약점/한계점 정밀 검증 (`docs/03_adversarial_review.md`) | M1, M2 | DONE (docs/03_adversarial_review.md, Gate PASS) |
| M4 | Action Items & Prioritized Roadmap | F5: 식별된 취약점을 해소하기 위한 즉각 실행 가능한 단계별 개선 조치 및 로드맵 (`docs/04_action_items_roadmap.md`) | M3 | DONE (docs/04_action_items_roadmap.md, Gate PASS) |
| M5 | Repo Assembly & Transconnectome Publication | F6, F7: 통합 README.md, E2E 검증, Git 커밋 및 GitHub Transconnectome 원격 저장소 푸시 | M1, M2, M3, M4 | IN_PROGRESS |

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

### M5
- Unified Executive Summary: `README.md`
- Verification suite: `tests/verify_acceptance_criteria.py`
- Git remote: `https://github.com/Transconnectome/chaewon_ahyeon_research_review.git`

## Code Layout
```
/home/juke/git/chaewon_ahyeon_research_review/
├── README.md                          # 종합 보고서 및 총괄 요약
├── docs/
│   ├── 01_research_synthesis.md       # R1: 연구 결과 및 원천 자료 체계적 요약
│   ├── 02_deep_research_literature.md # R2-1: 최신 학술 문헌 딥리서치 및 비교 분석
│   ├── 03_adversarial_review.md       # R2-2: 과학적 방법론 기반 적대적 리뷰
│   └── 04_action_items_roadmap.md     # R3: 개선 액션 아이템 및 단계별 로드맵
├── tests/
│   └── verify_acceptance_criteria.py  # 인수 조건 자동 검증 테스트
├── .gitignore                         # Git 제외 설정
└── .agents/teamwork/                  # 오케스트레이션 및 에이전트 메타데이터
```
