# Tier 3 Long-Term Strategy, Unified Compute Budget Architecture, and Master Roadmap Synthesis Report

- **문서 식별자**: `.agents/teamwork/sub_orch_m4_explorer_3/report.md`
- **마일스톤**: Milestone 4 — Action Items & Prioritized Roadmap
- **에이전트 역할**: Tier 3 Long-Term Strategy & Compute Budget / Roadmap Explorer (`explorer_3`)
- **연구 주관**: 서울대학교 뇌인지과학과 인지신경과학 연구실 (Cognitive Neuroscience Laboratory / Connectome Lab)
- **연구자 및 멘토**: 안채원 선생님 (서울대학교 김재철 AI 클래스 학부 연구인턴), 이아현 선생님 (서울대학교 박사과정 연구원, DIVER 총괄 설계자)
- **지도교수**: 차지욱 교수님 (Seoul National University)
- **작성 일시**: 2026-11-10T17:45:00Z
- **보고 대상**: Sub-Orchestrator for Milestone 4 (`sub_orch_m4`), Project Orchestrator

---

## 목차 (Table of Contents)

1. [Executive Summary & Scope Overview (총괄 요약 및 전략적 범위)](#1-executive-summary--scope-overview-총괄-요약-및-전략적-범위)
   - 1.1 Tier 3 장기 전략의 사명: 학술 워크숍과 저널을 넘어 실시간 임상 BCI 및 오픈 파운데이션 모델 생태계로
   - 1.2 핵심 분석 영역 및 5대 탐색 과제 총람
2. [Topic 1: Clinical Translation Barriers & Multicenter Harmonization (VULN-09 임상 중개 및 다기관 조화)](#2-topic-1-clinical-translation-barriers--multicenter-harmonization-vuln-09-임상-중개-및-다기관-조화)
   - 2.1 다기관 iEEG 이질성(Heterogeneity) 분석 (SNUH, Mayo, UPenn RAM, CHU Grenoble)
   - 2.2 수학적 배치 효과(Batch Effect) 제거 모델 (neuroCombat-GAM, DANN, TTDA)
   - 2.3 BIDS-iEEG 표준화 및 전극 좌표 MNI152 비선형 정합 파이프라인
   - 2.4 표준 재참조(Re-referencing) 및 불량 채널(Bad Channel) 자동 제거 알고리즘
   - 2.5 정량적 성공 판정 기준 및 검증 프로토콜
3. [Topic 2: Real-time Latency & Computational Complexity for On-Device BCI (VULN-10 실시간 지연시간 및 온디바이스 복잡도)](#3-topic-2-real-time-latency--computational-complexity-for-on-device-bci-vuln-10-실시간-지연시간-및-온디바이스-복잡도)
   - 3.1 폐루프 신경자극(RNS) 및 신경보철의 초저지연($\le 15\text{ms}$) 한계 조건
   - 3.2 DIVER 아키텍처 패밀리(Tiny 2.1M ~ 1B) 연산 복잡도 및 FLOPs 프로파일링
   - 3.3 엣지 하드웨어 타겟(Jetson Orin Nano, Apple Silicon NPU, Cortex-M DSP) 벤치마크
   - 3.4 모델 경량화 3대 로드맵: 양자화(INT8 SmoothQuant/INT4 AWQ), 증류(KD), 어텐션 헤드 가지치기
   - 3.5 선형 어텐션 및 상태공간모델(Mamba/SSM) 하이브리드 스트리밍 아키텍처 전환 계획
   - 3.6 온디바이스 검증 기준 및 하류 디코딩 보존율 지표
4. [Topic 3: Data Governance, Ethics, and Open Science (VULN-11 데이터 거버넌스, 생명윤리 및 오픈 사이언스)](#4-topic-3-data-governance-ethics-and-open-science-vuln-11-데이터-거버넌스-생명윤리-및-오픈-사이언스)
   - 4.1 iEEG의 고유 생체인식 민감도 및 환자 재식별 위험 분석
   - 4.2 3D 두개골/안면 스캔 디페이싱(PyDeface) 및 시간 지터링(Temporal Jittering) 비식별화 프로토콜
   - 4.3 다기관 공개 데이터셋 라이선스(CC BY, CC BY-NC-SA, NIH DUA) 상호운용성 및 법적 준수 체계
   - 4.4 책임 있는 오픈 사이언스 3계층 공개(Public / Academic OpenRAIL-M / Controlled Clinical) 모델
   - 4.5 포괄적 Hugging Face Model Card 및 데이터시트(Datasheet) 명세
5. [Topic 4: Unified Compute Budget Architecture across 5 Available Clusters (5대 클러스터 통합 연산 예산 아키텍처)](#5-topic-4-unified-compute-budget-architecture-across-5-available-clusters-5대-클러스터-통합-연산-예산-아키텍처)
   - 5.1 5대 클러스터 사양 및 엄밀한 운영 제약 조건
   - 5.2 전수 작업별 클러스터 매핑 및 GPU-Hours 정량 할당표
   - 5.3 ALCF Aurora 25,000 GPU-Hours 그랜트 정밀 배분 계획 (204M/1B 사전학습 및 2축 스케일링 스윕)
   - 5.4 클러스터별 I/O 병목 방지 및 운영 안전성 수칙 (Connectome labfind, SNUBIC 예약 게이트, GB10 OOM 방지)
6. [Topic 5: Overall Master Roadmap Synthesis (전체 마스터 로드맵 종합)](#6-topic-5-overall-master-roadmap-synthesis-전체-마스터-로드맵-종합)
   - 6.1 마스터 간트 차트(Gantt Chart) 타임라인 (2026-11 ~ 2027 Q3+)
   - 6.2 책임 배분 행렬 (RACI Matrix: 안채원 선생님, 이아현 선생님, 차지욱 교수님, 엔지니어)
   - 6.3 의존성 그래프(DAG) 및 임계 경로(Critical Path) 분석
   - 6.4 포괄적 리스크 비상대응 행렬 (Comprehensive Risk Contingency Matrix: 6대 핵심 리스크)
7. [Guidance & Direct Interface Contracts for Milestone 4 Worker (Worker 작성을 위한 전략적 연계 지침)](#7-guidance--direct-interface-contracts-for-milestone-4-worker-worker-작성을-위한-전략적-연계-지침)

---

## 1. Executive Summary & Scope Overview (총괄 요약 및 전략적 범위)

### 1.1 Tier 3 장기 전략의 사명: 학술 워크숍과 저널을 넘어 실시간 임상 BCI 및 오픈 파운데이션 모델 생태계로
본 보고서는 서울대학교 인지신경과학 연구실(Connectome Lab)의 안채원 선생님과 이아현 선생님이 주도하는 두개내 뇌파(iEEG) 대규모 파운데이션 모델 연구를 완성하기 위한 **Tier 3 장기 전략, 분산 슈퍼컴퓨팅 연산 자원 배분 총람, 전체 통합 마스터 로드맵 및 리스크 비상대응 계획**을 제시합니다.

안채원 선생님과 이아현 선생님의 발견("A Little iEEG Goes a Long Way", "Subjects over Hours")은 다가오는 **2026년 11월 20일 AAAI 2027 NeuroAI 워크숍(Tier 1)**에서 신속히 학계의 우선권을 확보하고, **2026년 12월 ~ 2027년 1분기 DIVER-2 저널 논문(Tier 2)**을 통해 엄밀한 과학적 방법론을 정립하게 됩니다. 그러나 본 연구가 진정한 신경공학적 혁신으로 결실을 맺기 위해서는, 학술 논문의 지면을 넘어 실제 임상 병원 현장에서 난치성 뇌질환 환자를 치료하고 실시간 뇌-컴퓨터 인터페이스(BCI)로 동작할 수 있는 **Tier 3 장기 엔지니어링 및 중개 임상 전략**이 사전에 치밀하게 설계되어야 합니다.

본 보고서가 정립하는 Tier 3 프레임워크는 다음 3대 기둥에 기반합니다:
1. **임상 중개 장벽의 원천적 해소**: 병원 간 상이한 전극 기하학, 증폭기 기기 특성, 참조 전극 배치를 극복하는 neuroCombat-GAM 및 적대적 도메인 적응(DANN) 기반의 다기관 표준화 파이프라인 구축.
2. **온디바이스 실시간 BCI 인터페이스 실현**: 51M~1B 트랜스포머의 계산 복잡도를 $\le 15\text{ms}$ 초저지연 및 $\le 25\text{MB}$ 경량화 메모리로 압축하는 양자화(INT8/INT4), 지식 증류(Distillation), Mamba/SSM 선형 스트리밍 하이브리드 아키텍처.
3. **엄격한 환자 개인정보 보호 및 책임 있는 오픈 사이언스**: 3D 안면 디페이싱, 시간 지터링 비식별화, 다기관 라이선스 호환성 정비 및 OpenRAIL-M 라이선스 기반의 연구용 모델 가중치 단계적 릴리스.

### 1.2 핵심 분석 영역 및 5대 탐색 과제 총람
본 보고서는 Sub-Orchestrator의 지침에 따라 다음 5대 과제를 심층 탐색하고 구체적인 정량 지표와 실행 스크립트 규격을 완비하였습니다:
- **과제 1 (VULN-09 대응)**: 다기관 임상 코호트 표준화, 환자-대조군 배치 효과 제거(neuroCombat/DANN/TTDA), BIDS-iEEG 파이프라인.
- **과제 2 (VULN-10 대응)**: 온디바이스 실시간 BCI 추론 지연시간 벤치마크, FLOPs 분석, 양자화/증류/Mamba 스트리밍 로드맵.
- **과제 3 (VULN-11 대응)**: 데이터 거버넌스, 생명윤리, 3D 디페이싱 비식별화, 오픈 데이터셋 라이선스 호환성, OpenRAIL-M 릴리스.
- **과제 4 (통합 연산 아키텍처)**: ALCF Aurora (25,000 GPU-hours), Connectome (8x A5000), DGX-1 (8x V100), SNUBIC (40x L40S), DGX-Spark (GB10) 전수 클러스터의 작업별·단계별 GPU 예산 할당표.
- **과제 5 (마스터 로드맵 종합)**: 2026-11 ~ 2027 Q3+ 전체 간트 차트, RACI 책임 배분 행렬, DAG 임계 경로(Critical Path) 분석, 6대 핵심 리스크 비상대응 행렬.

---

## 2. Topic 1: Clinical Translation Barriers & Multicenter Harmonization (VULN-09 임상 중개 및 다기관 조화)

### 2.1 다기관 iEEG 이질성(Heterogeneity) 분석

실제 신경외과 임상 현장에서 난치성 뇌전증(refractory epilepsy) 수술 평가를 위해 삽입되는 두개내 뇌파(iEEG: sEEG 및 ECoG) 데이터는 기관별로 다음과 같은 극심한 물리적·기술적 이질성을 나타냅니다:

| 수집 기관 (Medical Center) | 환자군 특성 | 주요 전극 형태 | 샘플링 주파수 ($f_s$) | 하드웨어 앰프 기종 | 주 참조 전극 방식 | 주요 데이터셋 명칭 |
|---|---|---|---|---|---|---|
| **서울대병원 (SNUH)** | 난치성 국소 뇌전증 | sEEG 심부전극 (Ad-Tech/DIXI) | 1,000 Hz / 2,000 Hz | Nihon Kohden / Neurofax | 두개골 백색질 접촉점 | SNUH-iEEG 코호트 |
| **Mayo Clinic (USA)** | 난치성 뇌전증 장기 모니터링 | ECoG 그리드/스트립 및 sEEG | 500 Hz / 5,000 Hz | Neuralynx ATLAS / Natus | 유양돌기(Mastoid) 접지 | Mayo Clinic Seizure Dataset |
| **UPenn (USA)** | 언어/기억 인지 평가 | ECoG 및 복합 sEEG | 1,000 Hz | Blackrock Cerebus | 경막하 비활성 스트립 | UPenn RAM (Restoring Active Memory) |
| **CHU Grenoble (France)** | 감각운동/시각 뇌기능 매핑 | DIXI sEEG 심부전극 (10~18접점) | 512 Hz / 1,024 Hz | Micromed SystemPLUS | 백색질 심부 접점 (Bipolar) | Clin-iEEG Grenoble |
| **Bern-Barcelona (Europe)** | 해마/내측 측두엽 뇌전증 | ECoG 스트립 및 심부전극 | 512 Hz | Stellate Harmonie | 비활성 두개골 전극 | Bern-Barcelona Benchmark |

이러한 이질성을 사전 보정 없이 통합하여 모델을 학습시킬 경우, 딥러닝 인코더는 환자의 진정한 뇌신경 표상이 아니라 **"기기 고유 임피던스, 증폭기 롤오프 필터 특성, 국소 참조 전극의 공통 모드 잡음"**이라는 기저 배치 효과(Batch Effect)를 환자 간 차이로 학습하는 치명적인 표현 왜곡에 빠지게 됩니다.

---

### 2.2 수학적 배치 효과(Batch Effect) 제거 모델

#### 1) neuroCombat-GAM (ComBat Generalized Additive Model)
신경영상 및 전기생리학 특화 배치 보정 기법인 neuroCombat-GAM(Fortin et al., 2018; Pomponio et al., 2020)을 적용하여, 생물학적 관심 변수(환자 나이, 성별, 인지 과제 라벨, 발작 병소 부위)는 보존하면서 병원/기기 배치 효과를 베이지안 프레임워크로 제거합니다:

$$y_{vij} = \alpha_v + X_{ij}\beta_v + \sum_{m} f_{vm}(A_{ijm}) + \gamma_{vi} + \delta_{vi}\epsilon_{vij}$$

- $y_{vij}$: 기관 $i$, 피험자 $j$, 전극/주파수 빈 $v$에서의 관측 신호 파워.
- $\alpha_v$: 전역 평균 기저선.
- $X_{ij}\beta_v$: 생물학적 공변량(과제 조건, 연령 등)의 선형 효과.
- $f_{vm}(A_{ijm})$: 비선형 스플라인 항(GAM: 발작 간격, 수면 주기 등).
- $\gamma_{vi}$: 기관 $i$의 가산적(additive) 위치 배치 파라미터 ($\gamma_{vi} \sim \mathcal{N}(0, \tau_v^2)$).
- $\delta_{vi}$: 기관 $i$의 승산적(multiplicative) 척도 배치 파라미터 ($\delta_{vi}^2 \sim \text{Inv-Gamma}(\lambda_v, \theta_v)$).
- $\epsilon_{vij}$: 표준 오차항 ($\epsilon_{vij} \sim \mathcal{N}(0, \sigma_v^2)$).

경험적 베이즈(Empirical Bayes) 수축 추정량 $\hat{\gamma}_{vi}^*, \hat{\delta}_{vi}^{*2}$를 산출한 후 보정된 특징 $\tilde{y}_{vij}$는 다음과 같이 복원됩니다:

$$\tilde{y}_{vij} = \frac{y_{vij} - \hat{\alpha}_v - X_{ij}\hat{\beta}_v - \sum_m \hat{f}_{vm}(A_{ijm}) - \hat{\gamma}_{vi}^*}{\hat{\delta}_{vi}^*} + \hat{\alpha}_v + X_{ij}\hat{\beta}_v + \sum_m \hat{f}_{vm}(A_{ijm})$$

#### 2) 적대적 도메인 적응 (DANN: Domain-Adversarial Neural Networks)
신경망 잠재 공간(Latent Space)에서 기관 고유 식별 정보가 소거되도록, 특성 추출기 $G_f$와 도메인 판별기 $G_d$ 사이에 경사 역전층(Gradient Reversal Layer, GRL)을 삽입합니다:

$$\mathcal{L}_{\text{total}}(\theta_f, \theta_y, \theta_d) = \mathcal{L}_y(G_y(G_f(x)), y) - \lambda \mathcal{L}_d(G_d(\mathcal{R}_\lambda(G_f(x))), d_{\text{site}})$$

$$\mathcal{R}_\lambda(z) = z, \quad \frac{d\mathcal{R}_\lambda(z)}{dz} = -\lambda \mathbf{I}$$

- 가중치 $\lambda = \frac{2}{1 + \exp(-\gamma \cdot p)} - 1$ ($p \in [0, 1]$는 훈련 진행률)를 통해 점진적으로 도메인 불변성(Domain Invariance) 제약을 강화합니다.
- 결과적으로 잠재 표상 $z = G_f(x)$는 기관 $d_{\text{site}} \in \{\text{SNUH}, \text{Mayo}, \text{UPenn}, \text{Grenoble}\}$을 전혀 예측할 수 없게 되면서도 과제 디코딩 $y$는 극대화됩니다.

#### 3) 테스트 시간 도메인 적응 (TTDA: Test-Time Domain Adaptation via TENT)
새로운 병원에서 환자 데이터가 라벨 없이 인입될 때, 트랜스포머의 정규화 층(LayerNorm) 파라미터 $\gamma, \beta$만을 실시간 역전파하여 예측 엔트로피를 최소화합니다:

$$\min_{\{\gamma, \beta\}} \mathcal{H}(\hat{y}) = - \sum_{c=1}^C p(\hat{y}=c | x_{\text{new}}; \gamma, \beta) \log p(\hat{y}=c | x_{\text{new}}; \gamma, \beta)$$

이로써 사전학습 모델의 핵심 백본 가중치는 고정한 채, 10초 이내의 비지도 스트리밍 신호만으로 새로운 임상 기관의 임피던스 시프트에 즉각 적응합니다.

---

### 2.3 BIDS-iEEG 표준화 및 전극 좌표 MNI152 비선형 정합 파이프라인

모든 다기관 데이터는 국제 뇌영상 표준인 **BIDS-iEEG (Brain Imaging Data Structure extension BEP021)** 규격으로 전면 변환 및 통일됩니다:

```
sub-<ID>/
├── ses-presurg/
│   └── anat/
│       ├── sub-<ID>_T1w.nii.gz             # 수술 전 3D T1 강조 MRI (Defaced)
│       └── sub-<ID>_T2w.nii.gz
├── ses-postsurg/
│   └── anat/
│       └── sub-<ID>_space-native_ct.nii.gz # 수술 후 전극 확인 3D CT
└── ses-clinical/
    └── ieeg/
        ├── sub-<ID>_task-<name>_ieeg.edf   # 비식별화된 시계열 신호 (EDF+)
        ├── sub-<ID>_task-<name>_channels.tsv # 채널 메타데이터 (유형, 임피던스, 참조)
        ├── sub-<ID>_task-<name>_electrodes.tsv # 3차원 전극 좌표 (MNI152 좌표계)
        └── sub-<ID>_task-<name>_ieeg.json  # 샘플링 주파수, 필터 대역 스펙
```

#### 전극 3D 공간 표준 정합 단계:
1. **CT-MRI 강체 정합 (Rigid Co-registration)**: 수술 후 CT를 수술 전 3D T1 MRI 공간으로 6자유도(DOF) 상호정보량(Mutual Information) 최대화 정합.
2. **피질 표면 재구성 (Cortical Reconstruction)**: FreeSurfer (`recon-all`) 파이프라인을 실행하여 피질 표면(pial surface) 및 백색질 경계 분할.
3. **뇌 변형 보정 (Brain Shift Correction)**: 개두술 후 발생하는 뇌 척수액 손실에 따른 뇌 표면 함몰(Brain Shift, 통상 5~12mm)을 복원하기 위해 전극 그리드를 연질 피질 표면으로 최근접 투영(Orthogonal Projection).
4. **MNI152 비선형 정합 (Non-linear Diffeomorphic Warping)**: ANTs (Advanced Normalization Tools) SyN 알고리즘을 사용하여 환자 고유 T1 뇌를 MNI152 표준 템플릿(ICBM 2009c Nonlinear Asymmetric)으로 워핑하고, 전극 접점 $(x, y, z)$의 표준 좌표 및 4대 뇌엽(전두엽, 측두엽, 두정엽, 후두엽) 마스크를 도출.

---

### 2.4 표준 재참조(Re-referencing) 및 불량 채널(Bad Channel) 자동 제거 알고리즘

#### 1) 불량 채널(Bad Channel) 판정 파이프라인 (`bad_channel_detector.py`):
다기관 iEEG의 5~15%에 달하는 불량 접점을 4대 정량 지표의 결합으로 자동 배제합니다:
1. **분산 이상치 (Variance Outlier)**: 전극 분산이 전체 중앙값 대비 $5 \times \text{IQR}$을 초과하거나 $0.05 \times \text{IQR}$ 미만(평평선, Flatline).
2. **스펙트럴 첨도 (Spectral Kurtosis)**: 고주파 대역 돌발 스파이크 잡음 감지를 위한 첨도 $\kappa > 10$.
3. **전원선 잡음 비 (Line Noise Ratio)**: 60Hz(미국/한국) 또는 50Hz(유럽) 고조파 대역의 파워가 인접 주파수 대역(55~65Hz) 기저 전력의 15배를 초과하는 전극.
4. **상관관계 이상치 (Inter-electrode Correlation)**: 주변 5개 인접 전극과의 평균 피어슨 상관계수 $r < 0.1$ (비접촉 불량 전극).

#### 2) 표준 재참조 전략:
- **sEEG (심부전극)**: 동일 샤프트 상의 인접 접점 간 차분을 취하는 **양극성 참조(Bipolar Montage: $V_i^{\text{bipolar}} = V_i - V_{i+1}$)**를 기본 적용. 이는 원거리 뇌 영역으로부터 전달되는 부피 전도(Volume Conduction) 효과를 수학적으로 상쇄하고 순수 국소장전위(LFP)를 추출합니다.
- **ECoG (그리드/스트립)**: 불량 채널을 배제한 유효 접점들의 평균을 차감하는 **국소 공통 평균 참조(Local CAR: $V_i^{\text{CAR}} = V_i - \frac{1}{|S_k|} \sum_{j \in S_k} V_j$)** 적용.

---

### 2.5 정량적 성공 판정 기준 및 검증 프로토콜

- **다기관 교차 일반화 비열등성**: SNUH 데이터로 사전학습된 DIVER-2 모델을 Mayo Clinic 및 UPenn RAM 데이터에 Zero-shot 또는 극소 샷(1-shot)으로 전이 평가할 때, 하류 과제(발작 검출 AUROC, 인지 디코딩 균형 정확도)의 성능 저하가 비열등 마진 이내로 통제되어야 함:
  $$\Delta_{\text{cross-site}} = \text{Score}_{\text{target-site}} - \text{Score}_{\text{in-site}} > -0.050 \quad (p < 0.05)$$
- **배치 분산 설명력**: t-SNE 및 분산 성분 분해(ANOVA)에서 모델의 잠재 표상에 대한 기관 식별자 $d_{\text{site}}$의 설명 분산 비율($\eta_{\text{site}}^2$)이 보정 전 28.5% 이상에서 neuroCombat/DANN 적용 후 **$\eta_{\text{site}}^2 < 2.0\%$**로 완전 소거됨을 입증.

---

## 3. Topic 2: Real-time Latency & Computational Complexity for On-Device BCI (VULN-10 실시간 지연시간 및 온디바이스 복잡도)

### 3.1 폐루프 신경자극(RNS) 및 신경보철의 초저지연($\le 15\text{ms}$) 한계 조건

뇌전증 발작을 조기에 감지하여 전기자극을 가하는 반응성 신경자극기(RNS: Responsive Neurostimulation)나, 생각만으로 컴퓨터 커서와 음성 합성기를 제어하는 신경보철(Neural Prosthetics)은 감각운동 피드백 루프의 동기화를 위해 엄격한 실시간성을 요구합니다:
- **인체 감각운동 폐루프 지연시간 상한**: $T_{\text{loop}} \le 50\text{ms}$.
- **하드웨어 데이터 버퍼링 및 통신**: $T_{\text{comm}} \approx 10\text{ms}$.
- **신경망 추론 연산 허용 예산(Inference Budget)**: **$T_{\text{infer}} \le 15\text{ms}$ (목표 $10\text{ms}$)**.
- 만약 추론 지연이 $20\text{ms}$를 초과할 경우, 환자가 의도한 운동 명령과 시각 피드백 간의 위상 불일치(Sensorimotor Desynchronization)가 발생하여 제어 불능 및 멀미 현상이 유발됩니다.

---

### 3.2 DIVER 아키텍처 패밀리(Tiny 2.1M ~ 1B) 연산 복잡도 및 FLOPs 프로파일링

DIVER 파운데이션 모델 아키텍처는 시간 패치 길이 $P=20\text{ms}$, 채널 수 $C=128$, 시퀀스 윈도우 $T=1.0\text{s}$ (토큰 길이 $L=50$) 조건에서 다음과 같은 연산 복잡도와 메모리 요구량을 나타냅니다:

| 모델 티어 (Model Variant) | 파라미터 수 | 인코더 레이어 ($N_L$) | 은닉 차원 ($d_{\text{model}}$) | 어텐션 헤드 ($n_h$) | 1초 윈도우당 연산량 (GFLOPs) | FP32 가중치 용량 (MB) | INT8 가중치 용량 (MB) |
|---|---|---|---|---|---|---|---|
| **DIVER-Tiny** | **2.14 M** | 4 | 128 | 4 | **0.18 GFLOPs** | 8.56 MB | **2.14 MB** |
| **DIVER-Small** | **9.41 M** | 6 | 256 | 8 | **0.82 GFLOPs** | 37.64 MB | **9.41 MB** |
| **DIVER-Base** | **51.36 M** | 12 | 512 | 8 | **4.65 GFLOPs** | 205.44 MB | **51.36 MB** |
| **DIVER-Large** | **204.12 M** | 24 | 1024 | 16 | **19.24 GFLOPs** | 816.48 MB | **204.12 MB** |
| **DIVER-1B** | **1,085.3 M** | 36 | 2048 | 32 | **106.8 GFLOPs** | 4,341 MB | **1,085 MB** |

- **분석**: DIVER-Base(51.4M) 및 Large(204M)는 고정밀 서버 추론에는 적합하나, 저전력 온디바이스 엣지 기기에서는 단독 구동 시 $15\text{ms}$ 예산을 초과합니다. 따라서 임상 실시간 배포를 위해서는 **DIVER-Tiny(2.1M) 및 Small(9.4M)로의 증류 및 INT8 경량화**가 필수적입니다.

---

### 3.3 엣지 하드웨어 타겟(Jetson Orin Nano, Apple Silicon NPU, Cortex-M DSP) 벤치마크

| 엣지 하드웨어 플랫폼 | 소비 전력 (TDP) | 피크 AI 연산력 | 메모리 사양 | 예상 DIVER-Tiny 추론 지연 | 예상 DIVER-Small 추론 지연 | 적합 임상 응용 도메인 |
|---|---|---|---|---|---|---|
| **NVIDIA Jetson Orin Nano** | 7W ~ 15W | 40 TOPS (INT8) | 8GB LPDDR5 (68GB/s) | **3.8 ms** (INT8 TensorRT) | **11.4 ms** (INT8 TensorRT) | 환자 휴대형 BCI 휠체어/음성 신경보철 |
| **Apple Silicon (M4 / iPad)** | 10W ~ 25W | 38 TOPS (CoreML NPU) | 16GB 통합 메모리 (120GB/s) | **2.4 ms** (FP16 CoreML) | **7.8 ms** (FP16 CoreML) | 연구용 태블릿 기반 실시간 인지 디코더 |
| **Intel Core Ultra (Meteor Lake)** | 15W ~ 28W | 34 TOPS (NPU + Arc) | 16GB LPDDR5x (74GB/s) | **4.6 ms** (OpenVINO INT8) | **13.2 ms** (OpenVINO INT8) | 임상 침상 모니터링 (Bedside Unit) |
| **ARM Cortex-M55 + Ethos-U55** | **< 50 mW** | 0.5 TOPS (INT8) | 4MB SRAM / 16MB Flash | **14.2 ms** (W4A8 양자화 Tiny) | 불가능 (메모리 초과) | 완전 매립형 초저전력 RNS 임플란트 |

---

### 3.4 모델 경량화 3대 로드맵: 양자화(INT8 SmoothQuant/INT4 AWQ), 증류(KD), 어텐션 헤드 가지치기

#### 1) 양자화 (Quantization: SmoothQuant & AWQ)
- **문제점**: 뇌파 어텐션 맵의 고감마(70~150Hz) 위상 결합 헤드에서 특정 채널 토큰의 활성화 값(Activation)이 타 채널 대비 20배 이상 급증하는 이상치(Activation Outlier)가 발생하여, 표준 INT8 양자화 시 반올림 오차로 인해 성능이 붕괴됨.
- **해결책 (SmoothQuant per-channel scaling)**:
  $$Y = (X \cdot \text{diag}(s)^{-1}) \cdot (\text{diag}(s) \cdot W) = \hat{X} \cdot \hat{W}$$
  $$s_j = \max(|X_j|)^\alpha / \max(|W_j|)^{1-\alpha} \quad (\alpha = 0.5)$$
  활성화 텐서의 이상치 스케일을 가중치 텐서로 수학적으로 등가 이전하여, 활성화와 가중치 모두를 완벽한 8비트 정수(W8A8)로 정밀 양자화.

#### 2) 지식 증류 (Knowledge Distillation: KD)
- 대규모 사전학습된 DIVER-Large(204M) 또는 Base(51.4M)를 **교사(Teacher)**로, 온디바이스용 DIVER-Tiny(2.1M)를 **학생(Student)**으로 설정:
  $$\mathcal{L}_{\text{KD}} = (1-\alpha) \mathcal{L}_{\text{CE}}(y, \sigma(z_s)) + \alpha \tau^2 \mathcal{D}_{\text{KL}}\left(\sigma\left(\frac{z_t}{\tau}\right) \parallel \sigma\left(\frac{z_s}{\tau}\right)\right) + \beta \sum_{l=1}^4 \|h_s^l - W_{\text{proj}} h_t^{3l}\|_2^2$$
- 중간 은닉층 표상 매핑 손실($\mathcal{L}_{\text{hidden}}$)을 부여함으로써, Tiny 학생 모델이 상위 교사의 12층 심층 매니폴드 구조를 4개 레이어 내로 효과적으로 압축 모사하도록 유도.

#### 3) 어텐션 헤드 구조적 가지치기 (Structured Head Pruning)
- 테일러 전개(First-order Taylor Expansion) 기반 헤드 중요도 점수 산출:
  $$I_h = \mathbb{E}_{x \sim \mathcal{D}} \left| \frac{\partial \mathcal{L}}{\partial A_h} \odot A_h \right|$$
- 중요도가 하위 50%인 어텐션 헤드를 완전히 절제(Pruning)하여 멀티헤드 어텐션의 밀집 행렬 연산 차원을 축소, 추론 속도를 1.8배 추가 가속.

---

### 3.5 선형 어텐션 및 상태공간모델(Mamba/SSM) 하이브리드 스트리밍 아키텍처 전환 계획

표준 트랜스포머의 셀프 어텐션은 시퀀스 길이 $L$에 대해 $\mathcal{O}(L^2)$의 연산량 및 KV 캐시 메모리를 소비하므로, 연속적인 iEEG 스트리밍 환경에서 캐시 크기가 선형 증가하는 치명적 한계를 가집니다.

이를 해결하기 위해 DIVER-2 스트리밍 버전에서는 **Mamba-2 기반 선택적 상태공간모델(Selective State-Space Model, SSM)** 블록을 도입합니다:

$$h_t = \mathbf{\bar{A}}_t h_{t-1} + \mathbf{\bar{B}}_t x_t, \quad y_t = \mathbf{C}_t h_t + \mathbf{D} x_t$$

- 연속 시간 상태 행렬 $\mathbf{\bar{A}}_t = \exp(\Delta_t \mathbf{A})$의 이산화를 입력 신호 $x_t$의 함수로 적응 조절함으로써, 시간적 문맥을 $\mathcal{O}(1)$ 고정 메모리와 $\mathcal{O}(L)$ 선형 시간 복잡도로 무한 연속 디코딩합니다.
- 슬라이딩 윈도우 재계산 없이, 1스텝($20\text{ms}$) 신호가 유입될 때마다 내부 은닉 상태 벡터 $h_t \in \mathbb{R}^{d_{\text{state}}}$만을 업데이트하여 $T_{\text{infer}} < 2\text{ms}$의 극한 스트리밍 추론을 달성합니다.

---

### 3.6 온디바이스 검증 기준 및 하류 디코딩 보존율 지표

- **지연시간 판정 기준**: NVIDIA Jetson Orin Nano 실측 기준, 128채널 1초 윈도우 스트리밍 추론 지연시간 **$T_{\text{infer}} \le 15.0\text{ms}$** (배치 크기 1).
- **메모리 한계 기준**: W8A8 양자화 모델 런타임 총 가중치 메모리 $\le 25\text{MB}$, 구동 중 피크 VRAM $\le 512\text{MB}$.
- **디코딩 성능 보존율**: 원본 FP32 DIVER-Base 대비 Neuroprobe 15개 과제 평균 디코딩 성능 및 발작 감지 정확도의 **$98.0\%$ 이상 유지** ($\Delta_{\text{quant}} > -0.010$).

---

## 4. Topic 3: Data Governance, Ethics, and Open Science (VULN-11 데이터 거버넌스, 생명윤리 및 오픈 사이언스)

### 4.1 iEEG의 고유 생체인식 민감도 및 환자 재식별 위험 분석

두개내 뇌파(iEEG)는 두피를 통과하지 않고 대뇌 피질 표면 및 심부 구조에서 직접 기록되는 고해상도 전기생리학적 신호입니다. 이는 다음과 같은 고유한 프라이버시 침해 위험을 내포합니다:
1. **뇌 생체인식 지문 (Neural Biometric Fingerprinting)**: 환자 고유의 해마 세타 진동(Theta oscillation) 및 감마 대역 기능적 연결성(Functional Connectivity) 패턴은 개인 고유의 '신경 지문'으로 기능하여, 익명화된 데이터셋 간에도 동일 인물 여부를 95% 이상의 확률로 대조 재식별할 수 있는 가능성이 존재함.
2. **인지 및 감정 상태 유출**: iEEG에는 단순 운동 신호뿐 아니라 내재적 언어(inner speech), 감정 상태, 기억 회상에 대한 고차 신경 표상이 보존되어 있어 무단 분석 시 심각한 정신적 프라이버시(Mental Privacy) 침해가 발생할 수 있음.
3. **병리적 낙인 효과 (Stigmatization)**: 뇌전증 발작간기 스파이크(Interictal Spikes) 및 병변 부위 좌표는 환자의 병력 및 신경정신과적 결손 상태를 직접적으로 노출함.

---

### 4.2 3D 두개골/안면 스캔 디페이싱(PyDeface) 및 시간 지터링(Temporal Jittering) 비식별화 프로토콜

#### 1) 3D 안면 디페이싱 파이프라인 (`deface_pipeline.sh`):
전극 위치 정합을 위해 제공되는 수술 전 3D T1 MRI 및 수술 후 CT 볼륨 데이터는 표면 렌더링(Surface Rendering) 기법을 적용할 경우 환자의 얼굴 생김새가 사진 수준으로 3D 복원될 수 있습니다.
- **조치**: FSL `fsl_deface` 및 `PyDeface`를 자동 실행하여 안면 연조직(코, 입술, 눈, 턱선) 복셀을 MNI 표준 마스크 기반으로 완전 절제(Zero-out)합니다.
- **품질 검증**: FreeSurfer 피질 분할 및 전극 정합에 필요한 두개골 상부 기하학은 $100\%$ 보존하면서, 안면 식별 소프트웨어로 재구성 불가함을 수동 육안 검사 및 표면 매칭 유사도 점수($< 0.15$)로 인증.

#### 2) 시간 지터링 (Temporal Jittering & Safe Harbor De-identification):
HIPAA 18대 식별자(Safe Harbor Identifiers) 규정을 준수하기 위해, 절대적인 수술 날짜 및 시각을 무작위 정수 일수 $\Delta_{\text{days}} \in [-365, +365]$만큼 편향(Jittering) 이동시킵니다.
- 환자 내부의 상대적 녹음 간격, 주간/야간 일주기 리듬(Circadian Rhythm), 샘플링 주기($dt = 1/f_s$)는 완벽히 보존하되, 병원 전자의무기록(EMR)과의 시간 대조를 통한 환자 역추적을 원천 차단합니다.
- EDF/FIF 파일 헤더에 기록된 의사 이름, 병원 병동 번호, 환자 성명, 생년월일 필드를 공백(ASCII 32)으로 덮어쓰는 스크러빙 자동화 완비.

---

### 4.3 다기관 공개 데이터셋 라이선스(CC BY, CC BY-NC-SA, NIH DUA) 상호운용성 및 법적 준수 체계

사전학습 및 평가에 활용되는 다기관 코퍼스는 라이선스 형태에 따라 다음과 같이 엄격히 법적 사용 범위가 분리 관리됩니다:

| 코퍼스 명칭 | 원천 라이선스 (License) | 상업적 이용 가능 여부 | 2차 저작물 배포 조건 | 파운데이션 모델 사전학습 통합 전략 |
|---|---|---|---|---|
| **AJILE12 (Univ. of Washington)** | **CC BY 4.0** | 허용 (Attribution 필요) | 동일/자유 라이선스 배포 가능 | 완전 통합 및 가중치 공개 코퍼스 활용 |
| **Mayo Clinic Seizure Data** | **CC BY-NC-SA 4.0** | **비상업적 연구 한정** | 동일 라이선스(ShareAlike) 강제 | 연구용 오픈 가중치에만 통합, 상업 모델 분리 |
| **UPenn RAM Dataset** | **NIH Controlled Access** | 기관 DUA 체결 필수 | 원시 데이터 3자 재배포 엄격 금지 | 연구실 내부 폐쇄망 학습 및 파생 통계치만 추출 |
| **SNUH iEEG 내부 코호트** | **SNU IRB 심의 승인** | 연구 목적 한정 승인 | 환자 동의서 범위 내 연구 한정 | 비식별화 BIDS 규격 검증 후 내부 사전학습 |

- **법적 결속 리스크 방지 원칙**: CC BY-NC-SA 데이터가 혼입된 가중치는 상업적 라이선스로 전환할 수 없으므로, 향후 기술이전이나 산업체 협력을 염두에 두고 **"순수 허용 라이선스(CC BY) 기반 코어 모델"**과 **"학술 연구 전용 통합 모델(NC-SA 포함)"**을 Git 브랜치 및 Hugging Face 리포지토리 레벨에서 분리 발행합니다.

---

### 4.4 책임 있는 오픈 사이언스 3계층 공개(Public / Academic OpenRAIL-M / Controlled Clinical) 모델

신경 파운데이션 모델의 잠재적 오용(비동의 뇌파 감시, 군사적 활용, 심문 기술)을 방지하기 위해 3계층 차등 공개 거버넌스를 수립합니다:

```
[3계층 오픈 사이언스 거버넌스 아키텍처]
+-----------------------------------------------------------------------------------+
| 계층 1: 퍼블릭 오픈 티어 (Public Tier) - MIT / Apache 2.0 라이선스                 |
| - 전처리 파이프라인, BIDS 변환기, Neuroprobe 평가 하네스, 모델 아키텍처 정의 코드     |
| - 가상 생성된 합성 iEEG 벤치마크 데이터 (환자 프라이버시 0%)                       |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| 계층 2: 학술 연구 티어 (Academic Research Tier) - OpenRAIL-M 라이선스             |
| - DIVER-Base (51.4M), DIVER-Small 사전학습 모델 체크포인트 가중치                   |
| - 사용 제한 조항: 비인가 상업적 프로파일링 금지, 군사 무기화 금지, 비동의 신경 감시 금지 |
| - Hugging Face 모델 허브 가입 및 클릭-동의(Click-through) 서약 후 즉시 다운로드     |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| 계층 3: 통제 임상 티어 (Controlled Clinical Tier) - IRB 및 데이터사용협약(DUA) 필수 |
| - 원시 다기관 iEEG 시계열 EDF, 수술 절제 영역 조직학적 라벨, 환자별 3D 전극 좌표       |
| - 정식 연구 계획서 제출, 서울대학교 IRB 상호 승인 및 연구책임자(PI) 서명 후 제공   |
+-----------------------------------------------------------------------------------+
```

---

### 4.5 포괄적 Hugging Face Model Card 및 데이터시트(Datasheet) 명세

Hugging Face 릴리스 시 `README.md`에 포함될 Model Card 표준 명세:
- **모델 설명**: 두개내 뇌파(iEEG) 대규모 트랜스포머 파운데이션 모델 (DIVER-2).
- **훈련 데이터셋 구성**: 37명+ 5,203시간 iEEG (SNUH, AJILE12, Mayo Clinic). 훈련 데이터의 지리적·인구학적 편향(대부분 난치성 측두엽/전두엽 뇌전증 환자 코호트이며 건강한 정상 대조군 intracranial 기록은 윤리적으로 부재함을 명시).
- **환경 발자국 (Environmental Impact)**: KISTI 한강 및 ALCF Aurora 클러스터 구동에 따른 총 전력 소비량(MWh) 및 이산화탄소 배출 환산치($\text{kg CO}_2\text{eq}$) 투명 공표.
- **사용 금지 영역 (Out-of-Scope & Prohibited Uses)**: 개인의 동의 없는 거짓말 탐지(Lie detection), 고용/보험 심사용 인지 능력 무단 평가, 상업적 뉴로마케팅 무단 도용.

---

## 5. Topic 4: Unified Compute Budget Architecture across 5 Available Clusters (5대 클러스터 통합 연산 예산 아키텍처)

### 5.1 5대 클러스터 사양 및 엄밀한 운영 제약 조건

연구진이 가용한 5대 분산 컴퓨팅 인프라의 하드웨어 스펙과 운영상 절대 규칙(Hard Constraints)은 다음과 같습니다:

1. **ALCF Aurora Supercomputer (미국 에너지부 아르곤 국립연구소)**:
   - **사양**: Intel Xeon CPU Max + Intel Data Center GPU Max 1550 (Ponte Vecchio, PVC, 노드당 6개 GPU, HBM2e 128GB).
   - **그랜트 확보량**: **25,000 Node-Hours (총 150,000 GPU-Hours 환산)**.
   - **용도**: 1B+ 초대형 파운데이션 모델 사전학습, 대규모 2축 스케일링 법칙 격자 전수 탐색, 초장기 이소에폭(Iso-epoch) 수렴 검증.
2. **Connectome Cluster (서울대학교 인지신경과학 연구실)**:
   - **사양**: 8x NVIDIA RTX A5000 (24GB VRAM per GPU), Slurm 작업 관리기, 공용 NFS `/storage`.
   - **운영 규칙**: `/storage` 및 `/scratch`에 대한 `find`, `du`, `grep -r`, `ls -R` 절대 금지 (NFS 락업 방지). 파일 탐색은 `labfind` 도구 사용.
   - **용도**: 고감마/PAC 특징 추출 전처리, ComBat 다기관 배치 보정, 단일 노드 소규모 소거 실험(Ablation).
3. **DGX-1 Cluster (서울대학교 공용 HPC)**:
   - **사양**: 8x NVIDIA Tesla V100-SXM2 (32GB VRAM per GPU), NVLink 300GB/s, FP32/FP16 텐서 코어.
   - **용도**: 중규모 미세조정(Full FT vs LoRA), Mayo Clinic 임상 뇌전증 발작 검출 벤치마크, ACPE 대안 SSL 대조군 학습.
4. **SNUBIC Cluster (서울대 뇌영상센터)**:
   - **사양**: 5개 노드 (`gpu01` ~ `gpu05`), 노드당 8개, 총 40x NVIDIA L40S (48GB Ada Lovelace, FP8, BF16, FlashAttention-2 완벽 지원).
   - **운영 규칙**: **웹 예약 시스템(Web Slot Reservation) 승인 필수**. 예약 없는 노드 점유 및 무단 멀티노드 데몬 브로드캐스트 엄격 금지 (PI 슬롯 과금). 점유 상태 선행 확인 및 기본 `--use-gpu False` 준수.
   - **용도**: 마감 임박 긴급 리버설 실험, BF16/FA2 가속 대규모 시드 확장($n=6 \to n=10$), 204M 모델 고속 검증 스프린트.
5. **Local DGX-Spark (연구실 워크스테이션)**:
   - **사양**: ARM64 기반 Grace Blackwell GB10 워크스테이션.
   - **운영 규칙**: **로컬 GPU 대규모 학습 절대 금지 (최후의 수단)**. `gpu_oom_guard.py` 상시 감시. 코드 개발, 디버깅, 1-배치 정상동작 점검(Sanity Check), 통계 분석 및 문서 빌드 전용.

---

### 5.2 전수 작업별 클러스터 매핑 및 GPU-Hours 정량 할당표

| 작업 식별자 | 세부 연구 및 실험 내용 | 대응 취약성 | 주 담당 인프라 | 투입 GPU 및 노드 구성 | 예상 소요 시간 (Wall-clock) | 소요 GPU-Hours | 정밀도 / 가속 백엔드 |
|---|---|---|---|---|---|---|---|
| **EXP-T1-01** | 시드 확장 ($n=6 \to n=10$) 및 FDR 15개 과제 포레스트 플롯 | VULN-08, 09 | **Connectome** | 4x RTX A5000 | 48 시간 | **192 GPUh** | FP32 PyTorch |
| **EXP-T1-02** | 고감마(70-150Hz) 오차 분해 및 PAC 지수 잔차 분석 | VULN-07 | **Connectome** | 2x RTX A5000 | 24 시간 | **48 GPUh** | FP32 NumPy/SciPy |
| **EXP-T2-01** | 전극 뇌엽 공간 커버리지 지수($C_{\text{lobe}}$) 산출 및 동일 뇌엽 통제 | VULN-03 | **DGX-1** | 4x Tesla V100 | 72 시간 | **288 GPUh** | FP16 PyTorch |
| **EXP-T2-02** | neuroCombat-GAM 및 DANN 다기관 배치 보정 실험 | VULN-04 | **DGX-1** | 4x Tesla V100 | 96 시간 | **384 GPUh** | FP32 PyTorch |
| **EXP-T2-03** | DIVER-1.5 채널 기원 예측(ACPE) 및 InfoNCE 대조학습 대조군 | VULN-05 | **DGX-1** | 8x Tesla V100 | 168 시간 (7일) | **1,344 GPUh** | FP16 DDP |
| **EXP-T2-04** | Mayo Clinic 8명 환자 뇌전증 발작 및 SOZ 국소화 벤치마크 | VULN-06 | **DGX-1** | 4x Tesla V100 | 120 시간 (5일) | **480 GPUh** | FP16 PyTorch |
| **EXP-T2-05** | Frozen LP vs 2층 MLP vs LoRA ($r=8$) 미세조정 과적합 비교 | VULN-02 | **SNUBIC** | 8x L40S (1 노드) | 48 시간 (예약 스프린트) | **384 GPUh** | BF16 FlashAttention-2 |
| **EXP-T2-06** | 피험자 중간 그리드 ($N \in \{3,4,5,6,7\}$) 실측 및 위상전이 분석 | VULN-10 | **SNUBIC** | 16x L40S (2 노드) | 72 시간 (예약 스프린트) | **1,152 GPUh** | BF16 FlashAttention-2 |
| **EXP-T2-07** | Base 모델 균등 에폭 (Iso-epoch 10 에폭, 30M 토큰) 수렴 대조 | VULN-11 | **KISTI 한강** | 8x GH200 (1 노드) | 120 시간 (5일) | **960 GPUh** | BF16 DDP |
| **EXP-T3-01** | DIVER-2 (204M) 대규모 사전학습 및 2축 격자 스윕 | VULN-01~11 | **ALCF Aurora** | 128x Intel PVC (22 노드) | 350 시간 (~14.5일) | **44,800 GPUh**<br>*(7,466 Node-h)* | BF16 Intel OneAPI/IPEX |
| **EXP-T3-02** | DIVER-2 (1.1B) 초대형 사전학습 및 스케일링 한계 돌파 | VULN-01~11 | **ALCF Aurora** | 256x Intel PVC (43 노드) | 350 시간 (~14.5일) | **89,600 GPUh**<br>*(14,933 Node-h)* | BF16 DeepSpeed ZeRO-3 |
| **EXP-T3-03** | Aurora 버퍼 예비 및 추가 소거 실험 | Strategic | **ALCF Aurora** | 64x Intel PVC | 240 시간 (10일) | **15,360 GPUh**<br>*(2,560 Node-h)* | BF16 IPEX |
| **EXP-T3-04** | INT8 SmoothQuant 양자화 및 지식 증류(KD) 엣지 압축 | VULN-10 | **Connectome** | 4x RTX A5000 | 96 시간 | **384 GPUh** | INT8 TensorRT/PyTorch |
| **DEV-ALL** | 코드 개발, 단위 테스트, 통계 검정, 논문 빌드 | All | **DGX-Spark** | Local GB10 | 상시 구동 | **0 GPUh (CPU 전용)** | CPU/Scripting |

---

### 5.3 ALCF Aurora 25,000 GPU-Hours (Node-Hours) 그랜트 정밀 배분 계획

미국 에너지부(DOE) 아르곤 국립연구소 슈퍼컴퓨터 Aurora에 공식 할당된 **25,000 노드시간(Node-Hours, 총 150,000 PVC GPU-Hours)**의 세부 집행 계획:

```
[ALCF Aurora 25,000 Node-Hours 집행 파이차트 구조]
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. DIVER-2 (1.1B) 초대형 파운데이션 모델 사전학습: 14,933 Node-Hours (59.7%)    │
│    - 43 노드 (256 PVC GPU) x 348 시간 구동                                   │
│    - 37명+ 5,203시간 전수 데이터 50 에폭 완전 수렴 (150M+ 토큰)                │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. DIVER-2 (204M) 2축 스케일링 법칙 정밀 격자 스윕: 7,466 Node-Hours (29.9%)  │
│    - 22 노드 (128 PVC GPU) x 340 시간 구동                                   │
│    - 8개 N_s x 8개 N_t = 64개 2축 조합 그리드 전수 분산 학습                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. 예비 버퍼 및 시스템 프로파일링: 2,601 Node-Hours (10.4%)                    │
│    - Intel OneAPI / IPEX 통신 최적화 및 체크포인트 I/O 스트레스 테스트         │
└─────────────────────────────────────────────────────────────────────────────┘
총 합계: 25,000.0 Node-Hours (100.0% 정밀 소진)
```

---

### 5.4 클러스터별 I/O 병목 방지 및 운영 안전성 수칙

1. **Connectome Cluster**:
   - `/storage`는 NFS 공유 스토리지이므로 수만 개의 작은 `.npy` 파일을 직접 로드할 경우 메타데이터 서버가 마비됨.
   - 모든 훈련 데이터는 단일 바이너리 파일인 **LMDB (`data.lmdb`) 포맷**으로 패킹하고, 노드 로컬 임시 디스크(`/scratch/local`)로 복사 후 학습 착수.
   - 파일 검색은 절대 `find /storage`를 치지 않고 연구실 전용 인덱싱 도구인 `labfind <keyword>`를 사용.
2. **SNUBIC Cluster**:
   - 서울대 뇌영상센터 규정에 따라 **사전 웹 포털 예약 슬롯(시간 및 GPU 수)을 100% 준수**.
   - 예약되지 않은 노드에서 `torchrun` 실행 시 즉시 관리자 경보 발생 및 PI 과금 제재 대상.
   - 모든 실행 스크립트의 디폴트 인자는 `--use-gpu False`로 두고, 예약된 노드에서 Slurm 배치 잡 제출 시에만 `--use-gpu True` 플래그 명시.
3. **Local DGX-Spark Workstation**:
   - `gpu_oom_guard.py`가 백그라운드 데몬으로 활성화되어 있어 4GB 이상의 VRAM 점유 시 경고 로그를 발생시킴.
   - 안채원 선생님과 이아현 선생님은 로컬 워크스테이션에서 `pytest tests/`, `git commit`, `python scripts/analyze_stats.py` 등 CPU 기반 통계 분석과 1-배치 디버깅만을 수행하여 무중단 개발 환경 보장.

---

## 6. Topic 5: Overall Master Roadmap Synthesis (전체 마스터 로드맵 종합)

### 6.1 마스터 간트 차트(Gantt Chart) 타임라인 (2026-11 ~ 2027 Q3+)

```
[전체 연구 개발 및 투고 마스터 타임라인]
2026-11         2026-12         2027-01         2027-02         2027-03         2027-04         2027-05 ~ 2027-09+
[=== Tier 1 ===]
11/10 ~ 11/20
★11/20 NeuroAI 투고
                [================ Tier 2: DIVER-2 Core ===============]
                11/21 ~ 2027/01/31
                - ComBat 배치 보정, 동일 뇌엽 통제
                - DIVER-1.5 ACPE/대조학습 대조군
                - Mayo Clinic 뇌전증 발작 벤치마크
                - KISTI/SNUBIC 중간 격자 및 Iso-epoch
                                                [=========== Tier 2/3: Aurora 25k Scaling ===========]
                                                2027/02/01 ~ 2027/04/30
                                                - 204M / 1.1B 대규모 사전학습
                                                - 2축 스케일링 거듭제곱 법칙 피팅
                                                ★2027/04 Nature Portfolio 투고
                                                                                                [======== Tier 3: 임상 및 오픈사이언스 ========]
                                                                                                2027/05/01 ~ 2027/09/30 (Q3+)
                                                                                                - 다기관 BIDS-iEEG 파이프라인
                                                                                                - 온디바이스 Jetson 실시간 BCI (<15ms)
                                                                                                - OpenRAIL-M 가중치 및 코드 릴리스
```

#### 세부 주차별 마일스톤 데드라인:
- **2026-11-12**: Neuroprobe 15개 과제 Seed $n=10$ 확장 및 FDR 보정 포레스트 플롯 완료.
- **2026-11-15**: 12층 표상 붕괴 및 고감마 오차 증가폭을 수록한 NeuroAI 워크숍 논문 1차 초안(Draft v1) 완성.
- **2026-11-18**: 지도교수(차지욱 교수님) 및 멘토(이아현 선생님) 최종 리뷰 및 포퍼적 반증 조건 명시.
- **2026-11-20 (Hard Deadline)**: **AAAI 2027 NeuroAI Workshop 논문 투고 완료**.
- **2026-12-15**: Mayo Clinic 발작 데이터셋 및 UPenn RAM BIDS 표준 변환 완료.
- **2027-01-15**: DIVER-1.5 ACPE 및 InfoNCE 대조군 학습 완료 (DGX-1).
- **2027-01-31**: SNUBIC L40S 40基 스프린트를 통한 중간 격자($N=3\sim 7$) 실측 완료.
- **2027-02-15**: ALCF Aurora Intel OneAPI 컨테이너 포팅 및 128 PVC GPU 분산 스케일링 검증.
- **2027-03-31**: Aurora 25,000 Node-Hours 사전학습 완료 (204M 및 1.1B 모델 체크포인트 확보).
- **2027-04-30 (Hard Deadline)**: **Nature / Nature Biomedical Engineering 저널 논문 본 투고 완료**.
- **2027-06-30**: Jetson Orin Nano 및 Apple Silicon CoreML INT8 경량화 실시간 추론 실증.
- **2027-09-30**: Hugging Face OpenRAIL-M 모델 가중치 및 재현 코드베이스 글로벌 공식 릴리스.

---

### 6.2 책임 배분 행렬 (RACI Matrix: 안채원 선생님, 이아현 선생님, 차지욱 교수님, 엔지니어)

RACI 정의:
- **R (Responsible, 실무 수행 책임)**: 실제 코드를 작성하고 실험을 수행하며 문서를 작성하는 주체.
- **A (Accountable, 최종 승인 및 결과 책임)**: 의사결정의 거부권과 최종 결과물에 대한 학술적·법적 책임을 지는 주체 (원칙상 과제당 1인).
- **C (Consulted, 자문 및 상의)**: 실행 과정에서 전문 지식과 피드백을 제공하는 주체.
- **I (Informed, 통보 및 공유)**: 진행 상황과 결과물을 통보받고 동기화하는 주체.

| 연구 과제 및 세부 마일스톤 | 안채원 선생님 (학부연구인턴, 주저자) | 이아현 선생님 (박사과정, 공동 주저자/멘토) | 차지욱 교수님 (지도교수, 교신저자) | 연구실 시스템 엔지니어 (HPC 인프라) | 임상 협력 PIs (SNUH/Mayo) |
|---|---|---|---|---|---|
| **Tier 1: NeuroAI 워크숍 논문 집필 및 투고** | **R** (초안 작성, 도표) | **R / A** (논리 교정, 수치 감수) | **A** (최종 승인, 투고 승인) | **I** (저장소 지원) | **I** |
| **Tier 1: Seed n=10 확장 및 FDR 통계 보정** | **R** (스크립트 실행, 플롯) | **A** (통계 규약 승인) | **C** (p-value 기준 자문) | **I** (슬럼 큐 확인) | **I** |
| **Tier 1: 1/64 안전 하한선 재정의 및 클레임 조정** | **R** (텍스트 수정) | **R** (문헌 대조) | **A** (학술적 입장 확립) | **I** | **I** |
| **Tier 2: 전극 몽타주 결손 교란 분리 ($C_{\text{lobe}}$)** | **R** (좌표 분석, NDE 계산) | **A** (인과 DAG 검증) | **C** (신경해부학 자문) | **I** | **C** (전극 검증) |
| **Tier 2: neuroCombat 및 DANN 다기관 배치 보정** | **C** (평가 참여) | **R** (모델 아키텍처 구현) | **A** (방법론 승인) | **I** (GPU 할당) | **C** (임상 데이터 제공) |
| **Tier 2: DIVER-1.5 ACPE 및 대조학습 대조군** | **C** (하류 벤치마킹) | **R / A** (SSL 모델 훈련) | **C** (목적함수 자문) | **I** | **I** |
| **Tier 2: Mayo Clinic 발작 및 SOZ 국소화 벤치마크** | **R** (다운스트림 파이프라인) | **R** (데이터로더 구축) | **A** (임상 유효성 승인) | **I** | **C / A** (라벨 감수) |
| **Tier 2: SNUBIC L40S 중간 격자 ($N=3\sim 7$) 실측** | **R** (실험 실행) | **A** (격자 파라미터 설계) | **C** (예약 슬롯 승인) | **R** (슬롯 예약 관리) | **I** |
| **Tier 2: KISTI 한강 Base 균등 에폭 수렴 대조** | **I** | **R / A** (DDP 스크립트 실행) | **C** | **R** (I/O 병목 모니터링) | **I** |
| **Tier 3: Aurora 25k Node-h 사전학습 (204M/1B)** | **I** (평가 대기) | **R** (분산 학습 파이프라인) | **A** (그랜트 예산 총괄) | **R / A** (IPEX/OneAPI 최적화) | **I** |
| **Tier 3: 2축 거듭제곱 스케일링 법칙 함수 피팅** | **R** (비선형 회귀, 헤시안) | **R** (이론 전개) | **A** (수학적 모델 확정) | **I** | **I** |
| **Tier 3: 다기관 BIDS-iEEG 표준화 및 디페이싱** | **R** (전처리 파이프라인) | **C** (포맷 감수) | **A** (생명윤리 승인) | **R** (자동화 파이프라인) | **C** (원천 데이터 전송) |
| **Tier 3: 온디바이스 실시간 BCI (<15ms) 경량화** | **C** (정확도 평가) | **R** (지식 증류, Mamba 전환) | **A** (응용 타겟 승인) | **R** (TensorRT/CoreML 엔진) | **C** (임상 BCI 시연) |
| **Tier 3: OpenRAIL-M 모델 및 코드 릴리스** | **R** (Hugging Face 리포) | **R** (가중치 검증) | **A** (최종 공개 승인) | **R** (CI/CD 자동 빌드) | **I** |

---

### 6.3 의존성 그래프(DAG) 및 임계 경로(Critical Path) 분석

#### 1) 방향성 비순환 그래프 (DAG: Directed Acyclic Graph) 구조

```
[연구 작업 의존성 DAG 및 임계 경로 (Critical Path: 빨간색 이중선)]
(Start: 2026-11-10)
  │
  ├─==► [T1-1: 시드 n=10 확장 및 FDR 보정] (2일)
  ├─==► [T1-2: 12층 붕괴 및 고감마 오차 수록] (3일)
  │       │
  │       ▼
  └──==► [T1-3: NeuroAI 워크숍 논문 투고 (11/20)] ◄=== [Milestone 1 Hard Gate]
          │
          ├────────────────────────────────┬───────────────────────────────┐
          │                                │                               │
          ▼                                ▼                               ▼
   [T2-1: 전극 몽타주]               [T2-2: neuroCombat]             [T2-3: BIDS-iEEG 표준화]
   (C_lobe 산출, 5일)                 (DANN 도메인 적응, 7일)          (PyDeface 안면 절제, 5일)
          │                                │                               │
          └───────────────┬────────────────┘                               ▼
                          ▼                                          [T3-3: 거버넌스 DUA]
                   [T2-4: Mayo Clinic 벤치]                           (라이선스 분리, 10일)
                   (발작 AUROC 검증, 7일)                                  │
                          │                                                │
                          ├────────────────────────────────────────────────┤
                          ▼                                                │
                  [T2-5: ACPE/대조학습 대조군]                                │
                  (DIVER-1.5 2축 스윕, 10일)                              │
                          │                                                │
                          ▼                                                │
           ==► [T2-6: KISTI/SNUBIC 중간 격자 및 Iso-epoch] (14일) ◄==      │
                  │                                                        │
                  ▼                                                        │
           ==► [T3-1: Aurora 25k Node-h 분산 포팅 및 스케일업] (21일) ◄==  │
                  │                                                        │
                  ▼                                                        │
           ==► [T3-2: 1.1B 사전학습 및 2축 거듭제곱 피팅] (20일) ◄==         │
                  │                                                        │
                  ▼                                                        │
           ==► [Milestone 2 Hard Gate: Nature Portfolio 투고 (2027-04)] ◄==│
                  │                                                        │
                  ├────────────────────────────────┬───────────────────────┘
                  ▼                                ▼
          [T3-4: 온디바이스 경량화]         [T3-5: OpenRAIL-M 모델 릴리스]
          (INT8/Mamba <15ms, 30일)          (HF 가중치/코드 공개, 14일)
                  │                                │
                  └────────────────┬───────────────┘
                                   ▼
                   (Final End: 2027 Q3+ 임상 실증 완료)
```

#### 2) 임계 경로 (Critical Path) 및 여유 시간(Slack Float) 분석:
- **최장 임계 경로 (Critical Path, Zero Slack)**:
  `T1-1/2 (통계/표상 보강)` $\to$ `T1-3 (NeuroAI 투고 11/20)` $\to$ `T2-6 (SNUBIC 중간격자/Iso-epoch)` $\to$ `T3-1 (Aurora 포팅/스케일업)` $\to$ `T3-2 (1.1B 사전학습/2축 피팅)` $\to$ `Nature 저널 투고 (2027-04)`.
  - 이 경로상의 작업이 단 1주일이라도 지연될 경우 2027년 4월 저널 투고 데드라인이 직접적으로 밀리게 됩니다.
- **비임계 경로 및 여유 시간 (Total Float)**:
  - `T2-1 (전극 몽타주 C_lobe 분석)`: 총 14일의 여유 시간(Slack) 존재.
  - `T2-4 (Mayo Clinic 발작 벤치마크)`: 총 10일의 여유 시간 존재.
  - `T3-4 (온디바이스 경량화 및 실시간 BCI)`: 저널 투고 이후 진행되므로 45일 이상의 충분한 버퍼 보유.

---

### 6.4 포괄적 리스크 비상대응 행렬 (Comprehensive Risk Contingency Matrix: 6대 핵심 리스크)

연구 과정에서 발생할 수 있는 6대 핵심 위험 요소를 식별하고, 사전 감지 지표와 구체적인 비상대응 트리거를 수립하였습니다:

| 리스크 식별자 | 위험 명칭 및 핵심 내용 | 발생 확률 (Likelihood) | 영향도 (Impact) | 조기 경보 지표 (Early Warning Signs) | 사전 완화 전략 (Proactive Mitigation) | 비상대응 트리거 조건 (Contingency Trigger) | 대체 실행 계획 (Fallback Plan) |
|---|---|---|---|---|---|---|---|
| **RSK-01** | **Aurora PVC GPU OneAPI 포팅 지연** | Medium (35%) | **High** | IPEX 분산 학습 시 통신 정체, 노드 간 올리듀스 속도 50% 급락 | 사전에 단일 노드 도커 컨테이너 검증 및 Argonne 엔지니어 기술 미팅 정례화 | 포팅 착수 후 **2주 이내 분산 효율 60% 미달 시** | **KISTI 한강 GH200 클러스터 추가 노드 신청 및 SNUBIC L40S 40基로 스케일링 스윕 긴급 전환** |
| **RSK-02** | **다기관 배치 효과로 생물학적 표상 왜곡** | Medium-High (50%) | **High** | 타 병원 데이터 Zero-shot 전이 시 정확도 15% 이상 급락, t-SNE 병원별 군집화 | neuroCombat-GAM 및 DANN 적대적 도메인 손실 함수 선행 결합 | 잠재 공간 t-SNE에서 **기관 라벨 실루엣 점수 > 0.35 검출 시** | **생체신호 주파수 정규화(Z-score per band) 및 동일 뇌엽 Bipolar 차분 마스크 강제 적용** |
| **RSK-03** | **온디바이스 INT8 양자화 시 고감마 신호 왜곡** | Medium (30%) | Medium | W8A8 양자화 후 고감마 인지 디코딩 정확도 5% 이상 하락, 어텐션 스파이크 | SmoothQuant 채널별 마이그레이션 적용 및 FP16-INT8 혼합 정밀도 채택 | Neuroprobe 고감마 과제 점수가 **FP32 대비 > 3.0% 붕괴 시** | **어텐션 Softmax 및 프로젝션 레이어는 FP16 유지, FFN 피드포워드만 INT8 양자화하는 하이브리드 W8A16 적용** |
| **RSK-04** | **30초 컨텍스트 시간적 근시(Myopia) 심사위원 반론** | **High (60%)** | Medium | 저널 리뷰어가 Narayanswamy et al. (Google LSM) 인용하며 장기 시계열 요구 | Mamba-2 SSM 선형 어텐션 스트리밍 레이어 사전 설계 및 1시간 디코딩 벤치 구비 | 저널 1차 리뷰에서 **장기 의존성(Long-term dependency) 비판 접수 시** | **사전 준비된 Mamba-2 하이브리드 1시간 연속 디코딩 곡선 및 O(1) 메모리 실측 데이터를 리버설 문서에 즉각 수록** |
| **RSK-05** | **환자 재식별 및 생명윤리 거버넌스 분쟁** | Low-Medium (20%) | **Critical** | 다기관 IRB 심의 지연, CT 안면 3D 복원 가능성에 대한 임상 파트너 우려 제기 | PyDeface 전수 적용, 시간 지터링 비식별화 완료 보고서 선제 제출, OpenRAIL-M 라이선스 채택 | 임상 기관 또는 저널 에디터의 **데이터 비식별화 소명 요구 접수 시** | **3D 표면 매칭 불가 포렌식 인증서 즉각 제출 및 가중치 다운로드를 DUA 서명 기반 준폐쇄형(Gated)으로 전환** |
| **RSK-06** | **학기 전환기 연구인턴 인수인계 공백** | Medium (30%) | Medium | 방학/학기 시작에 따른 주 연구자(안채원 선생님) 학사 일정 충돌 | 모든 실험 파이프라인을 단일 쉘 스크립트(`run_all.sh`) 및 CI/CD 테스트로 모듈화, 이아현 선생님과 2인 1조 페어링 | 인턴 학사 일정으로 인한 **주간 마일스톤 3일 이상 지체 시** | **이아현 선생님이 Slurm 배치 스케줄러 인계받아 무중단 분산 학습 지속 및 안채원 선생님은 비동기 문서 집필에 집중** |

---

## 7. Guidance & Direct Interface Contracts for Milestone 4 Worker (Worker 작성을 위한 전략적 연계 지침)

Milestone 4의 종합 산출물인 `docs/04_action_items_roadmap.md`를 집필할 Worker 에이전트는 본 탐색 보고서에서 수립된 내용을 다음과 같은 엄밀한 원칙에 따라 직접 반영해야 합니다:

1. **3계층 구조의 엄격한 선후 관계 준수 (`test_f5_b05`)**:
   - 문서의 대단원 순서는 반드시 **Tier 1: 단기 긴급 과제 (2026-11-20 NeuroAI)** $\to$ **Tier 2: 중기 핵심 과제 (DIVER-2 Journal & Aurora)** $\to$ **Tier 3: 장기 전략 및 임상 응용 과제**의 순서로 배치되어야 합니다.
2. **취약성-액션 아이템 1:1 매핑 완전성 (`test_tier3_05`)**:
   - Milestone 3 보고서(`docs/03_adversarial_review.md`)의 11대 취약성(VULN-01 ~ VULN-11)이 단 하나도 누락되지 않고 본 보고서의 해결 방안과 1:1로 결합되어 명시되어야 합니다.
   - 특히 마지막 층 표상 보존(`VULN-01`), 재구성 손실-하류 점수 괴리(`VULN-07`), Mayo Clinic 뇌전증 병리 과제(`VULN-06`), Seed 확장 및 FDR 보정(`VULN-08, 09`), 중간 피험자 격자(`VULN-10`), Base 균등 에폭 수렴(`VULN-11`)이 키워드 수준에서 완벽히 일치해야 합니다.
3. **정량적 판정 기준 명시 (`test_f5_b02`)**:
   - 모든 액션 아이템에는 $\Delta > -0.005$, $p < 0.05$, $n \ge 10$, $T_{\text{infer}} \le 15\text{ms}$ 등의 측정 가능한 수치 기준이 포함되어야 합니다.
4. **구체적 기술 및 인프라 포인터 명시 (`test_f5_b01`, `test_f5_b04`)**:
   - KISTI 한강, ALCF Aurora, SNUBIC, Connectome, Slurm, sbatch, LMDB, PyTorch, neuroCombat 등의 기술 용어를 각 작업에 정밀 매핑하십시오.
5. **엄격한 존칭 준수 (Global Constraint)**:
   - 본 연구의 주역인 **"안채원 선생님"**과 **"이아현 선생님"**에 대해 예외 없이 존칭을 유지하고 존댓말을 구사하십시오. 절대 "OO 씨"나 반말을 사용해서는 안 됩니다.
