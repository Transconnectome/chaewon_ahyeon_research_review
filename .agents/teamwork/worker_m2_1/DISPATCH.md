## 2026-11-10T16:41:19Z
You are the Worker for Milestone 2 (Deep Research & Scholarly Literature Benchmarking).
State folder: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/worker_m2_1
Working directory: /home/juke/git/chaewon_ahyeon_research_review
Exclusive file write ownership: /home/juke/git/chaewon_ahyeon_research_review/docs/02_deep_research_literature.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

MANDATORY INSTRUCTIONS:
1. Read ORIGINAL_REQUEST.md at /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/ORIGINAL_REQUEST.md.
2. Read SCOPE.md at /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m2/SCOPE.md.
3. Read PROJECT.md at /home/juke/git/chaewon_ahyeon_research_review/PROJECT.md.
4. Read Milestone 1 deliverable: /home/juke/git/chaewon_ahyeon_research_review/docs/01_research_synthesis.md.
5. Read the 3 Explorer handoff reports:
   - /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m2_1/handoff.md (2-axis scaling equations, parameter behaviors, Oliveira, Narayanswamy, Banville, Ooi, Truong, and iEEG 2-axis formulation)
   - /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m2_2/handoff.md (94-paper foundation corpus, 10-model comparison matrix, negative transfer biophysical mechanics of EEG_fill vs iEEG_re)
   - /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m2_3/handoff.md (Chai 2026 entropy proxy, Layer 1 vs 12 readout divergence, held-out MAE loss vs downstream probe paradox resolution, SPEC v1 benchmarks)

YOUR TASK:
Synthesize and author the definitive academic benchmarking report:
`/home/juke/git/chaewon_ahyeon_research_review/docs/02_deep_research_literature.md`

STRUCTURE & CONTENT REQUIREMENTS:
1. Executive Summary & Research Charter (김재철 AI 클래스 인턴십, 최우수 학부생 헌장, 2축 신경 스케일링 연구의 학술적 의의).
2. Theoretical Framework of 2-Axis Neural Scaling Laws:
   - Full mathematical formulations, loss equations, and parameter dynamics of:
     * Oliveira et al. (2026, arXiv:2609.35056) Scalp EEG ($L = A N_t^{-\alpha} + B N_s^{-\beta} + L_\infty$, $\beta$ instability $0.07 \sim 1.99$).
     * Narayanswamy et al. (2024, Google LSM, arXiv:2410.13638) single-axis time scaling hypothesis ($S \times H = \text{const}$) and breakdown in iEEG.
     * Banville et al. (2025, Meta FAIR, arXiv:2501.15322) subject-specific input layers and masking of subject diversity ($p=0.49$).
     * Ooi et al. (2025, Nature 644:731) fMRI phenotype scaling ($r = K_0 \sqrt{1/(1 + K_1/N + K_2/(NT))}$), bottleneck transition from $NT$ to $N$, and temporal regime differences between fMRI (BOLD 0.1Hz) and iEEG (LFP 500Hz).
     * Truong et al. (2026, arXiv:2610.09287) Scalp EEG 10 -> 1,863 subjects, onset threshold at ~50 subjects vs iEEG threshold at $N \ge 8$.
   - iEEG-Specific 2-Axis Scaling Law Formulation derived from 안채원 선생님 & 이아현 선생님의 실측 데이터:
     * Pretraining validation loss model: $L(N_s, N_h) = L_\infty + \frac{K_s}{N_s^\beta} + \frac{K_h}{[N_s \min(N_h, H_{\text{sat}})]^\alpha}$ ($H_{\text{sat}} \approx 81.3$h).
     * Downstream linear probe score model: $S(N_s, N_h) = S_0 + \Delta S_{\max} \cdot \left[1 + (N_{\text{crit}}/N_s)^{\gamma_s}\right]^{-1} \cdot \left[1 + (H_{\text{floor}}/N_h)^{\gamma_h}\right]^{-1}$ ($N_{\text{crit}} \approx 4 \sim 8$, $H_{\text{floor}} \approx 81.3$h).
3. 94-Paper Electrophysiology Foundation Model Corpus & 10-Model Comparison Matrix:
   - Comprehensive taxonomy: MAE, CL, AR, Multimodal.
   - Full structured comparison table of 10 key models: BrainWave, BrainOmni, DIVER-0, DIVER-1 (arXiv:2512.19097), DIVER-1.5 (ACPE + channel origin prediction), Neuro-BERT, BIOT, LaBraM, Brant, CBraM (Modalities, patch size, 3D coordinate encoding vs discrete tokens, permutation equivariance, temporal receptive field, objective, scaling test).
4. Biophysical & Neurophysiological Mechanics of Modality Non-Interchangeability:
   - Rigorous physical explanation of why `EEG_fill` causes $-0.0100 [+0.0074, +0.0125]$ negative transfer penalty vs `iEEG_re`.
   - Skull volume conduction filtering: skull resistivity $\sigma_{\text{skull}} \approx 0.01\text{ S/m}$ (40~80x insulation), 10~20 $\text{cm}^2$ spatial low-pass smoothing, high-gamma (>40Hz) attenuation.
   - SNR disparity (10~100x), frequency power distribution mismatch (high-gamma 70~150 Hz local spiking vs alpha/beta 8~30 Hz).
   - Analysis of why 6 recovery ablations (`lp45`, batch z-score, adversarial training, modality tokens, etc.) all failed.
5. Information-Theoretic Grounding & Mechanistic Paradox Resolution:
   - Chai et al. (2026, arXiv:2610.05591) repetition law $\Delta L = A z^p$ ($z = (R-1) N_{\text{total}}/U$) and unigram entropy proxy ($r = -0.89$ with repetition tolerance). Explanation of iEEG intrinsic low manifold dimension.
   - Layer 1 vs Layer 12 representation readout divergence: Why 1/1024 condition preserves Layer 1 (-0.0039) but degrades Layer 12 (-0.0210), grounded in Raghu et al. (2021) and Kornblith et al. (2019).
   - Held-Out MAE reconstruction loss (+8.5%) vs downstream probe accuracy ($\Delta < -0.005$) disconnect: Grounded in Vision MAE (He et al., Goyal et al.) and SSL representation theory (reconstruction of high-frequency pixel residuals vs linear semantic separation).
6. Downstream Benchmark Evaluation Standards:
   - SPEC v1 frozen linear probe protocol vs Full Fine-Tuning trade-offs.
   - Clinical task generalization (Mayo Clinic seizure, motor BCI, cognitive speech).
7. Downstream Interface Contracts:
   - Precise input specifications for Milestone 3 (Adversarial Review) and Milestone 4 (Action Items Roadmap).

STRICT HONORIFIC RULES:
- ALWAYS "안채원 선생님", "이아현 선생님" + 존댓말 — NEVER "OO 씨" or 반말.
