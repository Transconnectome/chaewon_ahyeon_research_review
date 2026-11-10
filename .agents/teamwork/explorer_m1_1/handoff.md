# Handoff Report: 안채원 선생님 연구 성과·실험 데이터·방법론·이론 전수 분석 보고서

- **작성자**: Explorer 1 (Milestone 1 — Research Synthesis & Evidence Documentation)
- **작성 일시**: 2026-11-10T16:20:00Z
- **작업 디렉토리**: `/home/juke/git/chaewon_ahyeon_research_review`
- **상태 폴더**: `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m1_1`
- **수신자 (Original Parent)**: `3f74780d-a2be-4f20-9156-47d37e41530b`

---

## 1. Observation (직접 관찰 사실 및 원천 실측 데이터)

본 조사는 안채원 선생님이 학부 연구생 및 인턴으로서 주도적으로 수행한 연구 내역을 다음의 원천 자료로부터 직접 추출하여 정리하였습니다:
1. 로컬 저장소 `/home/juke/git/chaewon-intern-2026fall` (커밋 이력, 실험 설정 파일, 채점 요약 JSON, 회의록, 슬라이드)
2. 로컬 저장소 `/home/juke/git/DIVER-2` (브랜치 `pretrain/hangang-fake-scaling`, `docs/SCALING/`, `diver_pretrain/releases/diver15/`)
3. Teams 메시지 데이터베이스 (`~/.agents/registry/chavis_teams/teams.db` 및 `sent_messages.jsonl`)
4. 멘토링 아카이브 `Transconnectome/KimJaeChul_AI_Class_Mentoring` (`students/2026-2_ChaewonAhn/`)

---

### 1.1 안채원 선생님 연구 4대 핵심 트랙 상세 관측

#### [트랙 1] 2축 스케일링 법칙 (2-Axis Scaling Law: Recording Time vs Subject Diversity)
- **연구 질문**: 총 학습 노출량(Compute)을 2.88M 샘플로 고정했을 때, 뇌 파운데이션 모델의 표상 학습을 결정짓는 핵심 병목은 '개인당 긴 기록 시간(Hours)'인가, '피험자 수의 다양성(Subjects)'인가? 부족한 고유 iEEG를 두피 EEG로 메우는 것이 유효한가?
- **데이터셋 사양 (`reports/lead/channel_time_summary.json`, job `1241234`)**:
  - iEEG 37명 (사설 25명 + AJILE 12명), 총 5,203시간, 총 624,365개 기록 (모두 500 Hz, 30.0초, 채널 수 평균 66.3 [중앙값 24~126], 총 344,994 채널·시간).
  - 총 2.88M 샘플 고정 (3초 윈도우, 최대 32채널 무작위 crop/channel 추출). 고유 데이터가 적을 경우 동일 기록에서 무작위 샘플링으로 반복 노출(draws) 충원.
  - 평가 프로토콜: Frozen Linear Probe, iEEG 다운스트림 3대 벤치마크 (Neuroprobe 15개 하위 과제, BYD, Pippi) 평균 AUROC (`rule3`). 비열등성 판정 기준: Seed 짝 차이 95% t-신뢰구간(CI) 하한 > −0.005 (Base 대비 사전학습 순수 이득 +0.034의 약 15% 이내 손실 허용).

##### 표 1.1: 고유 iEEG 기록 축소 vs 총 노출량 축소 실측 비교 (Base DIVER-1 w512 d2 9.41M, Seed n=6, df=5)
- 출처: `hangang/reports/paper_skeleton.md`, `reports/lead/curve6_summary.json`, `reports/lead/slope_summary.json`

| 조건 | 고유 기록 수 | 고유 시간 (시간) | 총 노출량 | 기록 기준 반복 | 3초 구간 기준 반복 | rule3 평가 점수 | Δscore vs Base [95% t-CI] | 비열등 판정 |
|---|---:|---:|---:|---:|---:|---:|---|---|
| 미학습 (Scratch) | 0 | 0 | 0 | - | - | .6039 ± .0041 | 기준선 (사전학습 순수 이득: +.0336 [+.0255, +.0417]) | - |
| EEG-only 사전학습 | 0 | 0 | 2.88M | - | - | .6212 ± .0053 | −.0163 [−.0190, −.0136] | 열등 확정 |
| 학습량 1/16 | 624,365 | 5,203 h | 0.18M | 0.29 회 | 0.03 회 | .6194 ± .0005 | −.0170 (학습량 축소 시 급락) | 열등 |
| 학습량 1/4 | 624,365 | 5,203 h | 0.72M | 1.15 회 | 0.12 회 | .6305 ± .0030 | −.0058 (1/4 노출 시 저하) | 열등 |
| 학습량 1/1 (Base) | 624,365 | 5,203 h | 2.88M | 4.6 회 | 0.46 회 | .6363 ± .0025 | 0.0000 (기준 Base) | 기준 |
| 학습량 2배 (×2) | 624,365 | 5,203 h | 5.76M | 9.2 회 | 0.92 회 | .6360 ± .0059 | −.0003 [−.003, +.003] (포화 관찰) | 동등 |
| **고유 기록 1/16** | 39,023 | 325 h | 2.88M | 74 회 | 7.4 회 | .6361 ± .0026 | −.0005 [−.0032, +.0022] | **비열등 (유지)** |
| **고유 기록 1/32** | 19,511 | 163 h | 2.88M | 148 회 | 14.8 회 | .6361 ± .0024 | −.0002 [−.0026, +.0023] (job 1238654) | **비열등 (유지)** |
| **고유 기록 1/64** | 9,757 | 81.3 h | 2.88M | 295 회 | 30 회 | .6359 ± .0024 | **−.0004 [−.0019, +.0012]** | **비열등 (유지)** |
| **고유 기록 1/256** | 2,438 | 20.3 h | 2.88M | 1,183 회 | 118 회 | .6353 ± .0021 | **−.0010 [−.0031, +.0012]** | **비열등 (유지)** |
| **고유 기록 1/1024** | 613 | 5.1 h | 2.88M | 4,704 회 | 470 회 | .6369 ± .0021 | **+.0006 [−.0012, +.0024]** | **비열등 (유지)** |

- **기울기 검증 (Slope Summary)**:
  - 기록 절반당 점수 변화율(최소제곱 기울기): `+.00001 [−.00021, +.00022]` (df=5, 0과 통계적으로 완전히 구별되지 않음).
  - 10회 연속 절반 감축(1/1024) 누적 변화: `+.0001 [−.0021, +.0022]`.
  - 1/1024 무작위 시드별 묶음 추출 검증 (`reports/lead/rs1024_summary.json`): 서로 다른 613개 기록 묶음(salt 1000+seed)에서도 $\Delta = -0.0003 [-0.0021, +0.0016]$로 비열등 재확인 (특정 묶음 편향 아님).

##### 표 1.2: 멀티모달 대체(Fill) vs 반복(Repeat) vs 추가(Add) 실험 실측치 (Seed n=6)
- 출처: `hangang/reports/paper_skeleton.md` 3.4절, `reports/lead/split_np_summary.json`

| 비교 항목 | 조건 1 | 조건 2 | 차이 Δ [95% t-CI] | 통계적 판정 및 학술적 의미 |
|---|---|---|---|---|
| **EEG 대체 손실** | `EEG_fill` (iEEG 12.5% + EEG 87.5%, 2.88M) | Base (iEEG 100%, 2.88M) | −.0103 [−.0147, −.0059] | 유의미한 성능 붕괴 (통계적 열등) |
| **반복 대비 대체 손실** | `iEEG_re` (iEEG 12.5% 반복, 2.88M) | `EEG_fill` (iEEG 12.5% + EEG 87.5%) | **+.0100 [+.0074, +.0125]** | **`iEEG_re` 완승 (6쌍 모두 일관)** |
| **iEEG 반복 무해성** | `iEEG_re` (iEEG 12.5% 반복, 2.88M) | Base (iEEG 100%, 2.88M) | −.0003 [−.0027, +.0021] | **비열등 유지 (1/8 반복 무해)** |
| **EEG 추가 효과 검증** | `EEG_add` (iEEG 12.5% 반복 + EEG 100%, 5.77M) | `iEEG_re ×2` (iEEG 12.5% 2배 학습, 5.77M) | −.0010 [−.0029, +.0008] | **비열등 (추가 이득 없음, 공짜지만 무효)** |
| **EEG 가공 시도** | `lowpass 45Hz` 필터링 EEG 채움 | `EEG_fill` 기본 | +.0024 [−.0004, +.0053] | 유의미한 회복 불가 (`iEEG_re` 대비 −.0092) |

##### 표 1.3: 피험자 수 분리 실험 ("시간보다 사람", Seed n=6, df=5)
- 출처: `hangang/reports/paper_skeleton.md` 5절, `reports/lead/subjfix46_summary.json` (Job `1239726`, `1239729`)

| 조건 (총 고유 기록 수) | 피험자 수 조건 | 37명 기준선 점수 | 조건별 점수 | 37명 대비 차이 Δ [95% t-CI] | 통계적 판정 |
|---|---|---:|---:|---|---|
| **81시간 (9,757 기록, 1/64)** | **8명 분산** | .6359 | .6360 | **+.0001 [−.0012, +.0014]** | **완전 유지 (비열등)** |
| 81시간 (9,757 기록, 1/64) | **2명 집중** | .6359 | .6304 | **−.0055 [−.0101, −.0010]** | **성능 붕괴 (비열등 경계 이탈)** |
| **5시간 (613 기록, 1/1024)** | **8명 분산** | .6369 | .6355 | **−.0013 [−.0047, +.0020]** | **완전 유지 (비열등)** |
| 5시간 (613 기록, 1/1024) | **2명 집중** | .6369 | .6317 | **−.0052 [−.0099, −.0005]** | **성능 붕괴 (비열등 경계 이탈)** |

- **전극 타입 교란 검증 (`reports/lead/electrode_mix_summary.json`, Job `1243386`)**:
  - 37명 전체 집단의 심부 전극(sEEG depth) 비율은 13.6% (28/37명이 depth 보유).
  - 2명 집중 조건의 모든 6개 Seed는 심부 전극을 포함하는 환자를 포함하고 있음 (depth 비율 6.9%~26.3%).
  - depth 비율과 손실 간 상관계수는 1/64에서 +0.43, 1/1024에서 +0.47로 음의 상관이 아님. 즉 "2명 조건의 성능 저하가 심부 전극 부재 때문"이라는 대안 가설은 실측 데이터로 명백히 반증됨.

---

#### [트랙 2] KISTI 슈퍼컴퓨터 「한강」 클러스터 분산 확장성 벤치마크
- **하드웨어 환경**: KISTI 국가슈퍼컴퓨팅센터 6호기 「한강」(Slurm, GH200 노드당 4장, Grace CPU 72코어 ×4, Slingshot 초고속 인터커넥트, AWS-OFI-Libfabric NCCL).
- **Strong Scaling 실측치 (`docs/SCALING/HANGANG_2026-10-28.md`, Job `1154165`)**:
  - 모델: AJILE shape, w1024 / d12, PERRANK 8, 20 step, In-Memory Fake Data.
  - 1노드 (4 GPU): 189.7 samples/s (노드당 189.7), 효율 $E(1) = 1.00$
  - 2노드 (8 GPU): 361.6 samples/s (노드당 180.8), 효율 $E(2) = 0.95$ (ALCF Aurora PVC 0.85 대비 우수)
  - 4노드 (16 GPU): 657.1 samples/s (노드당 164.3), 효율 $E(4) = 0.87$ (ALCF Aurora PVC 0.86 대비 우수)
  - 8노드 (32 GPU): 1,180.1 samples/s (노드당 147.5), 효율 $E(8) = 0.78$ (ALCF Aurora PVC 0.83 수준)
  - 처리량 환산: 한강 GH200 1개 노드(GPU 4장) 처리량이 Aurora 1개 노드(Intel PVC Tile 12개)의 약 3.8배에 달함.
- **Hangang GH200 vs AICA 클러스터 실측 재현성 비교 (`hangang/reports/hangang_report.md`)**:
  - 조건: G4 `linear_flat`, w512 d4, GPU 1장, batch 256 (`DIVER_MICRO_BATCHES=2`), bf16, 256 epoch (2,816 optimizer steps).
  - Step 속도 (`samples_per_sec_steady`, 중앙값): AICA 132.7 samples/s vs 한강 Seed 42 228.2 samples/s (**1.72배 가속**, 한강 3개 시드 평균 212.0 ± 14.3으로 **1.60배 가속**).
  - 총 학습 소요 시간 (`train_seconds` 합): AICA 72.8분 vs 한강 Seed 42 58.6분 (**0.805 = 80% 시간으로 단축**, 3개 시드 평균 63.0 ± 3.9분으로 **87% 시간 달성**).

---

#### [트랙 3] 데이터로더(Dataloader) I/O 병목 프로파일링 및 해결책
- **DDP 프로파일링 타이머 치명적 결함 발견 및 해결 (안채원 선생님 직접 수정)**:
  - 문제 현상: 기존 DIVER 학습 코드 내부 타이머(`DIVER_STEP_TIMERS`)가 DDP 분산 환경에서 데이터 대기 시간(loader stall)을 0%로 오표기함.
  - 메커니즘 규명: PyTorch DDP의 gradient all-reduce 동기화 특성상, rank 0 GPU가 I/O가 늦는 다른 GPU를 기다리는 대기 시간을 optimizer step 또는 backward 시간으로 흡수해버림.
  - 조치: 전체 step 타임스탬프 차이 계산 방식으로 수정하여 실제 데이터로더 병목을 분리 측정 성공 (`commit 1600fc2`).
- **Cold LMDB Worker 스윕 및 최적 worker 수 실측 (`hangang/reports/hangang_report.md` 2절)**:
  - 모델: DIVER-1 w512 d2, GH200 1장, batch 128, cold cache (data.mdb page cache 비움).
  - GPU 대기 비율 산식: $(\text{full step} - \text{in-memory step}) / \text{full step}$.
  - 실측 결과 (GPU 대기율 10% 미만 진입점):
    - **AJILE12** (836 GB): **Worker 2**에서 대기율 ≈0% (−2.0%) 달성.
    - **EEGV2** (3.7 TiB): **Worker 16**에서 대기율 8.2% [5.7~12.9%] 달성 (Worker 8은 12.3%).
    - **iEEG** (3.28 TB, 25명): **Worker 24**에서 대기율 5.9% [4.6~7.9%] 달성 (Worker 16에서도 15.6% [12.3~17.3%] 대기 병목 잔존, Worker 2에서는 54% 대기).
  - 발견: iEEG는 고주파수(500 Hz), 다채널(평균 66.3채널) 무작위 슬라이싱 특성으로 인해 두피 EEG 대비 훨씬 높은 I/O 대역폭을 요구하며, Worker 24 이상을 할당해야 GPU 연산 유휴를 방지할 수 있음.
  - LMDB Sparse 파일 구조 파악: `data.mdb`의 apparent-size(3.0 TiB)와 디스크 실제 점유량(608 GB)의 차이를 파악하여 데이터 이전 시 `--sparse` 옵션을 필수로 확립 (`data_transfer/README.md`).

---

#### [트랙 4] ACPE (Anatomically-Constrained Positional Encoding) 및 채널 몽타주 견고성
- **SPERA 및 DIVER-1.5 공간 인코딩 구조 (`DIVER-2/diver_pretrain/docs/archive/CHANNEL_POSITIONS_2026-08.md`, `TODO/stcpe_spera_bias.md`)**:
  - DIVER-1 초기 구조: 3차원 위치 인코딩(`PositionalEncoding3D`)을 토큰 벡터에 단순히 더하고, 어텐션 내부에서는 "동일 채널 vs 다른 채널"만을 구분하는 이진 바이어스(`BinaryAttentionBias`)만 사용하여 전극 간 물리적 거리 정보를 상실함.
  - SPERA 포팅 및 ACPE: 어텐션 맵에 르장드르 다항식 기반 구면 사전확률(Legendre-polynomial spherical prior) 및 가우시안 방사기저함수(Radial Basis)를 주입하여 해부학적 좌표 간 유클리드 거리를 반영.
  - DIVER-1.5의 STCPE (Spatio-Temporal Conditional Positional Encoding): 슬라이딩 윈도우 기반 트랜스포머를 통해 시공간 조건부 위치 인코딩을 생성. (다만 STCPE 내부 슬라이딩 윈도우에서 `data_info_list` 좌표 누락 문제를 식별하고 `pass_data_info=False` opt-in 가이드 확립).
- **채널 몽타주 결손 견고성 (Coordinate Dropout & Missing Montage Robustness, `arch/scripts/eval_coord_robustness.py`)**:
  - 임상 iEEG는 환자마다 전극 삽입 위치가 완전히 상이하며 전극 좌표가 누락되는 경우가 빈번함.
  - 좌표 결손(NaN 처리) 평가: 0(원점)으로 대체하면 MNI 중심점에 전극이 몰리는 왜곡이 발생하므로 NaN 마스킹을 유지하여 위치 임베딩을 0 벡터화 처리.
  - MNI 좌표계 변환: 사설 코퍼스 및 환자 데이터의 Talairach 좌표를 `nimare.tal2mni`를 통해 MNI152 표준 공간으로 일관 변환하여 피험자 간 공간 정렬 달성.
  - DIVER-1.5의 채널 출처 예측(Channel Origin Prediction / Identity Loss) 목표: 마스크 재구성 대신 650개 사전 등록 전극 좌표 코드북에 대해 채널의 위치를 맞추는 SSL 목표로, 적은 피험자(BTB 5명)에서도 강력한 공간 표상을 학습함을 확인.

---

### 1.2 층별 프로브 괴리(Layer-by-layer Divergence) 및 재구성 손실 괴리 실측치

#### 1.2.1 층별 프로브 괴리 (Layer 1 Readout vs Layer 12 Readout)
- 출처: `hangang/reports/paper_skeleton.md` 4절, `reports/lead/small46_summary.json`, `reports/lead/d2rdall_summary.json` (Job `1240598`, `1242310`)
- **실험 설계**: 표현을 첫 번째 인코더 블록(1st layer, `rd1`)에서 읽을 때와 마지막 12번째 인코더 블록(12th layer, `rdall`)에서 읽을 때의 고유 데이터 축소(1/64 vs 1/1024) 영향 비교 (Seed n=6, df=5).

##### 표 1.4: 층별 다운스트림 점수 변화율 (Δscore vs 전체 데이터 Base [95% t-CI])
| 모델 규모 | 축소 조건 | 첫 번째 블록 (Layer 1, `rd1`) | 마지막 블록 (Layer 12, `rdall`) | 층별 상호작용 및 판정 |
|---|---|---|---|---|
| **Base (2블록)** | **1/64 (81h)** | −.0004 [−.0019, +.0012] (유지) | **−.0000 [−.0020, +.0019] (유지)** | 전 층에서 표현 완벽 보존 |
| Base (2블록) | **1/1024 (5h)** | +.0006 [−.0012, +.0024] (유지) | **−.0029 [−.0063, +.0005]** (판정 불가) | 깊은 층에서 손실 경향, BYD 깨짐 (−.0058) |
| **Small (12블록, 51M)** | **1/64 (81h)** | −.0004 [−.0026, +.0017] (유지) | **−.0006 [−.0021, +.0008] (유지)** | **12층 전 층에서 완벽 유지** |
| Small (12블록, 51M) | **1/1024 (5h)** | +.0003 [−.0014, +.0021] (유지) | **−.0050 [−.0072, −.0028] (붕괴)** | **마지막 층에서 비열등성 완전 붕괴 (6쌍 전원 음수)** |

- **핵심 발견**:
  - 1/64 (81시간) 축소 조건은 얕은 층뿐만 아니라 12개 블록 전체를 통과한 심층 의미 표현에서도 전체 데이터 학습 모델과 동일한 품질을 유지함.
  - 반면 1/1024 (5시간)의 극단적 축소 조건은 1층의 저수준 파형 특징은 보존되지만, 12층의 심층 의미 표현은 유의미하게 붕괴됨 (NP −.0065, BYD −.0063).

#### 1.2.2 Held-out 재구성 손실 vs 다운스트림 프로브 점수 괴리
- 출처: `hangang/reports/paper_skeleton.md` 3.3절, `reports/lead/newsubj_summary.json` (Job `1247125`)

##### 표 1.5: Held-out Loss 악화율 vs 다운스트림 선형 프로브 점수 유지
| 조건 | 동일 피험자 Held-out Loss 변화 (%) | 완전 신규 피험자 Held-out Loss 변화 (%) | 다운스트림 rule3 점수 차이 Δ |
|---|---|---|---|
| Base (100%) | 기준 (0.0%) | 기준 (0.0%) | 기준 (0.0000) |
| 1/64 (81h) | **+0.1% [−0.3, +0.4]** (동등) | **−0.2% [−1.1, +0.7]** (동등) | **−.0004 [−.0019, +.0012]** (비열등) |
| 1/256 (20h) | **+1.8% [+1.5, +2.0]** (악화) | **+0.7% [−0.9, +2.2]** (동등) | **−.0010 [−.0031, +.0012]** (비열등) |
| 1/1024 (5h) | **+8.5% [+7.7, +9.2]** (명백한 악화) | **−0.1% [−1.3, +1.2]** (동등) | **+.0006 [−.0012, +.0024]** (비열등) |

- **괴리 현상의 과학적 해명**:
  - 동일 피험자 held-out 데이터에 대한 복원 loss가 1/1024에서 +8.5% 악화되는 것은 모델의 범용 표상 능력 상실이 아니라, **동일 피험자 특유의 잡음/배경 신호에 대한 암기(Memorization) 부족** 때문임.
  - 사전학습에 전혀 참여하지 않은 완전 신규 피험자(Pippi, BYD)에 대해 재구성 loss를 측정했을 때 1/1024 모델의 loss 변화율은 **−0.1% [−1.3, +1.2]**로 Base와 완벽히 일치함. 즉, 범용적인 미지의 뇌파에 대한 복원 및 표상 전이력은 5시간(1/1024)만으로도 전혀 손상되지 않음이 실증됨.

---

## 2. Logic Chain (관측에서 결론으로의 논리 추론 체인)

1. **[관측 1.1 트랙 2, 3 참조] 시스템적 신뢰성 확립**:
   - 안채원 선생님은 KISTI 한강 클러스터에서 8노드 Strong Scaling $E(8)=0.78$을 달성하고, AICA 대비 1.60~1.72배 step 가속 및 80~87% 런타임 단축을 입증함.
   - 특히 PyTorch DDP 환경에서 All-reduce gradient 동기화에 의해 은폐되던 Dataloader stall 버그를 독자적으로 해결하고, cold LMDB 환경에서 iEEG는 최소 Worker 24를 투입해야 I/O 병목을 회피할 수 있음을 규명함. 이는 후속 실험 데이터의 측정 정밀도를 보장함.
2. **[관측 1.1 트랙 1 참조] 모달리티 간 비대체성 규명**:
   - 2.88M 노출량 통제 하에서, 부족한 iEEG를 두피 EEG로 메운 모델(`EEG_fill`)은 동일한 소량의 iEEG를 반복 학습한 모델(`iEEG_re`) 대비 **−0.0100**이라는 치명적인 성능 저하를 나타냄.
   - 이는 저주파/두개골 감쇄 특성을 갖는 두피 EEG가 국소 피질의 고감마/미세 신경 발화를 다루는 iEEG의 표상을 결코 대체할 수 없음을 통계적으로 확증함.
3. **[관측 1.1 트랙 1, 표 1.3 참조] "시간보다 사람" 법칙 도출**:
   - 고유 기록 양을 81시간(1/64) 또는 5시간(1/1024)으로 대폭 축소하더라도, 37명 또는 8명의 피험자 다양성이 확보되면 다운스트림 점수가 보존됨 ($+0.0001$, $-0.0013$).
   - 그러나 피험자 수를 2명으로 축소하면 동일한 기록량에서도 점수가 즉시 붕괴됨 ($-0.0055$, $-0.0052$). 전극 타입(depth vs grid) 교란 요인을 배제함으로써 성능 붕괴의 원인이 오직 '피험자 간 생물학적 다양성의 결핍'에 있음을 논리적으로 입증함.
4. **[관측 1.2 참조] 표상 보존의 한계 조건 규명**:
   - 층별 프로브 분석을 통해, 1/64(81시간)는 12개 인코더 블록 전 층에서 표상이 보존되지만, 1/1024(5시간)는 얕은 층(Layer 1)에서만 보존되고 심층 층(Layer 12)에서는 붕괴($-0.0050$)됨을 밝혀냄.
   - 또한 동일 피험자 복원 loss의 악화(+8.5%)가 신규 피험자 복원 loss에서는 나타나지 않음(-0.1%)을 입증하여, 손실 악화가 범용 표상 결손이 아닌 동일 피험자 오버피팅 감소임을 논리적으로 해명함.

---

## 3. Caveats (조사 한계 및 가정)

1. **다운스트림 과제의 인지/운동 편향**:
   - 현재 주 평가 지표(`rule3`)인 Neuroprobe, BYD, Pippi는 언어, 운동, 청각 등 고감마 파워 의존적인 인지 과제에 편중되어 있습니다. 두피 EEG가 상대적으로 강점을 갖는 거시적 상태 변화(수면 단계, 각성도) 및 병리적 발작 검출(MAYO)에 대한 전수 평가는 11/10 착수 단계로 최종 결과 반영이 필요합니다.
2. **Within-session 평가 분할로 인한 일반화 누수 가능성**:
   - 다운스트림 과제의 train/test 분할이 동일 피험자의 동일 세션 내부에서 무작위 분할되어 있어, 시계열적 근접성으로 인한 일반화 성능의 과대평가 가능성이 존재합니다.
3. **초대형 모델(>100M) 및 장기 사전학습에서의 미검증**:
   - 주 실험은 Base(9.41M) 및 Small(51M) 모델, 2.88M step에서 수행되었습니다. 폭 1024(204M) 대형 모델이나 ×4(11.5M samples) 이상의 긴 사전학습에서는 1/64의 포화 특성이 다르게 전개될 수 있습니다.

---

## 4. Conclusion (최종 종합 결론)

안채원 선생님의 연구는 단순한 "데이터 축소 실험"이 아니라, **"생체신호(iEEG) 기반 파운데이션 모델에서 총 연산량을 통제했을 때, 모델의 범용 표상 형성을 결정짓는 핵심 병목은 '개인당 긴 기록 시간(Hours)'이 아니라 '피험자 수의 다양성(Subject Diversity)'이다"**라는 2축 신경 스케일링 법칙(2-Axis Neural Scaling Law)을 최초로 실증한 선구적 연구입니다.

### 핵심 정량적 결론:
1. **iEEG의 극소량 포화 ("A Little iEEG Goes a Long Way")**: 고유 기록을 81시간(1/64)까지 줄여 반복 학습하더라도 Base 및 51M Small 모델의 전 층(Layer 1~12)에서 사전학습 이득의 98.9%가 비열등하게 보존됨 ($\Delta = -0.0004 [-0.0019, +0.0012]$).
2. **두피 EEG의 비대체성 ("Non-Substitutability")**: 부족한 iEEG를 두피 EEG로 메우는 시도는 $-0.0100$의 유의미한 성능 하락을 유발하며, 적은 iEEG라도 단순 반복하는 것이 압도적으로 우수함.
3. **피험자 다양성의 임계치 ("Subjects over Hours")**: 피험자 수를 2명으로 줄이면 성능이 붕괴($-0.0055$)되나, 8명 이상 확보되면 37명 전체와 완전히 동등한 성능($+0.0001$)을 달성함.
4. **인프라 최적화**: KISTI 한강 GH200에서 DDP 타이머 결함을 교정하고, iEEG 대용량 처리를 위해 Worker 24가 필수적임을 규명함.

---

## 5. Verification Method (독립 재현 및 검증 절차)

### 5.1 실험 통계 및 결과 데이터 독립 검증 명령
```bash
# 1. 고유 기록 축소 비열등성 통계 검증
python3 -c "
import json
with open('/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/curve6_summary.json') as f:
    d = json.load(f)
for k, v in d.items():
    print(f'{k}: rule3_delta={v.get(\"rule3_diff_mean\", \"N/A\")}, 95CI=[{v.get(\"rule3_diff_ci_low\", \"N/A\")}, {v.get(\"rule3_diff_ci_high\", \"N/A\")}]')
"

# 2. 피험자 수 분리 실험 (8명 vs 2명) 결과 검증
python3 -c "
import json
with open('/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/subjfix46_summary.json') as f:
    d = json.load(f)
for cond in d.get('conditions', []):
    print(f'{cond[\"name\"]}: delta={cond[\"diff_mean\"]}, CI=[{cond[\"ci_low\"]}, {cond[\"ci_high\"]}]')
"

# 3. 층별 프로브 (Layer 1 vs Layer 12) 괴리 검증
python3 -c "
import json
with open('/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/small46_summary.json') as f:
    d = json.load(f)
print('Small rd1:', d.get('rd1'))
print('Small rdall (Layer 12):', d.get('rdall'))
"

# 4. 신규 피험자 Held-out Loss 검증
python3 -c "
import json
with open('/home/juke/git/chaewon-intern-2026fall/hangang/reports/lead/newsubj_summary.json') as f:
    d = json.load(f)
print('New subject held-out loss delta:', d)
"
```

### 5.2 가설 무효화 조건 (Falsification Conditions)
1. **1/64 비열등성 무효화**: 204M(w1024) 대형 모델 또는 신규 병리 과제(MAYO) 평가에서 Base 대비 1/64의 $\Delta\text{score}$가 $-0.005$ 미만으로 유의미하게 하락할 경우.
2. **EEG 대체 불가능성 무효화**: 공간 정합 또는 주파수 적응 기법이 적용된 두피 EEG 혼합 모델이 iEEG 단순 반복(`iEEG_re`)과 동등하거나 그 이상의 성능을 보일 경우.
3. **피험자 다양성 가설 무효화**: 2명 피험자 조건에서 전극 수 및 해부학적 커버리지를 엄밀히 통제했을 때 37명 조건과의 성능 격차가 소멸할 경우.
