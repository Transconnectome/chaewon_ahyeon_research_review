## 2026-11-10T16:34:30Z
You are an Explorer for Milestone 2 (Deep Research & Scholarly Literature Benchmarking).
State folder: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m2_2
Working directory: /home/juke/git/chaewon_ahyeon_research_review

MANDATORY INSTRUCTIONS:
1. First, read ORIGINAL_REQUEST.md at /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/ORIGINAL_REQUEST.md.
2. Read SCOPE.md at /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m2/SCOPE.md.
3. Read PROJECT.md at /home/juke/git/chaewon_ahyeon_research_review/PROJECT.md.
4. Read docs/01_research_synthesis.md at /home/juke/git/chaewon_ahyeon_research_review/docs/01_research_synthesis.md.
5. Read 94-paper foundation model survey at /home/juke/git/ephys-foundation-model-plan/submissions/2026/20261010-yahyunee-diver2-scaling-survey/originals_diver2_scaling_survey.md and summary.md.
6. Read Survey 3 handoff at /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_survey_3/handoff.md.

YOUR MISSION:
Deeply explore, categorize, and benchmark the 94-paper electrophysiology foundation model literature corpus against the empirical discoveries of 안채원 선생님 and 이아현 선생님:
1. Foundation Model Taxonomy & Landscape:
   - Comprehensive taxonomy: Masked Autoencoders (MAE), Contrastive Learning (CL), Autoregressive Models (AR), and Multimodal Foundation Models.
   - Direct competitor analysis: BrainWave, BrainOmni, DIVER-0, DIVER-1 (arXiv:2512.19097), DIVER-1.5 (ACPE + channel origin prediction), Neuro-BERT, BIOT, LaBraM, Brant, CBraM.
   - Architectural comparisons: Patching schemes, spatial encoding, channel permutation invariance, temporal receptive fields.
2. Cross-Modality Transfer & Negative Transfer Mechanics:
   - Why replacing scarce iEEG with scalp EEG (EEG_fill) causes statistically significant negative transfer (-0.0100 [+0.0074, +0.0125] penalty) compared to iEEG repetition (iEEG_re).
   - Mechanistic physical/biological causes: scalp low-pass volume conduction filtering vs localized field potentials, channel montage variability, signal-to-noise ratio discrepancy (10-100x), distinct frequency power distributions (high-gamma vs alpha/beta).
   - Multi-modal co-training confounders: why naive joint pretraining fails without specialized adapters or loss balancing.

Strictly follow honorific rules: ALWAYS "안채원 선생님", "이아현 선생님" (NEVER "OO 씨" or 반말).
Save your full findings in /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m2_2/handoff.md and report completion via send_message.
