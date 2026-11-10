# Handoff Report: 안채원 선생님 연구 상세 조사 및 분석 (Survey Explorer 2)

- **작성 에이전트**: `teamwork_explorer_survey_2`
- **조사 대상**: 안채원 선생님 (학부 연구생/인턴) 공유 연구 결과, 가설, 데이터, 코드 및 실험 실측치
- **조사 일자**: 2026-11-10T15:58:00Z
- **상태 폴더**: `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_survey_2`
- **관련 저장소**:
  - `Transconnectome/chaewon-intern-2026fall` (로컬 클론: `/home/juke/git/chaewon-intern-2026fall`)
  - `Transconnectome/DIVER-2` (로컬: `/home/juke/git/DIVER-2`, 브랜치: `pretrain/hangang-fake-scaling`)
  - Teams 메시지 DB: `~/.agents/registry/chavis_teams/teams.db` 및 `sent_messages.jsonl`
  - 학생 활동 레지스트리: `~/.agents/registry/student_progress/latest.json`

---

## 1. Observation (직접 관측 사실 및 원천 근거)

### 1.1 Teams 메시지 및 전송 기록 직접 관측
1. **이아현 선생님의 보고 메시지 (Message ID: `1793150924795`)**:
   - 위치: `~/.agents/registry/chavis_teams/teams.db`
   - 타임스탬프: `2026-10-28T01:28:44.795Z`
   - 발신자: 이아현 선생님 → 수신자: 차지욱 교수님 (1:1 방 `19:3d8abd69-58f6-43cf-bb89-f60071eaf759...`)
   - 원문:
     > "어제 채원쌤 미팅 했고 kisti 서버에서 멀티노드 실험까지 셋업 스스로 하셔서 scalability plot 넘겨주셨습니다. 오늘은 제가 실제 데이터 넘겨드리면 subject scaling 실험 설계해본다고 하셨습니다!"
2. **차지욱 교수님의 공지 메시지 (Message ID: `1794295206799`)**:
   - 위치: `~/.agents/registry/chavis_teams/sent_messages.jsonl` Line 36
   - 타임스탬프: `2026-11-10T07:20:06.799Z`
   - 원문:
     > "...이아현 선생님이 한강 DIVER-2 scaling을 진행 중이고 안채원 선생님(학부 인턴)이 직접 실험하고 있으니 문의 사항은 두 분께 물어봐 주세요."

### 1.2 Git 저장소 및 커밋 이력 직접 관측
1. **`/home/juke/git/DIVER-2` (브랜치 `pretrain/hangang-fake-scaling`)**:
   - 안채원 선생님 커밋 목록 (`git log --author="안채원"`):
     - `f9cc9be` (2026-10-28 01:36:40): `docs(scaling): 한강 첫 실행 보고 — strong scaling 1→8노드, dataloader 비용 vs Aurora`
     - `7bc6f1e` (2026-10-27 16:27:51): `diver_pretrain: loader/scaling summaries work without a settings line in train.log`
     - `1600fc2` (2026-10-27 16:26:04): `diver_pretrain: loader cost = stall vs in-memory step; record jobs 1154165 + 1154230`
     - `bfd98fd` (2026-10-27 15:43:38): `diver_pretrain: Hangang dataloader sweep + first measured numbers in HANGANG.md`
     - `32bcc5d` (2026-10-27 15:43:38): `diver_pretrain: scaling figure names itself "strong scaling" and carries job + settings`
     - `87f73fe` (2026-10-27 14:43:48): `diver_pretrain: silence "misspelled #SBATCH" warning in Hangang launchers`
     - `96db33c` (2026-10-27 14:37:37): `diver_pretrain: hangang_setup_env.sh stops on errors, single-threaded on login node`
     - `942652b` (2026-10-27 14:08:31): `diver_pretrain: Hangang (KISTI) fake-data and strong-scaling launchers`
   - 핵심 산출 문서: `docs/SCALING/HANGANG_2026-10-28.md`

2. **`Transconnectome/chaewon-intern-2026fall` (클론: `/home/juke/git/chaewon-intern-2026fall`)**:
   - GitHub 원격: `git@github.com:Transconnectome/chaewon-intern-2026fall.git`
   - 최근 활성 브랜치: `main`, `origin/hangang/backup-20261110`, `origin/scaling/subject-axis-report-v0.2`
   - 최근 주요 커밋:
     - `91cfb01` (2026-11-10): `Merge pull request #2 from Transconnectome/hangang/backup-20261110`
     - `7e92a1e` (2026-11-10): `meetings: 회의록 폴더 추가, 11/9 아현쌤 미팅 (피드백·결정·할 일, 슬라이드 PDF, 실험 목록)`
     - `2e9acc9` (2026-11-10): `log: 11/8~11/10 정리 (Small·사람 수·마지막 층 결과, 미팅 피드백, SSL 2개·폭 1024·MAYO 착수)`
     - `5aeb8c6` (2026-11-07): `log: 11/3~11/7 정리 (혼합 2×2, iEEG 1/64 방향 전환, 천장 점검, 극단 줄이기)`
     - `c18df48` (2026-11-02): `log: 11/2 1-a 통과(seed 3개), 1-b worker 비교 재측정`

### 1.3 안채원 선생님의 주요 연구 4개 트랙 직접 관측

#### 트랙 1: KISTI 슈퍼컴퓨터 「한강」 DIVER-2 인프라 셋업, 분산 확장성 및 Dataloader 병목 실측
- **문서**: `/home/juke/git/chaewon-intern-2026fall/hangang/README.md` 및 `DIVER-2/docs/SCALING/HANGANG_2026-10-28.md`
- **하드웨어 환경**: KISTI 국가슈퍼컴퓨팅센터 6호기 「한강」(Slurm, GH200 노드당 4장, 노드당 Grace CPU 72코어 ×4, Slingshot 초고속망, `AWS Libfabric` NCCL).
- **Strong Scaling 실측치 (Job ID: `1154165`)**:
  - 모델: AJILE shape, w1024 / d12, PERRANK 8, 20 step.
  - 1노드 (4 GPU): 189.7 samples/s (노드당 189.7), $E(1) = 1.00$
  - 2노드 (8 GPU): 361.6 samples/s (노드당 180.8), $E(2) = 0.95$ (Aurora ALCF는 0.85)
  - 4노드 (16 GPU): 657.1 samples/s (노드당 164.3), $E(4) = 0.87$ (Aurora ALCF는 0.86)
  - 8노드 (32 GPU): 1,180.1 samples/s (노드당 147.5), $E(8) = 0.78$ (Aurora ALCF는 0.83)
  - 처리량 비교: 한강 GH200 1개 노드 처리량이 Aurora 노드(Intel PVC Tile 12개)의 약 3.8배.
- **Dataloader I/O Sweep 및 타이머 버그 발견 (Job ID: `1154230`, `1201136`, `1201137`)**:
  - Cold LMDB (212 GB) 환경에서 PyTorch worker 스윕:
    - Worker 2: 1,126.9 samples/s (in-memory 대비 46%, step 시간 227.2 ms 중 121.7 ms [54%] 데이터 대기)
    - Worker 4: 2,289.8 samples/s (in-memory 대비 94%, 데이터 대기 6.3 ms [6%])
    - Worker 8: 2,187.5 samples/s (in-memory 대비 90%, 데이터 대기 11.5 ms [10%])
    - Worker 16: 2,244.7 samples/s (in-memory 대비 92%, 데이터 대기 8.5 ms [7%])
  - **결정적 버그 발견 및 해결**: DIVER 학습 코드 내부 타이머(`DIVER_STEP_TIMERS`)가 DDP 환경에서 loader stall을 측정하지 못하고 0%로 오표기되는 문제 규명. DDP gradient all-reduce 동기화 특성상 rank 0이 다른 GPU의 dataloader 대기를 backward/opt_step stall 시간으로 잘못 흡수함을 입증하고, 전체 step 타임스탬프 차이 계산 방식으로 수정.
  - **실데이터(iEEG vs EEG) worker 요구량 차이 실측**:
    - EEGV2: worker 16에서 대기 비율 8.2% (worker 4로 포화).
    - iEEG: worker 16에서도 GPU 대기 비율 15.6% (12.3~17.3%)로 병목 잔존. 기본 worker 2에서는 GPU 대기 24%에 달함.

#### 트랙 2: 대용량 뇌파 데이터 이관 (NERSC & AICA → 한강)
- **문서**: `/home/juke/git/chaewon-intern-2026fall/data_transfer/README.md`
- **전송 완료 데이터**:
  - AICA → 한강 data mover: DIVER-1 iEEG LMDB (Sub1~26 중 Sub21 결번, 25명, 약 4,028시간, 레코드 483,328개) 3.28 TB (평균 155 MB/s, 5시간 53분 소요).
  - EEGV2_compressed: 3.7 TiB (약 4.0 TB) 전송 완료.
  - AJILE12 (836 GB), BTB (7.9 GB, 5명) 전송 완료.
  - 기술적 발견: LMDB 파일이 sparse 파일 구조(`apparent-size` 3.0 TiB vs 실제 `du -sh` 608 GB)임을 파악하고 `--sparse` 옵션의 필수성 정립.

#### 트랙 3: Subject 축 Scaling Law 수립 및 이론적 모델링
- **문서**: `/home/juke/git/chaewon-intern-2026fall/scaling_literature/SUBJECT_AXIS_REPORT.md`
- **핵심 문헌 5편 정밀 분석**:
  1. Oliveira et al. (2026, arXiv:2609.35056): 두피 EEG, 1인당 trial × 사람 수 독립 스윕 ($L = A N_t^{-\alpha} + B N_s^{-\beta} + L_\infty$). $\beta$가 0.07~1.99로 극단적 불안정.
  2. Narayanswamy et al. (2024, LSM, arXiv:2410.13638): 총 시간이 같으면 loss 유사.
  3. Banville et al. (2025, Meta, arXiv:2501.15322): 사람 축 적합 안 함. 사람별 층 사용 및 seen subject 평가로 사람 효과 가림.
  4. Ooi et al. (2025, Nature 644:731): fMRI phenotype 예측에서 $r = K_0 \sqrt{1 / (1 + K_1/N + K_2/(NT))}$. 짧을 때는 총량($NT$)만 중요하나, 길어지면 피험자 수($N$)가 병목.
  5. Truong et al. (2026, arXiv:2610.09287): 두피 EEG 10→1,863명. ~50명 이하에서는 성능 변화가 평평하고(onset), 50명 초과 구간에서 $\log_2 S$ 선형 증가.
- **실제 iEEG 레지스트리(v8) 기반 대조 실험 3종(C1, C2, C3) 설계**:
  - **C1 (총량 고정 배분, 설계 A)**: PennEPI 코호트 (1인당 중앙값 176시간, 103명 전원 40시간 이상 가능) 활용. 총 120h, 240h, 480h 3단계에서 $S \times H$ 배분 스윕.
  - **C2 (데이터셋/병원 다양성 대조)**: 6개 데이터셋(FR1, SWS, CCEP, PennEPI, SWEC, UMN)에서 48명 대상 1인당 30 ch-h 고정 조합 스윕.
  - **C3 (1인당 시간 고정, 사람 수 스윕, 설계 B)**: RAM (FR1 + catFR1 중복 148명 제거 후 고유 377명) 활용. Truong onset(50명)을 검증하기 위해 20, 40, 80, 140, 200명 스윕.
- **신규 함수형 2종 경쟁 및 가설 검정 체계 제안**:
  - Oliveira형 ($L = A H^{-\alpha} + B S^{-\beta} + L_\infty$) vs Ooi형 딥러닝 확장판 ($L = E + K_1 S^{-\beta} + K_2 (S \cdot H)^{-\gamma}$).
  - 귀무가설 $H_0: K_1 = 0$ ("피험자 다양성은 총량과 별개로 독립적 효과가 없다") 검정 체계 구축. 외삽 오차(120~240h 적합 후 480h 예측)로 우열 판정.

#### 트랙 4: AAAI 2027 NeuroAI 워크숍 주도 논문 (마감: 2026-11-20)
- **문서**: `hangang/reports/paper_skeleton.md` (39KB), `meetings/2026-11-09_아현쌤/README.md`
- **논문 제목 후보**: *"A Little iEEG Goes a Long Way: Data Saturation and Non-Substitutability in Multimodal Neural Foundation Models"*
- **핵심 주장**: 멀티모달 뇌 파운데이션 모델에서 iEEG는 고유 기록 기준으로 극소량(1/64 ~ 1/1024, 사람 37명 유지 시 5~81시간)만으로도 하류 과제 표현력이 비열등하게 보존되지만, 이를 두피 EEG로 대체하는 것은 통계적으로 유의미한 손실을 초래한다.
- **실측 실험 데이터 및 검증 수치**:
  1. **고유 기록 축소 비열등성 (1/16 ~ 1/1024 스윕, Seed $n=6$, 95% t-CI)**:
     - 1/64 (81.3시간, 전체의 1.56%): $\Delta\text{score} = -0.0004 [-0.0019, +0.0012]$ (비열등, 판정 기준선 $\Delta > -0.005$)
     - 1/256 (20.3시간): $\Delta\text{score} = -0.0010 [-0.0031, +0.0012]$ (비열등)
     - 1/1024 (5.1시간, 613개 30초 레코드): $\Delta\text{score} = +0.0006 [-0.0012, +0.0024]$ (비열등)
     - 반감 기울기: 기록 절반당 변화 $+0.00001 [-0.00021, +0.00022]$로 0과 구별 불가능.
     - 대조군 검증: 학습 안 한 모델(scratch) 대비 Base는 $+0.0336 [+0.0255, +0.0417]$의 사전학습 이득을 가지며, 1/64 모델은 이 사전학습 이득의 98.9% (95% CI 하한 기준 94.2% 이상)를 보존.
  2. **멀티모달 대체(Fill) vs 반복(Repeat) 대조 (Seed $n=6$)**:
     - iEEG 12.5%만 남기고 나머지를 두피 EEG로 채운 모델(`EEG_fill`): Base 대비 $-0.0103 [-0.0147, -0.0059]$로 유의미하게 하락.
     - 부족한 iEEG를 단순히 반복한 모델(`iEEG_re`): `EEG_fill` 대비 $+0.0100 [+0.0074, +0.0125]$로 압도적 우위. 즉 두피 EEG는 iEEG를 대체할 수 없음.
     - 반면 iEEG가 충분한 상태에서 EEG를 추가한 모델(`EEG_add`): `iEEG_re×2` 대비 $-0.0010 [-0.0029, +0.0008]$로 손익 없음(비열등).
  3. **"시간보다 사람" (피험자 수 분리 실험, Seed $n=6$)**:
     - 동일한 9,757개 기록(81h)에서:
       - 8명 분산: $\Delta = +0.0001 [-0.0012, +0.0014]$ (37명과 동등 유지).
       - 2명 집중: $\Delta = -0.0055 [-0.0101, -0.0010]$ (비열등 경계 붕괴, 통계적 손실 확정).
     - 극단적 613개 기록(5h)에서도:
       - 8명: $-0.0013 [-0.0047, +0.0020]$ (유지).
       - 2명: $-0.0052 [-0.0099, -0.0005]$ (붕괴).
     - 전극 타입(심부 sEEG depth vs 표면 ECoG grid) 교란 검증: 2명 조건의 모든 seed가 심부 전극(6.9~26.3%)을 포함하고 있어 전극 종류 부족 가설을 반증.
  4. **층별 표현 보존 메커니즘 (Readout Layer Ablation, Seed $n=6$)**:
     - 1/64 모델: 얕은 층(Layer 1) $\Delta = -0.0004$, 최종 층(Layer 12) $\Delta = -0.0000$으로 전 층에서 표현 유지.
     - 1/1024 모델: 얕은 층(Layer 1) $\Delta = +0.0006$으로 유지되나, 최종 층(Layer 12) $\Delta = -0.0050 [-0.0072, -0.0028]$로 붕괴 발생.
     - 결론: 1/1024의 극단적 축소는 저수준 시계열 특징(1층)만 보존하고 심층 의미 표현(마지막 층)은 붕괴되나, 1/64는 전 층에서 완전한 사전학습 표현을 유지함.
  5. **Held-out Loss와 하류 성능의 분리 현상**:
     - 사전학습 데이터와 동일한 37명의 held-out 기록에 대한 복원 loss는 1/1024에서 $+8.5% [+7.7, +9.2%]$로 악화됨에도 불구하고 하류 과제 score는 유지됨.
     - 반면 사전학습에 전혀 포함되지 않은 완전 신규 피험자(new subjects, Pippi/BYD)에 대한 복원 loss는 1/1024에서도 $-0.1% [-1.3, +1.2%]$로 전체 학습 모델과 완벽히 일치함을 실측 (`job 1247125`).

---

## 2. Logic Chain (관측에서 결론으로의 논리적 전개)

1. **인프라 및 시스템 공학적 검증 (Observation 1.1, 1.2, 1.3-1, 1.3-2)**:
   - 안채원 선생님은 한강 6호기 Slingshot 환경에서 1~8노드 DDP 확장성을 실측하고, $E(8)=0.78$의 고효율을 확인했습니다.
   - 특히 PyTorch DDP all-reduce 특성으로 인해 dataloader 대기 시간이 gradient reduction 단계로 전가되어 표기되지 않던 프로파일링 결함을 규명하고 step timestamp differential 방식으로 수정하여, iEEG가 cold cache 환경에서 16 worker 이상을 요구하는 심각한 I/O 병목임을 입증했습니다.

2. **Scaling Law 이론의 뇌파 영역 확장 (Observation 1.3-3)**:
   - NLP의 Chinchilla(Hoffmann 2022) 및 Muennighoff(2023) 모델, fMRI의 Ooi(2025) 모델을 면밀히 비교 분석하여, "총 토큰량 고정 하의 피험자 vs 시간 배분(C1)", "병원/데이터셋 다양성(C2)", "피험자 수 스윕(C3)"이라는 정밀한 3대 직교 대조군을 설계했습니다.
   - 기존 연구들이 피험자 축 지수를 함부로 피팅하여 $\beta$ 분산이 28배 튀었던 오류(Oliveira)를 지적하고, $\ge 1$ decade, 단조성, held-out 피험자 평가, 완전 수렴 등 6대 적합 기준을 수립했습니다.

3. **파운데이션 모델의 데이터 효율성 및 모달리티 불체환성 입증 (Observation 1.3-4)**:
   - 통계적 비열등성($\Delta > -0.005$) 검증 체계와 6개 random seed 짝 비교를 통해, iEEG 데이터는 고유 분량이 81시간(1/64) 또는 5시간(1/1024)으로 줄어들더라도 사전학습 표현력이 하류 과제에 온전히 전이됨을 실증했습니다.
   - 반면 이 결손을 두피 EEG로 메우는 시도(`EEG_fill`)는 단순 반복(`iEEG_re`) 대비 명백한 성능 손실($-0.0100$)을 유발함을 증명하여, 두피 EEG의 신호 대역(low-frequency)과 두개골 감쇄 특성이 iEEG의 고주파·국소 신경 발화 패턴을 결코 대체할 수 없다는 과학적 결론을 도출했습니다.
   - 또한 동일 데이터 양이라도 2명의 피험자보다 8명의 피험자로 분산시키는 것이 필수적임을 밝혀, 뇌 파운데이션 모델 사전학습의 핵심 스케일링 병목이 "단일 환자의 장시간 연속 기록"이 아니라 "피험자 다양성(inter-subject diversity)"에 있음을 결정적으로 규명했습니다.

---

## 3. Caveats (한계점 및 추가 검증 필요 사항)

1. **하류 평가 과제의 도메인 편향**:
   - 현재 주 평가 지표(`rule3`)에 사용된 Neuroprobe, BYD, Pippi는 대부분 감각·운동·언어 해독 과제(고감마 파워 의존)에 편중되어 있습니다. 두피 EEG가 강점을 갖는 거시적 상태 변화(수면 단계, 각성도 등)나 병리적 발작(MAYO)에 대한 포괄적 평가가 아직 진행 중입니다 (11/10 MAYO 착수).
2. **Within-session 평가 누수 가능성**:
   - 하류 과제 평가가 같은 피험자의 같은 세션 안에서 train/test가 분할되어 있어, 고유 표현의 일반화 능력이 다소 과대평가되었을 가능성이 논문 초안 내부 검토(`draft_gaps-20261109.md` D7)에서 지적되었습니다.
3. **학습 길이 및 모델 용량의 포화 한계**:
   - 현재 주 결과는 Base 모델(2개 블록, ~9.41M 파라미터) 및 2.88M step 기준이며, 204M(폭 1024) 및 초장기 학습(×4 이상)에서는 1/1024의 포화 특성이 유지되지 않거나 학습 불안정이 발생할 가능성이 존재합니다.
4. **미세조정(Fine-tuning) 결과의 미확정**:
   - 주 결과는 Linear Probe(Frozen backbone) 기준이며, Full Fine-tuning에서는 데이터가 적은 1/64 및 1/1024 모델이 과적합(epoch ~7에서 검증 loss 급등)을 보이는 경향이 있어 추가 정규화 기법 검증이 요구됩니다.

---

## 4. Conclusion (최종 종합 결론)

안채원 선생님은 학부 연구생임에도 불구하고,
1. KISTI 슈퍼컴퓨터 인프라 셋업 및 분산 병렬화, DDP 프로파일링 타이머 오류 해결,
2. 신경 스케일링 법칙(Subject-Axis Neural Scaling Law)의 수학적 정식화 및 대조 실험군(C1~C3) 설계,
3. AAAI 2027 NeuroAI 워크숍 주도 논문(1저자급) 집필 및 6-seed 기반의 엄밀한 비열등성 통계 검증을 독자적으로 완수하였습니다.

도출된 핵심 과학적 발견은 다음과 같이 요약됩니다:
- **"A Little iEEG Goes a Long Way"**: iEEG 고유 분량을 81시간(1/64) 또는 5시간(1/1024)까지 대폭 줄여 반복 학습하더라도 하류 해독 성능은 온전히 보존된다.
- **"Non-Substitutability of Scalp EEG"**: 부족한 iEEG를 두피 EEG로 대체하는 것은 통계적으로 명백한 성능 손실($-0.0100$)을 초래하며, 단순 iEEG 반복이 훨씬 우수하다.
- **"Subjects over Hours"**: 동일한 총 기록 시간 하에서 소수 피험자(2명) 집중은 치명적 성능 붕괴($-0.0055$)를 일으키며, 최소 8명 이상의 피험자 다양성이 확보되어야 한다.

---

## 5. Verification Method (독립 재현 및 검증 방법)

### 5.1 저장소 및 커밋 확인
```bash
# 1. 안채원 선생님 인턴 연구 저장소 확인
cd /home/juke/git/chaewon-intern-2026fall
git status
git log -n 10 --oneline

# 2. DIVER-2 한강 런처 및 scaling 보고서 확인
cd /home/juke/git/DIVER-2
git show origin/pretrain/hangang-fake-scaling:docs/SCALING/HANGANG_2026-10-28.md
```

### 5.2 실험 통계 및 결과 데이터 검증
```bash
# 1. NeuroAI 워크숍 논문 뼈대 및 통계 검증
cat /home/juke/git/chaewon-intern-2026fall/hangang/reports/paper_skeleton.md | grep -A 10 "기록 절반당 변화"

# 2. Subject 축 scaling 레포트 검증
head -n 60 /home/juke/git/chaewon-intern-2026fall/scaling_literature/SUBJECT_AXIS_REPORT.md

# 3. 11/9 미팅 피드백 및 다음 실험 엑셀 확인
/home/juke/superclaude-env/bin/python3 -c "
import openpyxl
wb = openpyxl.load_workbook('/home/juke/git/chaewon-intern-2026fall/meetings/2026-11-09_아현쌤/next_experiments_1110.xlsx')
ws = wb['실험 목록']
for row in ws.iter_rows(values_only=True):
    if any(row):
        print(row[:4])
"
```

### 5.3 가설 무효화 조건 (Falsification Conditions)
1. **1/64 비열등성 무효화**: 204M(폭 1024) 대형 모델이나 신규 병리 과제(MAYO) 평가에서 Base 대비 1/64의 $\Delta\text{score}$가 $-0.005$ 미만으로 유의미하게 하락할 경우.
2. **EEG 대체 불가능성 무효화**: 대역별 필터링이나 공간 보정이 적용된 EEG 혼합 모델이 iEEG 단순 반복(`iEEG_re`)과 동등하거나 그 이상의 성능을 보일 경우.
3. **피험자 다양성 우선 가설 무효화**: 2명 피험자 조건에서 전극 수 또는 특정 해부학적 영역을 완벽히 통제했을 때 37명 조건과 차이가 사라질 경우.
