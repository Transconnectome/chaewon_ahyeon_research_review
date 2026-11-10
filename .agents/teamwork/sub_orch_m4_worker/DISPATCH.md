## 2026-11-10T17:47:45Z
You are teamwork_worker for Milestone 4 (Action Items & Prioritized Roadmap).
Your role: Milestone 4 Roadmap Synthesis Worker.
Your state folder: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m4_worker
Working directory: /home/juke/git/chaewon_ahyeon_research_review

MANDATORY FIRST STEP:
Read ORIGINAL_REQUEST.md at:
/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/ORIGINAL_REQUEST.md

Also read:
- /home/juke/git/chaewon_ahyeon_research_review/PROJECT.md
- /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m4/SCOPE.md
- /home/juke/git/chaewon_ahyeon_research_review/docs/01_research_synthesis.md
- /home/juke/git/chaewon_ahyeon_research_review/docs/02_deep_research_literature.md
- /home/juke/git/chaewon_ahyeon_research_review/docs/03_adversarial_review.md
- /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m4_explorer_1/report.md
- /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m4_explorer_2/report.md
- /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m4_explorer_3/report.md

WRITE OWNERSHIP:
You have exclusive write ownership of:
`/home/juke/git/chaewon_ahyeon_research_review/docs/04_action_items_roadmap.md`
Do NOT edit other docs or code files.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

MISSION:
Author the definitive deliverable `docs/04_action_items_roadmap.md` by synthesizing the findings and detailed specifications from Explorer 1 (Tier 1), Explorer 2 (Tier 2), and Explorer 3 (Tier 3 & Compute/Timeline/Risk).

The document MUST directly remediate all 11 vulnerabilities (VULN-01 to VULN-11) identified in Milestone 3 (`docs/03_adversarial_review.md`) and must be strictly structured into 3 distinct tiers:
1. **Tier 1: 최우선 긴급 과제 (NeuroAI Workshop AAAI 2027 마감: 2026-11-20)**
   - ACT-T1-01 ~ ACT-T1-05: Claims scoping ("시간 불필요" 과대주장 수정, 1/64 다운샘플링 및 8명 소표본 한계 명시, 층별 보존 경계), Bonferroni/FDR 다중비교 보정 및 n=6->10 시드 신뢰구간/효과크기, PSD 스펙트럼 베이스라인 대조 제어 실험, 워크숍 논문 수정 초안(Abstract, Method, Discussion, Limitations), KISTI GH200 매핑.
2. **Tier 2: 중기 핵심 과제 (DIVER-2 Aurora 슈퍼컴퓨팅 25,000 GPU 시간 & Nature Portfolio 저널 투고: 2026-12 ~ 2027 Q1)**
   - ACT-T2-01 ~ ACT-T2-11: 4대 뇌엽 공간 커버리지 지수($C_{\text{lobe}}$) 및 동일 뇌엽 통제, 연속 3D MNI 가상 전극 RBF 보간, ComBat/neuroCombat 다기관 배치 보정, 탈지름길 ACPE (iCAR + 1차 차분 백색화), InfoNCE / JEPA SSL 비교 벤치마크, 48개 조밀 격자 2축 스케일링 법칙 레벤버그-마쿼트 피팅 ($\kappa(\mathcal{H}) < 500$), ALCF Aurora 25,000 GPUh 분산 파이프라인, MAYO Clinic 8명 뇌전증 발작파 벤치마크, LoRA ($r=8$) vs LP-FT vs Full FT 과적합 방지, 다층 프로빙(Linear/MLP/Attentive) 및 CKA 매니폴드 추적, Yeo 7-Network 피질 계층(1차 감각 vs 연합 피질) 표상 전이도 분석.
   - DIVER-2 상세 기술 명세서(Small 51M, Base 103M, Large 204M, XL 412M, 르장드르 연속 거리 바이어스, 손실 함수 수식, BrainBERT/BIOT/LaBraM 대조 매트릭스).
3. **Tier 3: 장기 전략 및 임상 응용 과제 (실시간 BCI, 오픈 파운데이션 모델 생태계)**
   - ACT-T3-01 ~ ACT-T3-06: 다기관 iEEG 이질성 극복 및 BIDS-iEEG 표준화, MNI152 3D 정합 및 양극성/국소 CAR 재참조, 폐루프 $\le 15\text{ms}$ 초저지연 온디바이스 BCI (FLOPs, Jetson Orin Nano / Apple NPU), INT8 SmoothQuant 양자화 + 지식 증류(KD) + 어텐션 헤드 가지치기, Mamba-2 선택적 SSM 스트리밍 전환, iEEG 생체인식 민감도 방어 및 PyDeface 3D 안면 절제, HIPAA Safe Harbor 시간 지터링 비식별화, CC BY vs CC BY-NC-SA 라이선스 충돌 방지 및 OpenRAIL-M 3계층 차등 공개 체계, Model Card 명세.
4. **5대 클러스터 통합 연산 예산 아키텍처**
   - ALCF Aurora (25,000 GPUh), Connectome (8x A5000), DGX-1 (8x V100), SNUBIC (40x L40S), Local DGX-Spark (GB10) 전수 작업별 매핑 및 GPU-Hours 정량 할당표.
   - 클러스터별 운영 규칙(Connectome labfind, SNUBIC 예약 필수, GB10 OOM 방지).
5. **마스터 로드맵 종합**
   - 2026-11 ~ 2027 Q3+ 전체 간트 차트 타임라인.
   - RACI 책임 배분 행렬 (안채원 선생님, 이아현 선생님, 차지욱 교수님, 엔지니어).
   - 의존성 그래프(DAG) 및 임계 경로(Critical Path) 분석.
   - 6대 핵심 리스크 비상대응 행렬 (RSK-01 ~ RSK-06).

METADATA & ACCEPTANCE CRITERIA ENFORCEMENT:
Every action item card MUST include:
- 담당 (Owner: ALWAYS "안채원 선생님" or "이아현 선생님")
- 일정 (Timeline: calendar deadlines including 2026-11-20 and intermediate milestones)
- 산출물 (Deliverables: code, scripts, configs, reports)
- 판정 기준 (Acceptance Criteria: quantitative thresholds like Delta > -0.005, p < 0.05, n >= 6, etc.)
- 기술 포인터 (Technical pointers: .py, SLURM, sbatch, dataloader, probe, seed, KISTI, Aurora, LMDB)
- 컴퓨팅 예산 (Compute budget mapped to infrastructure: KISTI, Aurora, GH200, GPU hours)

STRICT HONORIFICS:
ALWAYS "안채원 선생님", "이아현 선생님" + 존댓말 — NEVER "OO 씨" or 반말.

VERIFICATION STEP:
After authoring `docs/04_action_items_roadmap.md`, you MUST run:
`python3 -m pytest tests/verify_acceptance_criteria.py`
Verify that all tests, especially all F5 tests (`test_f5_*`), pass with exit code 0.
Include the verification command output in your handoff.md.

When finished, write your handoff.md in your state folder and message the orchestrator.
