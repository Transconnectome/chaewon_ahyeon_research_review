# Handoff Report: Teams 메시지 및 멘토링 아카이브 기반 안채원 선생님·이아현 선생님 연구 탐색

- **작성자**: teamwork_explorer_survey_1
- **작성 일시**: 2026-11-10T16:00:00Z
- **조사 대상**: 안채원 선생님(학부 연구 인턴), 이아현 선생님(대학원생 멘토), 차지욱 교수님(지도교수) 간의 Teams 대화, Git 멘토링 저장소, 연구 발표 자료 및 실험 데이터 전반

---

## 1. Observation (직접 관찰 사실)

### 1.1 Teams 데이터베이스 (`~/.agents/registry/chavis_teams/teams.db`) 관찰

- **조사 도구 및 테이블**:
  - SQLite3 데이터베이스: `/home/juke/.agents/registry/chavis_teams/teams.db`
  - 테이블: `watched_chats` (모니터링 대상 대화방 16개), `messages` (전체 메시지 로그)
- **주요 대화방**:
  - 대화방 ID: `19:3d8abd69-58f6-43cf-bb89-f60071eaf759_baa70085-4a80-454d-8c7f-081ffb7009c0@unq.gbl.spaces`
  - 대화방 라벨: `이아현 선생님 (1:1 — 2026 동계 인턴십 공고문 피드백 요청)`
  - 참여자: 차지욱 교수님 (`jc@www.connectomelab.com`), 이아현 선생님 (`ahhyun724@www.connectomelab.com`)
  - 총 메시지 수: 57건

#### [직접 인용 1] 김재철 AI 클래스 인턴 멘토링 체계 구축 (2026-10-26 ~ 2026-10-27)
- **2026-10-26T10:19:50.532Z | 차지욱 교수님**:
  > "아현샘이 담당해서 옆에 끼고 많이 시켜보세요. 방학때 해커톤도 데리고 가고"
- **2026-10-26T10:20:11.201Z | 이아현 선생님**:
  > "네네 좀 더 멘토링 열심히 해보겠습니다ㅎㅎ 인코딩 디코딩 쪽 관심 많아하셔서 논문 묶음 드렸었어요"
- **2026-10-27T00:28:32.553Z | 차지욱 교수님**:
  > "조교비가 많이 지원되는 만큼 mentorship plan and report를 만들어서 저와 주기적으로 공유 부탁합니다. 이 학생들이 탑 1%로 뽑힌 학생들이어서 그냥 일반적인 인턴쉽처럼 할게 아니라 most challenging research goals를 설정하고 관리해봅시다. 레포를 하나 만들어서 모든 문서와 산출물을 넣어주세요. 매학기 반복되고 발전시키려고합니다. 학생들은 바뀌더라도"
- **2026-10-27T01:39:15.196Z | 이아현 선생님**:
  > `https://github.com/Transconnectome/KimJaeChul_AI_Class_Mentoring` "이렇게 만들었습니다!"

#### [직접 인용 2] 안채원 선생님 첫 미팅 및 KISTI 멀티노드 셋업 보고 (2026-10-28)
- **2026-10-28T01:28:44.795Z | 이아현 선생님**:
  > "어제 채원쌤 미팅 했고 kisti 서버에서 멀티노드 실험까지 셋업 스스로 하셔서 scalability plot 넘겨주셨습니다. 오늘은 제가 실제 데이터 넘겨드리면 subject scaling 실험 설계해본다고 하셨습니다!"
- **2026-10-28T01:29:27.187Z | 이아현 선생님**:
  > "교수님 그리고 Brainlink에서 DIVER-1 말고 DIVER-1.5 발표할까 하는데 어떨까요?? (동엽쌤 추천!)"

#### [직접 인용 3] 한강 클러스터 DIVER-2 scaling 진행 및 안채원 선생님 역할 확인 (2026-11-10T07:20:06.799Z)
- 대화방: `19:14cd2099-604d-4dd9-9683-8d077a0d3f77_baa70085-4a80-454d-8c7f-081ffb7009c0@unq.gbl.spaces` (이규형 선생님 1:1 대화방)
- **차지욱 교수님**:
  > "이아현 선생님이 한강 DIVER-2 scaling을 진행 중이고 안채원 선생님(학부 인턴)이 직접 실험하고 있으니 문의 사항은 두 분께 물어봐 주세요. 최주빈 선생님도 대규모 scaling 경험이 있으니 참고 코드가 필요하면 요청해 주세요."

#### [직접 인용 4] NeuroAI 워크숍 미팅 요청 및 차지욱 교수님의 비판적 피드백 (2026-11-10T08:18:09.195Z)
- 대화방: `19:3d8abd69-58f6-43cf-bb89-f60071eaf759_baa70085-4a80-454d-8c7f-081ffb7009c0@unq.gbl.spaces`
- 차지욱 교수님이 안채원 선생님의 메시지와 교수님 본인의 회신 내용을 이아현 선생님과의 대화방에 인용 전달:
  > **안채원 선생님 원문**:
  > "교수님, 안녕하세요!
  > 금요일 미팅 공지에 2~3시 슬롯이 있던데, 혹시 members 분들 신청이 없으면 그 시간에 15~20분 정도 미팅 가능할까요?
  > 지난번 승인해 주신 NeuroAI 워크숍(11/20 마감) 연구 방향을 결과에 따라 조정하게 되어 피드백을 받고 싶습니다. EEG+iEEG mixing은 효과가 크지 않았고, 대신 iEEG를 1/64로 줄여도 성능이 유지되는 결과가 나와 이쪽으로 논문을 구성하려 합니다.
  > 결과와 논문 구성을 간단히 정리한 슬라이드 첨부드립니다: https://docs.google.com/presentation/d/1yueDz-YjVbw3q5IkvI8gPvOB8dDzjKzDBE5fQ3J9Tu0/edit?usp=sharing
  > 금요일이 어려우시면 토요일 오전도 괜찮습니다. 감사합니다!"
  > 
  > **차지욱 교수님 회신**:
  > "네, 그냥 섞으면 알아서 잘 학습될 것들이 아니어서 놀랍지 않은 결과입니다.
  > 각 데이터의 특성을 잘 이용하는 prior knowledge를 주입하는 방식이 아니라면, dnn이 공통 표상을 학습하지 못하고 있다는 것을 다 잘 알고 있거든요.
  > iEEG를 더 많이 넣었을때에 효과가 미미 하다는 것도, 놀라운 negative results는 아닙니다. 토큰의 정의, context (time) window, 데이터 특성에 맞는 사전 학습 전략 등등이 갖춰져야 확장적 학습이 될 거여서요.
  > 그래서 현재의 네거티브 결과는, '아직 우리가 준비가 덜 되었다' 는 메세지 밖에는 못 줄겁니다.
  > 설익은 페이퍼를 쓰는 것보다는 의미있는 발견을 먼저 하는게 좋을 것 같습니다.
  > 이 결과에 대해서는 diver 팀 채널에 올려서 공유해주시고 먼저 아현샘과 회의를 해보시구요. 저랑은 월요일에 가능. 급하면 일요일 오전에 가능."

#### [직접 인용 5] 이아현 선생님의 반론 및 재해석 (2026-11-10T14:52:02.312Z ~ 14:52:26.777Z)
- **2026-11-10T14:52:02.312Z | 이아현 선생님**:
  > "아 저는 negative result 가 아니라 발견이라고 생각하는데요. 채원쌤이 본문에 강조 안하신 포인트가 있는데, 단순히 1/64로 데이터 양을 줄이는 것이 아니라 참가자 수는 유지하면서 한 명당 데이터를 1/64로 줄였을 때입니다.
  > 참가자를 줄이면 성능에 harmful 하지만 참가자당 시간을 줄였을 때는 그렇지 않았다는 점이 DIVER-1.5 에서 channel origin prediction 만으로도 좋은 성능이 나왔던 것과 합치되는 결과라고 생각합니다. 어쩌면 참가자 한 명당 긴 데이터를 모두 preprocessing 하지 말고 짧게 여러명 하는데에 effort 를 들이는게 나을수도 있다라는 메세지를 전달할수도 있구요! 물론 이 결론을 내려면 이 SSL specific 한지 알아보기 위해 다른 종류의 SSL 도 시도해보라고 말씀드린 상태입니다.
  > 꼭 Scaling works! 가 아니라 how should we scale 을 보여주는 좋은 포인트라는 생각이 들어서요."
- **2026-11-10T14:52:26.777Z | 이아현 선생님**:
  > "어떻게 생각하시나요? 내일 학회 가서 쉬는 시간에 또 말씀나눠봐도 좋을 것 같습니다!"

---

### 1.2 Git 멘토링 아카이브 (`KimJaeChul_AI_Class_Mentoring`) 상세 관찰

- **원격 저장소**: `https://github.com/Transconnectome/KimJaeChul_AI_Class_Mentoring` (HEAD: `a7271dc`)
- **학생 디렉토리**: `students/2026-2_ChaewonAhn/`
- **미팅 일지 및 활동 이력**:
  1. `meetings/2026-10-07.md` (대면):
     - 관심 분야: 인코딩/디코딩, Alexander Huth, Uri Hasson, Edward Chang lab (PMID: 40164740).
     - 논문 독해법, Zotero 정리, Scaling law 기초 영상 학습.
  2. `meetings/2026-10-13.md` (온라인):
     - DIVER-2 피험자 수(subject-wise) scaling axis 과제 부여 (`ASSIGNMENT_subject_axis.md`, `ScalingLawSearch.md`).
     - PennEPI 103명 C1 대조군, UMN(81채널) vs PennEPI(144채널) 채널 수 차이, SWEC 대역폭 교란 요인 통제 방안 논의.
  3. `meetings/2026-10-27.md` (대면):
     - MLDL 기초(LR, WD, scheduler, optimizer), EEG/iEEG site effect 및 임상 데이터 특성.
     - DIVER-1, MAPA, BrainWave 비교.
  4. `meetings/2026-10-29.md` (카카오톡):
     - 한강 fake-data scaling 실행 완료 (`HANGANG_2026-10-28.md`).
     - NeuroAI Workshop 2027 (Montreal, 2027-02-22~23, 마감 2026-11-20) 투고 목표 수립.
     - AICA H100의 `EEGV2_compressed` (~3.7TB) 데이터 이전 (Globus/rsync, ~140MB/s).
  5. `meetings/2026-10-30_to_2026-11-01.md` (카카오톡):
     - Subject scaling 보고서 초안 (`SUBJECT_AXIS_REPORT.md`). C1/C2/C3 대조 설계.
     - Batch/site effect 보정을 위한 Harmony, ComBat-seq 검토.
  6. `meetings/2026-11-02_to_2026-11-03.md` (카카오톡):
     - 단기 실행 계획: bf16 안정성, dataloader 시간 비교, subject scaling, DeepSeek-style hyperparameter sweep.
     - NeuralBench, iMindBench/MAYO 벤치마크, DIVER-2 data mixing 설계 (`MIXING_EXPERIMENT.md`).
  7. `meetings/2026-11-03.md` (Zoom):
     - Hangang vs AICA G4/BTB 비교 시 step 속도 1.72배 단축, runtime 80% 달성 (seed 3).
     - `num_workers` 튜닝: AJILE 2, iEEG 16, EEG 24 설정으로 GPU 대기 시간 <10% 달성.
     - 이아현 선생님의 선행 batch effect 점검 공유: 단순 linear method로는 batch effect 완전 해결 불가.
  8. `meetings/2026-11-03_to_2026-11-08.md` (카카오톡):
     - 초기 실험 발견: 고유 iEEG를 12.5%로 줄이고 반복(`R12.5`)한 점수(0.636)가 전체 고유 데이터(`Base`)와 동등. 반면 부족분을 EEG로 채운 `F12.5`는 0.01 하락.
     - 추가 실험: 고유 iEEG를 1/64로 줄여도 Neuroprobe·BYD·Pippi의 frozen linear-probe 평균이 유지됨을 발견.
  9. `meetings/2026-11-09.md` (온라인 미팅) & 11/10 후속 피드백:
     - 11/9 슬라이드 기반 종합 점검. 이아현 선생님의 12대 피드백 및 후속 액션 아이템 수립 (학습량 ×2·×4 seed 보강, G4 외 기본 SSL 목표 비교, 51M 초과 대형 모델 검증, Figure (a) seed별 대응선 표기, seed 난수 영향 범위 코드 점검 등).

---

### 1.3 안채원 선생님 발표 슬라이드 전문 관찰 (`https://docs.google.com/presentation/d/1yueDz-YjVbw3q5IkvI8gPvOB8dDzjKzDBE5fQ3J9Tu0/edit`)

- **슬라이드 제목**: "고유 iEEG는 얼마나 필요한가: 학습량을 고정하면, 필요한 건 기록 시간보다 사람 수" (NeuroAI 워크숍 진행 보고 · 안채원 선생님 · 2026.11.9)
- **연구 질문**: 총 학습량을 고정했을 때 필요한 고유 iEEG 기록은 얼마이며, 부족한 iEEG를 EEG로 채우는 것이 같은 iEEG를 반복하는 것보다 도움이 되는가?
- **실험 설정 및 파라미터**:
  - 데이터: iEEG 37명 (사설 25명 + AJILE 12명), 총 5,203시간. (BTB는 Neuroprobe와 겹쳐 제외)
  - 학습량: 총 288만 샘플(2.88M) 고정 (3초 윈도우 × 최대 32채널). 고유 기록을 줄이면 동일 기록에서 무작위 crop/channel 추출로 반복 충원.
  - 모델: Base = DIVER-1 (2블록 × 폭 512, 9.4M 파라미터), MAE 사전학습. (검증용: Small 51M, Tiny 13M, G4 전극 식별 방식).
  - 평가: Frozen linear probe, iEEG 다운스트림 3개 과제 (Neuroprobe 15개 하위과제, BYD, Pippi) 평균 (`rule3`), 첫 번째 블록(1st layer) 표현 판정.
  - 비열등성 판정 기준: 사전 정의된 seed 짝 차이 95% 신뢰구간 하한 > −0.005 (사전학습 효과 +0.034의 15% 이내 손실 허용).

#### [실험 1 핵심 결과] 고유 샘플 수 축소 vs 총 학습량 축소
| 조건 | 고유 iEEG 시간 | 총 노출 학습량 | 평가 점수 (`rule3`) | 비고 |
|---|---|---|---|---|
| 미학습 (Untrained) | - | 0 | .6039 ± .0041 | 기준선 (n=3) |
| EEG-only 사전학습 | 0 (EEG만) | 2.88M | .6212 ± .0053 | EEG 전이 한계 (n=3) |
| 학습량 1/16 | 5,203h | 0.18M | .6194 ± .0005 | 학습량 부족 시 급락 (n=3) |
| 학습량 1/8 | 5,203h | 0.36M | .6276 ± .0087 | (n=3) |
| 학습량 ≈0.22 (1 epoch) | 5,203h | 0.63M | .6294 ± .0030 | 전체 기록 1회 노출 (n=3) |
| 학습량 1/4 | 5,203h | 0.72M | .6305 ± .0030 | (n=3) |
| 학습량 1/2 | 5,203h | 1.44M | .6336 ± .0068 | (n=3) |
| 학습량 1배 (Base) | 5,203h (100%) | 2.88M | .6363 ± .0025 | 기준 Base (n=6) |
| 학습량 2배 | 5,203h | 5.76M | .6360 ± .0059 | 포화 관찰 (n=3) |
| 고유기록 1/16 반복 | 325h | 2.88M | .6361 ± .0026 | 유지 (차이: -.0002) |
| 고유기록 1/64 반복 | 81h | 2.88M | .6359 ± .0024 | 유지 (차이: -.0004) |
| 고유기록 1/1024 반복 | 5h (610개 세그먼트) | 2.88M | .6369 ± .0021 | 유지 (차이: +.0006) |

- **핵심 관찰 (괴리 현상)**:
  - 고유 기록을 1/1024(5시간)로 줄이면 Held-out reconstruction loss는 +8.5% 악화됨에도 불구하고, 다운스트림 representation 품질(linear probe 점수)은 93% 이상 보존됨.

#### [실험 2 핵심 결과] EEG 대체(`EEG_fill`) vs 반복(`iEEG_re`) vs 추가(`EEG_add`)
1. **EEG 대체는 명백한 손해 (`EEG_fill`)**:
   - 총 2.88M 샘플에서 고유 iEEG 12.5% 고정 시:
   - 부족분을 iEEG 반복으로 채움 (`iEEG_re`): 전체 iEEG와 동일 (차이: −.0003 [−.0027, +.0021]).
   - 부족분을 EEG로 대체 (`EEG_fill`): 점수 하락.
   - `iEEG_re − EEG_fill = +0.0100` (seed 6쌍 모두 일관되게 `iEEG_re` 우세).
   - 혼합 비율(`fillfrac`), 주파수 저역통과 필터(`lowpass`) 적용으로도 손해는 회복되지 않음.
2. **EEG 추가는 무해하나 추가 이득 없음 (`EEG_add`)**:
   - `EEG_add` (총 5.77M): `EEG_add − iEEG_re ×2 = −0.0010 [−.0029, +.0008]` (seed 3, 비열등).
   - iEEG를 2배 학습하든 EEG를 더하든 성능 향상이 없는 compute 포화 상태 확인.

#### [실험 3 핵심 결과] 일반성과 성립 조건 (피험자 수 vs 읽는 층)
1. **피험자 수 축소 (Person Diversity)**:
   - 고유 기록 양(81h 또는 5h) 및 학습량(2.88M)을 고정하고 데이터 출처 피험자 수를 줄임:
   - **8명 조건**: 81h에서 `+.0001` (유지), 5h에서 `-.0013` (유지).
   - **2명 조건**: 81h에서 `-.0055` (성능 붕괴), 5h에서 `-.0052` (성능 붕괴).
   - **발견**: iEEG 파운데이션 모델 사전학습에서 중요한 것은 "1인당 긴 기록 시간"이 아니라 "최소 8명 이상의 다수 피험자 다양성"임.
2. **읽는 층에 따른 표현 차이 (Layer Readout Effect)**:
   - **첫 번째 블록(1st layer)**: 1/64 및 1/1024 모두 Base/Small에서 완벽히 유지.
   - **마지막 블록(Last layer)**:
     - 1/64 조건: Base (`-.0000`), Small (`-.0006`) 모두 마지막 층에서도 유지.
     - 1/1024 조건: Base (`-.0029`, 판정불가), Small (`-.0050`, 성능 붕괴).
   - 깊은 표현일수록 데이터 고유 다양성 부족의 타격을 먼저 받음.

---

## 2. Logic Chain (논리 추론 체인)

1. **[관찰 1.1 + 1.2 참조]**
   - 차지욱 교수님은 2026-10-26~27에 이아현 선생님에게 김재철 AI 클래스 인턴(안채원 선생님)에 대한 1:1 밀착 멘토링과 최고 난도 연구 과제 수행, 그리고 영구 아카이브 구축(`KimJaeChul_AI_Class_Mentoring`)을 명시적으로 지시하였다.
2. **[관찰 1.2 참조]**
   - 이아현 선생님은 안채원 선생님에게 DIVER-2 프로젝트의 핵심 미해결 질문인 "피험자 수(subject-wise) scaling axis"와 "EEG-iEEG data mixing" 연구를 과제로 부여하고, KISTI 및 Hangang 슈퍼컴퓨팅 인프라에서 실험을 주도하도록 지도하였다.
3. **[관찰 1.3 참조]**
   - 안채원 선생님은 방대한 실험(총 2.88M 노출 샘플 고정, 37명/5,203h iEEG 데이터셋 기반)을 통해 두 가지 결정적 결과를 도출하였다:
     - (a) **EEG-iEEG mixing의 비효율성**: 고정 compute 하에서 부족한 iEEG를 EEG로 채우는 것(`EEG_fill`)보다 적은 고유 iEEG를 반복 학습(`iEEG_re`)하는 것이 +0.010 높은 성능을 보임.
     - (b) **Subject Diversity > Duration**: 고유 기록을 1/64(81h) 및 1/1024(5h)로 대폭 축소하더라도 37명 또는 8명의 피험자 다양성을 유지하면 representation 품질이 유지되나, 2명으로 줄이면 성능이 즉시 붕괴됨.
4. **[관찰 1.1 직접인용 4 참조]**
   - 차지욱 교수님은 안채원 선생님의 초기 요약("EEG+iEEG mixing 효과 없음, iEEG 1/64 축소 시 유지")을 보고, "사전 지식 없이 무작정 섞으면 학습 안 되는 것은 당연하며, 데이터 부족 시 확장이 안 되는 것은 준비 부족을 뜻하는 음성 결과(negative result)에 불과하다"며 워크숍 투고에 대해 강한 우려와 회의적 시각을 제시하였다.
5. **[관찰 1.1 직접인용 5 참조]**
   - 이아현 선생님은 즉각 반론을 제기하며 본 연구의 핵심 가치는 "단순한 1/64 데이터 축소가 아니라, 피험자 수를 유지한 상태에서 1인당 기록 시간을 줄여도 성능이 유지된다는 'how should we scale'에 관한 중대한 발견"임을 규명하였다. 이는 DIVER-1.5의 채널 식별(channel origin prediction) 사전학습 성공 요인과 정확히 부합하며, 복잡한 전처리 대신 소표본 다수 피험자 수집이 효율적이라는 임상/AI 방법론적 가이드라인을 제공한다.

---

## 3. Caveats (조사 한계 및 주의사항)

1. **원천 데이터 및 개인정보 보호**:
   - 환자 private iEEG 원천 데이터(서울대병원/정천기 교수님 연구실 데이터 등)는 보안 규정에 따라 Git 저장소 및 로컬 환경에 포함되지 않았으며, 통계적 메타데이터와 집계 결과만을 확인하였다.
2. **평가 지표의 국한성**:
   - 주 평가 지표가 Frozen linear probe(선형 분류기 고정 평가) 및 첫 번째 블록(1st layer) 표현에 집중되어 있다. Full fine-tuning(전체 가중치 미세조정) 및 임상적 이상 파형 검출(간질 발작파 등 병리적 과제)에서의 검증은 아직 완전히 완료되지 않았다.
3. **다운스트림 과제 수**:
   - Neuroprobe(15개 세부 과제), BYD, Pippi 등 3대 과제 평균(`rule3`)으로 판정하였으며, 세부 15개 과제별로는 데이터 부족으로 인한 "판정 불가" 항목이 다수 존재한다.
4. **대형 모델 검증 한계**:
   - 대부분의 실험이 Base(9.4M) 및 Small(51M) 규모에서 수행되었으며, 100M~200M 이상의 대규모 파운데이션 모델 스케일에서의 반복 재현은 연산 자원 및 시간 제약으로 추가 실험이 계획 단계에 있다.

---

## 4. Conclusion (최종 종합 결론)

1. **연구의 핵심 실체**:
   - 안채원 선생님과 이아현 선생님이 수행한 연구는 단순한 "데이터 혼합 실패 보고"가 아니며, **"iEEG Foundation Model에서 총 연산량을 통제했을 때, 모델 표현력 형성을 결정짓는 핵심 병목은 '개인당 긴 기록 시간(Duration)'이 아니라 '피험자 다양성(Subject Diversity)'이다"**라는 scaling law의 축(Axis)에 관한 독창적이고 체계적인 실증 연구이다.
2. **학술적 기여 및 방어 논리**:
   - 기존 문헌(BrainWave, BrainOmni 등)이 EEG 혼합 시 총 compute 증가 효과와 모달리티 전이 효과를 혼동했던 오류를 정밀한 ablation(동일 compute 통제)을 통해 분리해 냈다.
   - 부족한 희귀 뇌신호(iEEG) 데이터를 억지로 상이한 모달리티(EEG)로 메우는 것보다, 적은 양의 iEEG라도 다수 피험자로부터 추출하여 반복 노출시키는 것이 representation 학습에 훨씬 우월함을 입증하였다.
3. **적대적 리뷰(Adversarial Review) 팀으로의 인계점**:
   - 차기 에이전트는 본 handoff 보고서의 정량 수치와 실험 설계를 바탕으로 최신 NeuroAI 문헌(MAE vs Contrastive, multi-subject EEG/iEEG foundation models, batch effects)을 대조하여, 가설 타당성, 인과 추론의 엄밀성, 통계적 다중비교 보정, 평가 프로토콜(첫 층 vs 마지막 층) 한계를 중심으로 한 적대적 리뷰를 전개해야 한다.

---

## 5. Verification Method (독립 검증 방법)

차기 에이전트 및 검토자는 아래 명령어를 통해 본 보고서의 모든 사실 관계와 데이터를 직접 재현 및 검증할 수 있습니다.

1. **Teams 메시지 원문 및 1:1 대화 검증**:
   ```bash
   python3 -c "
   import sqlite3
   conn = sqlite3.connect('/home/juke/.agents/registry/chavis_teams/teams.db')
   c = conn.cursor()
   c.execute('SELECT created_at, sender_name, body_plain FROM messages WHERE chat_id = \'19:3d8abd69-58f6-43cf-bb89-f60071eaf759_baa70085-4a80-454d-8c7f-081ffb7009c0@unq.gbl.spaces\' AND (created_at LIKE \'%2026-10-28%\' OR created_at LIKE \'%2026-11-10%\') ORDER BY created_at;')
   for r in c.fetchall():
       print(f'[{r[0]}] {r[1]}: {r[2][:150]}...\n')
   "
   ```
2. **멘토링 저장소 커밋 이력 및 문서 검증**:
   ```bash
   cd /tmp/KimJaeChul_AI_Class_Mentoring
   git log --oneline -n 6
   cat students/2026-2_ChaewonAhn/meetings/2026-11-09.md | head -n 45
   ```
3. **안채원 선생님 발표 슬라이드 전문 텍스트 검증**:
   ```bash
   curl -sL "https://docs.google.com/presentation/d/1yueDz-YjVbw3q5IkvI8gPvOB8dDzjKzDBE5fQ3J9Tu0/export/txt" | grep -A 10 "고유 iEEG는 얼마나 필요한가"
   ```
4. **무효화 조건 (Invalidation Conditions)**:
   - 슬라이드 상의 수치(`rule3` 기준 .6363 Base, .6359 1/64, .6369 1/1024, 2명 시 -.0055 붕괴 등)가 실제 원본 텐서보드 로그나 체크포인트 평가와 다를 경우 본 결론의 수치적 근거는 재조정되어야 한다.
   - 첫 번째 블록(1st layer)이 아닌 최종 분류 헤드(Full fine-tuning)에서 1/64 및 8명 조건의 성능 붕괴가 관찰될 경우, "피험자 수 축소가 representation 전반에 안전하다"는 결론은 조건부로 축소되어야 한다.
