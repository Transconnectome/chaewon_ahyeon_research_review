# BRIEFING — 2026-11-10T16:37:30Z

## Mission
Deeply explore, compare, and mathematically formulate 2-axis neural scaling laws in the literature vs empirical findings of 안채원 선생님 and 이아현 선생님 ("A Little iEEG Goes a Long Way", "Subjects over Hours").

## 🔒 My Identity
- Archetype: explorer
- Roles: Read-only investigation: analyze problems, synthesize findings, produce structured reports
- Working directory: /home/juke/git/chaewon_ahyeon_research_review
- State folder: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m2_1
- Original parent: a8c191d0-18a2-4bb2-8c56-b2765dcf4415
- Milestone: Milestone 2 (Deep Research & Scholarly Literature Benchmarking)

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Strictly follow honorific rules: ALWAYS "안채원 선생님", "이아현 선생님" (NEVER "OO 씨" or 반말)
- Evidence over agreement — verify actual mathematical equations, parameter behaviors, experimental setups, and empirical constants
- Write output to handoff.md in state folder

## Current Parent
- Conversation ID: a8c191d0-18a2-4bb2-8c56-b2765dcf4415
- Updated: not yet

## Investigation State
- **Explored paths**:
  - `ORIGINAL_REQUEST.md`, `SCOPE.md`, `PROJECT.md`, `docs/01_research_synthesis.md`, Survey 2 handoff
  - `SUBJECT_AXIS_REPORT.md` and `check_subject_axis.py` in `/home/juke/git/chaewon-intern-2026fall/scaling_literature/`
  - `summary.md` and `originals_diver2_scaling_survey.md` in `/home/juke/git/ephys-foundation-model-plan/submissions/2026/20261010-yahyunee-diver2-scaling-survey/`
  - `paper_skeleton.md` in `/home/juke/git/chaewon-intern-2026fall/hangang/reports/`
- **Key findings**:
  - Mathematical formulation of Oliveira et al. (2026): $L = A(N_t/\bar{N}_t)^{-\alpha} + B(N_s/\bar{N}_s)^{-\beta} + L_\infty$, explaining 28-fold variance in $\beta \in [0.07, 1.99]$.
  - Narayanswamy et al. (2024): LSM single-axis scaling $S \times H = \text{const}$ broken in iEEG due to patient-specific invasive electrode montages and idiosyncratic noise memorization.
  - Banville et al. (2025): Subject-specific input projection layers and seen-subject evaluation hid the subject scaling axis ($p=0.49$).
  - Ooi et al. (2025): fMRI $r = K_0 \sqrt{1/(1 + K_1/N + K_2/(NT))}$, bottleneck transition from $NT$ to $N$. Contrast between low temporal resolution BOLD (averaging helps) vs high SNR/high-gamma iEEG (hours saturate quickly, subjects are anatomical bottleneck).
  - Truong et al. (2026): Scalp EEG onset threshold at $\sim 50$ subjects; in iEEG, critical threshold shifts down to $N \approx 8$ due to high SNR and direct cortical placement.
  - Empirical constants of 안채원 선생님 & 이아현 선생님: $N=8$ preserves $\Delta = +0.0001$, $N=2$ collapses $\Delta = -0.0055$; 81.3h (1/64) preserves deep layer 12 representations ($\Delta = -0.0000$), while 5.1h (1/1024) collapses layer 12 ($\Delta = -0.0050$).
- **Unexplored areas**: None for this milestone phase.

## Key Decisions Made
- Formulate the iEEG 2-axis scaling law using both a modified rational model (extending Ooi et al.) and an asymptotic broken power-law for downstream probing accuracy.

## Artifact Index
- /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m2_1/DISPATCH.md
- /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m2_1/BRIEFING.md
- /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m2_1/progress.md
- /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m2_1/handoff.md (in progress)
