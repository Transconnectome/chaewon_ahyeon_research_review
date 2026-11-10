# Adversarial Challenge & Stress-Test Report: Milestone 4 Deliverable

- **문서 식별자**: `.agents/teamwork/sub_orch_m4_challenger_1/challenge.md`
- **검증 대상 산출물**: `/home/juke/git/chaewon_ahyeon_research_review/docs/04_action_items_roadmap.md`
- **검증 주체**: `sub_orch_m4_challenger_1` (Milestone 4 Adversarial Empirical Challenger)
- **수신 주체**: `sub_orch_m4` (Milestone 4 Sub-Orchestrator, Conversation ID: `d3aa6605-d0ef-4e42-badb-a3155a1ef4fe`)
- **실시 일시**: 2026-11-10T18:05:00Z
- **최종 판정 (Verdict)**: **REQUEST_CHANGES** (경미하지만 즉각 수정 가능한 3대 실증적 결함 보정 요청)

---

## 1. Challenge Summary (총괄 평가)

**종합 위험도 평가 (Overall Risk Assessment)**: **MEDIUM**

`docs/04_action_items_roadmap.md`는 83.5 KB, 957줄에 달하는 대규모 마스터 로드맵 문서로서, Milestone 3에서 제기된 11대 과학적 취약성(VULN-01 ~ VULN-11)을 3대 우선순위 티어(Tier 1 NeuroAI 워크숍 11/20, Tier 2 DIVER-2 저널, Tier 3 온디바이스 BCI)로 완벽히 분해하고, 5대 클러스터 자원 배분, RACI 행렬, DAG 임계 경로, 6대 리스크 완화책을 매우 탁월한 수준으로 체계화하였습니다.

`pytest tests/verify_acceptance_criteria.py` 상의 F5 10개 인수 조건 테스트 및 `test_tier3_05`를 100% 통과하였고, 전 문서에 걸친 연구실 엄격 존칭("안채원 선생님", "이아현 선생님") 준수율은 **100% 무결점(위반 0건)**이 확인되었습니다.

그러나 본 챌린저가 자체 구축한 **독립 실증 검증 하네스 (`verify_m4_empirical.py`)**를 통한 수치 계산, 코드 실행, 통계 매트릭스 스트레스 테스트 결과, **동료 심사관(Hostile Peer Reviewer)의 공격에 즉각 노출될 수 있는 3건의 실증적 오류 및 2건의 정합성 불일치**가 발견되었습니다. 이에 따라 산출물의 완전성을 기하기 위해 명확한 수정안을 첨부하여 **REQUEST_CHANGES**를 판정합니다.

---

## 2. Identified Challenges (구체적 결함 및 스트레스 테스트 분석)

### [High] Challenge 1: Table 5.2 클러스터 통합 연산 예산 산술 합계 불일치 (400 GPUh 괴리)

- **검증된 가정 (Assumption challenged)**: Table 5.2 (lines 798-820)의 개별 20개 실험 항목(`EXP-T1-01` ~ `EXP-T3-05`)의 GPU-Hours 합계가 최하단 합계 행에 명시된 `30,240 GPUh`와 일치한다는 주장.
- **실증 공격 시나리오 (Attack scenario)**:
  - 검증 스크립트 `verify_m4_empirical.py`를 통해 Table 5.2의 20개 행을 전수 파싱하여 합산한 결과:
    $$\begin{aligned}
    \sum \text{GPUh} &= 4 + 2 + 250 + 400 + 150 + 800 + 3500 + 8500 + 6000 + 5000 + 2000 \\
    &\quad + 500 + 600 + 450 + 350 + 350 + 200 + 384 + 300 + 100 = \mathbf{29,840 \text{ GPUh}}
    \end{aligned}$$
  - 실제 합계는 **29,840 GPUh**이나, line 820의 합계 행에는 **30,240 GPUh**로 표기되어 있어 **정확히 400 GPUh의 산술적 괴리(Discrepancy)**가 발생함.
- **영향 범위 (Blast radius)**: 연구비 감사관이나 학술지 에디터가 연산 예산의 정합성을 검증할 때 단순 산술 오류로 인해 연구진의 정량적 정밀도 전반에 대한 신뢰를 훼손할 수 있음.
- **구체적 수정 권고 (Mitigation)**:
  - Table 5.2 line 820의 합계 수치를 `30,240 GPUh`에서 `29,840 GPUh`로 수정 (또는 누락된 400 GPUh가 특정 실험, 예: EXP-T2-02의 800h 조정에 해당하는지 확인 후 정합성 일치).

---

### [High] Challenge 2: 초록(Abstract) 내 전 과제 비열등성 과대주장 (15개 중 4개 과제 미달)

- **검증된 가정 (Assumption challenged)**: 개정 초록 초안(line 201)에서 1/64 조건이 *"maintaining rigorous statistical non-inferiority ($\Delta > -0.005$) across all individual subtasks under Benjamini–Hochberg False Discovery Rate (FDR) control ($q < 0.05$, $n=10$ random seeds)"*을 달성한다는 주장.
- **실증 공격 시나리오 (Attack scenario)**:
  - 본문 line 301-317에 명시된 15개 과제의 실제 실측 델타 매트릭스 `RAW_DELTAS` (6개 시드)에 대해 Benjamini-Hochberg FDR 보정($q < 0.05$) 및 비열등성 단측 t-검정($H_0: \mu \le -0.005$)을 독립 실행한 결과:
    - **통과 (11개 과제)**: Task 01~08, Task 11~12, Task 15 (모두 $q < 10^{-4}$ 수준으로 비열등성 확정).
    - **기각 실패 (4개 과제)**:
      - `Task 09 (Syntax / Phrase Parsing)`: 평균 $\Delta = -0.0070$ ($p = 1.000$, $q = 1.000$) $\to$ 마진 $-0.005$보다 $0.0020$ 낮음.
      - `Task 10 (Lexical Semantics)`: 평균 $\Delta = -0.0050$ ($p = 0.500$, $q = 0.577$) $\to$ 정확히 경계선상 위치.
      - `Task 13 (Spatial Navigation)`: 평균 $\Delta = -0.0050$ ($p = 0.500$, $q = 0.577$) $\to$ 경계선상 위치.
      - `Task 14 (Temporal Transition)`: 평균 $\Delta = -0.0060$ ($p = 0.999$, $q = 1.000$) $\to$ 마진 $-0.005$보다 $0.0010$ 낮음.
  - 이 결과는 문서 본문 line 118(*"과반수 이상의 핵심 과제(특히 언어/음성 디코딩)가 비열등 마진을 유지"*) 및 line 126(*"특정 고차 과제(Sentence Onset, Syntax Parsing 등)의 거동을 투명하게 공개하여 평균화의 오류 방어"*)과도 모순됨.
- **영향 범위 (Blast radius)**: 적대적 심사관이 Forest Plot을 검토하는 즉시 "초록에는 전 과제(all individual subtasks)가 비열등성을 유지한다고 썼으나, 구문 파싱(-0.0070) 등 고차 과제는 명백히 붕괴했다"는 지적과 함께 **초록 과대주장(Overclaim)**으로 논문 리젝을 유발할 수 있음.
- **구체적 수정 권고 (Mitigation)**:
  - 초록 line 201의 표현을 다음과 같이 수정:
    - **수정 전**: `maintaining rigorous statistical non-inferiority (\Delta > -0.005) across all individual subtasks under Benjamini–Hochberg False Discovery Rate (FDR) control`
    - **수정 후**: `maintaining rigorous statistical non-inferiority (\Delta > -0.005) across 11 out of 15 individual subtasks (encompassing all primary auditory, speech, and phonemic decoding benchmarks) under Benjamini–Hochberg False Discovery Rate (FDR) control (q < 0.05), while high-level syntactic and temporal transition tasks reveal bounded representation degradation`

---

### [Medium] Challenge 3: 임베디드 스크립트 `run_psd_baseline.py` 내 모의 테스트 데이터 무결성 결함

- **검증된 가정 (Assumption challenged)**: Section 2.3의 저주파 PSD 베이스라인 대조 스크립트 (`scripts/run_psd_baseline.py`, lines 225-280)가 독자적으로 바로 실행 가능한 무결한 검증 프로토콜이라는 주장.
- **실증 공격 시나리오 (Attack scenario)**:
  - 스크립트의 `if __name__ == "__main__":` 블록(lines 271-280)을 파이썬 인터프리터로 실제 실행한 결과:
    ```bash
    PSD Baseline AUROC:  0.5229
    DIVER Probing AUROC: 0.3650
    Advantage (Delta):   -0.1579
    AssertionError: DIVER fails to significantly outperform PSD baseline: Delta = -0.1579
    ```
  - 원인: 모의 데이터 생성 시 학습용 `div_tr`에는 레이블 `y_tr`에 대한 신호가 전혀 주입되지 않은 순수 가우시안 잡음(`np.random.randn(200, 512)`)인 반면, 테스트용 `div_te`에만 레이블 신호(`+ y_te * 0.5`)가 주입되어 선형 분류기가 무작위 가중치를 학습함. 이에 따라 DIVER AUROC가 0.36으로 급락하여 line 268의 `assert delta > 0.020` 단언문에서 크래시 발생.
- **영향 범위 (Blast radius)**: 자동화 CI/CD 또는 외부 재현 시 스크립트가 1회 실행만으로 실패하여 코드의 신뢰도 저하.
- **구체적 수정 권고 (Mitigation)**:
  - line 277의 모의 학습 데이터 생성 코드에 레이블 신호를 주입:
    - **수정 전**: `div_tr = np.random.randn(200, 512)`
    - **수정 후**: `div_tr = np.random.randn(200, 512) + np.expand_dims(y_tr, 1) * 0.5`

---

### [Medium] Challenge 4: DAG 및 간트 차트 내 1.1B 초대형 모델 표기 불일치

- **검증된 가정 (Assumption challenged)**: DAG 임계 경로 및 간트 차트가 Section 3.2 모델 스펙 및 Table 5.2 연산 예산과 100% 정렬되어 있다는 주장.
- **실증 공격 시나리오 (Attack scenario)**:
  - Section 3.2 line 628-633 모델 규격: Small(51.4M), Base(103.2M), Large(204.8M), XL(412.5M 파일럿).
  - Table 5.2 연산 예산: Base(103M) 및 Large(204M)만 Aurora 25,000 GPUh 내에 배분 (EXP-T2-07 6,000 GPUh, EXP-T2-08 5,000 GPUh).
  - 그러나 Section 6.1 간트 차트(line 842): `- 204M / 1.1B 대규모 사전학습`
  - Section 6.3 DAG 다이어그램(line 914): `[T3-2: 1.1B 사전학습 및 2축 거듭제곱 피팅] (20일)`
  - 1.1B 모델을 학습하려면 최소 89,600 GPU-Hours가 소요되므로, 25,000 GPUh 예산 통제 하에서는 학습이 원천 불가능함. 이는 Explorer 3의 초안 잔재가 최종 마스터 문서에 남아 발생한 표기 불일치임.
- **영향 범위 (Blast radius)**: 모델 규격표(최대 Large 204M / XL 412M)와 DAG 다이어그램 간 내부 정합성 위배.
- **구체적 수정 권고 (Mitigation)**:
  - line 842: `- 204M / 1.1B` $\to$ `- 103M / 204M (Large)`로 수정.
  - line 914: `[T3-2: 1.1B 사전학습 및 2축 거듭제곱 피팅]` $\to$ `[T3-2: 204M 대규모 사전학습 및 2축 거듭제곱 피팅]`으로 수정.

---

### [Low] Challenge 5: KISTI 슈퍼컴퓨터 단일 작업 200시간 Wall-Clock 큐 한계 위험

- **검증된 가정 (Assumption challenged)**: KISTI 한강 클러스터에서 `EXP-T2-02`(200시간) 및 `EXP-T2-04`(200시간)가 단일 작업으로 중단 없이 실행될 수 있다는 가정.
- **실증 공격 시나리오 (Attack scenario)**:
  - KISTI 등 국가 슈퍼컴퓨팅 센터의 Slurm 작업 스케줄러는 통상 단일 작업당 최대 24시간 또는 48시간의 Wall-time limit(`--time`)을 강제함.
  - 200시간(약 8.3일)의 장기 연산은 단일 Slurm 배치 제출로는 타임아웃 킬(TIMEOUT SIGKILL)에 직면하게 됨.
- **영향 범위 (Blast radius)**: 24시간 도달 시 작업 강제 종료 및 중간 상태 유실 위험.
- **구체적 수정 권고 (Mitigation)**:
  - 해당 작업 설명 및 Slurm 가이드에 "체크포인트 자동 재시작 및 의존성 체이닝 (`sbatch --dependency=afterok:$SLURM_JOB_ID`)" 기술 규격을 명시하여 운영 실현 가능성 보강.

---

## 3. Stress Test Results Summary (스트레스 테스트 결과 요약)

| 스트레스 테스트 시나리오 | 대상 및 도구 | 기대 거동 | 실제 관측 거동 | 판정 |
|---|---|---|---|---|
| **F5 단위 테스트 전수 검증** | `tests/verify_acceptance_criteria.py` | 10개 테스트 전수 통과 | 10/10 PASS (0.02s) | **PASS** |
| **VULN 1:1 매핑 정합성** | `test_tier3_05` | 11대 취약성 전수 매핑 | 1/1 PASS | **PASS** |
| **연구실 엄격 존칭 전수 감사** | `verify_m4_empirical.py` (전 마크다운) | "안채원 선생님", "이아현 선생님" 100% 준수 | 위반 0건 (100% 준수) | **PASS** |
| **마크다운 테이블 파이프 무결성** | `verify_m4_empirical.py` | 테이블 행 열 수 일치 | 오류 행 0건 | **PASS** |
| **통합 연산 예산 산술 검증** | Table 5.2 개별 합 vs 합계 행 | 일치 ($\Delta = 0$) | 29,840 GPUh vs 30,240 GPUh ($\Delta = -400$) | **FAIL** |
| **FDR 비열등성 매트릭스 재현** | 15개 과제 `RAW_DELTAS` 수학 검증 | 15개 과제 비열등성 판정 | 11개 통과, 4개 기각 실패 (Task 9, 10, 13, 14) | **FAIL (초록과 모순)** |
| **PSD 베이스라인 모의 실행** | `scripts/run_psd_baseline.py` | `AssertionError` 없이 완료 | 레이블 신호 결손으로 `AssertionError` 발생 | **FAIL** |
| **클러스터 거버넌스 정책 준수** | SNUBIC, Connectome, DGX-Spark | 예약 규정, NFS 금지규정, OOM 가드 수록 | 전 규정 정확히 명시 | **PASS** |
| **마스터 일정 및 데드라인 정합성** | 11/11 ~ 11/20 Day-by-Day | 중간 점검 11/15, 11/17 수록 | 정확히 수록 및 실행 가능 | **PASS** |

---

## 4. Unchallenged Areas (견고성이 입증된 영역)

1. **VULN-01 (1/64 안전 하한선 및 1/1024 음성 경계 재정립)**:
   - 12개 층 표상 보존 곡선과 국소 필터 vs 문맥 추상화 이론(Raghu et al., Kornblith et al.)의 도입은 논문의 방어력을 획기적으로 강화함.
2. **Pearl 인과 매개 분석 기반 4대 뇌엽 커버리지 ($C_{\text{lobe}}$) 분리**:
   - 공간 결손 교란과 피험자 다양성의 인과적 분해(NDE vs NIE)는 최고 수준의 방법론적 엄밀성을 가짐.
3. **Tier 3 온디바이스 BCI 아키텍처**:
   - SmoothQuant INT8 W8A8 양자화, Apple Silicon M4 / Jetson Orin Nano 지연 프로파일($\le 15\text{ms}$), Mamba-2 SSM 스트리밍 전환은 신경공학적 응용 관점에서 결함 없이 완벽히 설계됨.
4. **리스크 비상대응 행렬 (RSK-01 ~ RSK-06)**:
   - 각 리스크의 트리거 조건과 폴백 플랜이 명확하고 현실적임.

---

## 5. Conclusion & Actionable Next Steps (최종 결론 및 조치 계획)

본 산출물 `docs/04_action_items_roadmap.md`는 프로젝트 마스터 로드맵으로서 탁월한 완성도를 갖추고 있으나, 위 4대 결함(산술 합계 400h 괴리, 초록 4개 과제 미달 과대주장, 모의 테스트 단언문 크래시, DAG 1.1B 잔재)을 그대로 유지할 경우 학술 검증 및 배포 단계에서 취약점이 될 수 있습니다.

따라서 본 챌린저는 **REQUEST_CHANGES**를 공식 판정하며, 워커 또는 오케스트레이터가 위 지적 사항에 대한 정밀 교정(약 5분 소요)을 완료한 후 최종 승인(Approval)으로 전환할 것을 권고합니다.
