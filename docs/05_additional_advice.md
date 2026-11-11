# DIVER-2 파운데이션 모델 및 iMindBench 전수 재검토 기반 결정적 추가 조언 (Additional Advice)

- **연구 주체**: 안채원 선생님, 이아현 선생님
- **지도 교수**: 차지욱 교수님 (서울대학교 뇌인지과학과 / 인공지능연구원)
- **작성 기관**: Transconnectome Research Review Group
- **작성 일자**: 2026-11-11
- **검토 대상 저장소**:
  - `/home/juke/git/chaewon-intern-2026fall` (원천 실험 코드, 통계 스크립트, 리포트, 최신 커밋 `91cfb01`, `99e9f22`, `7e92a1e`)
  - `/home/juke/git/DIVER-2` (STRICT READ-ONLY: `diver_pretrain`, `imindbench`)
  - `/home/juke/git/DIVER` (STRICT READ-ONLY: 레거시 베이스라인)
  - `/home/juke/git/DIVER-dense-long-context` (STRICT READ-ONLY: 장기 문맥 최적화 브랜치)
  - `/home/juke/git/chaewon_ahyeon_research_review` (작업 디렉토리)

---

## 1. 개요 및 연구 맥락 (Overview & Research Context)

### 1.1 연구 배경 및 핵심 가설의 학술적 파급력
안채원 선생님, 이아현 선생님, 차지욱 교수님께서 추진하고 계신 뇌파(iEEG/EEG) 파운데이션 모델 연구는 침습적 뇌신호 분야에서 전례 없는 대규모 사전학습 데이터셋(37명, 5,203시간)과 KISTI 한강(Hangang) 슈퍼컴퓨팅 클러스터(GH200 다중 노드)를 활용하여, **"A Little iEEG Goes a Long Way: 침습 뇌파 파운데이션 모델에서 고유 기록 시간(Unique Recording Hours)은 80시간(1/64) 및 5시간(1/1024) 수준으로 대폭 축소해도 하류 신경 인지 과제 분리도가 보존된다"**는 획기적인 2축 스케일링 법칙(Two-Axis Scaling Law)을 실증적으로 규명하고 있습니다.

이 발견은 데이터 획득 비용이 극도로 높고 임상적 제약이 따르는 신경공학 및 뇌전증 모니터링 분야에서 모델 학습의 패러다임을 바꿀 수 있는 중대한 학술적 잠재력을 지니고 있습니다.

### 1.2 11/20 NeuroAI 워크숍 마감 vs 향후 본 논문(Top-Tier Journal/Conference) 확장 목표의 이원화
본 연구는 시간적으로 매우 중요한 분기점에 서 있습니다:
1. **단기 목표 (11/20 NeuroAI 워크숍 마감, 4페이지 Extended Abstract)**:
   - 한강 클러스터에서 완주된 실측치(6개 시드, 15개 과제, 1/64 및 1/1024 비열등성 한계 $\Delta > -0.0050$)를 방어력 높게 압축하여 제출해야 합니다.
   - 단기 투고에서는 발견된 실험적·통계적 한계를 숨기지 않고 정직하게 기술(Transparent Limitations)함으로써 적대적 심사위원의 리젝 트랩을 선제 차단해야 합니다.
2. **중장기 목표 (Nature BME / NeurIPS / ICLR 본 논문 확장)**:
   - 워크숍 이후에는 단순한 현상 관찰을 넘어, 기존 DIVER 아키텍처의 구조적 버그를 원천 해결하고, 진정한 교차 피험자(Zero-shot Cross-subject) 일반화 및 수백 초 단위의 장기 문맥 인과 추론 능력을 갖춘 `DIVER-2.5 / DIVER-3` 프레임워크로 완전 개편해야 합니다.

### 1.3 본 보고서의 목적 및 분석 원칙
본 보고서는 팀워크 원칙 중 **"Evidence over agreement(합의보다 실증 증거)"** 및 **"No sycophancy(맹목적 동조 배제)"** 원칙에 따라 작성되었습니다. 기존 4편의 검토 문서(`docs/01`~`04`)에서 추상적으로 다루어졌거나 간과되었던 원천 실험 코드, 통계 스크립트, DIVER 트랜스포머 아키텍처 내부의 잠재적 결함 15건을 파일 경로와 라인 번호 단위로 적시하고, 이를 극복하기 위한 즉각 조치와 전략 로드맵을 제공합니다.

---

## 2. 5대 원천 실험 설계 및 통계 사각지대 정밀 분석 (5 Critical Empirical & Statistical Blind Spots)

### 2.1 동일 피험자 2% 기록 분할 데이터 누수 및 신규 피험자 손실 2.88배 폭증 실측
- **실측 코드 위치**:
  - `/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/night-20261110/8_figs.md:26-30`
  - `/home/juke/git/chaewon-intern-2026fall/hangang/experiments/20261105_neuro-bands_gap/gen_gap_eval.py:53-57`
  - `/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/newsubj_summary.json:16-24`
  - `/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/heldout_summary.json:4`
  - `/home/juke/git/DIVER-2/diver_pretrain/benchmarks/imindbench/README.md:60-64`
  - `/home/juke/git/chaewon-intern-2026fall/hangang/cards/20261105-H-sfm-npsplit.md:34-38`

#### 정밀 분석
1. **피험자 내(within-subject) 기록 분할 실체**:
   `gen_gap_eval.py:53-57`에서 검증 셋(`ds_ho`)은 `record_holdout=0.02, record_holdout_split="holdout"` 파라미터로 구축되었습니다. `8_figs.md:26-30`에 명시된 바와 같이 이는 동일한 37명 환자의 30초 단위 기록(record) 중 2%를 무작위 분할한 것으로, 사전학습 피험자와 검증 피험자가 100% 동일합니다.
2. **신규 피험자(New Unseen Subjects)에서의 손실 수치(2.88배) 정밀 해부 및 코드 검증**:
   `newsubj_summary.json`에 따르면, 사전학습에 전혀 참여하지 않은 미학습 환자(Pippi, BYD)에 대한 복원 손실(`both all mean`)은 **0.2791**로, 동일 피험자 검증 손실(**0.0970**; `heldout_summary.json`) 대비 외관상 **2.88배** 높게 측정됩니다.
   다만 추가 코드 대조(`newsubj_cell.py:68,94` vs `gen_gap_eval.py:85-86` 및 `dataloader_utils.py:452`) 결과, 이 절대 수치 차이의 주된 원인은 모델의 교차 환자 붕괴가 아니라 **(a) `newsubj_cell.py`에서 사전학습 `collate`의 iEEG `/ 2.0` 전압 스케일링이 누락되어 입력 진폭이 2배(`/ 100` vs `/ 200 uV`) 크게 주입된 점**과 **(b) 평가 창 길이가 3초(`N=3`) 대신 1초(`tokens_used=[1]`)여서 마스킹된 채널의 시간 이웃 참조가 불가능했던 점**으로 확인되었습니다([06_student_friendly_guide_and_solutions.md](06_student_friendly_guide_and_solutions.md) 참조).
   한편 동일한 평가 파이프라인 안에서 비교한 전체 5,203시간 모델(`all`)과 5시간 모델(`1of1024`) 간의 신규 피험자 상대적 손실 차이는 **-0.06% [-1.34, 1.21]**로 완전히 일치(바닥 효과 및 데이터 양 무관 동등 수렴)하며, 동일 환자에서 관찰된 `+8.5%` 손실 격차가 순수한 환자 내 파형 암기 차이였음을 깔끔하게 뒷받침합니다.
3. **다운스트림 SPEC v1의 `within-session` 평가 제약**:
   `imindbench`의 실행 명령(`README.md:60-64`) 및 결과 JSON 4행 공통으로 `"regime": "within-session"`이 강제되어 있습니다. `20261105-H-sfm-npsplit.md:34-38`에서 안채원 선생님께서 지적하셨듯이, SPEC v1의 선형 판별기(`feature_tap=n_plus_org`)는 고정된 채널 순서에 의존하므로 교차 피험자(cross-subject) 전이가 원천적으로 평가되지 않았습니다.
4. **학술적 시사점**:
   현재 관찰된 "데이터 축소에도 일반화 성능 보존" 현상은 미지의 환자나 뇌 구조로 전이되는 범용 일반화(Foundation generalization)가 아니라, **동일 환자의 동일 세션 내 정상성(Stationarity)에 의존한 저주파 파형 피팅**에 가깝습니다.

---

### 2.2 Neuroprobe 15개 과제 다중 비교 무보정(FWER 53.67%) 및 본페로니 붕괴
- **실측 코드 위치**:
  - `/home/juke/git/chaewon-intern-2026fall/hangang/experiments/20261107_lead_top/split_np.py:6, 13`
  - `/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/night-20261110/8_figs.md:67, 91`

#### 정밀 분석
1. **다중 비교 무보정 선언**:
   `split_np.py:6`에는 `"Aux only (many comparisons, no correction)"`이라는 규칙이 명시되어 있으며, 6개 시드 표본($df = 5$)에 대해 단일 비교 임계값 $t_{0.05, 5} = 2.571$을 일괄 적용하였습니다. `8_figs.md:67`에서도 `"15 번 비교에 다중 비교 보정은 하지 않았다"`고 기록되어 있습니다.
2. **FWER 팽창 및 본페로니 붕괴 수치 증명**:
   15개 하위 과제를 독립 검정할 때 최소 1개 과제에서 1종 오류가 발생할 확률(Family-Wise Error Rate)은 다음과 같습니다:
   $$\text{FWER} = 1 - (1 - 0.05)^{15} = 1 - 0.95^{15} \approx 53.67\%$$
   본페로니 유의수준 $\alpha = 0.05 / 15 \approx 0.00333$을 적용할 경우 양측 임계값은 $t \approx 5.38$로 급증하며, 오차한계(Margin of Error)는 **2.09배 팽창**합니다.
   그 결과 1/64에서 유지 판정을 받았던 **5개 과제**(초안 `draft_user_20261109.md:61` 및 `8_figs.md:88`의 `유지 6·판정 불가 9`는 합산 오타이며 `split_np_summary.json` 실측은 **유지 5·판정 불가 10·깨짐 0**) 및 1/1024에서 유지 판정을 받았던 **7개 과제**(초안의 `유지 8·판정 불가 7` 역시 합산 오타이며 실측은 **유지 7·판정 불가 8·깨짐 0**)의 신뢰구간 하한이 본페로니 동시 구간 기준으로는 비열등성 기준치($-0.0050$) 아래로 내려갑니다(단, 시각·구문 과제의 환자 세션 수가 1~3개뿐이어서 개별 검정력이 낮은 구조적 이유 때문이며, BH-FDR 보정 시 유의하게 하락한 과제는 0개입니다).
3. **`word_index` 및 `word_gap` 점수 상승의 탐색적 해석**:
   `8_figs.md:91`에서 안채원 선생님께서 지적하셨듯이, 1/1024에서 `word_index`(+0.0074, 무보정 $p=0.0354 \to q_{\text{BH}}=0.2654$)는 FDR 보정 후 유의성이 완전히 사라지는 표본 변동이며, `word_gap`(+0.0078, $q_{\text{BH}(15)}=0.0340$) 역시 미세한 탐색적 관찰로만 기술하는 것이 타당합니다.

---

### 2.3 2.88M 샘플 고정 실험의 에폭 편향 및 심부 전극(sEEG Depth) 비율($r=+0.473$) 교란
- **실측 코드 위치**:
  - `/home/juke/git/chaewon-intern-2026fall/hangang/cards/20261103-B-feas.md:93`
  - `/home/juke/git/chaewon-intern-2026fall/hangang/experiments/20261109_lead_audit/electrode_mix.py:70-78`
  - `/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/electrode_mix_summary.json`
  - `/home/juke/git/chaewon-intern-2026fall/hangang/cards/20261104-H-batch-zscore.md:28-31`

#### 정밀 분석 (`P6.25` 초기 실험 vs `subjfix46` 통제 실험 구분)
1. **반복 횟수 통제 여부 검증**:
   `20261103-B-feas.md:93`에 명시된 대로 사전학습 스텝은 총 2,883,584회 draw(45,056 samples $\times$ 64 epochs)로 고정되었습니다.
   초기 비통제 `P6.25`($N=2$, 약 35,000개 기록) 조건은 동일 뇌파가 82.4회 반복된 반면, 안채원 선생님과 이아현 선생님의 최종 **`subjfix46` 실험(`plan.py`, `plan46.py`)에서는 고유 기록 수를 `9,757개(1/64, 295회 반복)` 및 `610개(1/1024, 4,704회 반복)`로 37명·8명 조건과 정확히 일치시켰으며 병원 비율도 6개 시드 모두 `SNUH 1명 + AJILE 1명`(총 12명 비중복)으로 완벽히 층화**하였습니다.
2. **심부 전극 비율 상관($r=+0.428 / +0.473$)의 통계적 유의성 재검증**:
   `electrode_mix_summary.json`에 따르면, $N=2$ 조건에서 심부 전극(sEEG Depth) 비율과 `rule3` 점수 차이의 상관계수는 1/64에서 **$r = +0.428$**($p=0.397$), 1/1024에서 **$r = +0.473$**($p=0.343$)으로 양(+)의 방향이나 표본 크기($n=6, df=4$) 기준 통계적으로 유의하지 않으며, BYD 과제에서는 부호가 반대($r = -0.415$)였습니다. 실제로 심부 전극이 26.3%(`s3`), 24.1%(`s4`)로 풍부한 시드에서도 $-0.0055$, $-0.0065$ 하락이 발생하여 단순 심부 전극 결핍만으로는 설명되지 않습니다.
3. **병원 사이트 진폭 차이 및 환자 간 기록 길이 불균형(`cap_fraction`) 미세 교란**:
   `20261104-H-batch-zscore.md:28-31`에 기록된 기관 간 진폭 차이(약 8배)는 `SNUH 1 + AJILE 1` 층화로 1차 통제되었으나, `plan.py:23`의 `cap_fraction`이 두 환자의 원래 기록 수에 동일한 스칼라 비율 $f$를 곱해 추출한 결과 녹음 길이가 긴 환자에게 데이터가 편중되는 시드(`S2_s2`: `Sub26`이 **79.8%** 점유, 유효 인원 $N_{\text{eff}} = 1.47$명, $\Delta = -0.0093$)가 발생했습니다(반면 유일하게 유지된 `S2_s1` $+0.0027$은 `56.3% : 43.7%` 균등 비중).
4. **학술적 시사점**:
   `subjfix46`의 $N=2$ 성능 저하($-0.0055$)는 총 기록 수와 병원 비율을 통제한 뒤에도 나타나는 진정한 소수 피험자 한계이되, 본문 해석에서는 **단 2명 추출 시의 뇌 영역 커버리지 편차와 환자별 원래 녹음 길이 불균형(`80:20` 쏠림)**이 시드 간 편차를 키웠음을 함께 명시하면 방어력이 완성됩니다.

---

### 2.4 다운스트림 1층 vs 12층 표상 붕괴 및 유효 차원(PR 5~6) 극단 축퇴
- **실측 코드 위치**:
  - `/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/small46_summary.json`
  - `/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/effdim_summary.json:6-9`
  - `/home/juke/git/chaewon-intern-2026fall/log.md:130-135`
  - `/home/juke/git/chaewon-intern-2026fall/meetings/2026-11-09_아현쌤/README.md:56`

#### 정밀 분석
1. **1층 유지 vs 12층 붕괴의 명확한 해리**:
   Small 51.4M (12층) 모델 실측 결과, 1층 판독(`rd1`)에서는 $\Delta = +0.0003 [-0.0014, +0.0021]$로 외관상 비열등성이 완벽히 유지되는 것처럼 보였으나, 최상위 12층 판독(`rdall`)에서는 **$\Delta = -0.0050 [-0.0072, -0.0028]$로 비열등성 기준이 완전히 붕괴**되었습니다. Base 9.4M (2층) 모델 역시 1층은 유지($\Delta = -0.0000$)되었으나 2층에서 BYD 언어 과제가 붕괴($\Delta = -0.0029$)되었습니다.
2. **참여율(Participation Ratio, PR 5~6) vs 90% 주성분 개수(`PC90_z`: $54.7 \to 28.1$)의 정확한 구분**:
   `effdim_summary.json:6-9` 및 `effdim2_summary.json`에 기록된 1층 풀링(`read_depth=1`) 512차원 임베딩의 참여율(PR)은 `Base_s1`: **5.89**, `Base_s2`: **5.08**, `Base_s3`: **5.29** (평균 `5.42 ± 0.42`)로 낮지만, 미학습 초기 모델(`scratch`) 역시 이미 **`5.01 ± 1.47`**(`R1024`: `7.35 ± 1.67`)이므로 "사전학습으로 인해 PR이 줄어들었다"고 기술하면 부정확합니다.
   실제 사전학습 데이터 증가에 따라 뚜렷하게 압축되는 지표는 **`90% 분산을 설명하는 주성분 개수(PC90_z)`**(`scratch` **54.7** $\to$ `1/1024` **49.2** $\to$ `1/64` **30.2** $\to$ `Base` **28.1**)와 비풀링 스케치 차원(`sketch.pr_z`: **136.8** $\to$ **86.3**)입니다.
3. **디코더 없는(Decoder-less) 최상위 층 파형 암기와 표면적 읽기 분기**:
   현재 DIVER 아키텍처는 별도의 복원 디코더 없이 인코더 마지막 층(Small의 12층) 바로 위에 선형 복원 헤드를 둡니다. 따라서 5시간(`1/1024`, 613개 기록)을 4,704회 반복 학습하면 12층이 해당 613개 클립의 국소 파형을 과암기(`train_loss 0.080` vs `Base 0.096`, 환자 내 암기 격차 `+0.0185`)하여 하류 전이 점수가 `-0.0050`으로 붕괴하는 반면, 1층은 사람 간 공통적인 기본 시간-주파수 필터를 유지하여 점수가 보존(`+0.0003`)됩니다.

---

### 2.5 Neuroprobe 56~167 복셀 좌표 입력 왜곡 및 결측 채널 제로필 인공물
- **실측 코드 위치**:
  - `/home/juke/git/DIVER-2/diver_pretrain/benchmarks/imindbench/COORDINATES_BYD_RESOLVED_BTB_STILL_BROKEN.md:7-10, 54-65`
  - `/home/juke/git/DIVER-2/diver_pretrain/src/layers/Attn_Bias.py:224-250`
  - `/home/juke/git/DIVER-2/diver_pretrain/datasets/dataloader_utils.py:304-307`
  - `/home/juke/git/DIVER-2/diver_pretrain/src/layers/Embed.py:1140-1149`

#### 정밀 분석
1. **Voxel vs MNI mm 좌표계 불일치**:
   `COORDINATES_BYD_RESOLVED_BTB_STILL_BROKEN.md:7-10`에 기술된 바와 같이, Neuroprobe 평가 h5의 `coord_btb_{x,y,z}`는 MNI mm 좌표가 아닌 피험자 고유의 56~167 양수 복셀 공간 좌표입니다.
   `Attn_Bias.py:224-250`의 르장드르 공간 사전분포(`split_coords`)는 MNI 원점 기준 반경 $r_{max} = 128\text{mm}$ 구(Sphere)를 가정하므로, 56~167 좌표가 입력되면 노름이 $244\text{mm}$ ($r\_hat > 1.9$)에 달하여 단위 구 밖으로 튕겨져 나가는 심각한 외삽(Extrapolation) 바이어스를 생성했습니다.
2. **결측 채널 NaN의 0.0 대체 및 무차별 어텐션**:
   `dataloader_utils.py:304-307`과 `Embed.py:1140-1149`에서 결측 채널 좌표는 NaN으로 마킹된 후 `pos.masked_fill(mask, 0.0)`에 의해 영벡터(`0.0`)로 채워집니다.
   이로 인해 결측 채널은 공간 거리 감쇠 없이 모든 정상 채널과 동일한 가중치로 어텐션 로짓을 교란합니다.
3. **BYD 채널 탈락 및 PIPPI 무좌표 결함**:
   `diver_mni_real` 프로파일 적용 시 BYD 데이터셋에서 좌표 결측 채널(8~12개)이 영벡터 마스킹 대신 완전히 제거되어 채널 수가 80개에서 70~72개로 축소되었습니다. 성능 향상(+0.031 AUROC)이 좌표 복원 덕분인지 채널 축소 효과인지 교란되었습니다. PIPPI는 ACPC 변환이 누락되어 전 채널 좌표가 NaN으로 무효화되었습니다.

---

## 3. DIVER 파운데이션 모델 아키텍처 결함 및 수치 한계 (DIVER Architectural Flaws & Numerical Bottlenecks)

### 3.1 패딩 마스크 단위 불일치 버그로 인한 0.3초(10.6%) 유효 학습 축약
- **실측 코드 위치**:
  - `/home/juke/git/DIVER-2/diver_pretrain/docs/PADDING_MASK_BUG.md:1-15`
  - `/home/juke/git/DIVER-2/diver_pretrain/src/SSL/SSL_methods.py:152-160`

#### 정밀 분석
데이터 로더의 `padding` 카운트는 **500-sample 로더 패치 단위**(`pad_times <= 3`)를 기록하지만, 모델 인코더는 **50-sample 모델 토큰 단위**(`N=30`)를 인덱싱했습니다.
이로 인해 패치 크기 50(0.1초)으로 학습된 모든 공식 실행(ARCH_p50 sweep, Muon vs AdamW, RECIPE.md 체크포인트)에서 **전체 3.0초 윈도우 중 앞선 0.3초(토큰 0~2, 전체의 10.6%)만 어텐션과 손실 계산에 참여하고, 나머지 89.4%의 뇌파 신호는 완전히 차단**되어 버려졌습니다.
연구진이 관찰한 "80시간 스케일링 조기 포화"는 뇌파 전체를 학습한 결과가 아니라, 각 윈도우의 0.3초 파편만을 학습하도록 제한된 아키텍처 버그에서 기인했을 가능성이 매우 높습니다.

---

### 3.2 RoPE bfloat16 arange 절단으로 인한 256 초과 위치 인덱스 충돌 (829개 생존)
- **실측 코드 위치**:
  - `/home/juke/git/DIVER-2/diver_pretrain/src/layers/Original_Moirai_projection.py:68-76`
  - `/home/juke/git/DIVER-dense-long-context/CBraMod/DIVER/layers/Original_Moirai_projection.py:84-106`

#### 정밀 분석
모델을 `bf16`으로 변환할 때 `self.theta` 버퍼가 `torch.bfloat16`이 되면서 `position = torch.arange(max_len, dtype=self.theta.dtype)` 역시 `bfloat16`으로 생성됩니다.
`bfloat16`의 가수부는 7비트에 불과하여 256을 초과하는 정수를 정확히 표현하지 못합니다.
실측 결과, 600초 장기 문맥 평가 시 6,001개 위치를 생성했을 때 **고유한 위치값은 단 829개에 불과하며 5,172개(86.2%)의 위치 차이가 0(중복 충돌)**이 되었습니다.
연속된 수십 개의 패치가 동일한 RoPE 위상각을 부여받아 장기 문맥에서 시계열 인과 순서 정보가 파괴되었습니다.

---

### 3.3 평탄화 시퀀스 $O(C^2 N^2)$ 연산 폭발 및 Dense Attention Bias 메모리 벽 (1,169 GiB)
- **실측 코드 위치**:
  - `/home/juke/git/DIVER-2/diver_pretrain/src/models/encoder_compoenents.py:285-292`
  - `/home/juke/git/DIVER-2/diver_pretrain/src/layers/Original_Moirai_bias.py:64-74`
  - `/home/juke/git/DIVER-2/diver_pretrain/src/layers/Original_Moirai_attention.py:350-355`
  - `/home/juke/git/DIVER-dense-long-context/docs/dense_long_context_plan.md:27-29`

#### 정밀 분석
채널 $C$와 시간 $N$을 단일 시퀀스로 평탄화(`rearrange(x, 'b c n d -> b (c n) d')`)함으로써 어텐션 복잡도는 $O(B \cdot C^2 \cdot N^2)$로 급증합니다.
Criss-Cross 분리형 어텐션($O(B \cdot C \cdot N \cdot (C + N))$) 대비 $C=32, N=300$ (30초) 기준 **28.9배**, $C=128, N=600$ (60초) 기준 **105배**의 연산량 격차가 발생합니다.
또한 `BinaryAttentionBias`가 매 레이어마다 `[B, H, C*N, C*N]` 텐서를 실체화하여 32채널 600초에서 레이어당 **1,169 GiB**의 VRAM을 요구하며, 이 편향 텐서로 인해 PyTorch SDPA의 FlashAttention-2 하드웨어 가속이 완전히 차단됩니다.

---

### 3.4 전역 GroupNorm 공변량 변화 및 0.75 마스킹 배치 통계 왜곡
- **실측 코드 위치**:
  - `/home/juke/git/DIVER-2/diver_pretrain/src/layers/Embed.py:721-729`
  - `/home/juke/git/DIVER-dense-long-context/docs/dense_long_context_plan.md:31`

#### 정밀 분석
토크나이저 입력 `(B, 1, C*N, P)`에 적용되는 GroupNorm은 전체 시퀀스 $C \times N \times P$에 대해 통계를 계산합니다.
3초 윈도우($N=30$)에서는 3초 국소 통계가 산출되지만, 30초~600초 장기 문맥($N=300 \sim 6,000$)으로 확장 시 시계열 전체 평균/분산으로 정규화되어 사전학습 통계와 심각한 공변량 변화(Covariate Shift)를 일으킵니다.
더욱이 사전학습 시 75%의 마스킹된 0 패딩이 GroupNorm 통계를 왜곡하며, 마스크가 없는 다운스트림 평가(`use_mask=False`) 시 입력 스케일 불일치를 유발합니다.

---

### 3.5 0.1초 무작위 패치 마스킹의 국소 스플라인 보간 과적합
- **실측 코드 위치**:
  - `/home/juke/git/DIVER-dense-long-context/docs/dense_long_context_plan.md:161-163`

#### 정밀 분석
현재 DIVER의 목적함수는 0.1초 단위의 미세 패치를 무작위로 50%~75% 마스킹합니다.
뇌파는 시간 축으로 강한 자기상관(Autocorrelation)을 가지므로 인접한 0.1초 가시 신호만으로도 스플라인 보간을 통해 완벽한 복원이 가능합니다.
모델은 원거리 문맥(1초 이상)을 볼 필요 없이 국소 보간 지름길(Shortcut)에 과적합되었으며, 문맥을 600초로 늘려도 장기 의존성을 학습할 그래디언트 유인이 수학적으로 부재했습니다 (Effective Receptive Field Saturation).

---

### 3.6 사전학습 재구성 손실과 하류 프로브 점수 간 상관계수 전무 ($\rho = +0.29$)
- **실측 코드 위치**:
  - `/home/juke/git/DIVER-2/diver_pretrain/arch/scripts/eval_probe_cv.py:4-8`
  - `/home/juke/git/DIVER-2/diver_pretrain/arch/ARCH_exp.md:14-19`

#### 정밀 분석
17개 체크포인트에 대한 실측 결과, 재구성 손실이 $0.0865 \to 0.0727$로 개선되었음에도 선형 프로브 점수와의 스피어만 상관계수는 **$\rho = +0.29$ ($p=0.26$)**로 통계적 유의성이 전혀 없었습니다.
실제로 재구성 손실이 가장 우수했던 최적 모델이 선형 프로브 평가에서는 상위 6개 모델 중 최하위를 기록했습니다.
원시 전압 도메인의 MSE 손실 하락은 신경생리학적으로 유의미한 잠재 표상의 완성을 대변하지 못합니다.

---

## 4. 신규 비대칭 MAE 구현 정밀 검증 및 코드 강화 내역 (Hardening of Asymmetric MAE)

본 연구 검토팀은 Layer 12 심층 표상 붕괴와 Throughput 병목을 해소하기 위해 제안된 `code/asymmetric_mae/asymmetric_mae.py`에 대해 4대 런타임 결함을 규명하고 즉각적인 코드 강화를 완료하였습니다.

```
[비대칭 MAE (Asymmetric MAE) 강화 아키텍처 개요]

  원시 뇌파 x [B, C, N*500]
         │
         ▼
  [가시 패치 추출 (Ids Keep, K_vis=25%)] ◄─── [결함 1 & 2 수정]
         │                                      - L=1 NaN 방어 fallback
         │                                      - 환자별 유효 토큰 기반 per-sample k_vis
         ▼
  [깊은 인코더 (12-layer, d=512)]        ◄─── [결함 3 수정]
  (오직 가시 토큰 25% + 레지스터 연산)           - closed-form 레지스터 인덱싱 (nonzero 동기화 제거)
         │
         ▼ (enc_to_dec 선형 투영: 512 -> 256)
  [마스크 토큰 결합 + 전체 패치 복원]
         │
         ▼
  [얕은 디코더 (2-layer Moirai, d=256)]
         │
         ▼
  재구성 손실 계산 [mask == 1]
         │
         ▼
  [체크포인트 내보내기]                  ◄─── [결함 4 수정]
  (export_imindbench_compat_checkpoint)         - DDP module. 접두사 제거
                                                - width/depth state_dict 기반 자동 역추론
```

### 4.1 $L=1$ 단일 패치 엣지 케이스 NaN loss 방어
- **결함 메커니즘**:
  $N=1, C=1$ ($L=1$) 입력 시 `k_vis = 1`로 계산되어 단 하나의 토큰이 visible로 지정되고 마스크 토큰이 0개가 됨(`mask.sum() == 0`). DIVER-2의 `nn.MSELoss()(masked_y, masked_x)`가 `[0, 500]` 빈 텐서를 입력받아 `NaN`을 발생시키고 전체 모델 가중치를 파괴함.
- **적용된 수정 코드** (`asymmetric_mae.py:201-260`):
  `ref_len = max(2, L)` 및 `if mask_flat.sum() == 0.0: mask_flat[0, 0] = 1.0`의 safety fallback을 구현하여, 단일 패치 입력 시에도 유효 손실 텐서 크기 `[1, 500]`을 유지하고 유한한 손실을 반환하도록 보장하였습니다.

### 4.2 이종 채널 몽타주 배치 시 환자별 per-sample `k_vis` 적용
- **결함 메커니즘**:
  환자 A(32채널, 96패치)와 환자 B(4채널, 12패치)가 단일 배치로 묶일 때, 최대 유효 토큰(96)에 맞춰 `k_vis = 24`가 적용되어 환자 B의 12개 토큰이 모두 visible로 흡수되고 마스크가 소멸(`mask[0].sum() == 0.0`)되는 심각한 환자 소외 결함 발생.
- **적용된 수정 코드** (`asymmetric_mae.py:210-250`):
  배치 내 각 환자 $b$의 실제 유효 토큰 수 $V_b$에 대해 독립적으로 $k_{vis, b} = \max(1, \min(V_b - 1, \text{round}(0.25 \times V_b)))$를 계산하고, 배치 최대 $K_{vis, \max}$에 맞추어 부족한 슬롯만 패딩 토큰으로 채우는 분할 샘플링 알고리즘을 구축하였습니다. 실측 결과 환자 B의 마스크 합이 0.0에서 **9.0**으로 정상 회복되었습니다.

### 4.3 레지스터 인덱싱 `torch.nonzero` $\to$ closed-form 변환
- **결함 메커니즘**:
  `torch.nonzero`는 출력 크기를 동적으로 결정하므로 CUDA 실행 시 GPU-호스트 동기화 버블을 발생시켜 Throughput을 저하시킴.
- **적용된 수정 코드** (`asymmetric_mae.py:307-313`):
  ```python
  row_part = torch.arange(kc * N_aug, device=device)
  r_idx = torch.arange(kc, C_aug, device=device).unsqueeze(1)
  c_idx = torch.arange(kn, device=device).unsqueeze(0)
  col_part = (r_idx * N_aug + c_idx).reshape(-1)
  reg_flat_idx = torch.cat([row_part, col_part])
  ```
  결정적 닫힌 형식 텐서 연결로 완전히 대체하여 GPU 동기화를 100% 제거하고 기존 nonzero 인덱스와의 수학적 동치성을 입증하였습니다.

### 4.4 `export_imindbench_compat_checkpoint` DDP 접두사 제거 및 형상 역추론
- **적용된 수정 코드** (`asymmetric_mae.py:593-625`):
  `asym_sd = {k.removeprefix("module."): v for k, v in raw_sd.items()}`로 DDP 접두사를 제거하고, `encoder.encoder.norm.weight.shape[0]` 및 `encoder.encoder.layers.<idx>`로부터 `width`와 `depth`를 자동 역추론하도록 강화하여 `imindbench`의 `strict=True` 로딩을 무결하게 지원하였습니다.

### 4.5 단위 테스트 11건 전수 통과 실측치
- 검증 실행: `CUDA_VISIBLE_DEVICES="" python3 -m pytest tests/test_asymmetric_mae_smoke.py`
- 결과: **11 passed in 8.27s (100% PASS)**

---

## 5. 11/20 NeuroAI 워크숍 투고 즉각 조치 5대 실행 가이드라인 (5 Immediate Workshop Actions)

안채원 선생님과 이아현 선생님께서 11/20 워크숍 마감(4페이지) 전 즉시 논문 본문 및 부록에 반영하실 수 있는 5대 방어 조치입니다:

### 1. [WS-ACT-01] 초록 및 본문 주장 수위의 엄격한 한정 (Defensive Scoping)
- **수정 지침**:
  - "고유 시간 축소에도 파운데이션 모델의 일반화 성능 유지"라는 포괄적 주장을 지양하십시오.
  - **"동일 피험자 세션 내 저주파 동결 선형 프로브(within-subject within-session frozen linear probe) 비열등성 유지"**로 명확히 한정 기술하십시오.
  - "잡음 암기 해소(Noise memorization dissociation)"라는 사후적 설명 대신, **"MAE 목적함수의 1/f 저주파 파워 편향과 얕은 층(Layer 1) 특징 재사용(Feature reuse)에 기인한 선형 분리도 보존"**으로 표현을 수정하십시오.

### 2. [WS-ACT-02] 동일 피험자 2% 분할 한계 및 신규 피험자 손실(2.88배) 투명 공개
- **수정 지침**:
  - 그림 3(b)의 범례 및 캡션을 **"held-out records from the same 37 pretraining subjects (2% intra-subject record split)"**로 명확히 수정하십시오 (`8_figs.md:45` 반영).
  - 본문 한계(Limitations) 절에 `newsubj_summary.json` 실측치(완전 미학습 환자 복원 손실 0.2791, 데이터 축소 간 차이 -0.06% 동등 수렴)를 인용하며, 제로샷 복원은 데이터 양에 무관하게 바닥 효과(Floor effect)를 보임을 한 줄 솔직하게 기술하십시오.

### 3. [WS-ACT-03] Neuroprobe 15개 과제 다중 비교 FDR $q$-값 표기 및 주장 정정
- **수정 지침**:
  - `split_np.py`의 15개 과제 분석에 대해 Benjamini-Hochberg FDR 보정 $q$-값 또는 본페로니 보정 신뢰구간을 표에 병기하십시오.
  - `word_gap`(+0.0078)과 `word_index`의 점수 상승을 "향상"으로 서술하지 말고, 무보정 다중 비교에 따른 탐색적 관찰치로 명시하십시오 (`8_figs.md:91` 지침 준수).

### 4. [WS-ACT-04] Layer 12 심층 표상 붕괴($-0.0050$) 솔직 기술 및 비대칭 해결책 제시
- **수정 지침**:
  - 1층 유지($+0.0003$)와 12층 붕괴($-0.0050$)의 괴리를 본문에 투명하게 기술하십시오.
  - 이를 해결하기 위한 아키텍처적 대안으로 **비대칭 MAE(얕은 2-layer 디코더 분리 및 25% 가시 토큰 학습)**를 제안하고, `code/asymmetric_mae/`의 단위 검증 결과와 28.9배의 주의집중 연산량 절감 효과를 1페이지 도표로 삽입하십시오.

### 5. [WS-ACT-05] RoPE bf16 `torch.float32` 패치 적용 및 DDP 체크포인트 클린업 배포
- **수정 지침**:
  - `Original_Moirai_projection.py:70-76`의 `position` 생성을 `torch.float32`로 강제하는 패치를 적용하여 위치 충돌 버그를 제거하십시오.
  - 오픈소스 배포 체크포인트에 대해 `export_imindbench_compat_checkpoint`를 실행하여 DDP `module.` 접두사를 제거한 표준 가중치를 제공하십시오.

---

## 6. 워크숍 이후 본 논문(Journal/Major Conference) 구조적 확장을 위한 5대 전략 로드맵 (5 Strategic Roadmaps for Full Paper)

워크숍 이후 본 논문(Nature BME, NeurIPS, ICLR)으로 도약하기 위한 중장기 구조적 개편 로드맵입니다:

### 1. [LT-ACT-01] 진정한 교차 피험자(Zero-shot Cross-Subject) 사전학습 및 평가 프로토콜 구축
- **실행 방안**:
  - 고정 채널 순서 플래트닝(`feature_tap=n_plus_org`)을 탈피하고, 3D MNI 좌표 기반 Cross-Attention Query 헤드 또는 Spatial Set Transformer를 도입하십시오 (`20261105-H-sfm-npsplit.md:34-38` 해결).
  - `regime: hold-out-subject` 벤치마크를 공식 수립하여 미학습 환자에 대한 선형 프로브 및 엔드투엔드 파인튜닝 성능을 재평가하십시오.

### 2. [LT-ACT-02] $O(C^2 N^2)$ 타파: `augmented` FlashAttention-2 및 Criss-Cross 하이브리드 백본
- **실행 방안**:
  - `DIVER-dense-long-context`에서 검증된 `bias_kernel='augmented'`를 DIVER-2 메인라인에 정식 병합하여 dense bias 행렬(1,169 GiB) 실체화를 완전 제거하고 순수 FlashAttention-2 커널을 구동하십시오.
  - 128채널 이상 고밀도 뇌파 대응을 위해 공간-시간 분리 어텐션(Spatio-Temporal Factorized Attention)을 결합하여 복잡도를 $O(C \cdot N \cdot (C+N))$으로 축소하십시오.

### 3. [LT-ACT-03] Span Masking ($1.0 \sim 5.0$초) 및 주파수 인식 다목적 손실 도입
- **실행 방안**:
  - 0.1초 국소 무작위 마스킹 대신 $1.0 \sim 5.0$초 연속 구간을 가리는 **Span Masking / Block Masking**을 채택하여, 모델이 국소 스플라인 보간 지름길에 빠지지 않고 원거리 뇌파 문맥을 강제로 참조하도록 유도하십시오 (`dense_long_context_plan.md:161-163` 해결).
  - 단순 시간 MSE 외에 주파수 대역 엔트로피 손실(`BC1_band_ce`) 및 전극 정위 대조학습(`G0_paper_id`)을 결합하여 High-gamma 대역의 인지 정보를 보존하십시오.

### 4. [LT-ACT-04] Neuroprobe MNI mm 좌표계 재정합 및 Varlen Jagged Tensor 파이프라인
- **실행 방안**:
  - Neuroprobe eval h5의 56~167 복셀 좌표를 사전학습과 동일한 centered MNI mm로 전처리 변환하여 르장드르 공간 사전분포(`Attn_Bias.py:224-250`)의 외삽 오류를 교정하십시오.
  - PIPPI의 ACPC 좌표 변환을 완수하고, FlashAttention-2의 `cu_seqlens` 기반 Varlen Jagged Tensor를 도입하여 채널 수가 다른 환자들의 불필요한 제로 패딩 연산 낭비를 원천 차단하십시오.

### 5. [LT-ACT-05] 임상 뇌전증 발작 및 수면 다기관 검증 파이프라인 정착
- **실행 방안**:
  - 11/10 제출된 MAYO 임상 발작 검출(8명, logistic AUROC 3초 .864, 6초 .873) 본 채점 결과를 최종 확정하고, 다기관 수면 다원 검사(PSG) 데이터셋으로 하류 과제 스펙트럼을 대폭 확장하십시오.
  - $N \in \{2, 4, 8, 16, 37\}$ 스윕 시 뇌엽 몽타주(Frontal, Temporal, Parietal, Hippocampal)가 균일하게 분포하도록 계층화 추출(Stratified sampling)을 강제하여 해부학적 커버리지 교란을 완벽히 통제하십시오.

---

## 7. 결론 (Conclusion)

안채원 선생님과 이아현 선생님의 연구는 대규모 실측 데이터를 기반으로 뇌파 파운데이션 모델의 스케일링 경계를 탐색한 선구적 업적입니다.
본 보고서에서 제시된 15대 사각지대 분석과 비대칭 MAE 코드 강화, 그리고 5대 워크숍 즉각 조치 및 5대 본 논문 확장 로드맵은 연구의 학술적 진실성(Scientific Rigor)과 방어력을 극대화하여, 11/20 NeuroAI 워크숍의 성공적 채택과 향후 최상위 저널 본 논문 출판을 위한 결정적 디딤돌이 될 것입니다.
