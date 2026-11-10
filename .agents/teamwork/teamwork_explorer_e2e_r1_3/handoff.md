# Handoff Report: E2E Test Matrix & Verification Design

- **Author**: Explorer 3 (Test Matrix & Design Specialist, E2E Testing Track)
- **State Folder**: `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_e2e_r1_3`
- **Date**: 2026-11-10T16:11:00Z
- **Deliverable**: `test_design_matrix.md` (Comprehensive specification of 82 test methods across 4 tiers)

---

## 1. Observation (직접 관찰 사실)

### 1.1 프로젝트 명세 및 요구사항 관찰
- **`ORIGINAL_REQUEST.md` (Lines 10–40)**:
  - R1: Teams 메시지 기반 연구 결과 및 원천 자료 분석 (안채원 선생님·이아현 선생님 핵심 주장, KISTI 한강 및 DIVER 실험 데이터)
  - R2: 딥리서치 및 과학적 방법론 기반 적대적 리뷰 (94편 문헌 메타분석, 5대 과학적 방법론 기반 비판적 검증)
  - R3: 개선 여지 도출 및 구체적 액션 아이템 수립 (우선순위 3단계 로드맵)
  - R4: Git 저장소 구축 및 Transconnectome 게시 (`README.md`, `.git`, GitHub remote push)
- **`PROJECT.md` (Lines 13–23, 33–59)**:
  - 7개 핵심 기능 (F1: Teams Trace, F2: Experimental Data, F3: Deep Research, F4: Adversarial Review, F5: Action Items, F6: Git & Publish, F7: E2E Verification)
  - 인터페이스 계약:
    - M1->M2, M3: 37명, 5,203h iEEG, 2.88M 샘플 고정, 1/64(81h) & 1/1024(5h) 비열등성($\Delta > -0.005$), `EEG_fill` vs `iEEG_re` ($-0.0100$ 페널티), 37 vs 8 vs 2명(2명 붕괴 $-0.0055$), 1층 vs 12층 괴리, 재구성 손실($+8.5%$) vs 하류 점수 안정성.
    - M2->M3: 5대 핵심 문헌 (Oliveira 2026, Ooi 2025, Narayanswamy 2024, Banville 2025, Truong 2026).
    - M3->M4: 5대 취약점 축 (Readout layer, Reconstruction loss paradox, Linear probing tasks, SSL specificity, Subject diversity & montage confounding).
    - M4->M5: 3단계 로드맵 (Immediate 11/20 NeuroAI, Medium DIVER-2, Long clinical).
- **`SCOPE.md` (Lines 33–64)**:
  - 4개 티어 최소 요건: Tier 1 $\ge 35$ tests (5 per F1–F7), Tier 2 $\ge 35$ tests (5 per F1–F7), Tier 3 $\ge 7$ pairwise tests, Tier 4 $\ge 5$ acceptance tests. 총합 $\ge 82$ tests.
  - 엄격한 호칭 규칙: "안채원 선생님", "이아현 선생님" 필수; "씨" 및 반말 절대 금지.

### 1.2 런타임 환경 관찰
- Python 3.12.3 및 pytest 9.1.1 확인 (`python3 --version` -> `Python 3.12.3`, `pytest 9.1.1`).
- 작업 디렉토리 `/home/juke/git/chaewon_ahyeon_research_review` 내에 `tests/` 및 `docs/` 디렉토리는 아직 생성되지 않음 (개발 진행 중).
- 표준 라이브러리(`unittest`, `re`, `subprocess`, `pathlib`, `json`, `argparse`)만으로 100% 호환되는 테스트 러너 구현 가능.

---

## 2. Logic Chain (논리 추론 체계)

1. **[관찰 1.1 SCOPE.md 및 PROJECT.md 참조]**
   - E2E 검증 트랙은 프로젝트 인수 조건(R1–R4, F1–F7)의 충족 여부를 객관적이고 불투명하게(opaque-box) 판정해야 한다.
   - 따라서 테스트 스위트는 단순한 파일 존재 여부를 넘어, 수치적 엄밀성(예: 37명, 5,203시간, 2.88M 샘플, $\Delta > -0.005$, $-0.0100$ 페널티), 인용의 진위성(arXiv ID 및 DOI), 논리적 일관성(취약점과 액션 아이템 간 1:1 매핑)을 엄격히 검증해야 한다.
2. **[관찰 1.1 및 연구실 규정 참조]**
   - 학생 및 연구원에 대한 호칭 규칙("선생님" 존칭, "씨" 및 반말 금지)은 단순한 스타일 가이드가 아니라 연결체 연구실(Connectome Lab)의 엄격한 거버넌스 원칙이다.
   - 따라서 Tier 2에 전수 정규표현식 검사(`test_f1_b01`, `test_f1_b02`, `test_f1_b03`, `test_tier4_s02`)를 배치하여 위반 발생 시 즉각 실패(assertion failure)하도록 설계하였다.
3. **[관찰 1.1 SCOPE.md 수량 기준 참조]**
   - Tier 1: 7개 기능 $\times$ 5개 = 35개
   - Tier 2: 7개 기능 $\times$ 5개 = 35개
   - Tier 3: 7개 pairwise 결합 = 7개
   - Tier 4: 5개 실전 시나리오 = 5개
   - 총 82개 테스트 케이스의 구체적 메서드명, 검증 로직, 입력 픽스처, 기대 산출물 및 실패 메시지를 `test_design_matrix.md`에 완전하게 명세하였다.
4. **[관찰 1.2 현재 작업 공간 상태 참조]**
   - 현재 산출물 문서가 작성 중이므로, 테스트 러너는 개발 중에도 점진적으로 실행 가능해야 한다.
   - 따라서 `--progressive` 옵션을 통해 미작성 마일스톤에 대한 구조화된 `PENDING` 진단을 지원하고, 개발 완료 시 `--strict` 모드로 82개 전수 통과(Exit Code 0)를 판정하도록 구조화하였다.

---

## 3. Caveats (한계 및 주의사항)

1. **구현 전 설계 산출물**:
   - 본 보고서는 테스트 설계 및 명세(Test Matrix & Design Specification)이며, `tests/verify_acceptance_criteria.py` 및 `TEST_INFRA.md`의 실제 코드 구현은 구현 에이전트(Implementer)의 작업 범위이다. (탐색 에이전트의 읽기 전용 제약 준수).
2. **원천 슬라이드 접근성**:
   - Google Slides(`1yueDz-YjVbw3q5IkvI8gPvOB8dDzjKzDBE5fQ3J9Tu0`)는 외부 URL이므로 로컬 오프라인 테스트 러너에서는 네트워크 요청 없이 텍스트 내 링크 유효성 및 인용 일치 여부로 검증하도록 격리하였다.
3. **Transconnectome 원격 저장소 푸시 권한**:
   - `gh auth status` 상 `snuconnectome` 계정이 확인되었으나, 최종 푸시는 M5 단계에서 실행되므로 테스트는 `git remote -v` 설정 및 git commit 내역을 검증하도록 설계되었다.

---

## 4. Conclusion (최종 종합 결론)

1. **82개 테스트 케이스 설계 완료**:
   - `SCOPE.md`와 `PROJECT.md`의 요구사항을 100% 충족하는 82개 테스트 케이스 카탈로그를 완성하여 `test_design_matrix.md`에 저장하였다.
   - Tier 1 (35개): F1–F7 전 기능의 구조적 존재성 및 필수 내용 검증.
   - Tier 2 (35개): 엄격한 호칭("안채원 선생님", "이아현 선생님"), 수치 경계값, 인용 진위성, 위생 검증.
   - Tier 3 (7개): Teams 대화-실험 데이터 일치, 반론-가설 정합, 취약점-액션아이템 1:1 대응 등 교차 검증.
   - Tier 4 (5개): 원본 요구사항(R1–R4) 완결성, 연구실 규정 준수, NeuroAI 워크숍 투고 준비도, 재현성 검증.
2. **구현 청사진 제공**:
   - `tests/verify_acceptance_criteria.py` 구현자를 위한 표준 라이브러리 기반 모듈 구조, CLI 인터페이스, 진단 에러 출력 형식 및 progressive 모드 규격을 완벽하게 정의하였다.

---

## 5. Verification Method (독립 검증 방법)

1. **설계 산출물 파일 확인 및 크기 검증**:
   ```bash
   ls -la /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_e2e_r1_3/test_design_matrix.md
   ```
2. **명세된 테스트 케이스 수량 검증 (82개 확인)**:
   ```bash
   grep -c "#### \`test_" /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_e2e_r1_3/test_design_matrix.md
   # 출력 결과: 82 확인
   ```
3. **티어별 분포 검증**:
   ```bash
   grep -E "(Tier 1|Tier 2|Tier 3|Tier 4)" /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_e2e_r1_3/test_design_matrix.md
   ```
4. **무효화 조건 (Invalidation Conditions)**:
   - 총 테스트 메서드 수가 82개 미만이거나, 특정 기능(F1–F7)의 테스트 수가 5개 미만인 경우 본 설계는 무효화된다.
   - 호칭 규칙 검증에서 "안채원 선생님" 또는 "이아현 선생님"에 대한 "씨" 검출 규칙이 누락된 경우 즉각 재설계되어야 한다.
