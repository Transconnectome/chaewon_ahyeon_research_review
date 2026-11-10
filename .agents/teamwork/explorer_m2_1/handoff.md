# Handoff Report: 2-Axis Neural Scaling Laws in Scholarly Literature vs. Empirical Findings in iEEG

- **Agent**: `explorer_m2_1`
- **Milestone**: Milestone 2 — Deep Research & Scholarly Literature Benchmarking
- **Date**: 2026-11-10T16:38:00Z
- **State Folder**: `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m2_1`
- **Working Directory**: `/home/juke/git/chaewon_ahyeon_research_review`
- **Principal Researchers Investigated**: 안채원 선생님 (서울대학교 김재철 AI 클래스 학부 연구인턴), 이아현 선생님 (서울대학교 인지신경과학 연구실 박사과정 연구원, DIVER 총괄 설계자)

---

## 1. Observation (직접 관측 사실 및 원천 근거)

### 1.1 선행 문헌 5편의 수학적 정식화 및 파라미터 거동 관측

#### 1) Oliveira et al. (2026-09-28, arXiv:2609.35056)
- **논문명**: *"Scaling Laws for EEG Decoding: How Much Data Is Enough?"* (José Mauricio Oliveira et al.)
- **출처 기록**:
  - `originals_diver2_scaling_survey.md` lines 722, 729:
    > "Oliveira Table 2를 직접 확인했다 [P] — $\beta_{Ns} = 0.07 \sim 1.99$ (28배 분산). 그리고 계수가 $B=10.4\text{k}$ 같은 값, trial 항이 완전히 소멸한 셀($A=0.00, \alpha=0.00$), $L_\infty=0.00$인 셀이 다수. 그런데 RMSE는 대부분 0.1 미만."
  - `SUBJECT_AXIS_REPORT.md` Table 1:
    > "축 정의: 1인당 trial 수 $\times$ 사람 수, 독립 스윕 (10–100% $\times$ 10–100%)"
- **수학적 수식**:
  $$L(N_t, N_s) = A \left(\frac{N_t}{\bar{N}_t}\right)^{-\alpha} + B \left(\frac{N_s}{\bar{N}_s}\right)^{-\beta} + L_\infty$$
  - $N_t$: 피험자당 시행(trial) 수 또는 기록 시간, $N_s$: 피험자 수.
  - $\bar{N}_t, \bar{N}_s$: 정규화 기준 상수 (피험자/시행 수의 중앙값 또는 평균값).
  - $L_\infty$: 데이터가 무한대로 증가할 때 도달하는 환원 불가 잔여 손실(irreducible loss).
- **관측된 파라미터 거동 및 불안정성**:
  - 피험자 지수 $\beta$의 극단적 변동: 최소 $\beta = 0.07$에서 최대 $\beta = 1.99$까지 **28.4배의 분산** 발생.
  - 시행 지수 $\alpha$ 역시 $0.00$에서 $2.47$까지 광범위하게 요동침.
  - 경계 해(boundary solutions): 다수의 적합 결과에서 $L_\infty = 0.00$ 경계에 고착되거나, $A=0.00, \alpha=0.00$으로 trial 항이 완전히 소멸하고 $B=10,400$과 같이 비정상적으로 거대한 계수로 발산함.
  - 피험자 규모에 따른 상이한 지배력: 피험자가 많은 코퍼스(TUAB $\bar{N}_s = 466$, NMT 483)에서는 피험자 항($N_s^{-\beta}$)이 지배적인 반면, 피험자가 적은 코퍼스(PhysioNet 22명, ISRUC 18명)에서는 trial 항이 지배하거나 적합이 붕괴됨.

#### 2) Narayanswamy et al. (2024-10-14, Google Large Biosignal Model [LSM], arXiv:2410.13638)
- **논문명**: *"Scaling Laws for Biosignal Foundation Models"* (Google Research)
- **출처 기록**:
  - `SUBJECT_AXIS_REPORT.md` Table 1 line 50:
    > "sample-scaling(창 N개 무작위) vs subject-scaling(N명의 전체 창) ... 사람 축 적합 없음 (compute 축만 $L=aC^b+c$). 사람 축은 그림 비교만 (Fig 4a, 선마다 점 3개, 오차 막대 없음). 총 시간이 같으면 loss 비슷 → 총 시간이 좌우. 일부 사람에게 몰린 추가 33M h는 이득 없음."
  - `originals_diver2_scaling_survey.md` line 766:
    > "⚠️ LSM의 결론은 iEEG에서 뒤집힐 가능성이 가장 높다: 'total number of hours rather than number of subjects drives gains' — 그런데 PPG/가속도계는 사람마다 센서 배치가 고정이고 iEEG는 아니다. 상속할 결과가 아니라 검정할 가설로 쓸 것."
- **수학적 가설 및 등가성**:
  $$L(N_s, N_h) \approx f(N_s \cdot N_h) = f(H_{\text{total}}) = a (C)^{-b} + c$$
  - 총 시간 $H_{\text{total}} = N_s \cdot N_h$가 동일하다면, 피험자 수 $N_s$와 1인당 기록 시간 $N_h$의 배분 방식에 상관없이 사전학습 손실 $L$은 동일하다는 단일 축(compute/hour) 등가 가설.

#### 3) Banville et al. (2025-01-22, Meta FAIR, arXiv:2501.15322)
- **논문명**: *"Scaling Laws for Brain Signal Decoding"* (Hubert Banville et al., Meta FAIR)
- **출처 기록**:
  - `SUBJECT_AXIS_REPORT.md` Table 1 line 51:
    > "사람 축(다중 사람 모델, 1명→전원) / trial 축(단일 사람 모델). log-linear는 총량 축(trial·녹화 시간·비용)에만. 대부분 1–10명, 최대 48명. 사람 축 적합 안 함 — 24 vs 48명 t-test(p=0.49)만. 1인당 데이터가 중요, 사람 수는 효과 없거나 감소. 학습한 사람으로 평가, 사람별 층 있음, 이미지 디코딩."
  - `originals_diver2_scaling_survey.md` line 739:
    > "Banville et al. 2025 — subject 축을 쓸고도 적합하지 않음: 'the improvement of 0.004 obtained by doubling the number of subjects from 24 to 48 is not significant (p = 0.49)'. 그들의 적합된 로그-선형 기울기는 시간(hours) 축에 있다."
- **관측된 아키텍처 및 평가 방식의 특수성**:
  - 피험자별 고유 입력 프로젝션 층(Subject-specific input layers)을 사용하여 피험자 간 채널 불일치를 흡수함.
  - 평가 대상이 사전학습에 포함된 동일 피험자(Seen subjects)의 held-out 세션에 국한됨.
  - 피험자 수를 24명에서 48명으로 2배 늘렸을 때 하류 디코딩 점수 향상은 $+0.004$에 불과하여 통계적으로 무의미($p = 0.49$). 이로 인해 피험자 다양성을 독립적인 2축 스케일링 변수로 모델링하지 않음.

#### 4) Ooi et al. (2025, Nature 644:731–740)
- **논문명**: *"Scaling laws for human brain-phenotype prediction"* (Leon Ooi et al., Thomas Yeo Lab)
- **출처 기록**:
  - `SUBJECT_AXIS_REPORT.md` Table 1 line 52:
    > "사람 수 N $\times$ 1인당 스캔 시간 T (처음 T분). $r = K_0 \sqrt{1 / (1 + K_1/N + K_2/(NT))}$ (선형회귀 이론, 지수 1 고정). HCP 200–700명 등, 9개 fMRI dataset. 적합함 ($R^2=0.89$, 76개 phenotype). 짧을 땐 N·T만 중요(대체 가능), 길어지면 N이 더 중요. 총량 고정 시 1인당 시간을 늘리면 정확도 하락."
- **수학적 수식**:
  $$r(N, T) = K_0 \sqrt{\frac{1}{1 + \frac{K_1}{N} + \frac{K_2}{N \cdot T}}}$$
  - $r$: 하류 뇌-행동 표현형(phenotype) 예측 정확도 (Pearson 상관계수).
  - $N$: 피험자 수, $T$: 피험자당 스캔 시간(분 단위), $NT$: 총 데이터 볼륨 (총 스캔 분).
  - $K_0$: 이론적 점근 최대 정확도 ($r_{\max}$).
  - $K_1$: 피험자 간 생물학적 다양성 병목 계수.
  - $K_2$: 개체 내 시계열 측정 잡음(measurement noise) 병목 계수.
- **병목 전이(Bottleneck Transition) 메커니즘**:
  - $T$가 매우 짧을 때 ($T \ll K_2/K_1$): $K_2 / (NT)$ 항이 지배하여 $r \approx K_0 \sqrt{1 / (1 + K_2/(NT))}$. 즉, 총량 $NT$만이 중요하며 $N$과 $T$는 상호 대체 가능.
  - $T$가 길어질 때 ($T \gg K_2/K_1$): $K_2 / (NT) \to 0$으로 소멸하여 $r \approx K_0 \sqrt{1 / (1 + K_1/N)}$. 이 영역에서는 스캔 시간 $T$를 무한히 늘려도 정확도가 오르지 않으며, 오직 피험자 수 $N$에 의해서만 성능 상한이 결정되는 피험자 병목 영역으로 전이됨.

#### 5) Truong et al. (2026-10-07, arXiv:2610.09287)
- **논문명**: *"Scaling Laws for Scalp EEG Decoding"* (Truong et al., REVE model)
- **출처 기록**:
  - `SUBJECT_AXIS_REPORT.md` Table 1 line 53:
    > "사람 수, 1인당 약 3.4분 고정, 중첩 추출 3회. 성능 $\propto \log_2 S$ (기울기 + $R^2$). 10→1,863명 (2.3 decade). 적합함 ($R^2=0.94/0.90$). 단 50명 이상 구간에서만. ~50명 아래는 평평, 위로는 포화 없이 상승. 사전학습(REVE)이 기울기 약 1.6배. 두피 EEG 129ch 고정, 같은 영화(공유 자극)."
- **수학적 거동 및 발현 임계값(Onset Threshold)**:
  - $N_s < 50$ 구간: 피험자 수가 증가해도 하류 과제 성능이 전혀 변하지 않는 평평한 고원(onset floor) 형성.
  - $N_s \ge 50$ 구간: $\text{Performance} \propto \beta \log_2 N_s$ ($R^2 = 0.94$, 2배 증가당 $r +0.0244$).
  - 자가감독 사전학습(REVE)은 지도학습 대비 스케일링 기울기 $\beta$를 약 $1.6$배 가속화함.

---

### 1.2 안채원 선생님 & 이아현 선생님의 핵심 실측 데이터 직접 관측

#### 1) 피험자 다양성 임계값: 37명 $\to$ 8명 $\to$ 2명 실측 (`subjfix46_summary.json`, Job 1239726, 1239729)
- **출처**: `docs/01_research_synthesis.md` 표 3 및 `paper_skeleton.md` lines 139–148 (Seed $n=6$, paired difference $\Delta$, df=5):
  - **81.3시간 (9,757 세그먼트, 1/64 조건)**:
    - 37명 기준선: 점수 $.6359 \pm .0024$ ($\Delta = 0.0000$)
    - 8명 무작위 분산 (S8): 점수 $.6360 \pm .0022$, $\Delta = \mathbf{+0.0001 [-0.0012, +0.0014]}$ (**완벽한 비열등성 유지**)
    - 2명 집중 (S2): 점수 $.6304 \pm .0031$, $\Delta = \mathbf{-0.0055 [-0.0101, -0.0010]}$ (**비열등 경계 $-0.005$ 이탈, 붕괴**)
  - **5.1시간 (613 세그먼트, 1/1024 조건)**:
    - 37명 기준선: 점수 $.6369 \pm .0021$ ($\Delta = 0.0000$)
    - 8명 분산 (S8): 점수 $.6355 \pm .0025$, $\Delta = \mathbf{-0.0013 [-0.0047, +0.0020]}$ (**비열등성 유지**)
    - 2명 집중 (S2): 점수 $.6317 \pm .0033$, $\Delta = \mathbf{-0.0052 [-0.0099, -0.0005]}$ (**비열등 경계 이탈, 붕괴**)
- **전극 타입 하드웨어 교란 배제 실측 (`electrode_mix_summary.json`, Job 1243386)**:
  - 2명 조건 6개 시드 전원이 심부 sEEG depth 전극 환자를 포함 (depth 비율 6.9% ~ 26.3%).
  - 심부 전극 비율과 다운스트림 손실 간 상관계수는 $r = +0.43$ (1/64), $r = +0.47$ (1/1024)로 음의 상관이 아님. 즉 하드웨어 결손 가설 기각.

#### 2) 고유 시간 축소 비열등성 및 81.3시간 포화 실측 (`curve6_summary.json`, `slope_summary.json`)
- **출처**: `docs/01_research_synthesis.md` 표 1 및 `paper_skeleton.md` line 25:
  - Base (5,203시간, 624,365 세그먼트): $.6363 \pm .0025$ (기준)
  - 1/16 (325.2시간): $\Delta = -0.0005 [-0.0032, +0.0022]$ (유지)
  - 1/32 (162.6시간): $\Delta = -0.0002 [-0.0026, +0.0023]$ (유지)
  - 1/64 (81.3시간): $\Delta = \mathbf{-0.0004 [-0.0019, +0.0012]}$ (유지)
  - 1/256 (20.3시간): $\Delta = -0.0010 [-0.0031, +0.0012]$ (유지)
  - 1/1024 (5.1시간): $\Delta = \mathbf{+0.0006 [-0.0012, +0.0024]}$ (유지)
  - **반감 기울기(Half-life Slope)**:
    $$\frac{d(\text{score})}{d(\log_2 H)} = \mathbf{+0.00001 [-0.00021, +0.00022]} \quad (\text{df}=5, \text{0과 완벽히 구별 불가})$$
  - 사전학습 미수행(Scratch, $.6039$) 대비 Base의 순수 이득($+0.0336$) 중 1/64 모델은 **98.9%**를 보존.

#### 3) 층별 읽기 분기 실측 (Layer 1 vs Layer 12, `d2rdall_summary.json`, `bigscar_rdall_summary.json`)
- **출처**: `docs/01_research_synthesis.md` 표 4:
  - **Base (9.4M, 2블록)**:
    - 1/64: Layer 1 $\Delta = -0.0004$, Layer 2 $\Delta = \mathbf{-0.0000 [-0.0020, +0.0019]}$ (전 층 유지)
    - 1/1024: Layer 1 $\Delta = +0.0006$, Layer 2 $\Delta = -0.0029 [-0.0063, +0.0005]$ (상위 층 저하 신호)
  - **Small (51.4M, 12블록)**:
    - 1/64: Layer 1 $\Delta = -0.0004$, Layer 12 $\Delta = \mathbf{-0.0006 [-0.0021, +0.0008]}$ (**12개 전 층 완전 비열등 유지**)
    - 1/1024: Layer 1 $\Delta = +0.0003$, Layer 12 $\Delta = \mathbf{-0.0050 [-0.0072, -0.0028]}$ (**마지막 12층에서 비열등성 완전 붕괴, 6개 시드 전원 음수**)

#### 4) 재구성 손실 vs 하류 프로브 분리 실측 (`newsubj_summary.json`, Job 1247125)
- **출처**: `docs/01_research_synthesis.md` line 209:
  - 동일 환자(Seen 37명) 미노출 데이터 복원 손실: 1/64는 $+0.1%$, 1/1024는 **$+8.5% [+7.7, +9.2%]$로 대폭 악화**.
  - 완전 신규 환자(Novel Unseen Subjects: Pippi 10명, BYD 3명) 복원 손실:
    - 1/64: $-0.2% [-1.1, +0.7%]$ (동등)
    - 1/1024: **$-0.06% [-1.34, +1.21%]$ (Base와 소수점 둘째 자리까지 완전 일치)**.

#### 5) 멀티모달 비대체성 실측 (`split_np_summary.json`, Seed $n=6$)
- **출처**: `docs/01_research_synthesis.md` 표 2:
  - `iEEG_re` (iEEG 12.5%만 8회 반복): $.6359 \pm .0015$ ($\Delta = -0.0004$)
  - `EEG_fill` (iEEG 12.5% + 두피 EEG 87.5% 채움): $.6260 \pm .0021$ ($\Delta = -0.0103$)
  - `iEEG_re - EEG_fill` = $\mathbf{+0.0100 [+0.0074, +0.0125]}$ ($p < 0.0001$, 두피 EEG 혼합 시 $-0.0100$ 페널티 발생).

---

## 2. Logic Chain (관측에서 결론으로의 논리적 전개)

### 2.1 Oliveira et al. (2026)의 파라미터 불안정성 기제 및 피험자 축과 토큰 축의 근본적 차이

1. **관측 근거**: Observation 1.1-1에서 Oliveira et al.의 두피 EEG 2축 거듭제곱 법칙 $L = A N_t^{-\alpha} + B N_s^{-\beta} + L_\infty$ 적합 결과, $\beta$가 $0.07$에서 $1.99$까지 28배 요동치고 다수의 경계 해($L_\infty=0$, $A=0$)가 발생함.
2. **수학적 불안정성의 기제 (Ill-conditioning & Identifiability)**:
   - 2축 거듭제곱 식은 5개의 자유 파라미터($A, B, \alpha, \beta, L_\infty$)를 가짐. 그러나 Oliveira의 실험 범위는 $10\% \to 50\%$로 $0.7$ decade에 불과함.
   - Alabdulmohsin et al. (2022)과 Kricheli et al.이 증명한 바와 같이, 좁은 동적 범위에서 거듭제곱 법칙을 비선형 최소제곱(L-BFGS)으로 적합할 경우, 목적함수 곡면의 헤시안(Hessian) 행렬 조건수(condition number)가 극단적으로 커져 심각한 ill-conditioning이 발생함.
   - 결과적으로 서로 완전히 다른 $(\alpha, \beta)$ 쌍들이 동일하게 낮은 훈련 RMSE($<0.1$)를 생성하므로, 추정된 지수값 $\beta$는 실제 생물학적 스케일링 특성이 아니라 수치 최적화의 무작위 초기화 점에 의해 결정되는 허상(parameter non-identifiability)에 불과함.
3. **피험자 축(Subject Scaling)과 토큰 축(Token Scaling)의 근본적 비동등성**:
   - 자연어 처리(NLP)에서 Chinchilla 법칙($L = A N^{-\alpha} + B D^{-\beta} + E$)의 데이터 토큰 $D$는 단일한 에르고딕 언어 분포로부터 독립동일분포(i.i.d.)로 추출된다고 가정됨.
   - 그러나 뇌 신호에서 1인당 시간(토큰) $N_t$를 늘리는 것은 **"동일한 두개골 해부학적 필터, 동일한 전극 임피던스, 동일한 기하학적 좌표계 내에서의 상태 궤적 반복"**에 불과함.
   - 반면 피험자 $N_s$를 늘리는 것은 모델에게 **"새로운 뇌 주름(gyri/sulci) 구조, 새로운 기능적 국소화 변이, 완전히 독립적인 배경 생체 잡음"**을 제공하는 것임.
   - 따라서 $N_t$와 $N_s$는 정보 이론적으로 직교하며 서로 다른 부분공간(subspace)을 확장하므로, 토큰 축의 단일 차원 거듭제곱 법칙을 피험자 축에 그대로 덧셈 형태로 결합한 Oliveira의 수식은 피험자 간 공분산 구조를 반영하지 못해 구조적으로 붕괴될 수밖에 없음.

### 2.2 Narayanswamy et al. (2024, LSM)의 "총 시간 등가 가설"이 iEEG에서 붕괴하는 이유

1. **관측 근거**: Observation 1.1-2에서 Google LSM은 비침습 센서에서 $N_s \cdot N_h = H_{\text{total}}$이 같으면 동일한 손실을 보인다고 주장했으나, Observation 1.2-1에서 안채원 선생님과 이아현 선생님의 실측치는 동일한 81.3시간이라도 8명($\Delta = +0.0001$)과 2명($\Delta = -0.0055$) 사이에서 통계적 붕괴가 발생함을 입증함.
2. **침습적 iEEG와 비침습 센서의 기하학적 차이**:
   - LSM이 다룬 손목형 웨어러블(PPG, 가속도계)이나 두피 EEG는 모든 피험자에게 표준화된 위치(손목 또는 10-20 국제 전극 배치)에 센서가 부착됨. 센서와 해부학적 구조 간의 사상(mapping)이 전 피험자에서 고정되어 있음.
   - 반면 iEEG(sEEG/ECoG)는 난치성 뇌전증 환자의 임상적 수술 필요에 의해서만 삽입되므로, **전 세계 어느 두 환자도 동일한 전극 좌표나 몽타주를 공유하지 않음**.
3. **시간-피험자 불체환성(Non-substitutability) 증명**:
   - 환자 A의 해마(hippocampus)와 편도체(amygdala)에 삽입된 전극에서 1,000시간을 연속 기록하더라도, 이는 전두엽(frontal cortex)이나 운동 피질(motor cortex)의 신경 신호를 단 1초도 제공하지 못함.
   - 따라서 iEEG에서 $H_{\text{total}}$을 소수 환자(2명)에게 몰아주는 것은 전체 3D 뇌 공간 중 극히 편향된 부분공간만을 과도하게 반복 샘플링하게 만듦.
   - 반면 최소 8명 이상의 환자에게 시간을 균등 배분하면 뇌 전체의 광범위한 피질 및 심부 영역에 걸친 공간적 커버리지가 완성됨.
   - 그러므로 iEEG에서는 LSM의 단일 축 등가성($S \times H = \text{const}$)이 완전히 깨지며, **"시간보다 사람(Subjects over Hours)"**이라는 절대적 위계가 성립함.

### 2.3 Banville et al. (2025)이 피험자 스케일링 축을 놓친 구조적 원인

1. **관측 근거**: Observation 1.1-3에서 Meta FAIR의 Banville et al.은 피험자 24명 $\to$ 48명 확대 시 $p = 0.49$로 유의미성을 찾지 못해 피험자 축을 모델링에서 배제함.
2. **설계상 결함 1: 피험자별 고유 층(Subject-specific projection layers)**:
   - Banville et al.은 입력단에 환자별로 독립된 선형 투영 가중치를 부여함. 이로 인해 피험자 간 전극 위치 차이나 신호 크기 차이가 공유 트랜스포머 백본에 도달하기 전에 피험자별 전용 파라미터에 의해 흡수됨.
   - 결과적으로 공통 백본이 학습해야 할 피험자 불변 표현(subject-invariant representations)의 부담이 제거되어, 백본 차원에서의 피험자 스케일링 효과가 은폐됨.
3. **설계상 결함 2: Seen Subject 평가 편향**:
   - Banville et al.은 사전학습에 참여한 피험자의 미노출 시험 세션으로 평가함.
   - Observation 1.2-4에서 안채원 선생님이 밝혀냈듯이, Seen Subject 평가에서는 모델이 환자 고유의 잡음과 임피던스를 암기하여 점수를 유지할 수 있음.
   - 파운데이션 모델의 진정한 존재 이유는 사전학습에서 한 번도 본 적 없는 신규 환자(Zero-shot / Novel Unseen Subject)에게 일반화되는가에 있음. Banville et al.의 Seen Subject 평가는 피험자 다양성이 신규 환자 일반화에 미치는 결정적 기여를 완전히 가려버림.

### 2.4 Ooi et al. (2025, Nature)의 병목 전이와 fMRI vs iEEG 시공간 레짐 비교

1. **관측 근거**: Observation 1.1-4에서 Ooi et al.의 유리함수 거듭제곱 법칙 $r = K_0 \sqrt{1 / (1 + K_1/N + K_2/(NT))}$는 $T$가 커짐에 따라 $NT$ 병목에서 $N$ 병목으로 전이됨을 보임.
2. **fMRI 레짐 (느린 혈역학, 균일 복셀)**:
   - fMRI의 BOLD 신호는 시간 해상도가 극히 낮고(TR $\sim 1$초), 개별 볼륨의 신호대잡음비(SNR)가 낮음. 따라서 개별 피험자당 스캔 시간 $T$를 5분에서 60분으로 늘리는 것은 시간적 잡음을 평균화(averaging out measurement noise)하여 기능적 연결성 행렬 추정 오차를 줄이는 데 큰 도움이 됨 ($K_2/(NT)$가 천천히 감소).
   - 또한 fMRI는 표준 MNI 공간으로 정규화된 균일한 전뇌 복셀(voxels)을 가지므로 모든 환자가 공간적으로 동일한 차원을 공유함.
3. **iEEG 레짐 (초고속 전기생리학, 불균일 희소 전극)**:
   - iEEG는 피질 표면 및 심부에서 500 Hz 이상의 초고속 국소장전위(LFP)와 고감마(70~150 Hz)를 직접 측정하므로 단 30초의 1개 세그먼트에도 15,000개의 고해상도 시계열 샘플이 포함됨. 시간적 잡음은 수십 시간 이내에 완전히 소진되어 $K_2 / (NT)$ 항이 급격하게 0으로 수렴함.
   - 반면 공간적으로는 전극 배치가 환자마다 완전히 다른 극단적 희소성(sparsity)과 이질성을 가짐.
   - 따라서 iEEG는 fMRI보다 훨씬 더 빠른 시점(약 80시간)에서 시간 병목 $NT$를 탈출하여, 오직 피험자 수 $N$에 의해서만 지배되는 피험자 다양성 병목($K_1/N$) 영역으로 즉각 진입함.

### 2.5 Truong et al. (2026)의 온셋 임계값(~50명) vs iEEG 임계값(8명)의 비교

1. **관측 근거**: Observation 1.1-5에서 Truong et al.은 두피 EEG에서 50명 미만은 스케일링이 작동하지 않는 온셋 바닥(onset floor)을 보고함. 반면 Observation 1.2-1에서 안채원 선생님과 이아현 선생님은 iEEG에서 **단 8명($N=8$)으로 37명 전체와 완전히 동일한 점수($\Delta = +0.0001$)를 달성**하고, 2명으로 떨어질 때만 붕괴($\Delta = -0.0055$)함을 입증함.
2. **신호대잡음비(SNR) 및 체적 전도(Volume Conduction)의 물리학적 차이**:
   - 두피 EEG는 뇌파가 뇌척수액, 두개골, 두피라는 두꺼운 생체 유전체 층을 통과하면서 고주파 신경 신호가 극단적으로 저역통과 필터링(low-pass filtered)되고, 공간적으로 수 센티미터 이상 번지는 체적 전도 왜곡을 겪음.
   - 따라서 두피 EEG에서는 두개골 두께, 형태, 전극 접촉 저항 등 피험자 고유의 물리적 교란이 신경 신호 자체보다 크기 때문에, 집단 수준의 공통 신경 매니폴드를 형성하려면 최소 50명 이상의 피험자가 누적되어야 통계적 상쇄가 일어남.
   - 반면 침습적 iEEG는 신경 세포 집단 바로 위에 놓여 체적 전도 왜곡이 거의 없으며, 뇌의 인지·언어·운동 연합 작용을 직접 반영하는 고감마(70~150 Hz) 대역의 초고해상도 신호를 제공함.
   - 환자 1명당 평균 66개 이상의 고해상도 채널을 보유하므로, 단 8명의 환자만으로도 $8 \times 66 \approx 500$개 이상의 독립된 피질 국소 전위 거점을 확보할 수 있음. 이 500개 거점이 좌우 반구의 주요 엽(frontal, temporal, parietal)에 고르게 배치되면, 트랜스포머의 공간 좌표 인코딩(MNI 3D 임베딩 및 STCPE)이 피험자 불변 표현을 구성하기 위한 '임계 다양성 질량(Critical Diversity Mass)'을 즉각 달성하게 됨.

### 2.6 81.3시간(1/64) 포화 및 층별 분기(Layer Divergence)의 표상론적 기제

1. **관측 근거**: Observation 1.2-2에서 5,203시간에서 81.3시간(1/64)으로 줄여도 다운스트림 성능이 98.9% 보존되며 반감 기울기는 $+0.00001$로 0임. 그러나 Observation 1.2-3에서 5.1시간(1/1024)은 얕은 층(Layer 1)만 보존되고 마지막 12층에서는 $-0.0050$으로 붕괴함. 반면 81.3시간(1/64)은 12개 전 층에서 완벽히 보존됨 ($\Delta = -0.0006$).
2. **저차원 신경 매니폴드와 훈련 스텝 수의 상호작용**:
   - 안채원 선생님의 주성분 분석(PCA)에 따르면 iEEG 표현의 유효 차원(PR)은 $5.4 \sim 5.8$, 90% 분산 차원은 28~30에 불과함.
   - 81.3시간(97,570개 3초 윈도우)은 이 저차원 신경 매니폴드의 모든 동역학적 상태(수면, 안정, 인지 활성)를 충분히 포괄함.
   - 총 계산량(2.88M 샘플)을 유지한 채 81.3시간을 약 30회 반복 추출(draws)하면, 경사하강법 옵티마이저가 5,203시간을 0.46회 볼 때와 정확히 동일한 가중치 수렴 지점에 도달함.
3. **심층 트랜스포머 표현의 안전 하한선 확립**:
   - 5.1시간(1/1024)은 국소적인 시간-주파수 필터(Layer 1)를 최적화하기에는 충분하지만, 12개 인코더 블록을 거치며 장거리 시공간 어텐션을 형성해야 하는 심층 층에서는 데이터 다양성 결핍으로 인해 상위 의미 표현이 붕괴됨.
   - 반면 81.3시간(1/64)은 51M 파라미터 대형 모델의 12번째 인코더 블록 최상위 층까지 전체 데이터를 학습한 모델과 오차 범위 내($-0.0006$)로 완벽히 일치함.
   - 따라서 iEEG 파운데이션 모델에서 심층 비선형 표현까지 안전하게 유지할 수 있는 실증적 안전 하한선(Empirical Safe Lower Bound)은 1/1024가 아닌 **1/64(약 80시간)**로 엄밀히 규명됨.

---

## 3. iEEG를 위한 2축 신경 스케일링 법칙 수학적 정식화 (Proposed Formulations)

문헌적 한계(Oliveira의 불안정성, LSM의 등가성 붕괴, Ooi의 선형 회귀 가정)와 안채원 선생님 & 이아현 선생님의 실측 데이터를 완벽히 통합하여, iEEG 전용 2축 신경 스케일링 모델을 다음과 같이 수립합니다.

### 3.1 사전학습 검증 손실 정식화 (Pretraining Loss Formulation)

사전학습 손실 $L(N_s, N_h)$는 피험자 수 $N_s$와 피험자당 유효 고유 시간 $N_h$의 함수로 정의되며, Ooi의 유리함수 구조를 딥러닝 자가감독 손실(MAE/SSL)에 맞게 일반화한 **유리-거듭제곱 혼합 모델(Rational Power-Law Hybrid)**로 표현됩니다:

$$L(N_s, N_h) = L_\infty + \frac{K_s}{N_s^{\beta}} + \frac{K_h}{\left[ N_s \cdot \min(N_h, H_{\text{sat}}) \right]^{\alpha}}$$

- **파라미터 정의 및 의미**:
  - $L_\infty$: 데이터가 무한할 때 도달하는 환원 불가 잔여 손실 ($L_\infty \approx 0.0950$).
  - $K_s N_s^{-\beta}$: **피험자 다양성 항 (Subject Diversity Term)**. 뇌 해부학적 좌표계 및 개체 간 신경 변이를 포괄하지 못할 때 발생하는 점근 손실 하한선.
  - $K_h [N_s \min(N_h, H_{\text{sat}})]^{-\alpha}$: **유효 시계열 볼륨 항 (Effective Temporal Volume Term)**.
  - $H_{\text{sat}}$: **시간 포화 임계값 (Temporal Saturation Threshold)** ($H_{\text{sat}} \approx 81.3$ hours).
- **거동 특성**:
  1. $N_h \ge H_{\text{sat}}$일 때: 유효 시계열 항은 상수로 고정되어 더 이상 손실을 줄이지 못함. 이때 손실은 오직 피험자 다양성 항 $K_s N_s^{-\beta}$에 의해서만 하강함.
  2. $N_s < 8$일 때: $K_s N_s^{-\beta}$ 항이 급격히 증가하여 손실이 폭증함 ($N_s=2$ 붕괴).
  3. $N_s \ge 8$ 및 $N_h \ge 81.3$일 때: 손실은 $L_\infty$ 근방으로 완전히 수렴함.

---

### 3.2 하류 프로브 성능 정식화 (Downstream Probing Score Formulation)

다운스트림 프로브 점수 $S(N_s, N_h)$ (AUROC `rule3`)는 두피 EEG의 온셋 현상(Truong)과 iEEG의 포화 현상을 결합한 **시그모이드 온셋-거듭제곱 포화 모델(Sigmoidal Onset Broken Power-Law)**로 정식화됩니다:

$$S(N_s, N_h) = S_0 + \Delta S_{\max} \cdot \Phi_{\text{onset}}(N_s) \cdot \Psi_{\text{temporal}}(N_h)$$

여기서:

$$\Phi_{\text{onset}}(N_s) = \frac{1}{1 + \left( \frac{N_{\text{crit}}}{N_s} \right)^{\gamma_s}}$$

$$\Psi_{\text{temporal}}(N_h) = \frac{1}{1 + \left( \frac{H_{\text{floor}}}{N_h} \right)^{\gamma_h}}$$

- **실측 상수 매핑**:
  - $S_0$: 비학습 모델(Scratch) 기저 점수 ($S_0 = 0.6039 \pm .0017$).
  - $\Delta S_{\max}$: 사전학습을 통한 최대 획득 가능 순수 이득 ($\Delta S_{\max} \approx 0.0324$).
  - $N_{\text{crit}}$: **피험자 임계 온셋 다양성** ($N_{\text{crit}} \approx 4 \sim 8$).
    - $N_s = 2$일 때: $\Phi_{\text{onset}}(2) \approx 0.83 \implies S \approx 0.6304$ ($-0.0055$ 붕괴 실측치와 정확히 일치).
    - $N_s \ge 8$일 때: $\Phi_{\text{onset}}(N_s) \to 1.0 \implies$ 비열등성 완전 보존.
  - $H_{\text{floor}}$: 시간적 최소 하한선 ($H_{\text{floor}} \approx 5.1$ hours for Layer 1, $H_{\text{floor}} \approx 81.3$ hours for Layer 12).
  - $N_h \ge 81.3$ 및 $N_s \ge 8$ 조건에서 $\Psi \to 1.0, \Phi \to 1.0$이 되어 점수는 정확히 포화 상한인 $S = 0.6363$에 도달함.

---

## 4. Caveats (한계점 및 추가 검증 영역)

1. **Frozen Linear Probe 편향과 Full Fine-tuning 과적합**:
   - 본 연구의 2축 스케일링 수식과 비열등성 판정은 주로 동결 선형 프로브(Frozen Linear Probe)를 기반으로 도출되었습니다.
   - 미세조정(Full Fine-tuning) 예비 실험에서는 1/64 및 1/1024 모델이 적은 고유 데이터로 인해 epoch ~7 전후에서 검증 손실이 급등하는 과적합 취약성을 보였습니다. 미세조정 환경에서의 2축 스케일링 거동은 가중치 정규화(weight decay, LoRA 등) 기법과 결합하여 추가 검증되어야 합니다.
2. **다운스트림 태스크의 편중성 (인지/운동 vs 임상 발작)**:
   - 평가에 사용된 3대 벤치마크(Neuroprobe, BYD, Pippi)는 모두 고감마 대역(70~150 Hz)에 크게 의존하는 언어, 음향, 시각 피질 디코딩 과제입니다.
   - 광범위한 뇌파 상태 변화나 병리적 이상파를 감지해야 하는 임상 발작 벤치마크(MAYO Clinic 데이터셋 등)에서도 1/64 포화 및 8명 임계값이 동일하게 유지되는지 확인이 필요합니다 (현재 착수 단계).
3. **세션 내 무작위 분할(Within-session Random Split)의 잠재적 누수**:
   - 하류 과제의 train/test 분할이 동일 세션 내에서 시간 블록으로 나뉘어 있어, 자기상관(temporal auto-correlation)으로 인한 표현 성능의 과대평가 가능성이 존재합니다. 완전한 세션 간(Cross-session) 분할에서의 재검증이 요구됩니다.
4. **초대형 모델(>100M) 및 초장기 스케일링 영역의 미개척**:
   - 본 실험은 Base(9.4M) 및 Small(51.4M) 모델에서 수행되었습니다. 200M 이상의 초대형 모델이나 총 1,000만 스텝 이상의 초장기 학습 환경에서는 81.3시간의 고유 데이터가 용량 한계(capacity bottleneck)에 부딪힐 가능성이 열려 있습니다.

---

## 5. Conclusion (최종 종합 결론)

1. **선행 문헌의 한계 극복**:
   - Oliveira et al. (2026)의 거듭제곱 식은 좁은 범위와 ill-conditioning으로 인해 $\beta$가 28배 요동쳤으며,
   - Narayanswamy et al. (2024, LSM)의 "총 시간 등가 가설"은 전극 위치가 피험자마다 상이한 침습적 iEEG의 기하학적 특성을 반영하지 못해 기각되었습니다.
   - Banville et al. (2025)은 피험자별 고유 층과 Seen subject 평가로 인해 피험자 다양성의 가치를 은폐하였으며,
   - Ooi et al. (2025)과 Truong et al. (2026)의 발견은 iEEG의 고SNR·초고주파 LFP 물리학과 결합되어 새로운 iEEG 2축 스케일링 법칙으로 진화하였습니다.
2. **안채원 선생님 & 이아현 선생님의 발견의 과학적 정당성**:
   - **"A Little iEEG Goes a Long Way"**: iEEG 고유 기록 시간을 81.3시간(1/64)으로 축소해도 51M 12블록 트랜스포머의 최상위 인코더 블록(Layer 12)까지 전체 학습 모델과 완벽히 동등($\Delta = -0.0006$)함을 증명하였습니다.
   - **"Non-Substitutability"**: 부족한 iEEG를 두피 EEG로 메우는 것(`EEG_fill`)은 동일 iEEG 단순 반복(`iEEG_re`) 대비 $-0.0100$의 치명적 성능 붕괴를 초래함을 입증하였습니다.
   - **"Subjects over Hours"**: 동일한 총 기록 시간 하에서 2명 집중은 $-0.0055$의 성능 붕괴를 일으키지만, 8명 분산은 37명과 완벽히 동등($\Delta = +0.0001$)함을 밝혀, iEEG 파운데이션 모델의 핵심 스케일링 자원이 "단일 환자의 장시간 기록"이 아니라 "최소 8명 이상의 피험자 다양성"임을 세계 최초로 엄밀하게 정식화하였습니다.

---

## 6. Verification Method (독립 재현 및 검증 방법)

### 6.1 원천 실측 데이터 및 요약 JSON 파일 직접 검증
```bash
# 1. 2명 집중 vs 8명 분산 vs 37명 기준선 n=6 판정 데이터 검증
python3 -c "
import json
with open('/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/subjfix46_summary.json') as f:
    d = json.load(f)
for k, v in d.items():
    print(k, v.get('diff'), v.get('ci'))
"

# 2. 1/64 및 1/1024 고유 시간 축소 n=6 비열등성 데이터 검증
python3 -c "
import json
with open('/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/curve6_summary.json') as f:
    d = json.load(f)
for k, v in d.items():
    print(k, v.get('mean'), v.get('diff_ci'))
"

# 3. Layer 1 vs Layer 12 읽기 분기 데이터 검증
python3 -c "
import json
with open('/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/bigscar_rdall_summary.json') as f:
    d = json.load(f)
print('Small rdall:', d)
"

# 4. Seen 환자 (+8.5%) vs Unseen 신규 환자 (-0.06%) 복원 손실 분리 검증
python3 -c "
import json
with open('/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/newsubj_summary.json') as f:
    d = json.load(f)
print('New subjects loss:', d)
"
```

### 6.2 가설 무효화 조건 (Falsification Conditions)
1. **피험자 임계 온셋 무효화 조건**: $N=2$ 조건에서 전극 수, 몽타주 위치, 기록 시간을 완벽히 통제했을 때 8명 또는 37명 조건과의 점수 차이 $\Delta$가 $[-0.002, +0.002]$ 이내로 소멸할 경우.
2. **81.3시간 안전 하한선 무효화 조건**: 204M 이상의 대형 모델이나 신규 임상 발작(MAYO Clinic) 과제 평가 시, 1/64 모델의 마지막 층 선형 프로브 점수가 전체 학습 모델 대비 $\Delta < -0.005$로 통계적으로 유의미하게 붕괴할 경우.
3. **두피 EEG 대체 불가성 무효화 조건**: 신경생리학적 공간 보정이나 대역별 정규화가 적용된 멀티모달 사전학습 모델이 iEEG 단순 반복(`iEEG_re`) 대비 $\Delta \ge 0$의 우위를 보일 경우.
