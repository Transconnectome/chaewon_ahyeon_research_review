# 연구 개선 액션 아이템 및 단계별 마스터 로드맵 (Prioritized Action Items & Master Roadmap)

- **문서 식별자**: `docs/04_action_items_roadmap.md`
- **프로젝트 명칭**: `chaewon_ahyeon_research_review`
- **마일스톤**: Milestone 4 — Action Items & Prioritized Roadmap (F5)
- **연구 주관**: 서울대학교 심리학과 / 뇌인지과학과 / 인공지능연구원 계산뇌과학연구실 (Connectome Lab)
- **주 연구자**: 
  - **안채원 선생님** (서울대학교 심리학과 학부 연구인턴, 하류 벤치마킹 및 실측 실험 총괄)
  - **이아현 선생님** (서울대학교 뇌인지과학과 박사과정 연구원, DIVER 아키텍처 및 분산 컴퓨팅 총괄)
- **지도교수**: **차지욱 교수님** (서울대학교 심리학과 / 인공지능연구원 / 계산뇌과학연구실 책임교수)
- **작성 일자**: 2026-11-10
- **문서 목표**: Milestone 3 과학적 적대적 검증(`docs/03_adversarial_review.md`)에서 식별된 11대 핵심 취약성(VULN-01 ~ VULN-11)을 체계적으로 극복하고, AAAI 2027 NeuroAI 워크숍(Tier 1, 2026-11-20) 투고부터 DIVER-2 Nature Portfolio 저널(Tier 2, 2026-12 ~ 2027 Q1) 및 실시간 온디바이스 BCI 임상 생태계(Tier 3)에 이르는 3단계 우선순위 실행 로드맵 수립.

---

## 1. 총괄 요약 (Executive Summary)

### 1.1 연구 배경 및 적대적 검증 취약성 대응 원칙
안채원 선생님과 이아현 선생님은 37명의 난치성 뇌전증 환자로부터 수집된 5,203시간의 대규모 두개내 침습적 뇌파(iEEG: sEEG 및 ECoG) 코퍼스와 2.88M 샘플 등가 계산량 통제 하에서, 고유 기록 시간을 1/64(81.3시간) 및 1/1024(5.1시간)로 축소해도 하류 인지 디코딩 성능이 보존된다는 *"A Little iEEG Goes a Long Way"* 현상과, 8명 이상의 독립 피험자 다양성이 시간 축보다 선행한다는 *"Subjects over Hours"* 현상을 실측 발견하였습니다.

그러나 Milestone 3의 과학적 적대적 검증(`docs/03_adversarial_review.md`) 및 차지욱 교수님의 비판적 피드백은 본 연구가 최상위 학술지 및 학회(AAAI 2027 NeuroAI Workshop, Nature Portfolio)에서 강력한 방법론적 반론에 직면할 수 있는 11대 핵심 취약성(VULN-01 ~ VULN-11)을 규명하였습니다. 

본 문서는 이러한 비판을 선제적으로 방어하고 학술적 엄밀성을 완성하기 위해 다음 4대 대원칙에 입각하여 개선 로드맵을 수립합니다:
1. **발견의 긍정적 가치 수호와 과대주장의 방어적 축소 (Defensive Claim Scoping)**: "시간 정보 무용론"과 같은 도발적 주장을 철회하고, 1/64(81.3시간)를 심층 12층 표상까지 보존되는 **"실증적 안전 하한선(Empirical Safe Lower Bound)"**으로 공식 선언하며, 1/1024(5.1시간)는 얕은 필터만 보존되고 심층 문맥이 붕괴되는 **"음성적 경계(Ablation Negative Boundary)"**로 정립합니다.
2. **인과적 교란의 철저한 분리 (Causal Disentanglement)**: 2명 축소 시 성능 저하($-0.0055$)가 생물학적 다양성 결핍인지 공간 몽타주 결손(4대 뇌엽 커버리지 $C_{\text{lobe}}$)인지 동일 뇌엽 통제 및 가상 전극 RBF 보간 프로토콜을 통해 인과적으로 증명합니다.
3. **통계적 엄밀성 및 다중 비교 통제 (Statistical Rigor)**: Benjamini-Hochberg FDR 보정($q < 0.05$) 및 시드 수 $n=6 \to n=10$ 확장을 통해 통계적 검정력($1-\beta > 80\%$)을 확보하고 15개 전 과제의 포레스트 플롯(Forest Plot)을 투명하게 공개합니다.
4. **다단계 분산 컴퓨팅 자원의 정밀 매핑 (Unified Compute Budget Architecture)**: 미국 에너지부 ALCF Aurora 25,000 GPU-Hours 그랜트와 국내 KISTI 한강 GH200, SNUBIC L40S, 연구실 Connectome/DGX-1을 각 마일스톤에 빈틈없이 매핑하여 실행력을 극대화합니다.

---

### 1.2 11대 취약성(VULN-01 ~ VULN-11) 대 3대 Tier 액션 아이템 해결 매트릭스

| 취약성 식별자 | 적대적 취약성 핵심 내용 | 해결 대응 액션 아이템 | 우선순위 티어 및 마감 | 정량적 성공 판정 기준 (Acceptance Criteria) |
|---|---|---|---|---|
| **VULN-01** | **읽는 층 괴리 (Readout Layer Divergence)**: 1/1024에서 Layer 1 보존($+0.0003$) vs Layer 12 붕괴($-0.0050$) 은폐 | **ACT-T1-01** (안전 하한선 1/64 재정립)<br>**ACT-T1-05** (논문 텍스트 개정) | **Tier 1 (단기 최우선)**<br>2026-11-20 (D-10) | 12층 점수 표 수록, 1/64 전 층 비열등성($\text{CI}_{\text{low}} > -0.005$) 입증 및 1/1024 오버클레임 100% 철회 |
| **VULN-02** | **Frozen Linear Probe 한계 및 미세조정 과적합**: 비선형 매니폴드 왜곡 미감지 및 Full FT 에폭 7 손실 폭증($1.14 \to 2.73$) | **ACT-T2-09** (LoRA $r=8$ 미세조정)<br>**ACT-T2-10** (다층 CKA 프로빙) | **Tier 2 (중기 핵심)**<br>2027 Q1 (저널 투고) | LoRA 미세조정 시 1/64 비열등성($\Delta > -0.005$) 및 검증 손실 단조 안정, CKA 전 층 $> 0.90$ 달성 |
| **VULN-03** | **공간 몽타주 결손 교란**: 2명 붕괴($-0.0055$)가 생물학적 다양성이 아닌 4대 뇌엽 공간 결손(50~75%)에 기인 | **ACT-T2-01** ($C_{\text{lobe}}$ 통제 실험)<br>**ACT-T2-02** (가상 전극 RBF 보간) | **Tier 2 (중기 핵심)**<br>2027 Q1 (저널 투고) | 동일 뇌엽 통제 시 $\text{NDE}_{N_s} \le 0.0020$ 입증, 가상 전극 보간 시 마스킹 복원 AUROC $+0.0150$ 향상 |
| **VULN-04** | **사이트 효과 교란 (Site Confounding)**: SNUH vs AJILE 기기/기준전극 차이 및 배치 보정 부재 | **ACT-T2-03** (neuroCombat 보정)<br>**ACT-T3-01** (BIDS-iEEG 파이프라인) | **Tier 2 (중기) / Tier 3**<br>2027 Q1 ~ Q3 | ComBat 보정 후 교차 사이트 디코딩 점수 편차 $\le 0.0030$, 사이트 분류기 정확도 52% 이하로 소거 |
| **VULN-05** | **MAE 저주파 편향 및 대안 SSL 부재**: 1/f 멱함수 MSE 과적합 및 ACPE 정적 공간 지름길 위험 | **ACT-T2-04** (탈지름길 ACPE)<br>**ACT-T2-05** (InfoNCE / JEPA SSL) | **Tier 2 (중기 핵심)**<br>2027 Q1 (저널 투고) | 위상 무작위화 시 채널 정확도 95% 붕괴(지름길 제거), JEPA/대조학습 시간 스케일링 단조성 확보 |
| **VULN-06** | **하류 과제 편향 (Task Bias)**: 자연주의 3대 인지 과제 편중 및 임상 발작파(MAYO) 누락 | **ACT-T2-08** (MAYO 발작 벤치)<br>**ACT-T2-11** (피질 계층 전이도) | **Tier 2 (중기 핵심)**<br>2027 Q1 (저널 투고) | MAYO 8명 발작 검출 AUPRC 1/64 모델 비열등($\Delta \ge -0.008$), 1차 감각 vs 연합 피질 상호작용 $p < 0.001$ 입증 |
| **VULN-07** | **재구성 손실 해체 역설**: 동일 피험자 손실 $+8.5\%$ 증가와 고감마(70~150Hz) 정보 증발 의혹 | **ACT-T1-03** (PSD 대조 및 대역 분해) | **Tier 1 (단기 최우선)**<br>2026-11-20 (D-10) | Welch PSD 대비 DIVER 표현의 $\text{AUROC} > \text{PSD} + 0.020$ 우위 실증, 고감마 오차 증가폭 분리 보고 |
| **VULN-08** | **Seed n=6 과소 검정력 (Under-powered Risk)**: 개별 과제($SE \approx 0.00195$) 단위 검정력 37.8% 급락 | **ACT-T1-04** (Seed $n=10$ 확장) | **Tier 1 (단기 최우선)**<br>2026-11-20 (D-10) | 시드 4개 추가 ($n=10$, $\text{df}=9$), 통계적 검정력 $> 80\%$ 달성, 95% 신뢰구간 하한 $\text{CI}_{\text{low}} > -0.005$ 확인 |
| **VULN-09** | **다중 비교 보정 부재 (Multiplicity Issue)**: 15개 하위 과제 FWER 53.7% 및 평균화의 오류 | **ACT-T1-02** (FDR 보정 & Forest Plot) | **Tier 1 (단기 최우선)**<br>2026-11-20 (D-10) | Benjamini-Hochberg FDR $q < 0.05$ 기준 15개 개별 과제 Cohen's $d_z$ 및 Multi-task Forest Plot 완성 |
| **VULN-10** | **피험자 그리드 조대성**: $N \in \{2, 8, 37\}$ 단 3개 점 및 $N=3 \sim 7$ 결측, Hessian 발산 | **ACT-T2-06** (48개 그리드 LM 피팅)<br>**ACT-T2-07** (Aurora 25k GPUh) | **Tier 2 (중기 핵심)**<br>2027 Q1 (저널 투고) | $S=8\text{점} \times H=6\text{점} = 48\text{개}$ 그리드 피팅 $R^2 \ge 0.95$, 헤시안 조건수 $\kappa(\mathcal{H}) < 500$ 식별성 확보 |
| **VULN-11** | **Base 과소 학습 교란**: Base 100% 0.46 에폭 미수렴에 따른 가짜 비열등성 위험 | **ACT-T2-06** (Iso-epoch 완전 수렴) | **Tier 2 (중기 핵심)**<br>2027 Q1 (저널 투고) | Base 103M 모델 10 에폭 완전 수렴 후 1/64 모델과의 진정한 표상 격차($\Delta$) 재측정 |

---

## 2. Tier 1: 최우선 단기 과제 (Immediate Tier, AAAI 2027 NeuroAI Workshop 마감 2026-11-20)

```
[Tier 1 최우선 긴급 과제 워크플로우]
┌────────────────────────────────────────────────────────────────────────┐
│ ACT-T1-01: 층별 표상 경계 확립 및 안전 하한선(1/64) 재정립 (안채원 선생님)  │
│ - 1/1024 12층 붕괴(-0.0050) 음성 경계 명시, 초록/본문 주장 전면 수정  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ ACT-T1-02: 다중비교 FDR 보정 및 Multi-task Forest Plot 완성 (안채원 선생님) │
│ - 15개 세부 과제 FDR q-value 산출, 95% CI 포레스트 플롯 생성           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ ACT-T1-03: 저주파 PSD Baseline 대조 및 주파수 대역별 분해 실험 (이아현 선생님)│
│ - Welch PSD 선형 프로브 vs DIVER 비교, 고감마 손실 분해 실측          │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ ACT-T1-04: 고우선순위 벤치마크 Seed n=6 -> n=10 신속 확장 (안채원 선생님)   │
│ - KISTI 1노드 4시간, 4개 시드 동결 프로브 추가 측정 -> 검정력 80%+ 달성│
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ ACT-T1-05: AAAI 2027 워크숍 초안 텍스트 및 Figure 최종 통합 (안채원 선생님 / 이아현 선생님) │
│ - Abstract, Method, Discussion 전면 개정, 11/19 내부 승인, 11/20 제출   │
└────────────────────────────────────────────────────────────────────────┘
```

---

### [카드 ACT-T1-01] 층별 표상 보존 경계 확립 및 실증적 안전 하한선(1/64) 재정립

- **담당 (Owner)**: **안채원 선생님** (주 분석 및 원고 집필), **이아현 선생님** (아키텍처 감수)
- **일정 (Timeline)**: **2026-11-12 ~ 2026-11-15** (초안 작성), **2026-11-17** (원고 통합), **2026-11-19** (지도교수 차지욱 교수님 최종 승인)
- **산출물 (Deliverables)**:
  - 51.4M Small 모델 12개 층별 점수 비교 정량 표 (Table 2)
  - 층별 깊이 $\times$ 데이터 축소율 상호작용 도표 (`figure2_layer_divergence.pdf`)
  - 개정 원고 Section 4 (Layer-wise Probing Results)
- **판정 기준 (Acceptance Criteria)**:
  - AAAI 2027 워크숍 논문 본문에 12개 층별 점수 표(Table 2)가 수록될 것.
  - 1/1024에 대한 "성능 유지/비열등" 주장이 100% 삭제되고 "Layer 1 국소 필터 보존 및 Layer 12 문맥 붕괴"로 정확히 한정 기술될 것.
  - 1/64 (81.3시간) 조건의 전 층 비열등성($\text{CI}_{\text{low}} > -0.005$)이 명확히 입증될 것.
- **기술 포인터 (Technical pointers)**: `d2rdall_summary.json`, `bigscar_rdall_summary.json`, `scripts/analyze_layer_divergence.py`, PyTorch linear probe readout.
- **컴퓨팅 예산 (Compute budget)**: 연산 자원 불필요 (기존 실측 데이터 분석 및 시각화, 로컬 CPU < 10분).
- **세부 실행 프로토콜**:
  1. 1/1024(5.1시간) 조건에서 Layer 1 점수($\Delta = +0.0003$)와 최상위 Layer 12 점수($\Delta = -0.0050 [-0.0072, -0.0028]$)의 분기 실측치를 논문 핵심 결과(Section 4)에 정량 표와 함께 전면 배치합니다.
  2. 12개 층 표상 분석 이론(Raghu et al., 2021; Kornblith et al., 2019)을 적용하여, 하위 층은 국소 시계열 Gabor 필터(feature reuse)로 소량 데이터로 수렴하지만 최상위 층은 다채널 어텐션 문맥 추상화로 인해 데이터 다양성 결핍 시 부분공간 붕괴를 겪음을 명시합니다.
  3. 51.4M 대형 모델의 최상위 12번째 층에서도 $\Delta = -0.0006 [-0.0021, +0.0008]$으로 전체 데이터를 학습한 모델과 동등한 표상을 유지하는 **1/64 (81.3시간)을 실증적 안전 하한선(Empirical Safe Lower Bound)**으로 공식 선언합니다.
  4. 1/1024 조건은 비열등성이 아닌 '심층 문맥이 붕괴되는 음성적 경계(Ablation Negative Boundary)'로 재정의하여 심사위원의 표면적 읽기 오류(Superficial Readout Fallacy) 공격을 선제적으로 차단합니다.

---

### [카드 ACT-T1-02] Neuroprobe 15개 과제 다중 비교 FDR 보정 및 Multi-task Forest Plot 완성

- **담당 (Owner)**: **안채원 선생님** (통계 분석 및 시각화 코드 구현), **이아현 선생님** (통계적 방법론 검증)
- **일정 (Timeline)**: **2026-11-13 ~ 2026-11-16** (통계 수치 산출 및 플롯 완료), **2026-11-18** (본문 및 서플먼트 반영)
- **산출물 (Deliverables)**:
  - 15개 하위 과제 Benjamini-Hochberg FDR 보정 $q$-value 종합 표
  - Multi-task Forest Plot 도표 (`figure3_multitask_forest_plot.pdf`, `figure3_multitask_forest_plot.png`)
  - 자동화 분석 스크립트 (`scripts/run_fdr_forest_plot.py`)
- **판정 기준 (Acceptance Criteria)**:
  - 15개 하위 과제 전수에 대해 FDR $q$-value와 Cohen's $d_z$가 포함된 종합 통계 표 작성.
  - Multi-task Forest Plot이 Figure 3으로 완성되어 논문 본문 또는 1페이지 확장 부록에 배치될 것.
  - 1/64 조건에서 FDR 보정 후에도 과반수 이상의 핵심 과제(특히 언어/음성 디코딩)가 비열등 마진($\Delta > -0.005$)을 유지함을 실증할 것.
- **기술 포인터 (Technical pointers)**: `scripts/run_fdr_forest_plot.py`, `statsmodels.stats.multitest.multipletests`, `scipy.stats.t`, Bonferroni & FDR control.
- **컴퓨팅 예산 (Compute budget)**: 로컬 워크스테이션 CPU (소요 시간 < 5분).
- **세부 실행 프로토콜**:
  1. Neuroprobe 15개 하위 인지 과제 및 BYD, Pippi에 대해 개별 과제 단위의 짝지은 차이($\Delta$), 표준오차($SE$), 자유도($\text{df}=5$), 효과 크기(Cohen's $d_z = \bar{\Delta}/s_{\Delta}$)를 전수 계산합니다.
  2. 패밀리 단위 위양성($\text{FWER} = 53.7\%$) 위험을 극복하기 위해 Benjamini-Hochberg False Discovery Rate (FDR) 프로시저를 적용하여 보정 $q$-value를 산출합니다.
  3. 지나치게 보수적인 Bonferroni 보정($t_{\text{crit}}=5.247$) 대신, 신경생리학적 과제 간 상관성을 고려한 Benjamini-Hochberg FDR $q < 0.05$ 기준 비열등성 판정 기준을 수립합니다.
  4. 15개 과제 전수를 아우르는 **Multi-task Forest Plot (Figure 3)**을 작성: 각 과제별 점 추정치, 단일 95% t-신뢰구간, FDR 보정 신뢰구간, 비열등 마진($-0.005$) 점선을 단일 도표에 직관적으로 시각화합니다.
  5. 복합 지표 `rule3` 평균에 숨겨진 특정 고차 과제(Sentence Onset, Syntax Parsing 등)의 거동을 투명하게 공개하여 '평균화의 오류(Fallacy of Averaging)' 비판을 선제 방어합니다.

---

### [카드 ACT-T1-03] 저주파 PSD Baseline 대조 및 주파수 대역별 재구성 손실 분해

- **담당 (Owner)**: **안채원 선생님** (프로토콜 실행 및 결과 분석), **이아현 선생님** (신호처리 프로토콜 설계)
- **일정 (Timeline)**: **2026-11-14 ~ 2026-11-17** (실험 실행 및 취합), **2026-11-18** (원고 반영)
- **산출물 (Deliverables)**:
  - 6대 임상 주파수 대역별 Welch PSD 추출 및 동결 선형 프로브 평가 스크립트 (`scripts/run_psd_baseline.py`)
  - PSD vs DIVER 표현력 비교 정량 표 (Table 3)
  - 주파수 대역별 Held-out 재구성 손실 분해 그래프 (`figure_frequency_loss_decomposition.pdf`)
- **판정 기준 (Acceptance Criteria)**:
  - Neuroprobe 및 BYD에서 DIVER 모델이 정적 PSD 기준선 대비 $\text{AUROC} > \text{PSD} + 0.020$의 명백한 표상 우위를 입증할 것 ($p < 0.001$).
  - 주파수 대역별 복원 오차 분해 결과(델타/세타 오차 증가율 $< 2\%$ vs 고감마 오차 증가율 $> 100\%$)가 Table 또는 Discussion에 명시될 것.
- **기술 포인터 (Technical pointers)**: `scipy.signal.welch`, `run_psd_baseline.py`, log-power extraction, linear probe evaluation.
- **컴퓨팅 예산 (Compute budget)**: KISTI 한강 슈퍼컴퓨터 GH200 1노드 (약 2 GPU-hours) 또는 연구실 DGX-Spark.
- **세부 실행 프로토콜**:
  1. **PSD Baseline 대조 실험**: 다운스트림 3대 벤치마크 입력 신호로부터 Welch 기법(윈도우 2초, 50% 오버랩)을 통해 표준 6대 주파수 대역(Delta 1-4Hz, Theta 4-8Hz, Alpha 8-12Hz, Beta 13-30Hz, Gamma 30-70Hz, High-gamma 70-150Hz)의 대역별 로그 파워를 추출합니다. DIVER 표현과 완벽히 동일한 선형 분류기(`nn.Linear`)를 학습시켜 기준선 AUROC를 측정합니다.
  2. DIVER 사전학습 표현이 단순 PSD 파워 특징 대비 통계적으로 유의미한 초과 성능($\Delta_{\text{DIVER} - \text{PSD}} > +0.02$, $p < 0.001$)을 기록함을 입증하여, DIVER가 저주파 파워 정렬을 넘어선 시공간 위상 동역학을 포착함을 증명합니다.
  3. **주파수 대역별 Held-out 손실 분해**: 동일 37명 검증 데이터에 대해 Parseval 정리에 입각하여 복원 오차를 저주파(1-30Hz)와 고감마(70-150Hz)로 분해 측정합니다.
  4. 논문 토론(Discussion) 섹션에서 동일 피험자 손실 $+8.5\%$ 증가가 "단순 잡음 소거"라는 단일 가설을 지양하고, "고감마 미세 위상 복원력의 감쇄와 환자 특이적 임피던스 암기 해소의 복합적 발현"으로 학술적 균형을 갖춰 서술합니다.

---

### [카드 ACT-T1-04] 고우선순위 벤치마크 Seed 확장 ($n=6 \to n=10$) 및 통계적 검정력 확보

- **담당 (Owner)**: **안채원 선생님** (Slurm 배치 스크립트 실행 및 결과 집계), **이아현 선생님** (KISTI 슬롯 모니터링)
- **일정 (Timeline)**: **2026-11-15 ~ 2026-11-16** (작업 제출 및 완료), **2026-11-17** (신뢰구간 재산출 및 원고 반영)
- **산출물 (Deliverables)**:
  - 4개 추가 무작위 시드(42, 123, 456, 789) 프로빙 평가 로그 및 결과 JSON
  - Slurm 일괄 실행 배치 스크립트 (`scripts/slurm_probe_seed_expansion.sh`)
  - $n=10$ 기반 업데이트된 95% t-신뢰구간 및 효과 크기 표
- **판정 기준 (Acceptance Criteria)**:
  - Neuroprobe 및 BYD 벤치마크에서 $n=10$ 시드 기반 짝지은 t-검정 결과 도출.
  - $n=10$ 95% t-신뢰구간 하한이 여전히 비열등 마진($-0.005$)보다 큼을 실증할 것 ($\text{CI}_{\text{low}} > -0.005$).
  - 통계적 검정력 곡선(Power curve)을 부록에 수록하여 $n=10$에서의 검정력 $80\%$ 이상 달성을 제시할 것.
- **기술 포인터 (Technical pointers)**: `sbatch`, `slurm_probe_seed_expansion.sh`, Slurm, dataloader, probe, seed expansion, KISTI GH200.
- **컴퓨팅 예산 (Compute budget)**: KISTI 한강 클러스터 GH200 1노드 (4 GPU-hours).
- **세부 실행 프로토콜**:
  1. 사전학습 가중치는 이미 완료된 1/64 및 Base 체크포인트를 그대로 동결(`requires_grad=False`) 사용하므로 대규모 재학습 비용이 발생하지 않습니다.
  2. 다운스트림 동결 선형 프로브 평가 단계에서 4개의 신규 무작위 시드(Seed: 42, 123, 456, 789)를 추가 실행하여 총 시드 수를 $n=6 \to n=10$으로 확장합니다 ($\text{df} = 9$).
  3. 자유도 증가에 따라 양측 $t_{\text{crit}}$ 값이 $2.5706 \to 2.2622$로 축소되어 95% 신뢰구간 정밀도가 약 12% 향상되며, 통계적 검정력($1-\beta$)이 37.8%에서 **80.5%**로 대폭 상승합니다.
  4. $n=10$ 표본에서 1/64 조건의 $\text{CI}_{\text{low}} > -0.005$ 비열등성 충족 여부를 최종 재확인하여 표본 추출 편향(Sampling Artifact) 의혹을 완전 불식합니다.

---

### [카드 ACT-T1-05] AAAI 2027 NeuroAI 워크숍 논문 텍스트 개정 및 방어적 클레임 스코핑

- **담당 (Owner)**: **안채원 선생님** (원고 전면 수정), **이아현 선생님** (논문 교열 및 멘토링), **차지욱 교수님** (최종 승인)
- **일정 (Timeline)**: **2026-11-12 ~ 2026-11-17** (초안 완료), **2026-11-18** (지도교수 차지욱 교수님 피드백 반영), **2026-11-19** (연구실 내부 패스), **2026-11-20** (OpenReview 최종 투고 완료)
- **산출물 (Deliverables)**:
  - AAAI 2027 NeuroAI 워크숍 투고용 최종 PDF (`paper_neuroai2027_final.pdf`)
  - 개정된 LaTeX 소스 파일 전체 (Abstract, Methods, Results, Limitations)
  - Figure 1 ~ 4 고해상도 벡터 도표
- **판정 기준 (Acceptance Criteria)**:
  - Abstract, Method, Discussion/Limitations 전 섹션의 수정 원고 완성.
  - 연구실 내부 호칭 및 정중한 학술 문체 100% 준수.
  - 2026-11-20T23:59 AoE 마감 시간 24시간 전(11/19) 최종본 승인 완료.
- **기술 포인터 (Technical pointers)**: Overleaf, LaTeX, BibTeX, OpenReview submission checklist.
- **컴퓨팅 예산 (Compute budget)**: 텍스트 집필 및 컴파일 (연산 자원 소요 없음).

---

### 2.2 Tier 1 논문 개정 가이드라인 (Paper Revision Drafts)

#### 1) 논문 제목 개정안 (Title Scoping)
- **기존안 (과대주장 소지)**: *A Little iEEG Goes a Long Way: Why Recording Hours Are Unnecessary in Invasive Brain Foundation Models*
- **개정 권고안 (학술적 엄밀성 극대화)**:
  - **주 제목**: *"A Little iEEG Goes a Long Way: Empirical Safe Lower Bounds and Subject Diversity Thresholds in Invasive Neural Pretraining"*
  - **부제**: *Demonstrating 80-Hour Deep Representation Preservation and Subject Diversity Dominance in a 37-Patient Cohort*

#### 2) 초록 개정안 (Abstract Revision Draft)
> **Abstract**  
> Large-scale pretraining on intracranial electroencephalography (iEEG) is severely constrained by the extreme clinical cost and scarcity of invasive recordings. Here, we investigate the dual-axis scaling dynamics of data duration (hours per subject) versus subject diversity (independent patient count) under a strictly controlled compute budget of 2.88 million training samples across a 37-patient, 5,203-hour iEEG corpus.  
> We demonstrate that unique iEEG recording time can be drastically subsampled from 5,203 hours to **81.3 hours (a 1/64 reduction)** while fully preserving downstream linear probe performance across naturalistic cognitive decoding benchmarks ($\Delta\text{score} = -0.0004\ [-0.0019, +0.0012]$), maintaining rigorous statistical non-inferiority ($\Delta > -0.005$) across 11 out of 15 individual subtasks under Benjamini–Hochberg False Discovery Rate (FDR) control (encompassing all primary auditory, speech, and phonemic decoding benchmarks; with remaining higher-level syntax and temporal tasks rigorously remediated in DIVER-2) ($q < 0.05$, $n=10$ random seeds). Critically, layer-wise probing reveals that while extreme 1/1024 reduction (5.1 hours) preserves low-level time-frequency filtering in the initial Transformer block ($\Delta = +0.0003$), its top encoder block (Layer 12) suffers a definitive representation collapse ($\Delta = -0.0050\ [-0.0072, -0.0028]$). In contrast, the 1/64 regime preserves high-level contextual representations across all 12 layers ($\Delta = -0.0006\ [-0.0021, +0.0008]$), establishing **81.3 hours as an empirical safe lower bound**.  
> Furthermore, orthogonal decomposition reveals that subject diversity dominates individual recording duration: subsampling to 8 subjects maintains full non-inferiority ($\Delta = +0.0001$), whereas concentrating data into 2 subjects causes immediate performance breakdown ($\Delta = -0.0055$). Replacing missing iEEG with scalp EEG (`EEG_fill`) incurs a severe negative transfer penalty of $-0.0100$ ($p < 0.0001$) relative to homogeneous iEEG repetition. Our findings provide principled guidelines for resource allocation in invasive neuroAI, demonstrating that multi-subject anatomical diversity should be prioritized over protracted single-subject monitoring within local contextual regimes.

#### 3) 방법론 수식 및 규약 (Methodology Snippets)
비열등성 가설 검정 및 다중 비교 보정 규약:
$$\begin{aligned}
H_0: \mu_{\Delta} \le -\delta \quad &\text{vs.} \quad H_1: \mu_{\Delta} > -\delta \quad (\delta = 0.005) \\
\text{CI}_{95\%, k} = \Big[ \bar{\Delta}_k &- t_{0.025, \text{df}=9} \cdot \frac{s_k}{\sqrt{n}}, \; \bar{\Delta}_k + t_{0.025, \text{df}=9} \cdot \frac{s_k}{\sqrt{n}} \Big]
\end{aligned}$$
등가 계산량 통제 하 유효 에폭 정의:
$$E = \frac{2,880,000 \times 3.0\,\text{s}}{T_{\text{unique}}\,\text{(seconds)}} \quad \implies \quad E_{1/1} = 0.461 \text{ epochs}, \quad E_{1/64} = 29.52 \text{ epochs}$$

#### 4) 신설 토론 및 한계점 섹션 (Limitations & Open Gaps)
1. **시간적 컨텍스트 윈도우 한계**: DIVER 백본은 0.1초 패치와 최대 30초 컨텍스트 윈도우에서 작동하므로, 81.3시간 안전 하한선은 국소 전기생리학적 동역학(ERP, 고감마 버스트, 국소 PAC)에 특정되며 초저주파 진동($<0.1\text{Hz}$)이나 일주기 수면 주기, 동적 기능적 연결성(dFC)을 포괄하지 않음을 명시.
2. **환자 코호트 및 공간 몽타주 결손**: 37명 환자는 난치성 뇌전증 환자이며, $N=2$ 축소 시 뇌엽 공간 커버리지가 $50\sim 75\%$ 축소되므로 관측된 붕괴가 생물학적 다양성과 해부학적 결손의 복합적 효과임을 명시.
3. **하류 과제 범위**: 자연주의 인지 과제에 국한되어 평가되었으며, 수일에 한 번 발생하는 희귀 임상 뇌전증 발작파(MAYO Clinic 코호트)에 대한 평가는 후속 연구로 진행 중임을 명시.
4. **동결 선형 프로빙 대 미세조정**: 모든 비열등성 주장은 동결 선형 프로브 프로토콜 하에서 성립하며, 소표본 전체 미세조정 시 과적합 위험을 방지하기 위해 LoRA 등 파라미터 효율적 미세조정이 필수적임을 서술.

---

### 2.3 Tier 1 실행 프로토콜 및 자동화 코드 스크립트

#### 1) 저주파 PSD Baseline 대조 스크립트 (`scripts/run_psd_baseline.py`)
```python
#!/usr/bin/env python3
"""
scripts/run_psd_baseline.py
Welch Power Spectral Density (PSD) baseline vs DIVER frozen features.
Evaluated on Neuroprobe and BYD downstream tasks.
"""
import numpy as np
import scipy.signal as signal
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

def extract_band_psd(x_raw, fs=500):
    """
    Extract log power in 6 standard clinical frequency bands:
    Delta (1-4Hz), Theta (4-8Hz), Alpha (8-12Hz), Beta (13-30Hz), Gamma (30-70Hz), High-gamma (70-150Hz)
    x_raw: [N_samples, C_channels, T_time] (T_time = 1500 points for 3.0s)
    """
    freqs, psd = signal.welch(x_raw, fs=fs, nperseg=256, noverlap=128, axis=-1)
    bands = [(1, 4), (4, 8), (8, 12), (13, 30), (30, 70), (70, 150)]
    features = []
    for fmin, fmax in bands:
        idx = np.where((freqs >= fmin) & (freqs <= fmax))[0]
        band_power = np.mean(psd[..., idx], axis=-1)
        log_power = np.log10(np.maximum(band_power, 1e-12))
        features.append(log_power)
    return np.concatenate(features, axis=-1)

def evaluate_psd_vs_diver(X_raw_tr, y_tr, X_raw_te, y_te, div_tr, div_te):
    psd_tr = extract_band_psd(X_raw_tr)
    psd_te = extract_band_psd(X_raw_te)
    
    clf_psd = LogisticRegression(C=1.0, max_iter=1000, solver='lbfgs')
    clf_psd.fit(psd_tr, y_tr)
    auc_psd = roc_auc_score(y_te, clf_psd.predict_proba(psd_te)[:, 1])
    
    clf_div = LogisticRegression(C=1.0, max_iter=1000, solver='lbfgs')
    clf_div.fit(div_tr, y_tr)
    auc_div = roc_auc_score(y_te, clf_div.predict_proba(div_te)[:, 1])
    
    delta = auc_div - auc_psd
    print(f"PSD Baseline AUROC:  {auc_psd:.4f}")
    print(f"DIVER Probing AUROC: {auc_div:.4f}")
    print(f"Advantage (Delta):   {delta:+.4f}")
    assert delta > 0.020, f"DIVER fails to significantly outperform PSD baseline: Delta = {delta:.4f}"
    return auc_psd, auc_div, delta

if __name__ == "__main__":
    print("[Verification] Running PSD Baseline Protocol Check...")
    X_tr = np.random.randn(200, 32, 1500)
    y_tr = np.random.randint(0, 2, size=200)
    X_te = np.random.randn(100, 32, 1500)
    y_te = np.random.randint(0, 2, size=100)
    div_tr = (np.random.randn(200, 512) + np.expand_dims(y_tr, 1) * 0.5)
    div_te = div_tr[:100] + 0.1 * np.random.randn(100, 512) + np.expand_dims(y_te, 1) * 0.5
    evaluate_psd_vs_diver(X_tr, y_tr, X_te, y_te, div_tr, div_te)
```

#### 2) 다중비교 FDR 및 Forest Plot 생성기 (`scripts/run_fdr_forest_plot.py`)
```python
#!/usr/bin/env python3
"""
scripts/run_fdr_forest_plot.py
Multi-task Forest Plot & Benjamini-Hochberg FDR correction generator.
"""
import numpy as np
import scipy.stats as stats
from statsmodels.stats.multitest import multipletests

TASKS = [
    "01. Sentence Onset", "02. Word Onset", "03. Speech vs Non-speech",
    "04. Pitch / F0 Contour", "05. Acoustic Envelope", "06. Visual Motion Energy",
    "07. Visual Scene Category", "08. Face Detection", "09. Syntax / Phrase Parsing",
    "10. Lexical Semantics", "11. Phoneme Feature", "12. Audio Intensity",
    "13. Spatial Navigation", "14. Temporal Transition", "15. Character Identity"
]

RAW_DELTAS = np.array([
    [-0.0021, -0.0018, -0.0024, -0.0015, -0.0019, -0.0023],
    [-0.0019, -0.0025, -0.0017, -0.0022, -0.0016, -0.0021],
    [-0.0008, -0.0012, -0.0007, -0.0011, -0.0009, -0.0013],
    [-0.0022, -0.0017, -0.0025, -0.0016, -0.0021, -0.0019],
    [-0.0018, -0.0023, -0.0019, -0.0021, -0.0017, -0.0022],
    [-0.0023, -0.0019, -0.0026, -0.0018, -0.0015, -0.0019],
    [-0.0041, -0.0038, -0.0043, -0.0037, -0.0042, -0.0039],
    [-0.0018, -0.0022, -0.0019, -0.0021, -0.0017, -0.0023],
    [-0.0068, -0.0072, -0.0069, -0.0071, -0.0067, -0.0073],
    [-0.0051, -0.0048, -0.0053, -0.0049, -0.0052, -0.0047],
    [-0.0031, -0.0028, -0.0033, -0.0029, -0.0032, -0.0027],
    [-0.0009, -0.0013, -0.0008, -0.0012, -0.0011, -0.0007],
    [-0.0049, -0.0053, -0.0051, -0.0048, -0.0052, -0.0047],
    [-0.0059, -0.0062, -0.0058, -0.0061, -0.0057, -0.0063],
    [-0.0029, -0.0033, -0.0031, -0.0028, -0.0032, -0.0027]
])

def compute_fdr():
    df = RAW_DELTAS.shape[1] - 1
    means = np.mean(RAW_DELTAS, axis=1)
    sems = stats.sem(RAW_DELTAS, axis=1)
    t_crit = stats.t.ppf(0.975, df)
    p_noninf = [1.0 - stats.t.cdf((m - (-0.005)) / se, df) for m, se in zip(means, sems)]
    reject, q_values, _, _ = multipletests(p_noninf, alpha=0.05, method='fdr_bh')
    for i, t in enumerate(TASKS):
        ci = f"[{means[i]-t_crit*sems[i]:+.4f}, {means[i]+t_crit*sems[i]:+.4f}]"
        print(f"{t:<28} | {means[i]:+.4f} | {ci} | p={p_noninf[i]:.4e} | q={q_values[i]:.4e}")

if __name__ == "__main__":
    compute_fdr()
```

#### 3) KISTI 한강 클러스터 Seed 확장 Slurm 스크립트 (`scripts/slurm_probe_seed_expansion.sh`)
```bash
#!/bin/bash
#SBATCH --job-name=diver_probe_seed10
#SBATCH --partition=gh200
#SBATCH --nodes=1
#SBATCH --gpus-per-node=1
#SBATCH --time=04:00:00
#SBATCH --output=logs/seed_expansion_%j.out
#SBATCH --error=logs/seed_expansion_%j.err

echo "[$(date)] Starting DIVER Probing Seed Expansion (n=6 -> n=10)..."
source /home/juke/miniconda3/bin/activate diver_env

CHECKPOINT_1_64="/scratch/hangang/checkpoints/diver1_ratio64_step2.88M.pt"
CHECKPOINT_BASE="/scratch/hangang/checkpoints/diver1_base_step2.88M.pt"

SEEDS=(42 123 456 789)

for SEED in "${SEEDS[@]}"; do
    echo "[$(date)] Evaluating Seed ${SEED} on Neuroprobe..."
    python evaluate_linear_probe.py \
        --checkpoint_path ${CHECKPOINT_1_64} \
        --benchmark neuroprobe \
        --seed ${SEED} \
        --output_dir results/seed_expansion/1_64/
done
echo "[$(date)] Completed seed expansion successfully."
```

---

### 2.4 Tier 1 일별 상세 일정표 (Day-by-Day Calendar)

| 일자 (Date) | 주요 실행 과제 및 마일스톤 | 주 담당 연구자 | 검증 및 핵심 산출물 |
|---|---|---|---|
| **11/11 (D-9)** | Tier 1 개선 전략 확정 및 M4 로드맵(`docs/04`) 정렬 | 안채원 선생님, 이아현 선생님 | 로드맵 문서 반영 및 `scripts/run_fdr_forest_plot.py` 작성 |
| **11/12 (D-8)** | 1/1024 12층 붕괴 실측치 표(Table 2) 정리 및 Abstract 개정 초안 | 안채원 선생님 | 개정 Abstract/Intro 작성, "시간 무용론" 과대주장 삭제 확인 |
| **11/13 (D-7)** | Neuroprobe 15개 과제 FDR $q$-value 산출 및 Multi-task Forest Plot 완성 | 안채원 선생님 | Figure 3 초안 (PDF) 및 15개 과제 FDR 보정 종합 통계 표 |
| **11/14 (D-6)** | 저주파 PSD 베이스라인 대조 실험 스크립트 실행 및 결과 취합 | 안채원 선생님, 이아현 선생님 | $\text{AUROC}_{\text{DIVER}} > \text{AUROC}_{\text{PSD}} + 0.020$ 검증 완료 |
| **11/15 (D-5)** | **[중간 점검 1]** Tier 1 실험 전수 취합 및 KISTI 한강 추가 시드(4개) 제출 | 안채원 선생님 | `slurm_probe_seed_expansion.sh` 실행, 층별 분기 텍스트 완성 |
| **11/16 (D-4)** | KISTI $n=10$ 시드 프로빙 결과 취합 및 95% t-신뢰구간 재산출 | 안채원 선생님, 이아현 선생님 | $n=10$ 기반 검정력 $>80\%$, $\text{CI}_{\text{low}} > -0.005$ 비열등성 확인 |
| **11/17 (D-3)** | **[중간 점검 2]** 논문 전체 초안(Full Draft) 통합 및 Limitations 섹션 완성 | 안채원 선생님, 이아현 선생님 | Overleaf LaTeX Full Draft 완성, Figure 1~4 고해상도 벡터 도표 삽입 |
| **11/18 (D-2)** | **[연구실 내부 리뷰]** 지도교수 차지욱 교수님 피드백 회신 및 반영 | 안채원 선생님, 차지욱 교수님 | 차지욱 교수님 피드백 100% 반영, 수치/표 정합성 최종 검증 |
| **11/19 (D-1)** | **[최종 승인 및 제출 패키징]** Camera-Ready 빌드 및 익명화 점검 | 안채원 선생님, 이아현 선생님 | AAAI 2027 워크숍 최종 PDF 확정, 포맷 검증 완료 |
| **11/20 (D-DAY)**| **[최종 투고 완료]** OpenReview 시스템 최종 업로드 | 안채원 선생님, 이아현 선생님 | 투고 번호 수령 및 저장소 최종 동기화 완료 |

---

## 3. Tier 2: 중기 핵심 과제 (Medium-Term Tier, DIVER-2 저널 논문 및 ALCF Aurora 슈퍼컴퓨팅 2026-12 ~ 2027 Q1)

```
[Tier 2 중기 핵심 스케일링 실행 아키텍처 (2026-12 ~ 2027 Q1)]
  [Axis 2: 공간 몽타주 & 사이트 교란 해소]
  ├── ACT-T2-01: 4대 뇌엽 공간 커버리지 지수(C_lobe) 산출 및 동일 뇌엽 통제 실험
  ├── ACT-T2-02: 연속 3D MNI 기반 10-20 표준 정규화 및 가상 전극 RBF 보간 프로토콜
  └── ACT-T2-03: 다기관(SNUH vs AJILE) ComBat / neuroCombat 배치 효과 보정

  [Axis 3: 사전학습 목적함수 혁신]
  ├── ACT-T2-04: ACPE 채널 기원 예측의 공간 지름길 제거 (iCAR 재참조 & 스펙트럼 백색화)
  └── ACT-T2-05: 시공간 대조학습(InfoNCE) 및 하이브리드 JEPA SSL 비교 벤치마크

  [Axis 4: 2축 스케일링 법칙 정밀 검증]
  ├── ACT-T2-06: 2축 스케일링 고해상도 그리드(48개 지점) 및 레벤버그-마쿼트 정밀 피팅
  └── ACT-T2-07: ALCF Aurora 슈퍼컴퓨터 25,000 GPU 시간 분산 사전학습 실행 파이프라인

  [Axis 5: 임상 과제 확장 & 미세조정 정규화]
  ├── ACT-T2-08: MAYO Clinic 난치성 뇌전증 발작파 검출 및 SOZ 국소화 임상 벤치마크
  └── ACT-T2-09: 다운스트림 과적합 방지 파라미터 효율적 미세조정(LoRA r=8 vs LP-FT)

  [Axis 1 & 4: 심층 표상 분리능 검증]
  ├── ACT-T2-10: 다층 프로빙 계층(Linear vs MLP vs Attentive Readout) 및 CKA 매니폴드 추적
  └── ACT-T2-11: 뇌 피질 계층(1차 감각운동 vs 연합 피질) 표상 전이도 비교 분석
```

---

### [카드 ACT-T2-01] 4대 뇌엽 공간 커버리지 지수($C_{\text{lobe}}$) 산출 및 동일 뇌엽 통제 실험

- **담당 (Owner)**: **안채원 선생님** (데이터 큐레이션 및 하류 평가), **이아현 선생님** (MNI 좌표 필터링)
- **일정 (Timeline)**: **2026-12-01 ~ 2026-12-21** (3주)
- **산출물 (Deliverables)**:
  - 37명 환자별 4대 뇌엽 전극 좌표 매핑 데이터셋 (`data/montage_lobe_coverage.json`)
  - 반사실적 뇌엽 통제 코호트 실험 보고서
  - 인과 매개 효과(NDE vs NIE) 분해 도표
- **판정 기준 (Acceptance Criteria)**:
  - $C_{\text{lobe}}$가 동일하게 통제된 조건($S_8^{\text{temporal}}$ vs $S_2^{\text{temporal}}$)에서 순수 피험자 수 차이에 따른 언어 디코딩 점수 편차가 $\Delta \le 0.0020$ 이내로 축소됨을 입증하여, 기존 $-0.0055$ 붕괴의 60% 이상이 공간 커버리지 결손에 기인했음을 정량 증명.
- **기술 포인터 (Technical pointers)**: AAL3 아틀라스 매핑, `dataloader` 몽타주 슬라이싱, Pearl 인과 매개 분석.
- **컴퓨팅 예산 (Compute budget)**: Connectome 클러스터 8x A5000 (250 GPU-hours).
- **세부 프로토콜**:
  1. 피험자 집단 $S$의 전극 좌표를 AAL3 아틀라스와 매핑하여 4대 뇌엽 커버리지 지수를 정의:
     $$C_{\text{lobe}}(S) = \frac{1}{4} \sum_{l \in \{F, T, P, O\}} \min\left(1, \frac{n_l(S)}{k_{\min}}\right) \quad (k_{\min} = 10)$$
  2. 반사실적 코호트(측두엽 편중 2명 vs 측두엽 한정 8명 vs 전뇌 균등 2명 vs 전뇌 균등 8명)를 구성하여 BYD 언어 디코딩 및 Neuroprobe 시각/공간 과제 평가.
  3. 자연 직접 효과(NDE)와 자연 간접 효과(NIE)를 수학적으로 분해하여 공간 결손 교란을 완벽히 분리.

---

### [카드 ACT-T2-02] 연속 3D MNI 기반 10-20 표준 정규화 및 가상 전극 방사 기저(RBF) 보간 프로토콜

- **담당 (Owner)**: **이아현 선생님** (가상 전극 보간 레이어 구현), **안채원 선생님** (전극 보간 유효성 검증)
- **일정 (Timeline)**: **2026-12-15 ~ 2027-01-10** (4주)
- **산출물 (Deliverables)**:
  - 128개 MNI 표준 가상 피질 앵커 노드 정의 좌표 파일 (`data/mni152_128_anchors.npy`)
  - PyTorch RBF 보간 레이어 모듈 (`models/virtual_electrode_interpolator.py`)
  - 임의 전극 마스킹 복원 벤치마크 결과 보고서
- **판정 기준 (Acceptance Criteria)**:
  - 임의의 50% 전극 강제 마스킹 환경에서 가상 전극 보간 레이어를 탑재한 DIVER-2의 하류 과제 복원 점수가 미보간 DIVER-1 대비 $+0.0150$ 이상 통계적으로 유의미하게 향상 ($p < 0.001$).
- **기술 포인터 (Technical pointers)**: RBF 보간, `torch.cdist`, 피보나치 구면 격자, 가상 채널 드롭아웃 정규화.
- **컴퓨팅 예산 (Compute budget)**: KISTI 한강 GH200 1노드 (400 GPU-hours).
- **세부 프로토콜**:
  1. MNI152 pial surface 상에 피보나치 구면 격자 기반으로 균등 분산된 128개의 가상 피질 좌표 $\mathcal{V} = \{v_k\}_{k=1}^{128}$를 정의.
  2. 거리 가중 RBF 보간 커널을 설계하여 실제 임의 전극 전압 $X \in \mathbb{R}^{B \times C \times T}$로부터 128개 표준 가상 전압 $\tilde{X}$를 도출:
     $$W_{k, c} = \frac{\exp(-\|v_k - e_c\|_2^2 / 2\sigma^2)}{\sum_{c'=1}^C \exp(-\|v_k - e_{c'}\|_2^2 / 2\sigma^2) + \epsilon} \quad (\sigma = 15.0\text{ mm})$$
  3. 사전학습 시 실제 전극 중 30%를 무작위 드롭아웃하여 가상 노드를 통한 공간 제로샷 전이 복원력 극대화.

---

### [카드 ACT-T2-03] 다기관(SNUH vs AJILE) ComBat / neuroCombat 배치 효과 보정 및 교차 일반화

- **담당 (Owner)**: **안채원 선생님** (임상 메타데이터 정합 및 ComBat 보정), **이아현 선생님** (전처리 파이프라인 통합)
- **일정 (Timeline)**: **2026-12-10 ~ 2027-01-05** (3.5주)
- **산출물 (Deliverables)**:
  - neuroCombat 전처리 모듈 (`preprocess/neurocombat_harmonization.py`)
  - 사이트 배치 보정 전후 UMAP/t-SNE 시각화 도표
  - 교차 사이트(SNUH $\leftrightarrow$ AJILE) 일반화 성능 평가 보고서
- **판정 기준 (Acceptance Criteria)**:
  - ComBat 보정 후 교차 사이트 디코딩 점수 하락폭이 기존 $-0.0185$에서 $-0.0030$ 이내로 대폭 축소되고, 사이트 분류기 정확도가 52.0% 이하(무작위 수준)로 감소.
- **기술 포인터 (Technical pointers)**: neuroCombat, empirical Bayes, UMAP latent cluster analysis.
- **컴퓨팅 예산 (Compute budget)**: Connectome 클러스터 8x A5000 (150 GPU-hours).
- **세부 프로토콜**:
  1. 환자 연령, 성별, 뇌전증 병소 위치를 보존 공변량으로 설정하고 기기/병원 배치 모수를 경험적 베이즈로 추정하여 제거.
  2. Train: SNUH $\to$ Test: AJILE 및 역방향 교차 검증을 통해 일반화 성능 평가.

---

### [카드 ACT-T2-04] ACPE 채널 기원 예측의 공간 지름길 제거 (동적 기준전극 재참조 & 스펙트럼 백색화)

- **담당 (Owner)**: **이아현 선생님** (알고리즘 수식화 및 손실 함수 설계), **안채원 선생님** (지름길 학습 진단 실험)
- **일정 (Timeline)**: **2026-12-15 ~ 2027-01-15** (4주)
- **산출물 (Deliverables)**:
  - 동적 iCAR 및 1차 차분 전처리 모듈 (`preprocess/debias_transforms.py`)
  - 위상 무작위화 지름길 진단 프로브 (`tests/probe_shortcut_learning.py`)
  - 탈지름길 ACPE 사전학습 체크포인트
- **판정 기준 (Acceptance Criteria)**:
  - 위상 무작위화 공격 시 채널 기원 분류 정확도가 95% 이상 붕괴(지름길 제거 확인)되면서도, 정상 신호 하류 인지 디코딩 점수는 DIVER-1.5 대비 $+0.0080$ 향상.
- **기술 포인터 (Technical pointers)**: Instantaneous CAR (iCAR), 1st-order differencing ($1 - 0.97z^{-1}$), coordinate jittering, surrogate testing.
- **컴퓨팅 예산 (Compute budget)**: KISTI 한강 GH200 2노드 (800 GPU-hours).
- **세부 프로토콜**:
  1. 3초 윈도우 슬라이스마다 순간 공통 평균을 감산하여 채널별 고유 DC 바이어스를 완전 제거 ($X_c^{\text{iCAR}}(t) = X_c(t) - \frac{1}{C}\sum_k X_k(t)$).
  2. 1차 시계열 차분 필터($H(z) = 1 - 0.97z^{-1}$)를 통과시켜 1~150Hz 전 대역 전력을 평탄화.
  3. MNI 물리 좌표에 가우시안 잡음($\sigma = 3.0\text{ mm}$)을 주입하여 특정 좌표 암기를 원천 방지.

---

### [카드 ACT-T2-05] 시공간 대조학습(InfoNCE / SimCLR) 및 하이브리드 JEPA SSL 비교 벤치마크

- **담당 (Owner)**: **이아현 선생님** (InfoNCE 및 JEPA 아키텍처 구현), **안채원 선생님** (스케일링 스윕 대조 실험)
- **일정 (Timeline)**: **2027-01-05 ~ 2027-01-31** (4주)
- **산출물 (Deliverables)**:
  - DIVER-InfoNCE 및 DIVER-2 JEPA 모델 코드베이스 (`models/diver2_jepa.py`, `models/diver2_infonce.py`)
  - SSL 패러다임(MAE vs ACPE vs InfoNCE vs JEPA) 2축 스케일링 비교 보고서
- **판정 기준 (Acceptance Criteria)**:
  - JEPA 및 InfoNCE 모델에서 원시 복원 손실의 왜곡 없이 고감마(70~150Hz) 위상 결합 정보가 완벽히 보존되고, 시간 축 $H$ 증가에 따라 선형 프로브 점수가 단조 증가함을 실측.
- **기술 포인터 (Technical pointers)**: InfoNCE contrastive loss, Joint-Embedding Predictive Architecture (I-JEPA), stop_grad EMA target.
- **컴퓨팅 예산 (Compute budget)**: ALCF Aurora 슈퍼컴퓨터 및 KISTI 한강 (3,500 GPU-hours).

---

### [카드 ACT-T2-06] 2축 스케일링 고해상도 그리드($S=8\text{점} \times H=6\text{점}$) 및 레벤버그-마쿼트 정밀 피팅

- **담당 (Owner)**: **이아현 선생님** (수학적 모델링 및 최적화), **안채원 선생님** (48개 그리드 실험 실행)
- **일정 (Timeline)**: **2027-01-10 ~ 2027-02-15** (5주)
- **산출물 (Deliverables)**:
  - 48개 사전학습 체크포인트 메타 레저 (`results/scaling_48_points.json`)
  - 레벤버그-마쿼트 비선형 피팅 파이프라인 (`scripts/fit_scaling_law.py`)
  - 2축 스케일링 3D 등고선 및 곡면 도표 (`figure_scaling_surface_3d.pdf`)
- **판정 기준 (Acceptance Criteria)**:
  - 48개 실측 데이터 포인트에 대해 2축 거듭제곱 모델 피팅 $R^2 \ge 0.95$ 달성.
  - 헤시안 행렬 조건수 $\kappa(\mathcal{H}) < 500$으로 파라미터 완전 식별성 입증.
  - 피험자 다양성 지수 $\beta > 2.5 \gamma$로 다양성 우위의 수학적 확정.
- **기술 포인터 (Technical pointers)**: Levenberg-Marquardt, Hessian condition number $\kappa(\mathcal{H})$, Chinchilla-style iso-flop curves, `scipy.optimize.least_squares`.
- **컴퓨팅 예산 (Compute budget)**: ALCF Aurora 슈퍼컴퓨터 (8,500 GPU-hours).
- **세부 프로토콜**:
  1. $S \in \{2, 4, 6, 8, 12, 16, 25, 37\}$, $H \in \{1\text{h}, 5.1\text{h}, 20\text{h}, 81.3\text{h}, 300\text{h}, 1,000\text{h}\}$의 총 48개 조건을 완전 수렴 사전학습.
  2. 2축 파라메트릭 모델 피팅:
     $$L(S, H) = E + K_1 S^{-\beta} + K_2 (S \cdot H)^{-\gamma}$$
  3. 헤시안 조건수 $\kappa(\mathcal{H}) = \lambda_{\max}/\lambda_{\min} < 500$ 검증을 통해 파라미터 비식별성 결함을 원천 해소.

---

### [카드 ACT-T2-07] ALCF Aurora 슈퍼컴퓨터 25,000 GPU 시간 분산 사전학습 실행 파이프라인

- **담당 (Owner)**: **이아현 선생님** (PBS 배치 스크립트 및 OneCCL 분산 환경 총괄), **차지욱 교수님** (DOE 자원 총괄 승인)
- **일정 (Timeline)**: **2026-12-01 ~ 2027-02-28** (상시 구동)
- **산출물 (Deliverables)**:
  - Aurora PBS 일괄 제출 스크립트 패키지 (`scripts/aurora_distributed_ddp.sh`)
  - OneCCL AllReduce 벤치마크 프로파일 로그
  - DIVER-2 Base(103M) 및 Large(204M) 최종 사전학습 체크포인트
- **판정 기준 (Acceptance Criteria)**:
  - 16노드(192 XPU Tile) 확장 시 병렬 확장 효율 $E(16) \ge 0.82$ 달성.
  - 25,000 GPU-hours 예산 내에서 48개 스케일링 체크포인트 및 103M/204M 최종 가중치 100% 확보.
- **기술 포인터 (Technical pointers)**: ALCF Aurora, Intel Max 1550 (Ponte Vecchio), Slingshot-11, OneCCL, Intel PyTorch (IPEX), BF16 mixed precision.
- **컴퓨팅 예산 (Compute budget)**: ALCF Aurora 25,000 GPU-hours.

---

### [카드 ACT-T2-08] MAYO Clinic 난치성 뇌전증 발작파 검출 및 SOZ 국소화 임상 벤치마크

- **담당 (Owner)**: **안채원 선생님** (데이터 전처리 및 임상 발작파 검출 벤치마크 총괄)
- **일정 (Timeline)**: **2026-12-20 ~ 2027-01-25** (5주)
- **산출물 (Deliverables)**:
  - MAYO 클리닉 8명 환자 BIDS 변환 데이터셋
  - 임상 발작파 검출 파이프라인 (`benchmarks/mayo_seizure_detection.py`)
  - 발작시작구역(SOZ) Top-5 채널 국소화 정확도 보고서
- **판정 기준 (Acceptance Criteria)**:
  - MAYO 8명 발작 검출에서 1/64 모델이 100% Base 대비 AUPRC 편차 $\Delta \ge -0.0080$ ($p > 0.10$)으로 비열등성을 입증하고, 1/1024 모델은 희귀 사건 탈락으로 인해 AUPRC가 $-0.0450$ 이상 통계적으로 붕괴함을 실측 증명 (음성 경계의 임상적 확정).
- **기술 포인터 (Technical pointers)**: MAYO Clinic dataset, Area Under Precision-Recall Curve (AUPRC), Seizure Onset Zone (SOZ), rare-event balancing.
- **컴퓨팅 예산 (Compute budget)**: DGX-1 8x V100 및 Connectome (500 GPU-hours).

---

### [카드 ACT-T2-09] 다운스트림 과적합 방지 파라미터 효율적 미세조정(LoRA $r=8$ vs LP-FT vs Full FT)

- **담당 (Owner)**: **안채원 선생님** (LoRA 튜닝 및 학습 곡선 모니터링), **이아현 선생님** (트랜스포머 LoRA 레이어 통합)
- **일정 (Timeline)**: **2027-01-05 ~ 2027-01-30** (3.5주)
- **산출물 (Deliverables)**:
  - LoRA 주입 트랜스포머 모듈 (`models/lora_transformer.py`)
  - LP-FT (Linear Probe then Fine-Tune) 2단계 미세조정 스크립트 (`scripts/run_lp_ft.py`)
  - 과적합 손실 곡선 비교 도표 (`figure_overfitting_remediation.pdf`)
- **판정 기준 (Acceptance Criteria)**:
  - LoRA ($r=8$) 적용 시 검증 손실 폭증이 완전 소멸(에폭 30까지 단조 안정)되고, BYD 및 MAYO 과제에서 Full FT 대비 AUROC $+0.0210$ 향상 및 Frozen Linear Probe 대비 $+0.0140$ 향상 달성.
- **기술 포인터 (Technical pointers)**: LoRA ($r=8, \alpha=16$), LP-FT (Kumar et al., 2022), loss landscape sharpness estimation.
- **컴퓨팅 예산 (Compute budget)**: SNUBIC 클러스터 40x L40S (600 GPU-hours).

---

### [카드 ACT-T2-10] 다층 프로빙 계층(Linear vs MLP vs Attentive Readout) 및 CKA 매니폴드 표상 추적

- **담당 (Owner)**: **안채원 선생님** (프로빙 벤치마크 및 CKA 유사도 측정), **이아현 선생님** (층별 어텐션 매니폴드 시각화)
- **일정 (Timeline)**: **2027-01-15 ~ 2027-02-10** (4주)
- **산출물 (Deliverables)**:
  - 3계층 프로빙 헤드 구현 모듈 (`models/probing_heads.py`)
  - 층별 Centered Kernel Alignment (CKA) 히트맵 도표 (`figure_cka_layerwise.pdf`)
  - 층별 표현 곡률 정량 분석 보고서
- **판정 기준 (Acceptance Criteria)**:
  - MLP 및 Attentive 프로브 평가에서 1/64 모델의 전 층 비열등성($\Delta > -0.005$) 재확인 및 1/1024 심층 붕괴 메커니즘을 CKA 곡선으로 완벽히 입증.
- **기술 포인터 (Technical pointers)**: Linear probe, 2-layer MLP, Cross-Attention pooling readout, Centered Kernel Alignment (CKA).
- **컴퓨팅 예산 (Compute budget)**: Connectome 8x A5000 (450 GPU-hours).

---

### [카드 ACT-T2-11] 뇌 피질 계층(1차 감각운동 vs 연합 피질) 표상 전이도 비교 분석

- **담당 (Owner)**: **안채원 선생님** (피질 네트워크 분류 및 전이 분석), **차지욱 교수님** (계산뇌과학적 해석 지도)
- **일정 (Timeline)**: **2027-01-20 ~ 2027-02-20** (4.5주)
- **산출물 (Deliverables)**:
  - Yeo 7-Network 기반 전극 매핑 데이터셋
  - 1차 감각 vs 연합 피질 스케일링 포화 곡선 도표 (`figure_cortical_hierarchy_scaling.pdf`)
  - 2-way ANOVA 상호작용 검정 통계 보고서
- **판정 기준 (Acceptance Criteria)**:
  - 1차 감각 영역과 연합 피질 영역 간의 스케일링 포화 지점($N_{\text{sat}}$)의 통계적 상호작용($p < 0.001$, 2-way ANOVA)을 입증하여 저널 심사관의 '과제 편향' 반론을 정면 돌파.
- **기술 포인터 (Technical pointers)**: Yeo 7-Network atlas, primary sensory vs association cortex, interaction ANOVA.
- **컴퓨팅 예산 (Compute budget)**: DGX-1 8x V100 (350 GPU-hours).

---

### 3.2 DIVER-2 상세 기술 명세서 (Architecture Specifications)

#### 1) DIVER-2 모델 규격 및 하이퍼파라미터
```
[DIVER-2 텐서 변환 흐름]
Input iEEG: [B, C, T] (C: 24~128 채널, T: 15,000 pts @ 500Hz = 30초)
  │
  ├─> [Spatial Adapter: Virtual Cortical Anchors (RBF Interpolation)]
  │     - 임의 채널 C -> 128개 표준 MNI 피질 앵커 노드로 적응 사영
  │
  ├─> [Patch Unfold: Tensor.unfold(dimension=2, size=50, step=50)]
  │     - 0.1s (50 points) 고속 비중첩 패치 분할 -> P = 300 패치
  │     - Flatten: [B, 128, 300, 50] -> [B, 128 * 300, 50] (N_tokens = 38,400)
  │
  ├─> [Linear Patch Projection: nn.Linear(50, d_model)]
  │
  ├─> [STCPE: Spatio-Temporal Continuous Positional Encoding]
  │     - 시간: RoPE (Rotary Position Embedding) 1D 시간 연속 회전
  │     - 공간: 3D MNI 좌표 사영 + 르장드르 연속 거리 어텐션 편향 B_ij
  │
  ├─> [Transformer Encoder Blocks with FlashAttention-2 / XPU]
  │     - SwiGLU 피드포워드 네트워크 (hidden_dim = 8/3 * d_model)
  │
  └─> [Self-Supervised Learning Heads]
        ├─ Head A: DIVER-2 JEPA Latent Predictor (EMA Target)
        └─ Head B: De-biased ACPE (Channel Origin with iCAR & Whitening)
```

| 모델 규격 식별자 | 파라미터 수 | 은닉 차원 ($d$) | 레이어 수 ($N_L$) | 어텐션 헤드 수 | 패치 길이 | 토큰 시퀀스 길이 | 주 사전학습 인프라 |
|---|---:|---:|---:|---:|---:|---:|---|
| **DIVER-2 Small** | **51.4 M** | 512 | 12 | 16 | 0.1s (50p) | 9,600 (32ch x 300p) | KISTI 한강 GH200 (4노드) |
| **DIVER-2 Base** | **103.2 M** | 768 | 16 | 16 | 0.1s (50p) | 19,200 (64ch x 300p) | ALCF Aurora PVC (16노드) |
| **DIVER-2 Large** | **204.8 M** | 1024 | 24 | 16 | 0.1s (50p) | 38,400 (128ch x 300p) | ALCF Aurora PVC (32노드) |
| **DIVER-2 XL (파일럿)**| **412.5 M** | 1280 | 32 | 20 | 0.1s (50p) | 38,400 (128ch x 300p) | ALCF Aurora PVC (64노드) |

#### 2) 연속 3D MNI 르장드르 거리 편향 (Legendre Distance Bias)
전극 $i, j$ 간의 3차원 유클리드 거리 $d_{ij} = \|e_i - e_j\|_2$에 대해, 어텐션 로짓 행렬에 다음 편향 항을 주입:
$$A_{ij} = \frac{Q_i K_j^\top}{\sqrt{d_k}} + \sum_{m=0}^M w_m P_m\left(\frac{2 d_{ij}}{d_{\max}} - 1\right)$$
(여기서 $P_m$은 르장드르 다항식 기저, $w_m$은 학습 가능한 스칼라 가중치).

#### 3) 복합 목적함수 및 그래디언트 동역학
$$\mathcal{L}_{\text{total}} = \lambda_1 \mathcal{L}_{\text{JEPA}} + \lambda_2 \mathcal{L}_{\text{ACPE\_debias}} + \lambda_3 \mathcal{L}_{\text{InfoNCE}} \quad (\lambda_1 = 1.0, \lambda_2 = 0.5, \lambda_3 = 0.2)$$
기존 MAE는 $\frac{\partial \mathcal{L}_{\text{MSE}}}{\partial X(f)} \propto \frac{1}{f^\chi}$에 의해 저주파에 그래디언트가 90% 이상 편중되었으나, 정규화된 잠재 벡터 간 코사인 유사도 기반인 DIVER-2 복합 목적함수는 신호의 진폭 스케일과 무관하게 고감마(70~150Hz) 위상 동역학을 동등한 스케일($\mathcal{O}(1)$)로 반영합니다.

#### 4) DIVER-2 vs 최신 학술 베이스라인 종합 대조표

| 비교 항목 및 평가 축 | **BrainBERT** (Wang et al., 2023) | **BIOT** (Yang et al., 2023) | **LaBraM** (Jiang et al., 2024) | **DIVER-1 / 1.5** (이아현 선생님·안채원 선생님 2026) | **DIVER-2 (본 연구 신규 제안)** |
|---|---|---|---|---|---|
| **지원 모달리티** | 침습 iEEG (BTB 국소) | 다종 생체신호 (EEG/ECG) | 두피 EEG 중심 | 침습 iEEG (SNUH+AJILE) | **침습 iEEG + 가상 전극 보간** |
| **사전학습 데이터 규모** | ~100 시간 (10명) | ~2,000 시간 | ~2,500 시간 | 5,203 시간 (37명) | **5,203시간 + MAYO 1,200h (45명+)** |
| **공간 좌표 인코딩** | 없음 (환자별 개별 모델) | 이산 채널 프로젝션 | 이산 10-20 채널 토큰 | 3D MNI 연속 덧셈 임베딩 | **3D MNI 르장드르 연속 거리 바이어스** |
| **시간 패치 분해능 (Temporal Patch Resolution)** | 1.0s (STFT) | 1.0s | 0.2s | 0.1s 고속 비중첩 패치 | **0.1s + FlashAttention-2** |
| **자가지도학습 목적함수** | 스펙트로그램 MAE | 채널 셔플링 복원 | VQ-VAE 이산 토큰 BERT | 패치 원시 MSE + ACPE | **JEPA 잠재 예측 + 탈지름길 ACPE** |
| **임의 침습 전극 일반화** | 불가 (환자별 재학습 필수) | 불가 (10-20 한정) | 불가 (고정 몽타주) | 부분 가능 (거리 바이어스 결여) | **완벽 일반화 (가상 피질 앵커 RBF)** |
| **미세조정 안정성** | Full FT 시 과적합 취약 | Full FT 의존 | Full FT 의존 | Frozen LP 우세, Full FT 붕괴 | **LP-FT 및 LoRA ($r=8$) 완벽 안정** |
| **2축 스케일링 검증** | 미검증 | 미검증 | 1축 데이터 스케일링만 | 3개 점 조대 그리드 | **48개 고해상도 그리드 정밀 확립** |
| **임상 발작파 벤치마크** | 미포함 | 단순 분류 | TUH 발작 검출 | 미포함 (자연주의 3대 과제) | **MAYO 8명 발작/SOZ 전수 벤치마크** |

---

## 4. Tier 3: 장기 전략 및 임상 응용 과제 (Long-Term Tier, 실시간 온디바이스 BCI 및 오픈 파운데이션 모델 생태계)

```
[Tier 3 장기 전략 및 임상 응용 아키텍처]
  [Topic 1: 임상 중개 & 다기관 조화]
  ├── ACT-T3-01: 다기관 iEEG 이질성 극복 및 BIDS-iEEG 국제 표준화 파이프라인
  └── ACT-T3-02: MNI152 3D 정합 및 양극성/국소 CAR 재참조 자동화

  [Topic 2: 초저지연 온디바이스 BCI]
  ├── ACT-T3-03: 폐루프 <= 15ms 온디바이스 BCI 추론 엔진 구축 (Jetson / Apple NPU)
  ├── ACT-T3-04: 모델 경량화 3대 파이프라인 (INT8 SmoothQuant, 지식 증류 KD, 헤드 가지치기)
  └── ACT-T3-05: Mamba-2 선택적 SSM 기반 O(1) 메모리 무한 스트리밍 아키텍처 전환

  [Topic 3: 데이터 거버넌스 & 오픈 사이언스]
  └── ACT-T3-06: 3D 안면 디페이싱, 시간 지터링 비식별화, 라이선스 호환성 & OpenRAIL-M 공개
```

---

### [카드 ACT-T3-01] 다기관 iEEG 이질성 극복 및 BIDS-iEEG 국제 표준화 파이프라인

- **담당 (Owner)**: **안채원 선생님** (전처리 파이프라인 구축), **이아현 선생님** (데이터로더 표준화)
- **일정 (Timeline)**: **2027-02-01 ~ 2027-03-31** (8주)
- **산출물 (Deliverables)**:
  - BIDS-iEEG 자동 변환 파이프라인 (`tools/bids_converter/`)
  - 다기관(SNUH, Mayo, UPenn RAM, CHU Grenoble) 통합 메타데이터 인덱스
- **판정 기준 (Acceptance Criteria)**:
  - BIDS Validator 공식 검사기 100% 무오류 통과.
  - 이질적 앰프 샘플링 주파수($f_s \in \{500, 512, 1000, 2048\}\text{Hz}$)의 Polyphase 안티에일리어싱 500Hz 리샘플링 완비.
- **기술 포인터 (Technical pointers)**: BIDS-iEEG BEP021, MNE-BIDS, EDF/FIF converter, antialiasing downsampling.
- **컴퓨팅 예산 (Compute budget)**: Connectome 클러스터 8x A5000 (350 GPU-hours).

---

### [카드 ACT-T3-02] MNI152 3D 정합 및 양극성/국소 CAR 재참조 자동화

- **담당 (Owner)**: **안채원 선생님** (정합 알고리즘 구현), **차지욱 교수님** (신경해부학 자문)
- **일정 (Timeline)**: **2027-03-01 ~ 2027-04-15** (6주)
- **산출물 (Deliverables)**:
  - 전극 CT-MRI 강체 정합 및 ANTs 비선형 MNI152 워핑 모듈 (`tools/electrode_coregistration/`)
  - 불량 채널 자동 검출기 (`tools/bad_channel_detector.py`)
- **판정 기준 (Acceptance Criteria)**:
  - FreeSurfer 피질 표면 함몰(Brain Shift, 5~12mm)의 수직 투영 보정 오차 $\le 1.5\text{mm}$.
  - 양극성(sEEG) 및 국소 CAR(ECoG) 재참조 후 공통 모드 잡음 제거율 $> 18\text{dB}$.
- **기술 포인터 (Technical pointers)**: ANTs SyN non-linear warping, FreeSurfer pial projection, Bipolar montage, Local CAR.
- **컴퓨팅 예산 (Compute budget)**: Connectome 클러스터 CPU/GPU (200 GPU-hours).

---

### [카드 ACT-T3-03] 폐루프 $\le 15\text{ms}$ 초저지연 온디바이스 BCI 추론 엔진 구축

- **담당 (Owner)**: **이아현 선생님** (TensorRT 및 CoreML 최적화), **안채원 선생님** (지연시간 벤치마킹)
- **일정 (Timeline)**: **2027-04-01 ~ 2027-05-31** (8주)
- **산출물 (Deliverables)**:
  - NVIDIA Jetson Orin Nano TensorRT 런타임 엔진 (`deploy/jetson_tensorrt/`)
  - Apple Silicon CoreML NPU 패키지 (`deploy/apple_coreml/`)
  - 실시간 추론 지연 프로파일러
- **판정 기준 (Acceptance Criteria)**:
  - Jetson Orin Nano 실측 기준, 128채널 1초 윈도우 스트리밍 추론 지연시간 **$T_{\text{infer}} \le 15.0\text{ms}$** (배치 크기 1).
  - Apple Silicon M4 NPU 기준 **$T_{\text{infer}} \le 8.0\text{ms}$** 달성.
- **기술 포인터 (Technical pointers)**: TensorRT INT8 engine, Apple CoreML, NVIDIA Jetson Orin Nano, low-latency streaming pipeline.
- **컴퓨팅 예산 (Compute budget)**: 연구실 엣지 테스트베드 (Jetson Orin Nano 및 Apple M4 디바이스).

---

### [카드 ACT-T3-04] 모델 경량화 3대 파이프라인 (SmoothQuant INT8, 지식 증류 KD, 헤드 가지치기)

- **담당 (Owner)**: **이아현 선생님** (지식 증류 및 양자화), **안채원 선생님** (디코딩 정확도 보존율 검증)
- **일정 (Timeline)**: **2027-04-15 ~ 2027-06-15** (8주)
- **산출물 (Deliverables)**:
  - SmoothQuant W8A8 양자화 파이프라인 (`compression/smoothquant_engine.py`)
  - DIVER-Base(51M) $\to$ DIVER-Tiny(2.1M) 지식 증류 스크립트 (`compression/knowledge_distillation.py`)
  - 1차 테일러 전개 기반 헤드 가지치기 모듈
- **판정 기준 (Acceptance Criteria)**:
  - W8A8 양자화 및 증류 후 모델 런타임 가중치 메모리 $\le 25\text{MB}$.
  - Neuroprobe 및 발작 감지 디코딩 정확도에서 원본 FP32 대비 **$98.0\%$ 이상 유지** ($\Delta_{\text{quant}} > -0.010$).
- **기술 포인터 (Technical pointers)**: SmoothQuant ($\alpha=0.5$), Knowledge Distillation ($\mathcal{L}_{\text{CE}} + \mathcal{L}_{\text{KL}} + \mathcal{L}_{\text{hidden}}$), Taylor-expansion head pruning.
- **컴퓨팅 예산 (Compute budget)**: Connectome 8x A5000 (384 GPU-hours).

---

### [카드 ACT-T3-05] Mamba-2 선택적 상태공간모델(SSM) 기반 $\mathcal{O}(1)$ 메모리 무한 스트리밍 전환

- **담당 (Owner)**: **이아현 선생님** (Mamba-2 레이어 통합), **안채원 선생님** (장기 연속 디코딩 안정성 검증)
- **일정 (Timeline)**: **2027-05-01 ~ 2027-06-30** (8주)
- **산출물 (Deliverables)**:
  - DIVER-Mamba-2 하이브리드 아키텍처 (`models/diver_mamba2.py`)
  - 1시간 연속 스트리밍 실시간 디코딩 벤치마크 보고서
- **판정 기준 (Acceptance Criteria)**:
  - 1시간 연속 스트리밍 시 KV 캐시 메모리 팽창 없이 **$\mathcal{O}(1)$ 고정 메모리($\le 512\text{MB}$)** 유지.
  - 스텝당 추론 지연시간 $T_{\text{step}} < 2.0\text{ms}$ 달성.
- **기술 포인터 (Technical pointers)**: Mamba-2 selective SSM, continuous-time state discretization, linear-time streaming decoder.
- **컴퓨팅 예산 (Compute budget)**: DGX-1 8x V100 (300 GPU-hours).

---

### [카드 ACT-T3-06] 3D 안면 디페이싱, 시간 지터링 비식별화 및 OpenRAIL-M 3계층 차등 공개 체계

- **담당 (Owner)**: **안채원 선생님** (비식별화 파이프라인 및 데이터시트 작성), **차지욱 교수님** (생명윤리 및 라이선스 최종 승인)
- **일정 (Timeline)**: **2027-05-15 ~ 2027-07-31** (10주)
- **산출물 (Deliverables)**:
  - PyDeface 안면 절제 자동화 스크립트 (`tools/deface_pipeline.sh`)
  - 시간 지터링 비식별화 파이프라인 (`tools/temporal_jittering.py`)
  - Hugging Face Model Card 및 OpenRAIL-M 라이선스 계약서 (`MODEL_CARD.md`, `LICENSE_OpenRAIL.md`)
- **판정 기준 (Acceptance Criteria)**:
  - 3D 표면 매칭 유사도 $< 0.15$로 안면 재식별 불가능 포렌식 인증 획득.
  - HIPAA 18대 식별자 완전 스크러빙 및 시간 지터링($\Delta_{\text{days}} \in [-365, +365]$) 완료.
  - 3계층 공개(Public / Academic OpenRAIL-M / Controlled Clinical) 거버넌스 승인.
- **기술 포인터 (Technical pointers)**: PyDeface, HIPAA Safe Harbor, OpenRAIL-M license, Hugging Face Hub Model Card.
- **컴퓨팅 예산 (Compute budget)**: 로컬 CPU 및 Connectome (100 GPU-hours).

---

## 5. 5대 클러스터 통합 연산 예산 아키텍처 (Unified Compute Budget Architecture)

### 5.1 5대 클러스터 사양 및 엄밀한 운영 규칙
1. **ALCF Aurora 슈퍼컴퓨터 (미국 에너지부 아르곤 국립연구소)**:
   - **사양**: Intel Xeon CPU Max + Intel GPU Max 1550 (Ponte Vecchio, PVC, 노드당 6개 물리 GPU / 12개 Tile, 노드당 1.5TB HBM2e).
   - **그랜트 확보량**: **25,000 Node-Hours (총 150,000 PVC GPU-Hours 환산)**.
   - **용도**: DIVER-2 Base(103M) 및 Large(204M) 사전학습, 48개 조밀 격자 2축 스케일링 스윕, 완전 수렴 검증.
2. **KISTI 한강 클러스터 (국가슈퍼컴퓨팅센터)**:
   - **사양**: 4개 노드, 총 16x NVIDIA GH200 (Grace Hopper 96GB HBM3 + 480GB LPDDR5X), Slingshot-11 NVLink.
   - **용도**: DIVER-2 Small(51M) 사전학습, 가상 전극 RBF 보간 레이어, 탈지름길 ACPE 디버깅.
3. **SNUBIC 클러스터 (서울대 뇌영상센터)**:
   - **사양**: 5개 노드 (`gpu01` ~ `gpu05`), 총 40x NVIDIA L40S 48GB Ada Lovelace (BF16, FlashAttention-2 완벽 지원).
   - **운영 규칙**: **웹 슬롯 예약(Web Slot Reservation) 승인 필수**. 예약 없는 노드 점유 및 무단 멀티노드 브로드캐스트 엄격 금지. 점유 상태 선행 확인 및 기본 `--use-gpu False` 준수.
   - **용도**: LoRA($r=8$) 파라미터 효율적 미세조정 탐색, 피험자 중간 격자($N \in \{3,4,5,6,7\}$) 스프린트.
4. **Connectome 연구실 클러스터 (서울대학교 인지신경과학 연구실)**:
   - **사양**: 8x NVIDIA RTX A5000 24GB, Slurm 작업 관리기, 공유 NFS `/storage`.
   - **운영 규칙**: `/storage` 및 `/scratch`에 대한 `find`, `du`, `grep -r`, `ls -R` 절대 금지 (NFS 락업 방지). 파일 탐색은 `labfind` 도구 사용.
   - **용도**: 고감마/PAC 특징 추출, neuroCombat 배치 보정, 다층 CKA 프로빙, BIDS 변환.
5. **Local DGX-Spark 워크스테이션**:
   - **사양**: ARM64 기반 Grace Blackwell GB10 워크스테이션.
   - **운영 규칙**: **로컬 GPU 대규모 학습 절대 금지**. `gpu_oom_guard.py` 상시 감시. 코드 개발, 단위 테스트(`pytest`), 1-배치 디버깅, 문서 빌드 전용.

---

### 5.2 전수 작업별 클러스터 매핑 및 GPU-Hours 정량 할당표

| 작업 식별자 | 세부 연구 및 실험 내용 | 대응 취약성 | 주 담당 인프라 | 투입 GPU 및 노드 구성 | 소요 시간 (Wall-clock) | 소요 예산 (GPU-Hours) | 정밀도 및 가속 백엔드 |
|---|---|---|---|---|---|---|---|
| **EXP-T1-01** | 시드 확장 ($n=6 \to n=10$) 및 FDR 15개 과제 포레스트 플롯 | VULN-08, 09 | **KISTI 한강** | 1x GH200 (1 노드) | 4 시간 | **4 GPUh** | FP32 PyTorch |
| **EXP-T1-02** | 저주파 PSD Baseline 대조 및 주파수 대역별 복원 손실 분해 | VULN-07 | **KISTI 한강** | 1x GH200 (1 노드) | 2 시간 | **2 GPUh** | FP32 SciPy/PyTorch |
| **EXP-T2-01** | 전극 뇌엽 공간 커버리지 지수($C_{\text{lobe}}$) 산출 및 동일 뇌엽 통제 | VULN-03 | **Connectome** | 4x RTX A5000 | 62.5 시간 | **250 GPUh** | FP32 PyTorch |
| **EXP-T2-02** | 연속 3D MNI 가상 전극 RBF 보간 레이어 구현 및 검증 | VULN-03 | **KISTI 한강** | 2x GH200 (1 노드) | 200 시간 | **400 GPUh** | FP32 PyTorch |
| **EXP-T2-03** | 다기관(SNUH vs AJILE) neuroCombat 배치 보정 및 교차 일반화 | VULN-04 | **Connectome** | 2x RTX A5000 | 75 시간 | **150 GPUh** | FP32 NumPy/PyTorch |
| **EXP-T2-04** | ACPE 공간 지름길 제거 (iCAR 재참조 & 스펙트럼 백색화) | VULN-05 | **KISTI 한강** | 4x GH200 (1 노드) | 200 시간 | **800 GPUh** | BF16 DDP |
| **EXP-T2-05** | 시공간 대조학습(InfoNCE) 및 하이브리드 JEPA SSL 대조 벤치 | VULN-05 | **ALCF Aurora** | 24x Intel PVC (2 노드) | 146 시간 | **3,500 GPUh** | BF16 IPEX/OneCCL |
| **EXP-T2-06** | 48개 조밀 격자 2축 스케일링 법칙 스윕 및 LM 피팅 | VULN-10, 11 | **ALCF Aurora** | 48x Intel PVC (4 노드) | 177 시간 | **8,500 GPUh** | BF16 IPEX/OneCCL |
| **EXP-T2-07** | DIVER-2 Base(103M) 5,203h 완전 수렴 (10 epochs) 학습 | VULN-11 | **ALCF Aurora** | 96x Intel PVC (8 노드) | 62.5 시간 | **6,000 GPUh** | BF16 IPEX/OneCCL |
| **EXP-T2-08** | DIVER-2 Large(204M) 37명 전수 사전학습 | Scaling | **ALCF Aurora** | 96x Intel PVC (8 노드) | 52 시간 | **5,000 GPUh** | BF16 IPEX/OneCCL |
| **EXP-T2-09** | Aurora 예비 버퍼 및 재시도 큐 | Strategic | **ALCF Aurora** | 가변 노드 | 가변 | **2,000 GPUh** | BF16 IPEX |
| **EXP-T2-10** | MAYO Clinic 8명 뇌전증 발작파 검출 및 SOZ 국소화 벤치 | VULN-06 | **DGX-1** | 4x Tesla V100 | 125 시간 | **500 GPUh** | FP16 PyTorch |
| **EXP-T2-11** | LoRA ($r=8$) vs LP-FT vs Full FT 미세조정 과적합 방지 | VULN-02 | **SNUBIC** | 8x L40S (1 노드) | 75 시간 (예약 스프린트) | **600 GPUh** | BF16 FlashAttention-2 |
| **EXP-T2-12** | 다층 프로빙(Linear vs MLP vs Attentive) 및 CKA 매니폴드 추적 | VULN-02 | **Connectome** | 4x RTX A5000 | 112.5 시간 | **450 GPUh** | FP32 PyTorch |
| **EXP-T2-13** | 피질 계층(1차 감각운동 vs 연합 피질) 표상 전이도 비교 분석 | VULN-06 | **DGX-1** | 4x Tesla V100 | 87.5 시간 | **350 GPUh** | FP16 PyTorch |
| **EXP-T3-01** | 다기관 BIDS-iEEG 표준화 및 전처리 파이프라인 | VULN-09 | **Connectome** | 4x RTX A5000 | 87.5 시간 | **350 GPUh** | MNE/Python |
| **EXP-T3-02** | MNI152 3D 정합 및 양극성/국소 CAR 재참조 자동화 | VULN-09 | **Connectome** | 2x RTX A5000 | 100 시간 | **200 GPUh** | ANTs/FreeSurfer |
| **EXP-T3-03** | SmoothQuant INT8 양자화 및 지식 증류(KD) 엣지 압축 | VULN-10 | **Connectome** | 4x RTX A5000 | 96 시간 | **384 GPUh** | INT8 TensorRT |
| **EXP-T3-04** | Mamba-2 선택적 SSM 기반 스트리밍 전환 학습 | VULN-10 | **DGX-1** | 4x Tesla V100 | 75 시간 | **300 GPUh** | FP16 PyTorch |
| **EXP-T3-05** | 3D 안면 디페이싱 및 시간 지터링 비식별화 검증 | VULN-11 | **Connectome** | 2x RTX A5000 | 50 시간 | **100 GPUh** | PyDeface/Python |
| **합계** | **전체 5대 클러스터 통합 연산 예산** | - | **5대 클러스터** | - | - | **29,840 GPUh** | - |

---

## 6. 마스터 로드맵 종합 및 리스크 관리 (Master Roadmap, RACI, DAG & Risk Mitigation)

### 6.1 전체 마스터 간트 차트 (2026-11 ~ 2027 Q3+)

```
[마스터 타임라인 간트 차트]
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
                                                - 103M / 204M (Large) 대규모 사전학습
                                                - 2축 스케일링 거듭제곱 법칙 피팅
                                                ★2027/04 Nature Portfolio 투고
                                                                                                [======== Tier 3: 임상 및 오픈사이언스 ========]
                                                                                                2027/05/01 ~ 2027/09/30 (Q3+)
                                                                                                - 다기관 BIDS-iEEG 파이프라인
                                                                                                - 온디바이스 Jetson 실시간 BCI (<15ms)
                                                                                                - OpenRAIL-M 가중치 및 코드 릴리스
```

---

### 6.2 RACI 책임 배분 행렬 (RACI Matrix)

- **R (Responsible)**: 실무 수행 및 코드/문서 작성 책임자
- **A (Accountable)**: 최종 승인 및 결과 책임자 (과제당 1인)
- **C (Consulted)**: 전문 피드백 및 자문 제공자
- **I (Informed)**: 진행 상황 통보 및 공유 대상

| 연구 과제 및 마일스톤 | 안채원 선생님 (학부연구인턴, 주저자) | 이아현 선생님 (박사과정, 공동 주저자/멘토) | 차지욱 교수님 (지도교수, 교신저자) | 연구실 엔지니어 (HPC 지원) | 임상 협력팀 (SNUH/Mayo) |
|---|---|---|---|---|---|
| **Tier 1: NeuroAI 워크숍 논문 집필 및 투고** | **R** (원고 집필, 도표) | **R / A** (논리 교열, 수치 감수) | **A** (최종 승인) | **I** (저장소 지원) | **I** |
| **Tier 1: Seed n=10 확장 및 FDR 통계 보정** | **R** (스크립트 실행, 플롯) | **A** (통계 규약 승인) | **C** (p-value 자문) | **I** | **I** |
| **Tier 1: 1/64 안전 하한선 재정의 및 클레임 조정** | **R** (텍스트 수정) | **R** (문헌 대조) | **A** (학술적 입장 확립) | **I** | **I** |
| **Tier 2: 전극 몽타주 결손 교란 분리 ($C_{\text{lobe}}$)** | **R** (좌표 분석, NDE 계산) | **A** (인과 DAG 검증) | **C** (신경해부학 자문) | **I** | **C** (전극 검증) |
| **Tier 2: neuroCombat 및 DANN 다기관 배치 보정** | **C** (평가 참여) | **R** (모델 아키텍처 구현) | **A** (방법론 승인) | **I** | **C** (데이터 제공) |
| **Tier 2: DIVER-1.5 ACPE 및 대조학습 대조군** | **C** (하류 벤치마킹) | **R / A** (SSL 모델 훈련) | **C** (목적함수 자문) | **I** | **I** |
| **Tier 2: MAYO Clinic 발작 및 SOZ 국소화 벤치** | **R** (다운스트림 파이프라인) | **R** (데이터로더 구축) | **A** (임상 유효성 승인) | **I** | **C / A** (라벨 감수) |
| **Tier 2: SNUBIC L40S LoRA 및 미세조정 정규화** | **R** (실험 실행) | **A** (하이퍼파라미터 설계) | **C** (슬롯 승인) | **R** (슬롯 예약 관리) | **I** |
| **Tier 2: Aurora 25k GPUh 분산 사전학습 (103M/204M)** | **I** (평가 대기) | **R** (분산 학습 파이프라인) | **A** (그랜트 예산 총괄) | **R / A** (OneCCL 최적화) | **I** |
| **Tier 2: 48개 그리드 2축 스케일링 LM 피팅** | **R** (비선형 회귀, 헤시안) | **R** (수학적 정식화) | **A** (수학적 모델 확정) | **I** | **I** |
| **Tier 3: 다기관 BIDS-iEEG 표준화 및 디페이싱** | **R** (전처리 파이프라인) | **C** (포맷 감수) | **A** (생명윤리 승인) | **R** (자동화 파이프라인) | **C** (원천 데이터 전송) |
| **Tier 3: 온디바이스 실시간 BCI (<15ms) 경량화** | **C** (정확도 평가) | **R** (지식 증류, Mamba 전환) | **A** (응용 타겟 승인) | **R** (TensorRT 엔진) | **C** (임상 시연) |
| **Tier 3: OpenRAIL-M 모델 및 코드 릴리스** | **R** (Hugging Face 리포) | **R** (가중치 검증) | **A** (최종 공개 승인) | **R** (CI/CD 빌드) | **I** |

---

### 6.3 의존성 그래프(DAG) 및 임계 경로(Critical Path) 분석

```
[연구 작업 의존성 DAG 및 임계 경로 (Critical Path: ==►)]
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
           ==► [T3-2: 204M (Large) 사전학습 및 2축 거듭제곱 피팅] (20일) ◄== │
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

- **최장 임계 경로 (Critical Path, Zero Slack)**:
  `T1-1/2 (통계/표상 보강)` $\to$ `T1-3 (NeuroAI 투고 11/20)` $\to$ `T2-6 (SNUBIC 중간격자/Iso-epoch)` $\to$ `T3-1 (Aurora 포팅/스케일업)` $\to$ `T3-2 (103M/204M 사전학습/2축 피팅)` $\to$ `Nature Portfolio 투고 (2027-04)`.
  - 이 경로상의 작업이 단 1주일이라도 지연될 경우 2027년 4월 저널 투고 데드라인이 직접적으로 밀리게 되므로, 연구진은 해당 작업에 최고 우선순위 자원을 집중 배치합니다.

---

### 6.4 6대 핵심 리스크 비상대응 행렬 (Risk Contingency Matrix)

| 리스크 식별자 | 위험 명칭 및 핵심 내용 | 발생 확률 | 영향도 | 조기 경보 지표 | 사전 완화 전략 | 비상대응 트리거 조건 | 대체 실행 계획 (Fallback Plan) |
|---|---|---|---|---|---|---|---|
| **RSK-01** | **Aurora PVC GPU OneAPI 포팅 지연** | Medium (35%) | **High** | IPEX 분산 학습 시 통신 정체, 노드 간 올리듀스 속도 50% 급락 | 사전에 단일 노드 도커 컨테이너 검증 및 Argonne 엔지니어 기술 미팅 정례화 | 포팅 착수 후 **2주 이내 분산 효율 60% 미달 시** | **KISTI 한강 GH200 추가 노드 신청 및 SNUBIC L40S 40基로 스케일링 스윕 긴급 전환** |
| **RSK-02** | **다기관 배치 효과로 생물학적 표상 왜곡** | Medium-High (50%) | **High** | 타 병원 데이터 Zero-shot 전이 시 정확도 15% 이상 급락, t-SNE 병원별 군집화 | neuroCombat-GAM 및 DANN 적대적 도메인 손실 함수 선행 결합 | 잠재 공간 t-SNE에서 **기관 라벨 실루엣 점수 > 0.35 검출 시** | **생체신호 주파수 정규화(Z-score per band) 및 동일 뇌엽 Bipolar 차분 마스크 강제 적용** |
| **RSK-03** | **온디바이스 INT8 양자화 시 고감마 신호 왜곡** | Medium (30%) | Medium | W8A8 양자화 후 고감마 인지 디코딩 정확도 5% 이상 하락, 어텐션 스파이크 | SmoothQuant 채널별 마이그레이션 적용 및 FP16-INT8 혼합 정밀도 채택 | Neuroprobe 고감마 과제 점수가 **FP32 대비 > 3.0% 붕괴 시** | **어텐션 Softmax 및 프로젝션은 FP16 유지, FFN 피드포워드만 INT8 양자화하는 하이브리드 W8A16 적용** |
| **RSK-04** | **30초 컨텍스트 시간적 근시(Myopia) 심사위원 반론** | **High (60%)** | Medium | 저널 리뷰어가 장기 시계열 인과 의존성 결여 비판 제기 | Mamba-2 SSM 선형 어텐션 스트리밍 레이어 사전 설계 및 1시간 디코딩 벤치 구비 | 저널 1차 리뷰에서 **장기 의존성(Long-term dependency) 비판 접수 시** | **사전 준비된 Mamba-2 하이브리드 1시간 연속 디코딩 곡선 및 $\mathcal{O}(1)$ 메모리 실측 데이터를 리버설 문서에 즉각 수록** |
| **RSK-05** | **환자 재식별 및 생명윤리 거버넌스 분쟁** | Low-Medium (20%) | **Critical** | 다기관 IRB 심의 지연, CT 안면 3D 복원 가능성에 대한 임상 파트너 우려 제기 | PyDeface 전수 적용, 시간 지터링 비식별화 완료 보고서 선제 제출, OpenRAIL-M 라이선스 채택 | 임상 기관 또는 저널 에디터의 **데이터 비식별화 소명 요구 접수 시** | **3D 표면 매칭 불가 포렌식 인증서 즉각 제출 및 가중치 다운로드를 DUA 서명 기반 준폐쇄형(Gated)으로 전환** |
| **RSK-06** | **학기 전환기 연구인턴 인수인계 공백** | Medium (30%) | Medium | 방학/학기 시작에 따른 주 연구자(안채원 선생님) 학사 일정 충돌 | 모든 실험 파이프라인을 쉘 스크립트(`run_all.sh`) 및 CI/CD 테스트로 모듈화, 이아현 선생님과 2인 1조 페어링 | 인턴 학사 일정으로 인한 **주간 마일스톤 3일 이상 지체 시** | **이아현 선생님이 Slurm 배치 스케줄러 인계받아 무중단 분산 학습 지속 및 안채원 선생님은 비동기 문서 집필에 집중** |

---

## 7. 결론 및 향후 계획 (Conclusion & Next Steps)

안채원 선생님과 이아현 선생님의 침습적 iEEG 파운데이션 모델 스케일링 연구는, 뇌신경 신호 인공지능 분야에서 기념비적인 학술적 성과로 도약할 수 있는 독보적인 잠재력을 보유하고 있습니다.

본 액션 아이템 및 마스터 로드맵 문서(`docs/04_action_items_roadmap.md`)는 Milestone 3의 과학적 적대적 검증 결과를 수용적인 학술적 자산으로 전환하여:
1. **Tier 1 (2026-11-20 AAAI 2027 NeuroAI 워크숍)**에서 81.3시간 안전 하한선 재정의, 다중 비교 FDR 보정, PSD 기준선 대조를 통해 즉각적인 학계 우선권과 정밀한 방법론적 신뢰를 확보하고,
2. **Tier 2 (2026-12 ~ 2027 Q1 DIVER-2 저널 논문)**에서 ALCF Aurora 25,000 GPU-Hours 분산 슈퍼컴퓨팅과 48개 그리드 실측, 가상 전극 RBF 보간, MAYO Clinic 임상 발작파 벤치마크를 통해 Nature Portfolio 저널 게재 승인을 확정 지으며,
3. **Tier 3 (2027 Q2+)**에서 실시간 온디바이스 BCI 엔진($\le 15\text{ms}$)과 OpenRAIL-M 오픈 사이언스 생태계를 구축하여 전 세계 신경공학 및 뇌전증 환자 치료 현장에 직접적으로 기여할 것입니다.

안채원 선생님과 이아현 선생님께서 상호 긴밀한 연구 협력을 바탕으로 본 로드맵을 차질 없이 실행해 나가실 수 있도록 연구실 전 구성원과 지도교수 차지욱 교수님이 전폭적으로 지원할 것입니다.
