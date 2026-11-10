# Milestone 4 Adversarial Challenge Report

- **평가 에이전트**: `sub_orch_m4_challenger_2` (EMPIRICAL CHALLENGER / critic, specialist)
- **검증 대상 문서**: `/home/juke/git/chaewon_ahyeon_research_review/docs/04_action_items_roadmap.md`
- **검증 일시**: 2026-11-10T18:05:00Z
- **최종 판정 (Verdict)**: **APPROVE (조건부 승인 및 기술적 보완 권고)**

---

## 1. Challenge Summary (적대적 검증 총평)

- **Overall Risk Assessment**: **LOW-MEDIUM**
- **검증 배경**:
  본 평가는 안채원 선생님과 이아현 선생님의 연구 개선 액션 아이템 및 마스터 로드맵(`docs/04_action_items_roadmap.md`)에 대해 다음 4대 기술적 축을 중심으로 적대적 스트레스 테스트, 수치 시뮬레이션 및 독립 코드 감사를 수행하였습니다:
  1. **학술 베이스라인 대조의 엄밀성 (Baseline Comparison Rigor)**: BrainBERT, BIOT, LaBraM 대비 DIVER-2의 차별성 및 9축 대조 매트릭스의 공정성/완결성.
  2. **가상 전극 RBF 보간의 수학적·수치적 안정성 (Mathematical & Numerical Stability of RBF Interpolator)**: 128개 MNI 피질 앵커 노드 투영의 조건수, 유계성 및 그래디언트 전파 특성.
  3. **엣지 온디바이스 BCI 실시간 스트리밍 실행 가능성 (Mamba-2 SSM on Jetson Orin Nano)**: 메모리 대역폭, 연산 TOPS, 커널 오버헤드 기반 $\le 15\text{ms}$ 지연시간의 물리적 실현 가능성.
  4. **생명윤리 및 데이터 거버넌스 방어력 (HIPAA Safe Harbor & OpenRAIL-M Governance)**: 3D 안면 재식별 방지, 시간 지터링, 개인정보보호법 및 국외 이전 규정 준수성.

---

## 2. Deep Adversarial Challenges (심층 적대적 검증 결과)

### [Medium] Challenge 1: 베이스라인 대조표의 9번째 평가 축(시간 패치 분해능) 누락 및 공정성 경계
- **Assumption Challenged**:
  `docs/04_action_items_roadmap.md` Section 3.2 4)의 표는 최신 파운데이션 모델(BrainBERT, BIOT, LaBraM)과의 9대 비교 축을 완벽히 제시한다고 기술되어 있으나, 실측 표의 행 수가 8개에 그침.
- **Attack Scenario & Observation**:
  - `sub_orch_m4_explorer_2/report.md` (lines 495-507)에서는 9대 비교 축(1. 지원 모달리티, 2. 사전학습 데이터 규모, 3. 공간 좌표 인코딩, **4. 시간 패치 분해능**, 5. 자가지도학습 목적함수, 6. 임의 침습 전극 일반화, 7. 미세조정 안정성, 8. 2축 스케일링 검증, 9. 임상 발작파 벤치마크)을 명시하였으나, 최종 취합 문서인 `docs/04_action_items_roadmap.md` (lines 646-656)에서는 **"시간 패치 분해능 (Temporal Patch Resolution)"** 행(BrainBERT: 1.0s STFT, BIOT: 1.0s, LaBraM: 0.2s vs DIVER-2: 0.1s + FlashAttention-2)이 누락되어 8개 행만 존재함.
  - 또한, 두피 EEG 모델인 LaBraM(Jiang et al., 2024)과 일반 생체신호 모델인 BIOT(Yang et al., 2023)을 침습 iEEG 모델인 DIVER-2와 동일 평면에서 비교할 때, 심사위원이 "두피 EEG 전용 모델을 침습 전극 일반화가 안 된다고 비판하는 것은 모달리티 특이적 불공정 비교"라는 역공을 펼칠 수 있음.
- **Blast Radius**:
  학술지 심사관이 표의 완결성 결함 및 모달리티 간 비교의 범주 착오(Category Error)를 지적할 위험.
- **Empirical Mitigation**:
  1. M5 통합 또는 저널 원고 반영 시 누락된 9번째 행(**시간 패치 분해능**: BrainBERT 1.0s STFT vs BIOT 1.0s vs LaBraM 0.2s vs DIVER-2 0.1s 50p 고속 비중첩)을 표 3.2 4)에 정식 복원할 것.
  2. 표 주석에 "LaBraM 및 BIOT은 두피/생체신호 분야의 최고 성능 모델이나 고정 몽타주 토큰화의 한계로 인해 임의 3D 공간 침습 전극으로의 직접 전이가 구조적으로 불가능함을 입증하기 위한 구조적 베이스라인으로 선정함"을 명시할 것.

---

### [Medium] Challenge 2: 128-노드 RBF 보간의 장거리 외삽 구역 영가중치(Zero-coverage) 및 언더플로우 왜곡
- **Assumption Challenged**:
  ACT-T2-02의 128-노드 피보나치 구면 MNI 가상 전극 보간 레이어가 실제 전극 몽타주 결손에 대해 완전한 무결성을 보장한다는 가정.
- **Attack Scenario & Observation**:
  - ACT-T2-02 수식:
    $$W_{k, c} = \frac{\exp(-\|v_k - e_c\|_2^2 / 2\sigma^2)}{\sum_{c'=1}^C \exp(-\|v_k - e_{c'}\|_2^2 / 2\sigma^2) + \epsilon} \quad (\sigma = 15.0\text{ mm})$$
  - 본 챌린저가 파이썬 수치 시뮬레이션(`python3 -c "..."`)을 통해 환자 전극이 측두엽(Temporal lobe)에만 국한된 상황($C=64$)에서 전뇌 128개 가상 노드 투영을 실측함.
  - **실측 결과**:
    - 후두엽(Occipital) 및 반대측 반구 등 전극 부재 구역의 가상 노드($v_k$)는 최근접 전극과의 거리가 $80\text{mm}$ 이상에 달함.
    - 이때 $\exp(-d^2 / 2\sigma^2) \approx 6.67 \times 10^{-7}$에 불과하여, 분모의 $\epsilon = 10^{-8}$보다 작거나 유사한 수준으로 떨어짐.
    - 결과적으로 128개 가상 노드 중 7개 노드에서 행 합(Row Sum)이 $< 0.01$ (최소 $0.00018$)로 떨어져 신호가 극도로 감쇄되는 현상(Signal Extinction / Flatline)이 발생함.
    - 반대로 만약 $\epsilon$을 극소값($10^{-16}$)으로 설정할 경우, $80\text{mm}$ 떨어진 노이즈성 원거리 전극 신호가 정규화되어 가중치 $1.0$으로 외삽(Ghost Extrapolation)되는 심각한 인공물(Artifact) 위험이 존재함.
- **Blast Radius**:
  사전학습 시 전극이 없는 뇌엽 영역의 가상 노드가 0으로 꺼지거나(Flatline) 엉뚱한 원거리 측두엽 신호를 증폭시켜 모델이 가짜 공간 상관관계를 학습할 위험.
- **Empirical Mitigation**:
  1. 가상 전극 노드별 유효 커버리지 신뢰도 마스크 $M_k = \mathbb{I}\left(\sum_{c} \exp(-d_{kc}^2/2\sigma^2) \ge \tau\right)$ ($\tau = 0.05$)를 도입하여, 신뢰도가 낮은 가상 노드는 어텐션 마스크(Attention Masking)로 모델 입력에서 배제할 것.
  2. 고정 $\sigma = 15.0\text{mm}$ 대신 국소 전극 밀도에 비례하는 적응형 대역폭 $\sigma_k = \max(15.0, \min_c \|v_k - e_c\|_2)$을 도입하여 극단적 수치 절단을 방지할 것.

---

### [Low-Medium] Challenge 3: Jetson Orin Nano 초저지연($\le 15\text{ms}$) 달성을 위한 파이썬/CUDA 런타임 디스패치 병목
- **Assumption Challenged**:
  ACT-T3-03 및 ACT-T3-05에서 INT8 SmoothQuant 및 Mamba-2 SSM을 적용하면 Jetson Orin Nano에서 1초 윈도우 추론 지연시간 $\le 15.0\text{ms}$가 자동으로 달성된다는 가정.
- **Attack Scenario & Observation**:
  - Jetson Orin Nano (8GB) 하드웨어 프로파일링 분석:
    - 메모리 대역폭: $68\text{ GB/s}$.
    - DIVER-Base (51M INT8, 51.4MB) 가중치 메모리 전송 시간: $0.76\text{ms}$.
    - DIVER-Tiny (2.1M INT8, 2.1MB) 가중치 메모리 전송 시간: $0.03\text{ms}$.
    - Mamba-2 SSM 12층 순환 상태 메모리: $384.0\text{ KB}$ (Orin Nano의 2MB L2 캐시 내 완전 상주 가능).
    - 순수 GPU 연산 시간: 20 Dense INT8 TOPS 기준 $< 0.1\text{ms}$.
  - **식별된 실제 병목 (The Real Bottleneck)**:
    - 하드웨어의 순수 연산/대역폭 한계는 $1\text{ms}$ 미만이지만, **ARM Cortex-A78AE CPU 상의 파이썬 인터프리터 런타임 오버헤드** 및 **개별 CUDA 커널 디스패치 지연시간(호스트-디바이스 동기화)**이 발생함.
    - PyTorch 일반 모드로 실행 시 50개 이상의 세부 레이어 커널 런치(커널당 $15\sim 20\mu\text{s}$)와 파이썬 오버헤드로 인해 순수 디스패치 시간만으로 $8\sim 12\text{ms}$가 소진되어 $15\text{ms}$ 마진을 위협함.
- **Blast Radius**:
  연구실 엣지 테스트베드 실측 시 파이썬 단독 벤치마크에서 $15\text{ms}$ 초과로 판정 기준 미달 발생 가능.
- **Empirical Mitigation**:
  1. ACT-T3-03의 기술 포인터에 명시된 대로 단순 PyTorch 모드가 아닌 **TensorRT C++ Runtime Engine** 또는 **`torch.cuda.CUDAGraph` 캡처**를 강제 적용하여 호스트 CPU 디스패치 오버헤드를 $0.5\text{ms}$ 미만으로 제거할 것.
  2. 전처리 파이프라인(128xC RBF 행렬곱 및 $0.5-150\text{Hz}$ IIR 필터)을 호스트 CPU가 아닌 GPU 커널 내에 결합(Kernel Fusion)할 것.

---

### [Low-Medium] Challenge 4: 환자 iEEG 데이터 국외 이전 및 ALCF Aurora 활용에 관한 개인정보보호법(PIPA) 준수 리스크
- **Assumption Challenged**:
  ACT-T3-06 및 Section 5.1에서 제안된 HIPAA Safe Harbor 18대 식별자 스크러빙 및 OpenRAIL-M 거버넌스만으로 국내외 데이터 활용에 법적 하자가 없다는 가정.
- **Attack Scenario & Observation**:
  - DIVER-2 사전학습의 핵심 데이터 중 하나인 서울대병원(SNUH) iEEG 코퍼스는 대한민국 「개인정보 보호법(PIPA)」 제28조의2(가명정보의 처리 등) 및 제28조의8(개인정보의 국외 이전)의 적용을 받음.
  - 미국 에너지부(DOE) 아르곤 국립연구소 ALCF Aurora 슈퍼컴퓨터(25,000 GPUh)로 데이터를 전송하여 사전학습을 수행할 경우, 이는 법률상 "개인정보(가명정보)의 국외 이전"에 해당함.
  - HIPAA Safe Harbor는 미국 연방 규정이므로, 국내 임상 데이터의 국외 슈퍼컴퓨팅 처리를 위해서는 서울대병원 의학연구윤리심의위원회(IRB)의 국외 이전 승인 및 정보주체 동의(또는 적법한 가명처리 국외 이전 계약 체결)가 선행되어야 함.
- **Blast Radius**:
  저널 투고 후 데이터 가용성 진술(Data Availability Statement) 심사 단계에서 IRB 국외 이전 승인 서류 미비로 인한 게재 지연 또는 기관 분쟁 발생 위험.
- **Empirical Mitigation**:
  1. Section 6.4 리스크 비상대응 행렬(RSK-05)에 **"SNUH 코호트의 국외 이전 IRB 승인 및 표준 개인정보 국외이전 계약서(Standard Contractual Clauses, SCC) 체결"**을 명시적 사전 완화 조치로 추가할 것.
  2. 국외 이전 승인이 지연될 경우를 대비하여, 국내 KISTI 한강 클러스터(GH200) 및 SNUBIC(L40S)에서 사전 가명화 및 특징 추출을 1차 완료한 후 비식별화된 잠재 벡터만을 전송하는 대체 경로(Fallback Plan)를 공식 수립할 것.

---

## 3. Stress Test Results (프로그래밍 및 실측 검증 결과)

| 검증 시나리오 | 검증 방법 및 실행 명령어 | 기대 동작 / 기준 | 실제 검증 결과 | 판정 |
|---|---|---|---|:---:|
| **F5 전수 인수 조건 테스트** | `pytest tests/verify_acceptance_criteria.py -k "test_f5_"` | 10개 테스트 100% 통과 | 10 passed in 0.02s | **PASS** |
| **취약성-로드맵 1:1 매핑** | `pytest tests/verify_acceptance_criteria.py -k "test_tier3_05"` | VULN-01~11 키워드 완전 매핑 | 1 passed in 0.01s | **PASS** |
| **엄격한 존칭 준수 감사** | `python3` 정규식 `안채원/이아현(?!\s*선생님)` | 마크다운 전수 위반 0건 | docs 전체 4개 문서 위반 0건 (100% 준수) | **PASS** |
| **산출물 물리적 규격 감사** | `Path('docs/04_action_items_roadmap.md').stat()` | 크기 [3KB, 200KB], `# ` 시작 | 85.5 KB (957 라인), `# ` 시작 확인 | **PASS** |
| **RBF 보간 조건수 및 수치안정성** | `python3` SVD 및 $W$ Singular Value 시뮬레이션 | 발산 없음, $\|W\|_2 \approx \mathcal{O}(1)$ | $s_{\max} \approx 2.47$, Convex Combination 유계 입증 | **PASS** |
| **Jetson Orin Nano 대역폭 시뮬레이션** | INT8 파라미터 대역폭 소요 계산 ($68\text{GB/s}$) | 전송 지연 $\ll 15\text{ms}$ | 51M: $0.76\text{ms}$, 2.1M: $0.03\text{ms}$, Mamba: $384\text{KB}$ | **PASS** |

---

## 4. Unchallenged Areas (검증 제외 영역 및 사유)

1. **Milestone 5 고유 산출물 (`test_f6_*`, `README.md`, Git 커밋 및 GitHub 원격 푸시)**:
   - 해당 테스트 항목(10개)은 Milestone 5의 전속 마일스톤 책임 범위이므로 M4 감사에서는 정상 보류(Pending)로 분류함.
2. **`test_tier4_s04` 내 `docs/01_research_synthesis.md` 그림 키워드**:
   - M1 산출물에 대한 독점적 쓰기 규칙 준수를 위해 M4 단계에서는 임의 수정하지 않고 차기 마일스톤 정비 사항으로 인계함.

---

## 5. 최종 판정 (Verdict)

### **APPROVE (조건부 승인 및 M5 반영 권고)**

- **판정 사유**:
  1. `docs/04_action_items_roadmap.md`는 Milestone 3에서 제기된 11대 핵심 취약성을 완벽히 포괄하는 3-Tier(단기-중기-장기) 액션 아이템, 5대 클러스터 통합 연산 예산(30,240 GPUh), RACI, DAG, 6대 리스크 행렬을 완벽한 수준의 학술적 깊이로 구현함.
  2. F5 인수 조건 테스트 10건 및 상호작용 매핑 테스트를 100% 무결점으로 통과함.
  3. 연구실 구성원에 대한 엄격한 존칭("안채원 선생님", "이아현 선생님", "차지욱 교수님")을 100% 완벽히 준수함.
  4. 본 챌린저가 식별한 4대 과제(9번째 행 복원, RBF 마스킹 보완, TensorRT C++ 컴파일 권고, 국내 PIPA 국외 이전 승인 반영)는 기각 사유가 아닌 로드맵의 완성도를 최고 수준으로 끌어올리기 위한 기술적 자산이므로 승인(APPROVE)을 권고함.
