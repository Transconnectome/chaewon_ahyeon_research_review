# Handoff Report: 이아현 선생님 연구 포트폴리오, DIVER 진화, 임상 벤치마크 및 연구 시너지 심층 조사

- **작성 에이전트**: `explorer_m1_2` (Teamwork Explorer Archetype)
- **작성 일시**: 2026-11-10T16:15:00Z
- **조사 대상**: 이아현 선생님(Connectome Lab 박사과정 연구원)의 DIVER 연구 포트폴리오 전반 (DIVER-0, DIVER-1, DIVER-1.5, DIVER-2), 임상 평가 과제, 공공/사설 벤치마크, 핵심 아키텍처 메커니즘, 정량적 실험 수치, 및 안채원 선생님과의 공동 연구 시너지
- **작업 디렉토리**: `/home/juke/git/chaewon_ahyeon_research_review`
- **상태 폴더**: `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m1_2`

---

## 1. Observation (직접 관측 사실 및 원천 근거)

### 1.1 이아현 선생님의 연구자 프로필 및 리더십
- **소속 및 직책**: 서울대학교 인지신경과학 연구실(Connectome Lab, 지도교수: 차지욱 교수님) 박사과정 연구원. 김재철 AI 클래스 학부 연구인턴 안채원 선생님의 1:1 전담 연구 멘토 (GitHub: `yahyunee`, 이메일: `ahhyun724@snu.ac.kr`).
- **연구 주도 범위**:
  - DIVER(Deep Integration of Vast Electrophysiological Recordings at Scale) 시리즈의 총괄 설계자 및 스케일링/사전학습/다운스트림 파이프라인 주도자.
  - 미국 아르곤 국립연구소(ALCF) Aurora 슈퍼컴퓨터(Intel Max PVC GPU, 25,000 노드시간 할당) 및 NERSC Perlmutter, Polaris, KISTI 한강 클러스터 대규모 분산학습 인프라 운영.
  - 전산생체신호 분야 파라메트릭 스케일링 법칙(Scaling Laws) 문헌 메타분석 (94편, 489MB) 및 이론적 정립.

---

### 1.2 DIVER 아키텍처 진화 (DIVER-0 $\to$ DIVER-1 $\to$ DIVER-1.5 $\to$ DIVER-2)

#### [1] DIVER-0: 완전 채널 등변성 두피 EEG 파운데이션 모델
- **논문 원문**: *DIVER-0: A Fully Channel Equivariant EEG Foundation Model* (arXiv:2507.14141v1, 2025-06-13, ICML 2025 GenBio Workshop).
- **출처 파일**: `/home/juke/git/ephys-foundation-model-plan/docs/11_joint_papers.md#L7`
- **핵심 아키텍처 설계**:
  - 두피 EEG(surface EEG) 전극 몽타주가 환자/기기마다 상이한 문제(arbitrary channel permutations and variable channel counts)를 해결하기 위해 **완전 채널 순열 등변성(Channel Permutation Equivariance)** 구조 도입.
  - 시간 축에는 RoPE(Rotary Position Embedding)를 적용하고, 채널 축과 시간 축을 통합한 full channel-time attention 메커니즘 설계.
- **평가 벤치마크**: FACED (감정 분류 9클래스), PhysioNet-MI (운동 상상 4클래스).

#### [2] DIVER-1: 대규모 침습적 iEEG 파운데이션 모델
- **논문 원문**: *DIVER-1: Scaling Intracranial EEG Foundation Models for Transferable Representations* (arXiv:2512.19097v3; ICML 2026 Sub #30376 $\to$ NeurIPS 2026 v1~v4 $\to$ ICLR 2027 Sub #37162).
- **출처 파일**:
  - `/home/juke/git/ephys-foundation-model-plan/docs/neurips2026_eeg_fm_survey/six_axis_synthesis_matrix.md#L35-L37`
  - `/home/juke/git/ephys-foundation-model-plan/submissions/2026/20261010-yahyunee-diver2-scaling-survey/originals_diver2_scaling_survey.md#L330-L415`
  - `/home/juke/git/DIVER/CBraMod/DIVER/models/diver.py`
- **아키텍처 및 파라미터**:
  - **백본**: Salesforce Moirai 시계열 백본 기반의 임의 변량 시퀀스 평탄화(Any-variate Sequence Flattening, `[B, C*N, D]`).
  - **패치 토큰화**: 다중 패치 스케일 — `DIVER-1-0.1s` ($P=50$ samples = 0.1s at 500 Hz) 및 `DIVER-1-1.0s` ($P=500$ samples = 1.0s).
  - **위치 인코딩**: 시간 축 RoPE + 채널 간 1-bit `BinaryAttentionBias` (`torch.eq(query_id, kv_id)`로 동일 채널 여부만 1-bit 플래그 처리) + 3D 연속 전극 좌표(MNI 공간)는 오직 입력 토큰에 덧셈(`PositionalEncoding3D`) 방식으로만 주입.
  - **모델 스케일 (6종, 12레이어 고정)**:
    - w256: 13.03M
    - w512: 51.36M
    - w768: 115.00M
    - w1024: 203.95M
    - w2048: 812.85M
    - w3072: 1.83B
- **학습 코퍼스의 진화와 결함 극복**:
  - **초기 (ICML 2026 / NeurIPS 2026 v1~v2)**: 두피 EEG 54,000시간 + iEEG 5,300시간(총 59,300시간, 17,700명 이상, 1.6M channel-hours)의 혼합 사전학습. 두피 EEG를 500 Hz로 무리하게 업샘플링하여 토큰 길이만 팽창. 리버설 실험 결과 iEEG 단독 학습이 EEG 혼합 학습과 동등하거나 우월함(FACED 0.280 vs 0.266)이 밝혀져 다중 모달 전이 내러티브가 붕괴되어 리젝.
  - **개정 (ICLR 2027)**: 혼합된 두피 EEG를 전면 절제하고 **순수 침습적 iEEG 단독 코퍼스(5,310시간, 352,035 channel-hours, 37명 환자)**로 전면 재정의.

#### [3] DIVER-1.5: ACPE/STCPE 및 채널 출처 예측(Channel Origin Prediction)
- **출처 파일**:
  - `/home/juke/git/DIVER-2/diver_pretrain/config/diver15/btb64.yaml`
  - `/home/juke/git/DIVER-2/diver_pretrain/config/diver15/README.md`
  - `/home/juke/git/DIVER-2/diver_pretrain/config/diver15/runs.tsv` (262개 사전학습 런 및 89개 설정)
  - `/home/juke/git/DIVER-2/diver_pretrain/src/layers/Embed.py#L1274-L1360`
- **핵심 혁신 메커니즘**:
  - **모델 규격 (BTB-64)**: 8.55M 파라미터 (Linear Tokenizer 50 samples/0.1s $\to$ Time-wise STCPE $d=64$, 1 layer, 2 heads, 윈도우 크기 7 $\to$ 2 Moirai blocks $d=512$, 16 heads).
  - **채널 출처 예측 SSL (`aux_channel_identity`)**:
    - **마스킹 비율 `mask_ratio = 0.0`**: 입력 신호를 가리지 않고(No masking, No raw MSE reconstruction) 원형 그대로 유지.
    - **코드북 분류**: 사전학습 코퍼스 내 650개 전극 3D 좌표 코드북(`codebook_excl_subjects.npy`) 기반 총 2,534개 클래스(`out_dim: 2534`)에 대한 Cross-Entropy 분류 손실 적용.
    - **의의**: 환자 및 뇌 영역 고유의 신호 패턴을 식별하도록 강제함으로써, 신호 공간의 저주파 전압 드리프트나 안구 잡음에 오버피팅되지 않고 해부학적/피험자간 공통 표상을 학습.
  - **STCPE 고속화 최적화 (2026-09-23)**:
    - 기존 PyTorch `F.unfold` (`im2col`) 연산이 전체 추론 시간의 92%를 잠식하던 병목을 규명.
    - `Tensor.unfold` 뷰 기반의 zero-copy strided gather 연산으로 교체하여 비트 단위 동일성(bit-identical)을 유지하면서 연산 속도를 10배 이상 단축 (`diver_pretrain/src/layers/Embed.py#L1338-L1348`).

#### [4] DIVER-2: 2축 파라메트릭 스케일링 법칙 및 Nature 자매지 투고 프로젝트
- **출처 파일**:
  - `/home/juke/git/DIVER-2/docs/SCALING/README.md`
  - `/home/juke/git/DIVER-2/docs/SCALING/PLAN_SCALING_EXPERIMENT.md`
  - `/home/juke/git/DIVER-2/docs/SCALING/ScalingLawSearch.md`
  - `/home/juke/git/ephys-foundation-model-plan/decisions/2026-10-12-project-strategy.md`
- **연구 규모 및 목표**:
  - 1,000명 이상의 임상 피험자, >1,000,000 channel-hours iEEG 코퍼스 구축.
  - ALCF Aurora 슈퍼컴퓨터(25,000 노드시간) 및 KISTI 한강 클러스터(GH200) 활용.
  - 2026년 12월 말 Nature 자매지 투고 목표.
- **핵심 방법론 전환**:
  - **손실 함수 패러다임 전환**: 원시 신호 MSE 재구성 손실의 "안구 및 근전도 잡음 함정(Ocular & EMG artifact trap)"을 탈피하여 SPERA 스타일의 잠재 공간 예측 아키텍처(JEPA: Joint-Embedding Predictive Architecture with EMA teacher) 및 관계적 스펙트럼 정규화(RSReg: Relational Spectral Regularization) 도입 검토.
  - **공간 바이어스 전환**: 1-bit binary attention bias를 폐기하고, MNI 공간에서의 연속 측지선/유클리드 거리 감쇠 및 구면 르장드르 앵커 인코딩(Legendre Anchor Encoding, $M=32$)을 적용하여 전극 간 기하학적 연속성을 어텐션에 직접 주입.
  - **2축 스케일링 모델링**: 피험자 수($N$)와 1인당 시간($T$)을 직교 분리하는 2축 스케일링 함수($L = E + K_1 N^{-\beta} + K_2 (N \cdot T)^{-\gamma}$) 적합 및 외삽 검증.

---

### 1.3 임상 평가 과제 및 공공/사설 벤치마크

DIVER 연구 포트폴리오에서 이아현 선생님이 설계·구축·평가한 벤치마크 체계 (`DIVER/CBraMod/generalized_finetuning_utils/task_attribute_lookup.py` 전수 확인):

| 벤치마크 구분 | 데이터셋 / 과제명 | 모달리티 및 채널 구성 | 과제 유형 및 클래스/타겟 | 평가 척도 및 임상적 의의 |
|---|---|---|---|---|
| **임상 간질/발작** | **MAYO Clinic** | iEEG, 8명 환자 (16~72 채널) | 발작 검출 (2-class, 6초 윈도우) | AUC, 환자별 발작 조직 국소화 검증 |
| **임상 간질/발작** | **CHB-MIT** | 두피 EEG, 16 채널 | 소아 발작 검출 (2-class, 10초) | Balanced Acc, Sensitivity |
| **임상 발작 이벤트** | **TUEV (TUH Events)** | 두피 EEG, 16 채널 | 간질 발작파 분류 (6-class, 5초) | Balanced Acc, 극파/서파/발작 분류 |
| **임상 이상 뇌파** | **TUAB (TUH Abnormal)** | 두피 EEG, 16 채널 | 정상 vs 병리 이상 판정 (2-class, 10초) | Balanced Acc (SPERA-Base 0.8488 vs DIVER) |
| **임상 수면 의학** | **ISRUC-Sleep** | 두피 EEG, 6 채널 | 수면 5단계 (W, N1, N2, N3, REM, 30초) | Macro F1, Macrostructure (REM latency) |
| **임상 혼수 예후** | **I-CARE** | 두피 EEG 다채널 | 심정지 후 혼수 환자 72시간 예후 예측 | CPC 점수 (좋음 vs 나쁨, FPR 5% 이하 True Positive) |
| **자연주의 인지/언어** | **Neuroprobe** | iEEG (BrainTreebank 10명, 96~244ch) | 15개 하위과제 (영화 시청 시 언어·음향·시각 디코딩) | Frozen LP AUROC (Sentence onset 0.930, Speech 0.897) |
| **자연주의 청각 회귀** | **Podcast** | iEEG, 9명 환자 (72~235 채널) | 팟캐스트 청취 중 뇌신호 회귀 (50-dim, 1초) | Pearson $r$, MSE |
| **BCI 운동/언어** | **BYD (`kelesbyd2024`)** | iEEG, 3명 이상 (70~80 채널) | 침습적 언어/운동 디코딩 (speech task) | Frozen LP AUROC (실좌표 0.767 vs NaN 0.735) |
| **BCI 운동 상상** | **BCI Comp IV 2a** | 두피 EEG, 22 채널 | 4-class 운동 상상 (좌수, 우수, 발, 혀, 3초) | Balanced Acc (SPERA-Base 0.6816 vs EEGNet 0.4482) |
| **BCI 운동 상상** | **PhysioNet-MI** | 두피 EEG, 64 채널 | 4-class 운동 상상 (4초) | Balanced Acc (SPERA-Base 0.6726) |
| **임상 정서/우울** | **FACED / Mumtaz2016** | 두피 EEG (32ch / 19ch) | 정서 9클래스 / 주요우울장애(MDD) 2클래스 | Balanced Acc (FACED 0.5754, Mumtaz 0.9637) |

---

### 1.4 핵심 아키텍처 메커니즘 심층 분석

#### [1] 연속 패치(Continuous Patch) vs 이산 토큰(Discrete Token) 표상
- **연속 선형 패치 방식 (DIVER 계열)**:
  - 연속 전압 시계열을 $P$개 샘플(0.1초=50샘플 또는 1.0초=500샘플) 단위로 분할하여 선형 투영(`nn.Linear(input_size, d_model)`) 또는 CNN을 통해 연속 벡터로 임베딩.
  - **장점**: 이산화(quantization)로 인한 위상(phase) 손실이나 코드북 붕괴(codebook collapse)가 없으며, 미세한 고주파 감마 진동(high-gamma, 70~150 Hz)의 연속적 진폭 변화를 보존.
  - **치명적 취약점 (신호 공간 MSE 재구성의 덫)**:
    - 뇌파 신호 분산의 70~80%는 비신경계 잡음(눈 깜빡임 100 $\mu\text{V}$, 저주파 피부 전위 드리프트 <1 Hz, 근전도 고주파 버스트)에 의해 발생.
    - 손실 함수가 raw MSE(`MSE(masked_y, masked_x)`)로 정의될 경우, 모델은 이 거대한 비신경계 전압 잡음을 복원하는 데 표현 용량의 대부분을 낭비하게 됨.
- **이아현 선생님의 해법**:
  - DIVER-1.5에서는 연속 패치를 유지하되 **재구성 손실(MSE)을 완전히 제거(`mask_ratio=0.0`)하고 채널 출처 식별(Cross-Entropy)로 전환**.
  - DIVER-2에서는 비신경계 잡음을 학습하지 않는 **잠재 공간 예측(JEPA with EMA teacher)** 및 주파수 구조 일치(RSReg) 도입 추진.

#### [2] 교차 어텐션(Cross-Attention) 및 Salesforce Moirai 평탄화
- Salesforce Moirai 시계열 백본을 차용하여 다채널 시계열 `[B, C, N, P]`를 `[B, C*N, D]` 형태로 평탄화.
- 단일 Transformer 블록 내에서 시간 축 토큰 간 어텐션과 공간 채널 간 어텐션이 완전히 결합된 교차 어텐션(full spatial-temporal cross-attention)을 수행.
- FlashAttention / SDPA(Scaled Dot-Product Attention) 커널과의 완벽한 호환을 통해 대규모 시퀀스 확장성 확보.

#### [3] 3D 공간 좌표 투영(Spatial Coordinate Projection) 및 MNI 프레임 정밀화
- **DIVER-1의 좌표 제거 역설(Paradox)**:
  - DIVER-1 원고 Table 1에서 3D 전극 좌표 임베딩을 제거했을 때 오히려 다운스트림 성능이 향상됨 (+0.010 on speech, +0.005 on onset).
  - **원인 규명**: 3D 좌표가 어텐션 가중치 계산에 거리 바이어스로 반영되지 않고 단순 토큰 덧셈으로만 들어갔으며, 어텐션 자체는 1-bit `BinaryAttentionBias`에 머물렀기 때문.
- **BYD 벤치마크 좌표 왜곡 발견 및 해결 (`COORDINATES_BYD_RESOLVED_BTB_STILL_BROKEN.md`)**:
  - **BYD 실제 MNI 좌표 복원 (`diver_mni_real`)**: 과거 `diver_mni` 프로파일이 MNI 좌표를 버리고 `NaN -> 0`으로 채워 모델을 '공간적 맹목' 상태로 평가했음을 발견. 실제 centered MNI152-RAS 좌표를 복원하자 **BYD speech AUROC가 0.735에서 0.767로 즉각 +0.031 (환자 CS51은 +0.067) 대폭 상승**.
  - **Neuroprobe 좌표계 불일치 경고**: Neuroprobe의 `coord_btb_{x,y,z}`는 양수 복셀 좌표계(56~167)로 MNI 좌표와 강체 변환(rigid transform) 관계가 없어 심각하게 왜곡되어 있음을 증명하고, MNI 정규화 전까지 DIVER 평가를 중단하도록 규정.

#### [4] ACPE / STCPE 시너지 및 슬라이드 윈도우 최적화
- CBraMod의 컨볼루션 위치 인코딩(ConvPositionalEncoding) 한계를 극복하기 위해 Moirai 기반의 Spatio-Temporal Conditional Positional Encoding(STCPE) 구축.
- 윈도우 크기 $K_N=7$로 시간 축 슬라이딩 윈도우를 수행하며 지역적 시계열 연속성을 임베딩.
- 기존 im2col 방식의 비효율성을 Tensor unfold view로 최적화하여 연산 오버헤드를 92% 절감.

---

### 1.5 정량적 수치 표 및 베이스라인 비교

#### [표 1] DIVER-1 Muennighoff 스케일링 법칙 적합 파라미터 실측치 (논문 vs 실제)
- 출처: `originals_diver2_scaling_survey.md#L363-L375` (로컬 `appendix.tex:497-518` 전수 실측)
- 수식: $L(N,D) = A(N')^{-\alpha} + B(D')^{-\beta} + E$, 여기서 $g(U,R,R^*) = U[1 + R^*(1 - e^{-R/R^*})]$

| 파라미터 / 메트릭 | DIVER-1-1.0s (1.0초 패치) | DIVER-1-0.1s (0.1초 패치) | 비고 및 방법론적 의미 |
|---|---|---|---|
| 모델 크기 계수 ($A$) | **19.217** | **101.52** | 0.1s에서 모델 크기 기여도가 지배적으로 급증 |
| 데이터 크기 계수 ($B$) | **57.065** | **1.1550** | 1.0s에서는 $B > A$, 0.1s에서는 $A \gg B$ (본문 0.3925 오기) |
| 기약 오차 ($E$) | 0.0092 | 0.0030 | 패치가 작을수록 기약 재구성 손실 하한 감소 |
| 모델 크기 지수 ($\alpha$) | **0.3773** | **0.5248** | 모델 파라미터 증가에 따른 loss 감소 기울기 |
| 데이터 크기 지수 ($\beta$) | **0.3504** | **0.1246** | 0.1s에서 데이터 스케일링 효율 급격히 둔화 |
| 유효 에폭 천장 ($R_D^*$) | **9.5372** | **19.705** | 데이터 반복 학습의 이론적 한계 (약 10~20배) |
| 파라미터 반복 천장 ($R_N^*$)| **3.3850** | **0.7191** | 모델 크기 반복 학습 한계 |
| 적합도 ($R^2$, log scale) | **0.8152** | **0.7718** | 31개 런 기반 적합 (Muennighoff 93개 대비 소표본) |

#### [표 2] Neuroprobe 15-task 다운스트림 벤치마크 비교 (AUROC)
- 출처: `six_axis_synthesis_matrix.md#L37`, `manuscript_current.txt#L1680-L1690`

| 모델 / 아키텍처 | 사전학습 코퍼스 | 평가 방식 | Sentence Onset | Speech | Mean 15-task AUROC |
|---|---|---|---|---|---|
| **Random Init (Control)** | 없음 | Frozen Linear Probe | 0.612 | 0.589 | 0.584 |
| **PopT** (NeurIPS 2024) | iEEG | Fine-tuning | 0.742 | 0.710 | 0.569 |
| **BaRISTA** (2024) | iEEG | Fine-tuning | 0.765 | 0.738 | 0.586 |
| **BrainBERT** (2023) | iEEG (BTB) | Fine-tuning | 0.811 | 0.785 | 0.626 |
| **DIVER-1-1.0s** | iEEG 5,310h | Frozen Linear Probe | 0.885 | 0.852 | 0.654 |
| **DIVER-1-0.1s** | iEEG 5,310h | Full Fine-tuning | 0.895 | 0.864 | 0.665 |
| **DIVER-1-0.1s** | iEEG 5,310h | **Frozen Linear Probe** | **0.930** | **0.897** | **0.678** |

*핵심 발견*: DIVER-1-0.1s에서 **Frozen Linear Probe(0.678)가 Full Fine-tuning(0.665)을 능가**함. 소규모 하류 데이터셋에서 파인튜닝 시 발생하는 과적합(overfitting) 및 치명적 망각(catastrophic forgetting)을 강력한 동결 표상이 방어함.

#### [표 3] 두피 EEG 통합 다운스트림 벤치마크 (SPERA Table 2 원문 대조)
- 출처: `six_axis_synthesis_matrix.md#L215-L227`

| 모델 아키텍처 | 파라미터 | BCIC-IV-2a (운동상상) | ISRUC (수면) | TUAB (이상) | TUEV (발작이벤트) | 전체 9개 태스크 평균 |
|---|---|---|---|---|---|---|
| EEGNet | ~2K | 0.4482 | 0.7154 | 0.7642 | 0.3876 | 0.5941 |
| BIOT | ~6M | 0.4748 | 0.7527 | 0.7959 | 0.5281 | 0.6438 |
| LaBraM-Base | 48M | 0.4869 | 0.7633 | 0.8140 | 0.6409 | 0.6653 |
| CBraMod | ~50M | 0.5138 | 0.7865 | 0.8289 | 0.6671 | 0.6898 |
| CSBrain | ~100M | 0.5657 | 0.7925 | 0.8172 | 0.6903 | 0.7102 |
| REVE-Base | 408M | 0.6396 | 0.7819 | 0.8315 | 0.6759 | 0.7150 |
| **SPERA-Base (194M)** | 194M | **0.6816** | **0.8137** | **0.8488** | **0.7684** | **0.7502** |
| **SPERA-Large (396M)**| 396M | **0.7023** | **0.8142** | **0.8608** | **0.7869** | **0.7665** |

---

### 1.6 이아현 선생님의 비판적 자체 감사 및 안채원 선생님과의 연구 시너지

#### [1] 이아현 선생님이 스스로 규명한 DIVER-1의 3대 치명적 결함
1. **내러티브 정반대 모순**:
   - 초록/본문에서는 "데이터 확장이 우선이고 파라미터 확장은 마지막"이라고 주장했으나, 실제 부록 C.3의 정량적 피팅 결과는 $\alpha=0.5248 \gg \beta=0.1246$ 및 $A=101.52 \gg B=1.155$로 **모델 크기 확장이 데이터 확장보다 4.2배 효과적**임을 증명하여 심사위원들의 강력한 비판을 초래함.
2. **데이터 누수(Leakage) 및 Split 취약성**:
   - `--train_val_split_ratio 0.001` 분할이 37명 환자 내부의 시간적 자기상관 윈도우를 무작위로 나눈 표본 수준 분할(`torch.utils.data.random_split`)이었으며, 진정한 의미의 subject-held-out 검증이 부재했음을 내부 감사에서 최초 지적 (`originals_diver2_scaling_survey.md#L393-L404`).
3. **$\mu$P 하이퍼파라미터 전이 오류**:
   - 2 에폭 프록시에서 튜닝한 LR/WD를 64 에폭 대규모 런에 그대로 적용하여 트레이닝 호라이즌 불일치로 인한 손실 최적화 왜곡 발생.

#### [2] 안채원 선생님과의 협업 및 멘토링 시너지
- **연구 질문 설정 및 인프라 전수**:
  - 이아현 선생님은 텍스트 스케일링 법칙(Chinchilla)과 달리 생체신호가 갖는 독특한 2축($N$: 피험자 수, $T$: 1인당 기록 시간)의 분리 문제를 안채원 선생님에게 과제로 부여 (`ASSIGNMENT_subject_axis.md`).
  - 안채원 선생님이 KISTI 한강 클러스터(GH200)에서 분산 학습 환경을 구축하고 실측치($E(8)=0.78$)와 dataloader stall 타이머 버그를 해결하도록 기술적 지도.
- **안채원 선생님의 실증 데이터 (2.88M 샘플 통제)**:
  - 1인당 고유 기록을 1/64(81h), 1/1024(5h)로 축소하고 반복(`iEEG_re`)해도 다운스트림 0.6359, 0.6369로 Base(0.6363) 대비 비열등 유지.
  - 부족분을 EEG로 채우는 `EEG_fill`은 일관되게 -0.0100 하락.
  - 피험자를 37명 $\to$ 8명으로 줄여도 유지(+0.0001)되나, 2명으로 줄이면 즉시 붕괴(-0.0055).
- **차지욱 교수님과의 논쟁과 이아현 선생님의 과학적 방어**:
  - 차지욱 교수님이 "그냥 섞어서 안 되는 것은 당연하며, 데이터 부족 시 확장이 안 되는 것은 준비 덜 된 네거티브 결과"라고 투고에 회의적 피드백을 주었을 때,
  - 이아현 선생님은 **"단순한 데이터 감축이 아니라 참가자 수를 보존한 채 1인당 시간을 줄인 조건에서의 성공이며, 이는 DIVER-1.5의 채널 출처 예측 성공과 직결되는 'How should we scale'에 관한 중대한 발견"**임을 정면으로 설득하고 연구의 과학적 정당성을 확립함.

---

## 2. Logic Chain (논리 추론 체인)

1. **[관찰 1.1 + 1.2 참조]**
   - DIVER 시리즈는 완전 채널 등변성을 추구한 DIVER-0에서 출발하여, 대규모 침습적 뇌신호에 Moirai 평탄화 및 패치 토큰화를 적용한 DIVER-1으로 확장되었다. 그러나 DIVER-1은 두피 EEG와 침습 iEEG의 무분별한 혼합과 500 Hz 업샘플링으로 인해 모달리티 간 교란을 겪고 ICML/NeurIPS에서 고배를 마셨다.
2. **[관찰 1.2 + 1.4 참조]**
   - 이아현 선생님은 DIVER-1의 실패 요인을 분석하면서 두 가지 결정적 한계를 도출했다. (a) 원시 전압 신호 MSE 재구성은 신호의 70~80%를 차지하는 비신경계 잡음(안구 깜빡임, 전압 드리프트)에 모델 용량을 낭비하게 만든다. (b) 3D 전극 좌표는 단순 덧셈 임베딩에 불과하여 어텐션 내부에서 거리로 활용되지 못했다.
3. **[관찰 1.2 + 1.5 [표 1] 참조]**
   - 이아현 선생님은 DIVER-1.5에서 마스킹을 전면 제거(`mask_ratio=0.0`)하고 650개 전극 좌표 코드북 기반의 "채널 출처 예측(Channel Origin Prediction)"을 도입했다. 이 단일 목적함수만으로 8.55M 소형 모델이 뛰어난 하류 표상 전이 능력을 달성함을 확인하였다.
4. **[관찰 1.4 + 1.6 참조]**
   - 안채원 선생님이 KISTI 한강 클러스터에서 2.88M 샘플을 엄격히 통제하여 수행한 실험에서, "고유 iEEG 시간을 1/64, 1/1024로 줄여도 37명 또는 8명의 피험자 다양성을 유지하면 하류 성능이 완벽히 보존되지만, 피험자를 2명으로 줄이면 성능이 즉시 붕괴한다"는 실측 결과가 도출되었다.
5. **[관찰 1.6 참조]**
   - 차지욱 교수님은 이를 "사전지식 없는 단순 혼합의 실패를 보여주는 네거티브 결과"로 평가절하했으나, 이아현 선생님은 "DIVER-1.5에서 채널 식별만으로 성능이 나왔던 이유가 바로 피험자 다양성이 뇌파 표상 학습의 진정한 병목이기 때문"임을 규명하며, "소수 환자의 장기 기록보다 다수 환자의 단기 기록을 수집하는 것이 훨씬 경제적이고 효율적"이라는 2축 스케일링의 핵심 발견으로 승화시켰다.

---

## 3. Caveats (한계 및 미검증 영역)

1. **재구성 손실과 하류 점수 간의 괴리 (Dissociation Paradox)**:
   - 안채원 선생님의 실험에서 고유 데이터를 1/1024로 줄였을 때 검증 재구성 손실(Reconstruction loss)은 +8.5% 악화되었음에도 하류 linear probe 점수는 유지되었다. 이는 현재의 MAE 손실이 표상 품질을 온전히 대변하지 못하거나, 하류 과제가 저차원 선형 특징에 과도하게 의존함을 시사한다.
2. **읽는 층(Readout Layer) 심층 붕괴 위험**:
   - 1번째 블록(1st layer) 출력에서는 1/64 및 1/1024 조건이 모두 유지되었으나, Small(51M) 모델의 마지막 블록(Last layer)에서는 1/1024 조건이 -0.0050으로 붕괴되었다. 심층 비선형 표현까지 데이터 감축이 안전한지에 대해서는 추가 검증이 필요하다.
3. **사설 코호트 접근성 및 재현 한계**:
   - 사전학습에 사용된 서울대병원(SNUH) 정천기 교수님 연구실 사설 iEEG 데이터는 환자 개인정보 보호 규정상 공개가 제한되어 있어, 외부 연구진의 완전 독립 재현 시 공공 데이터(PennEPI, UMN, SWEC, AJILE)에 의존해야 한다.

---

## 4. Conclusion (최종 종합 결론)

1. **이아현 선생님의 독보적 연구 기여**:
   - 이아현 선생님은 DIVER-0에서 DIVER-2에 이르는 전산생체신호 파운데이션 모델의 아키텍처 진화를 이끌었으며, DIVER-1의 방법론적 오류(초록-부록 간 스케일링 모순, 데이터 누수)를 가감 없이 스스로 밝혀내고 DIVER-1.5의 채널 출처 예측 및 DIVER-2의 2축 스케일링 법칙으로 정밀하게 교정해 냈다.
2. **핵심 메커니즘의 실체**:
   - 뇌파 파운데이션 모델에서 중요한 것은 단순한 모델 파라미터 팽창이나 1인당 긴 시계열 기록이 아니며, **"다양한 피험자로부터 추출된 해부학적 다양성($N$)"**과 **"원시 전압 신호의 잡음 함정을 극복하는 자체지도학습 목표(Channel Origin Prediction / JEPA)"**의 결합이다.
3. **M1 연구 종합 및 차기 마일스톤(M2 딥리서치, M3 적대적 리뷰) 연계**:
   - 본 보고서에 수록된 정량적 수치 표([표 1], [표 2], [표 3]), 아키텍처 파라미터, 및 논쟁의 실체는 `docs/01_research_synthesis.md`의 핵심 장(Chapter)을 구성하며, M2/M3에서 수행될 5대 과학적 방법론 기반 적대적 리뷰의 확고한 팩트 기반이 된다.

---

## 5. Verification Method (독립 검증 방법)

차기 에이전트 및 검토자는 아래 명령어를 통해 본 보고서의 모든 사실 관계와 수치를 독립적으로 검증할 수 있습니다.

1. **DIVER-1.5 설정 및 채널 식별 목적함수 검증**:
   ```bash
   cat /home/juke/git/DIVER-2/diver_pretrain/config/diver15/btb64.yaml | grep -E "mask_ratio|aux_channel_identity|out_dim|d_model"
   ```
2. **DIVER-1 실제 스케일링 적합 계수 및 수치 불일치 검증**:
   ```bash
   sed -n '365,385p' /home/juke/git/ephys-foundation-model-plan/submissions/2026/20261010-yahyunee-diver2-scaling-survey/originals_diver2_scaling_survey.md
   ```
3. **BYD 벤치마크 실제 MNI 좌표 복원 효과 (+0.031 AUROC) 검증**:
   ```bash
   cat /home/juke/git/DIVER-2/diver_pretrain/benchmarks/imindbench/COORDINATES_BYD_RESOLVED_BTB_STILL_BROKEN.md | head -n 45
   ```
4. **STCPE 슬라이딩 윈도우 Gather 최적화 코드 검증**:
   ```bash
   sed -n '1338,1360p' /home/juke/git/DIVER-2/diver_pretrain/src/layers/Embed.py
   ```
5. **무효화 조건 (Invalidation Conditions)**:
   - DIVER-1.5의 체크포인트 평가에서 채널 출처 예측 목적함수가 아닌 단순 재구성 MAE가 주도적 기여를 한 것으로 드러날 경우, 본 연구의 메커니즘 해석은 수정되어야 한다.
   - 마지막 레이어(Last block) 풀 파인튜닝 시 1/64 및 8명 피험자 조건이 통계적으로 유의미한 성능 붕괴를 보일 경우, 피험자 축 스케일링 법칙의 일반화 범위는 '표층 표현(shallow representation)'으로 한정되어야 한다.
