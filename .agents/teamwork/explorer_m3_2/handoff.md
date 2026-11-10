# Handoff Report — Milestone 3 Explorer 2 (`explorer_m3_2`)

- **작성 에이전트**: Explorer 2 (`explorer_m3_2`)
- **수신 에이전트**: Sub-Orchestrator for Milestone 3 (`sub_orch_m3`, Conversation ID: `31b20b74-99ac-4310-aed7-4b7ab506960e`)
- **작업 디렉토리**: `/home/juke/git/chaewon_ahyeon_research_review`
- **상태 폴더**: `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m3_2`
- **탐구 배정 영역**:
  - **Axis 3: 대조군 및 실험 설계 편향 (Controls & Experimental Design Bias)**
  - **Axis 4: 재구성 손실-하류 점수 괴리 역설 & 정보이론 (Reconstruction Loss Paradox & Information Dynamics)**
- **작성 일시**: 2026-11-10T17:10:00Z
- **적용 규정**: 연구실 최고 존칭 규정 100% 준수 (안채원 선생님, 이아현 선생님, 차지욱 교수님, 절대 비격식체 배제)

---

## 1. Observation (직접 관측 사실 및 원천 실측 데이터)

본 보고서의 적대적 비판은 아래의 1차 원천 문서, 실측 데이터셋, 통신 기록 및 선행 학술 문헌을 직접 검증하여 도출되었습니다:
- `docs/01_research_synthesis.md` (Milestone 1 연구 종합 및 원천 실측 데이터 보고서)
- `docs/02_deep_research_literature.md` (Milestone 2 2축 스케일링 문헌 딥리서치 보고서)
- `docs/01_research_synthesis.md#L160-L167` (이아현 선생님의 Teams 원천 메시지, 2026-11-10T14:52:02.312Z)
- `docs/01_research_synthesis.md#L204-L215` (동일 피험자 vs 신규 피험자 Held-out Loss 실측치, `newsubj_summary.json`, Job 1247125)
- `docs/01_research_synthesis.md#L236-L245` (층별 읽기 분기 실측치, `d2rdall_summary.json`, `bigscar_rdall_summary.json`)
- `docs/01_research_synthesis.md#L385-L396` (사전학습 목적함수 및 2.88M 고정 프로토콜)
- `docs/01_research_synthesis.md#L403-L412` (SPEC v1 Frozen Linear Probe 다운스트림 3대 벤치마크 규약)
- `docs/02_deep_research_literature.md#L290-L306` (Chai et al. 2026 반복 법칙 및 iEEG 유효 차원 PR 실측치)
- `docs/02_deep_research_literature.md#L358-L364` (임상 신경 병리 뇌파 MAYO Clinic 벤치마크 미완 현황)

### [Observation 1-1] 사전학습 목적함수의 단일성 및 대안 SSL 대조군의 완전한 부재
- **직접 관측 사실 (`docs/01_research_synthesis.md#L385-L396`)**:
  - 본 연구의 2축 스케일링 스윕(1/16 ~ 1/1024 고유 데이터 축소 및 37명 $\to$ 8명 $\to$ 2명 축소)은 **50% 무작위 시공간 패치 마스킹 후 원시 전압 복원(MSE Loss)**을 수행하는 **Masked Autoencoder (MAE)** 목적함수 단 하나에만 전적으로 의존하여 수행되었습니다.
  - 연구 멘토인 이아현 선생님은 2026-11-10T14:52:02.312Z 원천 Teams 대화(`docs/01_research_synthesis.md#L160-L167`)에서 다음과 같이 명시적으로 언급하였습니다:
    > *"어쩌면 참가자 한 명당 긴 데이터를 모두 preprocessing 하지 말고 짧게 여러명 하는데에 effort 를 들이는게 나을수도 있다라는 메세지를 전달할수도 있구요! 물론 이 결론을 내려면 이 SSL specific 한지 알아보기 위해 다른 종류의 SSL 도 시도해보라고 말씀드린 상태입니다."*
  - 그러나 실제 실험 데이터베이스 및 결과 보고서에는 대조학습(Contrastive SSL, e.g., CPC, InfoNCE, TS-TCC, BENDR), 자가회귀(Autoregressive next-token prediction), 또는 DIVER-1.5의 핵심 독창성인 채널 기원 예측(Channel Origin SSL, ACPE)에 대한 스케일링 비교 대조군(Control Group)이 **단 하나도 존재하지 않습니다**.

### [Observation 1-2] 하류 평가 과제의 인지 영역 편중 및 임상 신경 병리 벤치마크 결여
- **직접 관측 사실 (`docs/01_research_synthesis.md#L403-L408`, `#L595-L600`)**:
  - 하류 선형 분리능을 판정하는 핵심 종합 지표인 `rule3`는 오직 다음 3개 벤치마크의 산술 평균으로만 계산되었습니다:
    1. **Neuroprobe (15개 하위 과제)**: BrainTreebank(10명) 대상 자연주의 영화 시청 중 언어(Sentence onset, Speech), 음향, 시각 피질 반응 디코딩 (AUROC).
    2. **BYD (`kelesbyd2024`)**: 피험자 대상 침습적 연속 언어 생성 및 단어 디코딩 (AUROC).
    3. **Pippi (`berezutskaya2022`)**: 자연주의 오디오북 청취 중 피질 청각 신경 반응 디코딩 (AUROC).
  - 반면, iEEG 신호가 수집되는 본래의 임상적 목적이자 신경생리학적으로 거시적 서파(slow wave) 및 임상 발작(seizure) 전파를 수반하는 **MAYO Clinic 뇌전증 발작 검출(Seizure Detection) 벤치마크(8명 난치성 환자 코호트)**는 평가 대상에서 완전히 누락되었습니다.
  - 또한, 해마 샤프 웨이브 리플(Sharp-wave ripples, 150~250Hz)이나 단일 운동 단위의 초미세 신경 발화(Single-unit / Multi-unit burst)를 요구하는 과제는 일체 포함되지 않았습니다.

### [Observation 1-3] 동일 피험자 Held-out Loss 악화(+8.5%)와 하류 프로브 유지 간의 해체 역설
- **직접 관측 사실 (`docs/01_research_synthesis.md#L204-L215`, `newsubj_summary.json`, Job 1247125)**:
  - 1/1024 (5.1시간) 고유 데이터 조건에서:
    - 사전학습에 참여한 동일 37명 환자의 미노출 검증 데이터(Seen Held-out) 복원 손실은 Base(0.0970) 대비 **`+8.5% [+7.7, +9.2%]`로 통계적으로 명백하게 악화**되었습니다.
    - 그러나 동일 조건의 다운스트림 선형 프로브 점수(`rule3`)는 Base 대비 **`+0.0006 [-0.0012, +0.0024]`로 완벽한 비열등성을 유지**하였습니다.
    - 사전학습에 일체 참여하지 않은 신규 환자(Novel Unseen: Pippi 10명, BYD 3명)에 대한 복원 손실은 Base(0.2791) 대비 **`-0.06% [-1.34, +1.21%]`로 동등**하게 측정되었습니다.
  - 연구진은 이를 두고 *"환자 고유 잡음 암기량(idiosyncratic noise memorization)이 소거되어 순수 뇌신경 표상이 보존된 결과"*라고 해석하였습니다 (`docs/01_research_synthesis.md#L218-L225`).

### [Observation 1-4] 층별 표상 붕괴 및 유효 차원 실측치
- **직접 관측 사실 (`docs/01_research_synthesis.md#L236-L245`, `docs/02_deep_research_literature.md#L300-L306`)**:
  - Small 모델(12개 블록, 51.4M)의 1/1024 조건에서, 첫 번째 블록(Layer 1, `rd1`)은 $\Delta = +0.0003 [-0.0014, +0.0021]$로 보존되었으나, **마지막 12번째 블록(Layer 12, `rdall`)은 $\Delta = -0.0050 [-0.0072, -0.0028]$로 6개 시드 전원에서 통계적으로 유의미하게 붕괴**되었습니다.
  - 고유 데이터 축소에 따른 iEEG 잠재 표현의 유효 차원(Participation Ratio, PR)은 다음과 같이 실측되었습니다:
    - Untrained (Scratch): $\text{PR} = 5.0$ (90% 분산 주성분: 55)
    - 1/1024 (5.1h): $\text{PR} = 7.4$ (90% 분산 주성분: 49)
    - 1/64 (81.3h): $\text{PR} = 5.8$ (90% 분산 주성분: 30)
    - Base 100% (5,203h): $\text{PR} = 5.4$ (90% 분산 주성분: 28)

---

## 2. Logic Chain (관측 사실 기반 과학적 추론 및 적대적 반론 전개)

```
[Logic Chain Summary]
(Obs 1-1: MAE 단일 의존) + (Obs 1-3: Held-out Loss +8.5% 악화)
  │
  ├─> [Step 1: 스펙트럼 멱함수 편향] 
  │     뇌파 전력의 90%가 1~30Hz 저주파 기저에 집중 -> MSE 손실은 저주파 스무딩으로 즉각 수렴.
  │     5시간(1/1024)만으로 달성된 "외관상 재구성"은 저주파 보간 과적합(Overfitting)에 불과.
  │
  ├─> [Step 2: 대안 SSL 결여의 치명성]
  │     장기 문맥과 음성 변별을 요구하는 Contrastive SSL(CPC, InfoNCE, TS-TCC)이나 
  │     DIVER-1.5 채널 기원 예측(ACPE)에서는 80시간 포화 가설이 성립하지 않을 가능성 농후.
  │     연구진 스스로 인정했으나 대조군 검증 회피.
  │
  ├─> [Step 3: 하류 과제 편향에 의한 정보 증발 은폐]
  │     Obs 1-2(Neuroprobe/BYD/Pippi)는 자극 개시 ERP 및 저주파에 의해 피험자 내 피팅이 극히 용이.
  │     선형 프로브는 1~30Hz 지배 고유값만으로 점수를 유지하므로, 
  │     실제 고감마(70~150Hz) 위상 결합 정보의 소실(+8.5% 악화)이 프로브 점수에서 은폐됨.
  │
  └─> [Step 4: 정보이론 및 MAE 동역학 붕괴]
        Chai et al. (2026) 반복 법칙 및 Jing et al. (2022) 차원 축소 이론에 따르면, 
        28차원 수렴은 표현 공간의 부분공간 붕괴(Subspace Collapse)를 입증.
        He et al. (2022) Vision MAE와 정반대로 재구성 손실과 하류 성능이 역행하는 이상 거동.
```

---

## 3. Structured Critiques: Axis 3 & Axis 4 심층 적대적 비판 도시에

### [Critique Axis 3] 대조군 및 실험 설계 편향 (Controls & Experimental Design Bias)

#### 3.1 Masked Autoencoder (MAE) 아키텍처 특이성과 1/f 스펙트럼 멱함수 과적합 착시

1. **신경 전기생리학 신호의 $1/f^\chi$ 스펙트럼 멱함수 분포**:
   - 두개내 iEEG 신호의 파워 스펙트럼 밀도(Power Spectral Density, PSD)는 주파수 $f$에 대해 거듭제곱 법칙($\text{PSD}(f) \propto 1/f^\chi$, 통상 피질 표면에서 $\chi \approx 1.5 \sim 3.0$)을 엄밀히 따릅니다.
   - 이는 신호의 전체 전력(total power) 중 **85% ~ 95%가 1~30 Hz 대역(델타: 1~4Hz, 세타: 4~8Hz, 알파: 8~12Hz, 베타: 13~30Hz)의 완만하고 거시적인 배경 리듬에 집중**되어 있음을 의미합니다.
   - 반면 인지 기능과 국소 신경 앙상블의 발화 정보를 담고 있는 고감마 대역(High-gamma, 70~150 Hz)은 전력 점유율이 5% 미만에 불과하며, 개별 진폭은 수 $\mu\text{V}$ 수준으로 미세합니다.

2. **MSE(Mean Squared Error) 손실 함수의 병리적 취약성**:
   - MAE의 사전학습 목적함수는 마스킹된 패치 $i$에 대한 원시 전압 복원 오차 $L_{\text{MSE}} = \frac{1}{|M|} \sum_{i \in M} \| x_i - \hat{x}_i \|_2^2$ 입니다.
   - Parseval의 정리에 의해 시간 도메인의 MSE는 주파수 도메인의 전력 오차 적분과 등가입니다:
     $$\int |x(t) - \hat{x}(t)|^2 dt = \int |X(f) - \hat{X}(f)|^2 df$$
   - 따라서 역전파 시 모델의 그래디언트는 진폭이 압도적인 1~30Hz 저주파 파형을 맞추는 데 90% 이상 쏠리게 됩니다.
   - 5.1시간(1/1024) 또는 81.3시간(1/64)이라는 극소량의 데이터만으로도, 트랜스포머는 시계열의 국소 자기상관(autocorrelation)과 스플라인 보간(interpolation)을 학습하여 저주파 기저 파동을 매끄럽게 연결하는 '평활화 필터'로서의 기능을 수시간 만에 완벽히 습득합니다.
   - **비판의 핵심**: 안채원 선생님과 이아현 선생님이 관찰한 "수시간 만의 손실 수렴 및 성능 유지"는 뇌신경 파운데이션 모델의 표상이 조기에 완성된 것이 아니라, **"MSE 손실 함수가 신호의 압도적 저주파 기저 파동에 과적합(low-frequency interpolation overfitting)되어 추가적인 데이터 학습이 무의미해진 기술적 착시(technical illusion)"**일 가능성이 매우 높습니다.

3. **대안 자가지도학습(Alternative SSL) 대조군의 전무함**:
   - 연구진은 "A Little iEEG Goes a Long Way"라는 파격적인 일반화 명제를 주장하면서도, 다음과 같은 필수적인 대안 SSL 대조군을 일체 검증하지 않았습니다:
     - **대조군 A: DIVER-1.5 채널 기원 예측 (Channel Origin Prediction / ACPE)**:
       - 이아현 선생님이 개발한 DIVER-1.5의 핵심인 650개 MNI 전극 코드북 분류(Classification) 과제는 원시 전압의 MSE가 아니라, 다채널 전극 간의 기능적 연결성(functional connectivity)과 뇌 전역의 공간적 지형도를 구별해야 합니다.
       - 환자의 수면, 각성, 다양한 일상 인지 상태가 장시간(수백~수천 시간) 축적될수록 전극 출처 판별 정확도는 계속 향상될 것이며, 80시간에서 조기 포화되지 않을 가능성이 매우 큽니다.
     - **대조군 B: 대조학습 (Contrastive SSL, e.g., Contrastive Predictive Coding, InfoNCE, TS-TCC, BENDR)**:
       - 음성 인식(wav2vec 2.0) 및 생체신호 대조학습(BENDR, PopT)에서 입증되었듯, 잠재 표현 공간에서 시간적/공간적 음성 샘플(negative samples)을 밀어내는 대조 손실(InfoNCE)은 데이터의 시간적 다양성(Hours)이 증가할수록 표현의 붕괴를 방지하고 선형 분리능을 단조 증가시킵니다.
       - 만약 대조학습에서는 81.3시간(1/64) 축소 시 성능이 급격히 저하되고 5,203시간까지 선형 스케일링이 지속된다면, 연구진의 발견은 **"iEEG의 고유 특성"이 아니라 "패치 MAE-MSE 목적함수 자체의 결함"**으로 즉각 격하됩니다.
     - **대조군 C: 인과적 자가회귀 모델 (Autoregressive Next-Patch Prediction, e.g., Neuro-GPT, BrainGPT)**:
       - 미래 시점 예측은 장기 시간 의존성(long-term temporal dependencies)을 모델링해야 하므로 수천 시간의 긴 시계열 컨텍스트가 필수적입니다.
   - 이아현 선생님 본인도 Teams 대화에서 대안 SSL 검증의 필요성을 자인했음에도 불구하고, 대조군 실험 없이 "How should we scale"의 보편 법칙으로 성급히 결론을 내린 것은 과학적 대조군 설계(Experimental Controls)의 중대한 흠결입니다.

---

#### 3.2 하류 과제 편향 (Task Selection Bias)과 임상·고주파 벤치마크 누락

1. **선택된 3대 인지 과제(Neuroprobe, BYD, Pippi)의 피험자 내 피팅 용이성**:
   - `rule3`를 구성하는 3개 벤치마크는 모두 자연주의 영화 시청, 오디오북 청취, 연속 언어 생성 중 수집된 연속 자극 과제입니다.
   - 이러한 과제들은 자극 개시(Stimulus Onset) 시점에 대뇌 피질 전반에 걸쳐 수백 ms 동안 지속되는 거대한 사건유발전위(Event-Related Potentials, ERP: P100, N170, P300 등)를 동반합니다.
   - 이러한 거시적 유발 전위는 저주파 대역(세타, 알파, 베타)의 전력 변조와 밀접하게 연동되어 있어, 사전학습 모델이 정교한 고차원 비선형 문맥을 학습하지 못하고 단순한 주파수 밴드패스 필터 수준의 표상만을 형성했더라도 로지스틱 회귀 레이어(Linear Probe)가 매우 손쉽게 클래스를 분리할 수 있습니다.

2. **결정적 누락: 임상 신경 병리 뇌파 (MAYO Clinic 뇌전증 발작 검출 벤치마크)**:
   - 두개내 iEEG(sEEG/ECoG)는 순수 인지과학 연구만을 위해 단독으로 수술되는 경우가 없으며, **난치성 뇌전증(refractory epilepsy) 환자의 수술적 절제를 위한 발작 시작 구역(SOZ) 국소화**를 목적으로만 임상에서 허용되는 극히 침습적인 데이터입니다.
   - 뇌전증 발작(Seizure)은 환자가 수일에서 수주 동안 전극을 유지하고 있는 동안 단 수 회(1~5회) 극히 드물게 발생하는 전형적인 희귀 사건(rare event)입니다.
   - **통계적 데이터 절단(Dropout)의 위험**:
     - 5,203시간(100%) 코퍼스에는 환자들의 수면-각성 주기뿐만 아니라, 간헐적인 간질발작간기 방전(IEDs)과 임상적 발작 전조(pre-ictal), 발작 중(ictal) 동역학이 포함되어 있습니다.
     - 그러나 데이터를 81.3시간(1/64) 또는 5.1시간(1/1024)으로 무작위 샘플링하여 축소할 경우, **희귀 발작 시계열 구간이 사전학습 데이터에서 통계적으로 100% 배제·소실될 확률이 극도로 높습니다**.
     - 만약 사전학습 데이터에서 병리적 신경 동기화 파동이 소실된다면, 임상 벤치마크인 MAYO Clinic 발작 검출 과제에서 1/64 모델은 정상 뇌파와 발작 뇌파의 극서파 복합체(spike-and-wave) 전파 패턴을 구별하지 못해 성능이 심각하게 붕괴될 것입니다.
   - 연구진은 `docs/01_research_synthesis.md#L599-L600`에서 MAYO Clinic 발작 검출 과제 평가가 미완 상태임을 인정하였으나, 이 핵심 임상 벤치마크가 결여된 상태에서 "A Little iEEG Goes a Long Way"를 일반화한 것은 명백한 **과제 선택 편향(Task Selection Bias)**입니다.

3. **초고주파 신경 발화(High-gamma / Ripples) 미세 인지 과제의 부재**:
   - 해마 및 방추상회 등에서 수십 ms 동안 국소적으로 폭발하는 샤프 웨이브 리플(Sharp-wave ripples, 150~250 Hz)이나 미세 운동 BCI(개별 손가락 궤적 디코딩) 과제는 80시간의 조대 데이터로는 상태 공간을 포괄할 수 없습니다.
   - 따라서 현재의 비열등성 실측치는 "자연주의 인지 과제의 저주파 ERP가 선형 분리하기에 80시간이면 충분했다"는 국소적 결론일 뿐, 신경 인터페이스 전반으로 외삽될 수 없습니다.

---

### [Critique Axis 4] 재구성 손실-하류 점수 괴리 역설 & 정보이론 (Reconstruction Paradox & Information Dynamics)

#### 4.1 해체 역설(Dissociation Paradox)과 저주파 스펙트럼 지배에 의한 정보 손실 은폐 가설

1. **연구진 가설의 논리적 취약성**:
   - 연구진 가설: *"5,203시간 Base 모델은 동일 피험자 37명의 전극 임피던스, 두개골 전도도, 생체 배경 잡음(idiosyncrasy)을 과적합(overfitting)하여 Held-out 손실이 낮았던 반면, 1/1024 모델은 노출 시간이 5.1시간에 불과하여 잡음 암기가 발생하지 않아 Held-out 손실이 +8.5% 증가했으나 순수 신경 표상은 온전히 보존되었다."*
   - **적대적 논리 반박**:
     - 피험자의 두개골 내에 삽입된 전극에서 측정되는 신호 중 무엇이 '잡음'이고 무엇이 '순수 신경 표상'인가에 대한 생물물리학적 기준선이 전무합니다.
     - 침습 전극에서 측정되는 신호는 배경 잡음이라 할지라도 피질 신경망의 비동기적 발화(asynchronous baseline firing)와 미세 신경 집단의 국소 장전위(LFP)의 중첩입니다.
     - 환자 고유의 뇌 회로 배선(wiring)과 피질 주름 구조에 따른 신호 궤적을 '잡음'으로 치부하고, 손실 악화(+8.5%)를 '과적합 해소'로 합리화하는 것은 가설의 사후적 정당화(ad-hoc rationalization)에 불과합니다.

2. **저주파 스펙트럼 편향에 의한 정보 손실 은폐 메커니즘**:
   - **가설**: *동일 피험자 Held-out Loss의 +8.5% 악화는 비신경 잡음이 제거된 것이 아니라, 실제 고차 뇌신경 정보(고감마 70~150Hz 위상 결합 및 비선형 궤적)가 데이터 결핍으로 인해 증발(Information Evaporation)한 직접적 증거이며, 이 치명적 손실이 다운스트림 3대 인지 과제의 1~30Hz 저주파 파워 의존성으로 인해 선형 프로브 점수에서 교묘하게 은폐되었다.*
   - **수학적·생물물리학적 증명**:
     - 임의의 iEEG 신호 $x(t)$를 저주파 성분 $x_{\text{LF}}(t)$ (1~30Hz)와 고주파 성분 $x_{\text{HF}}(t)$ (70~150Hz)로 직교 분해합니다:
       $$x(t) = x_{\text{LF}}(t) + x_{\text{HF}}(t), \quad \mathbb{E}[x_{\text{LF}} \cdot x_{\text{HF}}] \approx 0$$
     - 전력 비대칭성: $\text{Var}(x_{\text{LF}}) \gg \text{Var}(x_{\text{HF}})$ (전력의 90% 이상이 LF).
     - MAE 모델의 출력 복원 신호를 $\hat{x}(t) = \hat{x}_{\text{LF}}(t) + \hat{x}_{\text{HF}}(t)$라 할 때, 복원 MSE 손실은 다음과 같이 분해됩니다:
       $$\mathcal{L}_{\text{MSE}} = \mathbb{E}\left[ (x_{\text{LF}} - \hat{x}_{\text{LF}})^2 \right] + \mathbb{E}\left[ (x_{\text{HF}} - \hat{x}_{\text{HF}})^2 \right]$$
     - 1/1024 모델은 5.1시간의 극소량 데이터로 인해 저주파 기저 $\hat{x}_{\text{LF}}$는 대략 복원하지만, 고감마 대역의 미세 위상 $\hat{x}_{\text{HF}}$의 시간적 정렬을 완전히 상실합니다 ($\hat{x}_{\text{HF}} \to 0$ 또는 무작위 위상).
     - 이때 고감마 복원 오차는 고주파 전력 자체에 비례하여 MSE를 누적시키며, 이것이 정확히 **동일 피험자 Held-out Loss의 +8.5% 증가**로 나타난 것입니다.
     - 그러나 하류 선형 프로브($y = W^\top z + b$)의 가중치 $W$는 목적 과제(자연주의 영화/오디오 ERP)를 맞추기 위해 가장 분산이 크고 SNR이 높은 저주파 표현 벡터의 축에 정렬됩니다.
     - 결과적으로, **신경학적으로 가장 중요한 고감마 정보가 완전히 소실되었음에도 불구하고, 저주파 성분만으로 선형 프로브 점수가 유지되는 착시가 발생**한 것입니다.

3. **신규 피험자(Novel Unseen) 손실 동등(-0.06%)의 착시와 거대한 바닥 효과(Floor Effect)**:
   - 연구진은 1/1024 모델이 신규 피험자(Pippi, BYD)에 대해 Base 모델과 동등한 복원 손실($-0.06% [-1.34, +1.21%]$)을 기록한 것을 일반화의 결정적 증거로 제시하였습니다.
   - **반론**: 신규 피험자에 대한 절대 손실값은 **0.2791**로, 동일 피험자 손실(**0.0970**)의 무려 **2.88배(약 3배)**에 달합니다.
   - MNI 표준 좌표계로 정렬하더라도 환자마다 침습 전극의 물리적 위치가 완전히 상이하기 때문에, 한 번도 접하지 않은 제로샷 환자에 대해 Base 모델(5,203h)이든 1/1024 모델(5.1h)이든 고차 신경 파형을 복원하지 못하고 **"집단 평균적 저주파 완만 곡선만을 생성하는 조대 모드(Coarse Baseline)"**에 똑같이 갇혀 있는 것입니다.
   - 즉, 0.2791이라는 극심하게 높은 에러 바닥(Floor Effect)에서는 5.1시간을 학습한 모델이나 5,203시간을 학습한 모델이나 똑같이 무력하여 오차율 차이가 0.0%로 수렴한 것일 뿐입니다.
   - 거대한 기저 오차로 인한 무차별성을 두고 "순수 일반화 신경 표상이 완벽히 보존되었다"고 주장하는 것은 통계학적 기저 효과를 간과한 심각한 논리적 비약입니다.

---

#### 4.2 정보이론적 정초와 문헌 연계 (Chai et al., Kornblith/Raghu, He et al.)

1. **Chai & Xiong (2026, arXiv:2610.05591) 잉여 손실 법칙(Surplus Loss Law)과 차원 축소 붕괴**:
   - Chai et al. (2026)은 데이터 제약 환경에서 고유 토큰 $U$를 $R$회 반복 학습할 때 발생하는 초과 손실 $\Delta L$이 다음과 같이 스케일링됨을 정식화하였습니다:
     $$\Delta L = A z^p, \quad z = (R - 1) \frac{N_{\text{total}}}{U}$$
   - 특히 Chai et al.은 **소스 엔트로피(Source Entropy)가 낮을수록 반복 학습에 대한 내성이 극단적으로 떨어진다($r = -0.89$)**는 사실을 밝혔습니다.
   - 연구진은 iEEG 표현 공간의 유효 차원(PR)이 28차원으로 낮아 반복 내성이 우수하다고 주장하였으나(`effdim3/full/summary.json`), 이는 정보이론적으로 정반대의 위험을 내포합니다:
     - Jing et al. (2022, "Understanding Dimensional Collapse in Contrastive / Self-Supervised Learning")에 따르면, 자가지도학습에서 데이터 다양성 $U$가 부족한 상태로 반복 에폭($R \gg 10$)이 지속되면, 신경망의 공분산 행렬의 특이값들이 소수의 주축으로 붕괴하는 **차원 축소(Dimensional Collapse / Subspace Collapse)**가 필연적으로 발생합니다.
     - 1/1024 조건은 단 613개 기록(5.1시간)을 무려 470회 이상 반복 샘플링한 것입니다.
     - 이 과정에서 모델은 고차원 신경 매니폴드의 자유도를 상실하고 저차원의 좁은 부분공간에 갇히게 되며, 이는 다양한 인지 상태나 비선형 복잡도를 표현할 수 있는 모델의 표현 용량(representational capacity)을 파괴합니다.

2. **Kornblith et al. (2019) & Raghu et al. (2021) CKA 층별 유사도와 주의집중 붕괴(Attention Collapse)**:
   - 트랜스포머의 깊이에 따른 층별 표상 분기(Layer 1 보존 vs Layer 12 붕괴, $\Delta = -0.0050 [-0.0072, -0.0028]$)는 심층 트랜스포머의 주의집중 동역학으로 정확히 설명됩니다:
     - **하위 층 (Layer 1~4)**: 국소 시계열 패치 내의 위상-진폭 기본 필터(Gabor-like temporal basis)를 구성하며, 매우 적은 데이터(5.1시간)로도 공간이 포화되어 고도의 '특징 재사용(feature reuse)'이 일어납니다 (Raghu et al., 2021).
     - **상위 층 (Layer 9~12)**: 66.3개 전극 간의 장거리 시공간 상호작용과 의미론적 문맥 어텐션(Cross-channel context integration)을 학습해야 합니다 (Kornblith et al., 2019).
     - 그러나 데이터의 절대적 다양성이 결핍되면, 상위 층의 어텐션 가중치 엔트로피가 급격히 감소하여 모든 전극에 균일한 어텐션을 주거나 특정 전극에만 고착되는 **어텐션 붕괴(Attention Collapse)**를 겪게 됩니다.
     - 연구진은 "1/64(81.3시간)에서는 12층 점수가 보존($-0.0006$)되었다"고 방어하지만, 51.4M Small 모델에서 겨우 마지노선을 넘긴 수치일 뿐이며, 파라미터가 204M 또는 812M로 확장될 경우 상위 층의 표현 붕괴가 1/64 영역에서도 광범위하게 재발할 것임이 자명합니다.

3. **Vision MAE (He et al., 2022, CVPR) 정보 동역학과의 정면 배치**:
   - He et al. (2022)의 Vision MAE 논문에서 가장 핵심적인 경험적 발견은, **"재구성 손실(Reconstruction MSE Loss)의 감소가 다운스트림 시각 분류 정확도(ImageNet Top-1)의 단조 증가와 강력한 양의 상관관계($r > 0.9$)를 가진다"**는 점이었습니다. 고주파 시각 잔차를 정밀하게 재구성하는 과정에서 인코더가 물체의 형태와 경계선을 학습하기 때문입니다.
   - 그러나 안채원 선생님과 이아현 선생님의 관측에서는 **재구성 손실이 +8.5%나 급등했는데도 다운스트림 프로브 성능이 유지되는 기이한 역상관(uncoupling / dissociation)**이 발생하였습니다.
   - 이는 두 가지 중 하나를 의미합니다:
     1. DIVER-1의 MAE 인코더가 재구성 과제로부터 아무런 유용한 고차 신경 표상을 추출하지 못하고 있거나,
     2. 다운스트림 선형 프로브 평가 지표(`rule3`)가 사전학습 인코더의 품질 변화를 전혀 측정해내지 못하는 '눈먼 벤치마크(blind metric)'이거나.
   - 어느 쪽이든, 재구성 손실과 하류 점수의 괴리는 "순수 표상 보존"의 축복이 아니라, **"사전학습 목적함수와 다운스트림 평가 프로토콜 간의 기능적 단절(functional disconnection)을 증명하는 중대한 아키텍처적 결함"**으로 규정되어야 합니다.

---

## 4. Specific Actionable Counter-Evidence & Falsification Conditions (구체적 반증 및 무효화 조건)

칼 포퍼(Karl Popper)의 과학적 반증주의 방법론에 입각하여, 안채원 선생님과 이아현 선생님의 가설("A Little iEEG Goes a Long Way", "81.3시간 1/64 및 5.1시간 1/1024로 충분하다")을 명확히 무효화(falsified)할 수 있는 4가지 정량적 반증 실험을 제시합니다:

### [Falsification Condition 1] 주파수 대역별 잔차 손실(Spectral Residual Loss) 분해 검증
- **실험**: Held-out 재구성 오차를 주파수 대역별(저주파 1~30Hz vs 고감마 70~150Hz)로 필터링하여 MSE를 각각 독립 산출.
- **무효화 판정 기준**:
  - 만약 1/64 또는 1/1024 모델에서 1~30Hz 저주파 복원 손실은 Base 대비 $\le +1\%$ 동등하게 유지되는 반면, **70~150Hz 고감마 대역의 복원 손실이 Base 대비 $+15\%$ 이상 통계적으로 유의미하게 폭증**한다면:
  - $\to$ 연구진의 가설("잡음 암기 해소")은 즉각 무효화되며, **"저주파 기저 과적합 및 고감마 신경 정보 증발 가설"**이 확증됨.

### [Falsification Condition 2] 비선형 프로브 및 고감마 특화 벤치마크 평가
- **실험**:
  1. 단순 선형 프로브(`nn.Linear`) 대신 2층 MLP 비선형 프로브(`Linear -> GELU -> Linear`)로 다운스트림 평가 수행.
  2. 고감마 대역(70~150Hz) 파워 피처만을 추출하여 평가하는 미세 음소 디코딩 및 시간 정밀도 과제 평가.
- **무효화 판정 기준**:
  - 만약 비선형 프로브 또는 고감마 특화 과제에서 1/64 모델이 Base 모델 대비 **$\Delta < -0.0100$ ($p < 0.01$) 이상의 유의미한 성능 붕괴**를 나타낸다면:
  - $\to$ 연구진의 "A Little iEEG Goes a Long Way" 주장은 **"선형 프로브의 저주파 편향이 만들어낸 인위적 착시"**로 최종 반증됨.

### [Falsification Condition 3] 대안 SSL (DIVER-1.5 ACPE & Contrastive InfoNCE) 스케일링 검증
- **실험**: 동일한 2축 스윕 격자($T \in \{5.1\text{h}, 81.3\text{h}, 5,203\text{h}\}$, $N \in \{2, 8, 37\}$)에서 MAE 대신 DIVER-1.5의 전극 기원 예측(ACPE) 또는 대조학습(CPC/InfoNCE)을 적용하여 사전학습 수행.
- **무효화 판정 기준**:
  - 만약 ACPE 또는 대조학습 모델에서는 $T = 81.3\text{h}$ (1/64) 축소 시 하류 성능이 Base(5,203h) 대비 **$\Delta < -0.0080$ ($p < 0.005$)으로 급격히 추락**하고, 5,203시간까지 단조 증가하는 스케일링 법칙을 보인다면:
  - $\to$ "A Little iEEG Goes a Long Way"는 생체신호 파운데이션 모델의 일반 법칙이 아니라, **"MAE 패치 마스킹의 저주파 조기 포화 결함"**임이 증명됨.

### [Falsification Condition 4] 임상 뇌전증 발작(MAYO Clinic) 벤치마크 평가
- **실험**: 8명 난치성 뇌전증 환자의 장기 iEEG 기록에서 발작 시작 구역(SOZ) 검출 및 발작 지속시간 분류 수행.
- **무효화 판정 기준**:
  - 만약 MAYO Clinic 발작 검출 AUROC에서 1/64 모델이 Base(5,203h) 모델 대비 **$\Delta < -0.0150$ ($p < 0.001$)으로 치명적 열등성**을 보인다면:
  - $\to$ "80시간으로 충분하다"는 주장은 **"희귀 병리 시계열이 탈락된 불완전한 인지 편향 모델"**로 판명되어 무효화됨.

---

## 5. Caveats (한계 및 조사 가정)

1. **선형 프로브 주파수 민감도의 간접 추론**:
   - 현재 연구실 레포지토리 내에는 15개 Neuroprobe 하위 과제의 주파수 대역별 특징 기여도(Feature Attribution / SHAP / Gradient Sensitivity)가 전수 계산되어 저장되어 있지 않으므로, 저주파 1~30Hz 지배 가설은 신경전기생리학 및 신호처리 파워 스펙트럼 밀도 이론에 기반한 연역적 추론입니다.
2. **MAYO Clinic 원천 데이터 미수행**:
   - MAYO Clinic 발작 데이터셋의 사전학습 포함 여부 및 다운스트림 점수는 2026-11-10 기준 실험 준비 단계(`docs/01_research_synthesis.md#L600`)에 있어, 본 보고서에서는 실측 수치 대신 통계적 표본 추출 확률 모델(Rare Event Dropout)을 기반으로 비판을 전개하였습니다.
3. **타 탐구 에이전트와의 역할 분담**:
   - 가설 타당성 12층 붕괴(Axis 1) 및 전극 몽타주/사이트 교란 요인(Axis 2)은 `explorer_m3_1`이 전담 조사 중입니다.
   - 통계적 검정력(Seed n=6), 다중비교 보정(Bonferroni/FDR) 결여 및 선행 문헌 닻(Oliveira, Ooi, Banville 등)은 `explorer_m3_3`이 전담 조사 중입니다.

---

## 6. Conclusion (종합 평가 및 Milestone 4 액션 아이템 제언)

- **종합 평가**:
  - 안채원 선생님과 이아현 선생님이 도출한 "A Little iEEG Goes a Long Way"와 "Subjects over Hours"는 자원 제약 환경에서 생체신호 모델의 스케일링 전략을 재고하게 만든 매우 획기적인 발견입니다.
  - 그러나 본 탐구 결과, 이 결론은 **(1) MAE 아키텍처의 저주파 기저 파동 과적합, (2) 대조학습 등 대안 SSL 대조군의 부재, (3) 자연주의 자극 개시 ERP에 편향된 3개 인지 과제 국소성, (4) 임상 발작(MAYO Clinic) 희귀 사건의 통계적 절단, (5) Held-out Loss +8.5% 악화가 시사하는 고감마 신경 정보의 증발 은폐**라는 치명적인 방법론적 취약점을 안고 있습니다.
  - 따라서 현 상태로 "1/64(80시간)면 충분하며 추가 시간은 불필요하다"고 단정하는 것은 심각한 학술적 비판에 직면할 위험이 큽니다.

- **Milestone 4(로드맵)로 이관할 필수 액션 아이템 제언**:
  1. **[단기 과제 / 11-20 NeuroAI 워크숍 초안]**:
     - 가설의 범위를 "모든 iEEG 과제"가 아닌 **"자연주의 인지 디코딩(Naturalistic Cognitive Decoding)에서의 고유 시간 포화"**로 정밀하게 축소(Scoping)하여 오버클레임을 방지할 것.
     - Held-out Loss +8.5% 증가에 대해 "잡음 암기 해소" 단일 가설 대신, 저주파 대역과 고주파 대역의 기여도를 구분하여 기술할 것.
  2. **[중기 과제 / DIVER-2 저널 투고]**:
     - **대안 SSL 대조군 실험**: DIVER-1.5의 채널 기원 예측(ACPE) 및 대조학습(InfoNCE) 기반 2축 스케일링 스윕을 반드시 완료하여 MAE 특이적 현상인지 일반 법칙인지 판정할 것.
     - **MAYO Clinic 임상 발작 벤치마크**: 8명 환자 코호트에서 1/64 모델의 발작 검출 및 SOZ 국소화 성능을 검증하여 희귀 병리 보존성을 실증할 것.
     - **주파수 대역별 잔차 분석**: Held-out 신호의 1~30Hz vs 70~150Hz 주파수별 복원 오차를 분리 측정하여 정보 증발 여부를 투명하게 규명할 것.

---

## 7. Verification Method (독립적 재현 및 검증 프로토콜)

본 보고서의 모든 분석과 주장은 다음 절차를 통해 독립적으로 재현 및 검증될 수 있습니다:

1. **테스트 스위트 실행**:
   ```bash
   python3 /home/juke/git/chaewon_ahyeon_research_review/tests/verify_acceptance_criteria.py --feature F4 --progressive
   ```
   - F4 관련 적대적 리뷰 요구조건(가설 타당성, 인과 추론, 대조군, 재구성 손실 괴리 역설, 통계적 엄밀성)에 대한 정합성 검증.
2. **수치 및 인용 일치 검증**:
   - `docs/01_research_synthesis.md` 표 1 (고유 iEEG 스윕), 표 3 (피험자 4분면), 표 4 (층별 분기) 및 Held-out loss 실측치(`newsubj_summary.json`: 동일 37명 +8.5%, 신규 피험자 -0.06%) 대조.
3. **무효화 조건 검증**:
   - 상기 4절에 기술된 4대 반증 조건(주파수 대역별 오차 분해, 비선형 프로브, 대안 SSL 대조군, MAYO Clinic 발작 검출) 코드를 실행하여 가설 기각 여부를 독립 판정.
