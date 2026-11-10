# Survey Explorer 3 Handoff Report: 이아현 선생님 Research Portfolio, Synergies with 안채원 선생님, & Infrastructure

- **작성자**: `teamwork_explorer_survey_3` (Explorer Archetype)
- **작성일시**: 2026-11-10T16:00:00Z
- **조사 대상**: 이아현 선생님의 연구 내역, 핵심 가설, 데이터·코드·실험 결과, 안채원 선생님과의 연구 시너지 및 GitHub Transconnectome 인프라 현황
- **참조 문서**:
  - `ORIGINAL_REQUEST.md`
  - `~/.agents/registry/chavis_teams/teams.db` 및 Teams Graph API (채팅 및 채널 전체)
  - `Transconnectome/KimJaeChul_AI_Class_Mentoring` (GitHub)
  - `~/git/DIVER-2` (branch: `docs/scaling-plan`)
  - `~/git/ephys-foundation-model-plan` (`submissions/2026/`)
  - `~/git/connectome-paper-submissions`

---

## 1. Observation (직접 관찰된 사실)

### 1.1 이아현 선생님의 연구자 프로필 및 핵심 역할
- **신원 및 직책**: 서울대학교 인지신경과학 연구실(Connectome Lab) 박사과정 연구원. 김재철 AI 클래스 학부 연구인턴 멘토 (학번: `2024-26798`, GitHub: `yahyunee`, 이메일: `ahhyun724@snu.ac.kr`).
- **연구 주도 과제**:
  - **DIVER-1**: 침습적 뇌파(iEEG) 대규모 파운데이션 모델 (5,203시간, 37명 피험자, ICLR 2027 revision 제출 및 arXiv:2512.19097).
  - **DIVER-1.5**: 비대칭 조건부 위치 인코딩(ACPE) 및 채널 출처 예측(channel origin prediction) 기반 자체지도학습(SSL) 모델링.
  - **DIVER-2**: iEEG 기반 최초의 파라메트릭 스케일링 법칙(Scaling Laws) 정립 및 Aurora 슈퍼컴퓨터(25,000 노드시간 할당) 기반 대규모 사전학습.
  - **김재철 AI 클래스 멘토링**: 안채원 선생님의 연구 주제 설정, 가설 수립, 실험 설계, 논문 작성을 1:1 전담 지도.

### 1.2 Teams 메시지 직접 관찰 및 인용
1. **김재철 AI 클래스 멘토링 저장소 구축 (2026-10-27)**
   - `19:3d8abd69-58f6-43cf-bb89-f60071eaf759_baa70085-4a80-454d-8c7f-081ffb7009c0@unq.gbl.spaces`:
   - 차지욱 교수님: *"조교비가 많이 지원되는 만큼 mentorship plan and report를 만들어서 저와 주기적으로 공유 부탁합니다... 레포를 하나 만들어서 모든 문서와 산출물을 넣어주세요."*
   - 이아현 선생님 (2026-10-27T01:39:15Z): `https://github.com/Transconnectome/KimJaeChul_AI_Class_Mentoring` 생성 보고.

2. **안채원 선생님과의 협업 및 멀티노드 셋업 보고 (2026-10-28)**
   - 이아현 선생님 (2026-10-28T01:28:44Z): *"어제 채원쌤 미팅 했고 kisti 서버에서 멀티노드 실험까지 셋업 스스로 하셔서 scalability plot 넘겨주셨습니다. 오늘은 제가 실제 데이터 넘겨드리면 subject scaling 실험 설계해본다고 하셨습니다!"*
   - 이아현 선생님 (2026-10-28T01:29:27Z): *"교수님 그리고 Brainlink에서 DIVER-1 말고 DIVER-1.5 발표할까 하는데 어떨까요?? (동엽쌤 추천!)"*

3. **안채원 선생님의 연구 결과에 대한 차지욱 교수님의 비평과 이아현 선생님의 적극적 반론·옹호 (2026-11-10)**
   - 차지욱 교수님 (2026-11-10T08:18:09Z, 안채원 선생님의 슬라이드 공유 및 미팅 요청 전달):
     > *"네, 그냥 섞으면 알아서 잘 학습될 것들이 아니어서 놀랍지 않은 결과입니다. 각 데이터의 특성을 잘 이용하는 prior knowledge를 주입하는 방식이 아니라면, dnn이 공통 표상을 학습하지 못하고 있다는 것을 다 잘 알고 있거든요. iEEG를 더 많이 넣었을때에 효과가 미미 하다는 것도, 놀라운 negative results는 아닙니다... 그래서 현재의 네거티브 결과는, '아직 우리가 준비가 덜 되었다' 는 메세지 밖에는 못 줄겁니다. 설익은 페이퍼를 쓰는 것보다는 의미있는 발견을 먼저 하는게 좋을 것 같습니다."*
   - 이아현 선생님의 직접 반론 (2026-11-10T14:52:02Z):
     > *"아 저는 negative result 가 아니라 발견이라고 생각하는데요. 채원쌤이 본문에 강조 안하신 포인트가 있는데, 단순히 1/64로 데이터 양을 줄이는 것이 아니라 참가자 수는 유지하면서 한 명당 데이터를 1/64로 줄였을 때입니다.*  
     > *참가자를 줄이면 성능에 harmful 하지만 참가자당 시간을 줄였을 때는 그렇지 않았다는 점이 DIVER-1.5 에서 channel origin prediction 만으로도 좋은 성능이 나왔던 것과 합치되는 결과라고 생각합니다. 어쩌면 참가자 한 명당 긴 데이터를 모두 preprocessing 하지 말고 짧게 여러명 하는데에 effort 를 들이는게 나을수도 있다라는 메세지를 전달할수도 있구요! 물론 이 결론을 내려면 이 SSL specific 한지 알아보기 위해 다른 종류의 SSL 도 시도해보라고 말씀드린 상태입니다.*  
     > *꼭 Scaling works! 가 아니라 how should we scale 을 보여주는 좋은 포인트라는 생각이 들어서요."*

4. **DIVER Scaling 채널 (`19:27441eb22b2343fa8630c5fd5896c9b1@thread.tacv2`) 기록**
   - 2026-11-07: 이아현 선생님: 5% 데이터셋에 대한 scaling plot 공유 (`https://claude.ai/artifact/FzS1uTW4WrKNVwBgRaJkwJ`), validation loss 추적 artifact (`https://claude.ai/artifact/Ps5hWnVkYoiHuT8BNCLRqw`).
   - 2026-10-13: 이아현 선생님: DIVER-2 예산 계획(Aurora 25,000시간 중 36% 활용 계획) 및 의사결정 사항 공유 (`https://github.com/DIVER-Project/DIVER-2/tree/docs/scaling-plan/docs/SCALING`). "Subject scaling & Data mixing 부분은 채원쌤께서 담당해주시기로 했습니다!" 명시.
   - 2026-09-28: 이아현 선생님: 올해 11월 submission format 완성 후 Nature 자매지 급 투고 목표 수립. 선행연구 BrainWave(임상 중심)와의 차별화(BCI+인지+임상 다운스트림 벤치마크 통합) 설정.

### 1.3 `Transconnectome/KimJaeChul_AI_Class_Mentoring` 상세 기록
- 저장소 경로: `https://github.com/Transconnectome/KimJaeChul_AI_Class_Mentoring` (최근 커밋: 2026-11-10T05:54:38Z).
- `students/2026-2_ChaewonAhn/meetings/2026-11-09.md` (2026-11-09 온라인 미팅 기록):
  - **연구 질문**: 총 학습량을 고정했을 때 필요한 고유 iEEG 기록은 얼마이며, 부족한 iEEG를 EEG로 채우는 것이 같은 iEEG를 반복하는 것보다 도움이 되는가?
  - **실험 데이터**: 37명의 iEEG 약 5,203시간, 총 학습 노출 샘플 수 288만으로 통제.
  - **모델 및 학습**: DIVER-1 Base (2블록 x 폭 512, 약 9.4M), 주 사전학습 목표 MAE (Masked Autoencoder).
  - **다운스트림 평가**: Neuroprobe, BYD, Pippi의 frozen linear-probe 평균(`rule3`), 1번째 블록 출력 기준.
  - **관찰 결과**:
    - 피험자 37명을 유지한 채 고유 기록을 1/64(약 81시간), 1/1024(약 5시간)까지 줄여도, 총 학습량(288만 샘플)을 맞추면 1블록 기준 downstream 점수가 유지됨.
    - 반면 총 학습량 자체를 줄이면 성능이 크게 하락함.
    - `iEEG_re`(고유 iEEG 줄이고 반복) 조건이 `EEG_fill`(부족한 양을 EEG로 대체) 조건보다 주 평가 점수가 약 0.010 우수함 (seed 6쌍).
    - `EEG_add`(iEEG 유지 + EEG 추가, 총 학습량 577만)는 `iEEG_re x2` 대비 뚜렷한 이득 없음.
    - 피험자 수를 37명에서 8명으로 줄였을 때는 유지되나, 2명으로 줄였을 때는 급격한 성능 저하 발생.
    - 층별 차이: 1/64 조건은 Base 및 Small(51M) 마지막 층에서도 유지되었으나, 1/1024 조건은 Small 마지막 층에서 저하됨.
  - **이아현 선생님의 멘토링 피드백 및 액션 아이템**:
    1. 주장의 일반화 한계 명확화: 1블록 평가에 한정된 결과인지 심층 층에서도 성립하는지 확인.
    2. Random seed의 영향 위치(데이터 추출, 초기화, 학습, 평가) 전수 감사.
    3. MAE 외의 다른 SSL 목표(단순 channel-identification, contrastive 등)와 비교하여 SSL-specific 현상인지 규명.
    4. Held-out reconstruction loss가 악화됨에도 downstream 점수가 유지되는 모순 관계 규명.

### 1.4 `DIVER-2` 저장소 (`docs/scaling-plan`) 및 문헌 조사
- 파일 경로: `~/git/DIVER-2` 브랜치 `origin/docs/scaling-plan`의 `docs/SCALING/`.
- `ASSIGNMENT_subject_axis.md` (2026-10-13, 이아현 선생님이 안채원 선생님에게 부여한 과제):
  - 질문: *"iEEG pretraining에서 '피험자 수'를 scaling 축으로 쓸 때, 무엇을 적합할 수 있고 무엇은 적합하면 안 되며, 우리 registry 데이터로 어떤 대조 실험이 실제로 구성 가능한가?"*
  - 분석 대상 논문 5편: Oliveira et al. 2026 (arXiv:2609.35056), Narayanswamy et al. 2024 (Google LSM, arXiv:2410.13638), Banville et al. 2025 (Meta, arXiv:2501.15322), Ooi et al. 2025 (Nature 644), Truong et al. 2026 (arXiv:2610.09287).
  - Entropy proxy(원시 float의 zstd 압축률)를 측정하여 repetition tolerance 예측 제안 (Chai 2026: $r=-0.89$).
- `PLAN_SCALING_EXPERIMENT.md` (§9b Seed 변동 실측):
  - 이아현 선생님이 Aurora XPU에서 직접 실측한 seed 간 loss 범위 분석: step 2,000에서 7.6%, step 5,000에서 5.9% 등 수렴 구간에서도 seed 노이즈가 단조 감소하지 않음을 입증.
  - 기존 data-mixture 논문들의 단일 seed 한계를 비판하며 paired seed 설계 및 3개 앵커 지점 3-seed 측정 제안.
- `~/git/ephys-foundation-model-plan/submissions/2026/20261010-yahyunee-diver2-scaling-survey/`:
  - 94편 논문(489MB) 전수 분석.
  - EEG/iEEG 파운데이션 모델 중 parametric scaling law를 적합한 논문은 전무함을 규명.
  - DIVER-1 원고의 치명적 결함 2건(서술과 표 불일치, 본문과 부록 결론 상충, learnable norm gain으로 인한 $\mu P$ LR transfer 붕괴 위험)을 자체 식별하고 DIVER-2에서 시정 조치 확립.

### 1.5 GitHub Transconnectome 인프라 현황
- 실행 명령: `/home/juke/.local/bin/gh auth status`
  - 결과: `github.com` 로그인 계정 `snuconnectome` (`/home/juke/.config/gh/hosts.yml`).
  - 권한 토큰 스코프: `'admin:org', 'delete_repo', 'gist', 'repo', 'workflow'`.
- 실행 명령: `/home/juke/.local/bin/gh repo list Transconnectome --limit 30`
  - 결과: `@Transconnectome` 조직 내 428개 저장소 운영 중.
  - 주요 관련 저장소: `Transconnectome/DIVER-2`, `Transconnectome/KimJaeChul_AI_Class_Mentoring`, `Transconnectome/DIVER` 등.
  - 현재 로컬 작업 디렉토리 `/home/juke/git/chaewon_ahyeon_research_review`는 아직 git 저장소로 초기화되지 않은 상태 (`fatal: .git이 아닙니다`).

---

## 2. Logic Chain (논리 추론 체계)

1. **이아현 선생님의 핵심 과학적 질문과 가설 구조**:
   - [관찰 1.3, 1.4]: 텍스트 기반 LLM의 Chinchilla/Kaplan 스케일링 법칙은 1차원 연속 토큰을 가정하지만, 생체 신호(iEEG)는 `피험자 수(N)`와 `피험자당 기록 시간(T)`이라는 직교하는 2개의 축을 갖는다.
   - [관찰 1.3, 1.4]: 문헌(Oliveira et al., Ooi et al.)과 자체 데이터 분석을 통해, 피험자 간 생물학적 다양성(inter-individual variability)이 존재할 때 모델 표상 학습의 병목은 "단일 피험자의 긴 시간"이 아니라 "다양한 피험자의 포괄"이라는 가설이 도출된다.
   - [관찰 1.2, 1.3]: 안채원 선생님이 관찰한 "피험자 37명을 유지하면 1인당 시간을 1/64로 줄여도 다운스트림 성능이 유지되고, 반대로 피험자 수를 2명으로 줄이면 급락한다"는 실험 결과는 이 가설을 정면으로 지지한다.

2. **차지욱 교수님의 비평과 이아현 선생님의 옹호 논리 분석**:
   - [관찰 1.2]: 차지욱 교수님은 단순히 데이터를 섞거나 줄였을 때의 성능 유지/정체를 "공통 표상 사전지식이 없는 상태에서의 당연한 네거티브 결과이며, 아직 준비가 덜 되었다는 메시지일 뿐"이라고 비판하며 섣부른 투고를 경계함.
   - [관찰 1.2]: 이에 대해 이아현 선생님은 "단순 데이터 감축이 아니라, 피험자 수를 보존한 채 피험자당 노출을 줄인 조건"임을 정확히 짚으며, "무조건 스케일링이 잘 된다(Scaling works)가 아니라 어떻게 스케일링해야 하는가(How should we scale: 소수 장기 기록보다 다수 단기 기록 수집이 비용 효율적)"라는 정량적 가이드라인을 제공하는 긍정적 발견(Discovery)으로 프레이밍을 전환함.

3. **안채원 선생님과의 협업 시너지 및 분업 구조**:
   - [관찰 1.2, 1.3, 1.4]:
     - **이아현 선생님**: DIVER 아키텍처 원천 설계, Aurora 슈퍼컴퓨터 인프라 및 예산 운용, 스케일링 법칙 이론 체계(94편 문헌 메타분석), 멘토링 평가 및 엄밀한 감사 기준 제공.
     - **안채원 선생님**: KISTI/한강 클러스터 멀티노드 학습 실증, iEEG 데이터 반복(`iEEG_re`) vs EEG 혼합(`EEG_fill`/`EEG_add`) 조건별 대조 실험 수행, AAAI 2027 NeuroAI 워크숍 논문 초안 작성.
   - [관찰 1.3]: 이아현 선생님은 안채원 선생님의 결과를 맹신하지 않고, 심층 레이어(끝에서 두 번째 층) 재평가, random seed 영향 범위 전수 조사, MAE 외 대안 SSL(채널 식별 등) 대조군 추가 등 극한의 과학적 엄밀성을 요구하며 연구의 질적 수준을 끌어올림.

4. **Transconnectome 인프라 및 게시 요구사항 정합성**:
   - [관찰 1.5]: `gh` CLI와 `snuconnectome` 관리자 인증이 이미 확보되어 있으므로, R4 요건(`~/git/chaewon_ahyeon_research_review` git 초기화 및 `Transconnectome` 조직 원격 저장소 생성/푸시)을 즉시 무결하게 수행할 수 있는 완벽한 환경이 갖추어져 있음.

---

## 3. Caveats (한계 및 미검증 영역)

1. **다운스트림 태스크의 편향**:
   - 현재 보고된 안채원 선생님의 주요 실험 결과는 Neuroprobe, BYD, Pippi 등 인지/운동 중심의 3개 과제, 그것도 1번째 블록 출력의 frozen linear probe에 집중되어 있습니다.
   - MAYO 등 임상/간질 병리 데이터나 full fine-tuning 조건에서는 1/64 데이터 축소가 유지되지 않을 가능성이 여전히 존재합니다.
2. **Reconstruction Loss vs Downstream Metric 간 괴리**:
   - 1/64, 1/1024로 고유 기록을 줄였을 때 held-out reconstruction loss는 유의미하게 악화되었음에도 linear probe 점수가 유지되는 현상은, 현재의 MAE 재구성 손실이 표상 품질을 온전히 반영하지 못하거나, downstream probe가 저차원 특징에 오버피팅되었을 위험성을 내포합니다.
3. **Aurora 슈퍼컴퓨터 시간 만료 기한**:
   - 이아현 선생님이 확보한 Aurora 자원(25,000시간)은 2026년 12월에 만료되므로, DIVER-2 본실험 및 후속 확증 실험의 일정 마진이 매우 촉박합니다.

---

## 4. Conclusion (결론 및 핵심 요약)

1. **연구의 핵심 발견**:
   - 이아현 선생님과 안채원 선생님의 공동 연구는 **"iEEG 대규모 사전학습에서 피험자 다양성($N$)이 단일 피험자당 기록 길이($T$)보다 훨씬 지배적인 표상 품질 결정 요인"**이라는 파괴적인 통찰을 도출했습니다.
   - 이는 뇌파 파운데이션 모델 구축 시 값비싼 장기 입원 모니터링 데이터보다, 다수 환자의 짧은 클립을 수집하는 것이 훨씬 경제적이고 확장적임을 시사합니다.
2. **적대적 리뷰 관점에서의 필수 보완 과제**:
   - 차지욱 교수님의 지적대로, 단순한 현상 보고에 그칠 경우 "사전지식 없는 무작위 믹싱의 실패"로 평가절하될 수 있습니다.
   - 따라서 ① 심층 레이어 및 full fine-tuning에서의 검증, ② 채널 출처 예측(DIVER-1.5) 등 대안 SSL 목적함수와의 대조, ③ random seed 변동 구간을 명시한 paired t-test 결과를 반드시 보강해야 합니다.
3. **저장소 게시 준비 완료**:
   - `snuconnectome` 계정을 통해 GitHub `Transconnectome` 조직에 신규 저장소(`Transconnectome/chaewon_ahyeon_research_review`)를 생성하고 산출물을 동기화할 수 있는 권한이 확인되었습니다.

---

## 5. Verification Method (독립 검증 방법)

### 5.1 Teams 데이터 및 메시지 검증
```bash
# 이아현 선생님 1:1 대화 검증
sqlite3 ~/.agents/registry/chavis_teams/teams.db \
  "SELECT created_at, sender_name, substr(body_plain, 1, 150) FROM messages WHERE chat_id='19:3d8abd69-58f6-43cf-bb89-f60071eaf759_baa70085-4a80-454d-8c7f-081ffb7009c0@unq.gbl.spaces' AND body_plain LIKE '%발견이라고 생각%' ORDER BY created_at DESC;"

# 안채원 선생님 대화 확인
/home/juke/superclaude-env/bin/python3 ~/scripts/teams_chat.py read-chat --chat-id "19:303a8151-8db2-4ecd-b99a-872ceadc02d9_baa70085-4a80-454d-8c7f-081ffb7009c0@unq.gbl.spaces" --top 10
```

### 5.2 멘토링 및 DIVER-2 문서 검증
```bash
# 멘토링 11/9 미팅 기록 확인 (GitHub Transconnectome)
/home/juke/.local/bin/gh api repos/Transconnectome/KimJaeChul_AI_Class_Mentoring/contents/students/2026-2_ChaewonAhn/meetings/2026-11-09.md -q .content | base64 -d | head -n 45

# DIVER-2 scaling plan 검증
cd ~/git/DIVER-2
git show origin/docs/scaling-plan:docs/SCALING/ASSIGNMENT_subject_axis.md | head -n 35
```

### 5.3 GitHub Transconnectome 인증 및 저장소 상태 검증
```bash
/home/juke/.local/bin/gh auth status
/home/juke/.local/bin/gh repo list Transconnectome --limit 5
```
