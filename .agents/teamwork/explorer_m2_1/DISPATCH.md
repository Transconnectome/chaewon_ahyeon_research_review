## 2026-11-10T16:34:18Z

You are an Explorer for Milestone 2 (Deep Research & Scholarly Literature Benchmarking).
State folder: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m2_1
Working directory: /home/juke/git/chaewon_ahyeon_research_review

MANDATORY INSTRUCTIONS:
1. First, read ORIGINAL_REQUEST.md at /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/ORIGINAL_REQUEST.md.
2. Read SCOPE.md at /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m2/SCOPE.md.
3. Read PROJECT.md at /home/juke/git/chaewon_ahyeon_research_review/PROJECT.md.
4. Read docs/01_research_synthesis.md at /home/juke/git/chaewon_ahyeon_research_review/docs/01_research_synthesis.md.
5. Read Survey 2 handoff at /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_survey_2/handoff.md.

YOUR MISSION:
Deeply explore, compare, and mathematically formulate the 2-axis neural scaling laws in the literature vs the empirical findings of 안채원 선생님 and 이아현 선생님 ("A Little iEEG Goes a Long Way", "Subjects over Hours"):
1. Mathematical equations and parameter behavior:
   - Oliveira et al. (2026, arXiv:2609.35056): Scalp EEG 2-axis scaling $L = A N_t^{-\alpha} + B N_s^{-\beta} + L_\infty$, explaining the high instability of $\beta$ (0.07 ~ 1.99) across tasks and why subject scaling behaves differently from token scaling.
   - Narayanswamy et al. (2024, Google LSM, arXiv:2410.13638): "Equal total hours yields equal loss" single-axis scaling hypothesis, and why iEEG breaks this equivalence.
   - Banville et al. (2025, Meta, arXiv:2501.15322): Subject-specific input layers, why subject diversity was unmodeled as an explicit scaling axis.
   - Ooi et al. (2025, Nature 644:731): fMRI phenotype scaling $r = K_0 \sqrt{1/(1 + K_1/N + K_2/(NT))}$, bottleneck transition from $NT$ (hours x subjects) to $N$ (subjects). Contrast fMRI vs iEEG spatial/temporal regimes.
   - Truong et al. (2026, arXiv:2610.09287): Scalp EEG 10 -> 1,863 subjects, onset threshold at ~50 subjects.
2. Contrast with 안채원 선생님 & 이아현 선생님의 발견:
   - Why 8 subjects ($N \ge 8$) is the critical diversity threshold in iEEG (preserving performance with $\Delta = +0.0001$), while dropping to 2 subjects collapses performance ($\Delta = -0.0055$).
   - Why 81.3 hours (1/64) saturates downstream probe performance while whole-data is 5,203 hours.
   - 2-axis power law formulation for iEEG: express how loss and downstream probe accuracy scale as a function of $N_s$ (subjects) and $N_h$ (hours).

Strictly follow honorific rules: ALWAYS "안채원 선생님", "이아현 선생님" (NEVER "OO 씨" or 반말).
Save your full findings in /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m2_1/handoff.md and report completion via send_message.
