## 2026-11-10T17:06:08Z

[Message] timestamp=2026-11-10T17:06:08Z sender=31b20b74-99ac-4310-aed7-4b7ab506960e priority=MESSAGE_PRIORITY_HIGH content=You are Explorer 3 (`explorer_m3_3`) for Milestone 3 (Scientific Adversarial Review).

## Working Directory
/home/juke/git/chaewon_ahyeon_research_review

## State Folder
/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m3_3

## Mandatory Documents to Read
1. Original Request (MANDATORY):
   `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/ORIGINAL_REQUEST.md`
2. Scope Document:
   `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m3/SCOPE.md`
3. Milestone 1 Deliverable:
   `/home/juke/git/chaewon_ahyeon_research_review/docs/01_research_synthesis.md`
4. Milestone 2 Deliverable:
   `/home/juke/git/chaewon_ahyeon_research_review/docs/02_deep_research_literature.md`

## Your Exploration Assignment
Investigate and formulate deep, rigorous, technically grounded scientific adversarial critique dossiers for **Axis 5 (통계적 엄밀성 & 다중비교 보정 결여)** and establish the **최신 문헌 기반 반론 닻 (Literature Anchors: Oliveira, Ooi, Narayanswamy, Banville, Truong)** regarding the research of 안채원 선생님 and 이아현 선생님 ("A Little iEEG Goes a Long Way", "Subjects over Hours").

### Axis 5: 통계적 엄밀성 및 다중 비교 보정 (Statistical Rigor & Multiple Comparisons)
1. **Seed n=6 조건의 통계적 검정력 한계**:
   - 겨우 6개의 랜덤 시드(seed n=6)로 도출된 평균과 표준오차를 바탕으로 비열등성($\Delta > -0.005$)을 결론짓는 것은 표본 오차에 극도로 취약함. 통계적 검정력(Power analysis, $1-\beta$) 결여.
2. **15개 하위 과제 다중 비교 보정의 완전 부재**:
   - Neuroprobe 15개 하위 과제(3개 과제 $\times$ 5개 피험자 또는 세부 분할)에서 Bonferroni 또는 Benjamini-Hochberg FDR(False Discovery Rate) 다중 비교 보정이 전혀 적용되지 않음.
   - 단일 유의수준 $\alpha=0.05$ 적용 시 적어도 하나의 위양성 발생 확률 $1 - (1-0.05)^{15} \approx 53.7\%$에 달하여 비열등성 판정의 통계적 신뢰도가 붕괴함.
3. **피험자 임계값($N_s \ge 8$)의 경험적 추정과 외삽 한계**:
   - 2명과 8명 사이의 N=3,4,5,6,7 데이터가 부재하여 비선형 급격 전이(Sharp transition)인지 완만한 곡선인지 검증되지 않음.
   - 37명 이상의 대규모 코호트로의 외삽(extrapolation) 불확실성.
4. **1/1 Base 모델의 계산량 교란 (Under-training Confounder)**:
   - 1/1 Base 모델이 0.46 epoch만 학습된 반면, 1/64 모델은 여러 epoch을 반복 학습하여, 실제로는 1/1 Base 모델의 과소 학습(under-training)이 데이터 감축의 성능 저하를 가렸을 가능성.

### 최신 문헌 기반 반론 닻 (Literature-anchored Counterarguments)
1. **Oliveira et al. (2026, arXiv:2609.35056)**:
   - 두피 EEG 2축 거듭제곱 스케일링에서 보고된 $\beta$ 요동 및 파라미터 비식별성(ill-conditioning)을 들어, 안채원 선생님과 이아현 선생님의 2축 스케일링 모델이 과도하게 단순화되었음을 비판.
2. **Narayanswamy et al. (2024, Google LSM, arXiv:2410.13638)**:
   - 시간 축 스케일링($S \times H = \text{const}$)의 유효성을 강조하는 구글 LSM 결과와 비교하여, 왜 유독 iEEG에서만 시간 축이 무용하다는 결론이 도출되었는지에 대한 기술적 반론.
3. **Banville et al. (2025, Meta FAIR, arXiv:2501.15322)**:
   - 피험자별 고유층(subject-specific layers) 및 Seen vs Unseen 피험자 분리 평가 시 발생하는 다양성 은폐 현상($p=0.49$)을 인용하여, 피험자 8명 포화 주장의 허점을 짚음.
4. **Ooi et al. (2025, Nature 644:731)**:
   - fMRI 표현형 스케일링의 점근적 병목 전이 공식과 iEEG 500Hz 초고주파 LFP 신호의 복잡도 차이를 들어 피험자 수 포화 한계 지적.
5. **Truong et al. (2026, arXiv:2610.09287)**:
   - 두피 EEG 50명 온셋 바닥 대비 iEEG 8명 온셋 주장의 생물물리학적 타당성 검토.

## Lab Policy & Governance
- STRICT HONORIFICS: ALWAYS "안채원 선생님", "이아현 선생님" + 존댓말. NEVER "OO 씨" or 반말. "차지욱 교수님".
- Objective, institutional, rigorous scientific voice (no colloquialisms).

## Deliverable
Write your comprehensive analysis and structured attack dossier to:
`/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m3_3/handoff.md`
Include: Observation, Logic Chain, Statistical Power & Multiple Comparison calculations, Literature Anchor cross-examinations.
When finished, send a message to your parent orchestrator with your report summary.
