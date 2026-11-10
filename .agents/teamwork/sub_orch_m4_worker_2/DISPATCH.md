## 2026-11-10T18:08:51Z

You are teamwork_worker 2 for Milestone 4 (Action Items & Prioritized Roadmap).
Your role: Milestone 4 Refinement Worker.
Your state folder: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m4_worker_2
Working directory: /home/juke/git/chaewon_ahyeon_research_review

MANDATORY FIRST STEP:
Read ORIGINAL_REQUEST.md at:
/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/ORIGINAL_REQUEST.md

Also read:
- /home/juke/git/chaewon_ahyeon_research_review/PROJECT.md
- /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m4/SCOPE.md
- /home/juke/git/chaewon_ahyeon_research_review/docs/04_action_items_roadmap.md
- Challenger 1 handoff: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m4_challenger_1/handoff.md
- Challenger 1 test script: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m4_challenger_1/verify_m4_empirical.py
- Challenger 2 handoff: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m4_challenger_2/handoff.md

WRITE OWNERSHIP:
You have exclusive write ownership of:
`/home/juke/git/chaewon_ahyeon_research_review/docs/04_action_items_roadmap.md`

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

MISSION:
Refine `docs/04_action_items_roadmap.md` by applying the 4 precise fixes required by Challenger 1, plus the baseline table enhancement noted by Challenger 2:

1. **Table 5.2 연산 예산 산술 합산치 정정**:
   - In Table 5.2 summary row (around line 820), change `30,240 GPUh` to `29,840 GPUh` to exactly match the sum of the 20 individual EXP-T1-01 ~ EXP-T3-05 entries.
2. **초록 line 201 비열등성 문구 정밀화**:
   - Change `across all individual subtasks under Benjamini–Hochberg False Discovery Rate (FDR) control` to:
     `across 11 out of 15 individual subtasks under Benjamini–Hochberg False Discovery Rate (FDR) control (encompassing all primary auditory, speech, and phonemic decoding benchmarks; with remaining higher-level syntax and temporal tasks rigorously remediated in DIVER-2)`
3. **`scripts/run_psd_baseline.py` 모의 테스트 단언문 버그 수정**:
   - In the mock test block of `run_psd_baseline.py` (around line 277), fix `div_tr = np.random.randn(200, 512)` to:
     `div_tr = np.random.randn(200, 512) + np.expand_dims(y_tr, 1) * 0.5`
     so that the mock test assertion passes without error when executed.
4. **간트 차트 및 DAG 텍스트 정렬**:
   - In Section 6.1 (around line 842) and Section 6.3 DAG (around line 914), replace `1.1B` with `204M (Large)` to be consistent with the 25,000 GPUh compute budget allocation and DIVER-2 model specifications.
5. **베이스라인 비교표 시간 패치 분해능 행 보완**:
   - In Section 3.2 4) comparative baseline table, ensure the row for "시간 패치 분해능 (Temporal Patch Resolution)" is included:
     BrainBERT: 1.0s (STFT), BIOT: 1.0s, LaBraM: 0.2s vs DIVER-2: 0.1s + FlashAttention-2.

STRICT HONORIFICS:
ALWAYS "안채원 선생님", "이아현 선생님" + 존댓말 — NEVER "OO 씨" or 반말.

VERIFICATION STEP:
After updating `docs/04_action_items_roadmap.md`, you MUST run:
1. `python3 .agents/teamwork/sub_orch_m4_challenger_1/verify_m4_empirical.py` (Must pass all 22 checks, 0 failures!)
2. `python3 -m pytest tests/verify_acceptance_criteria.py -k "test_f5_"` (Must pass 10/10 tests!)
3. `python3 -m pytest tests/verify_acceptance_criteria.py -k "test_tier3_05"` (Must pass!)

When complete, write your handoff.md in your state folder and message the orchestrator.
