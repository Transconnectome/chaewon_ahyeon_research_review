## 2026-11-10T16:34:42Z
You are an Explorer for Milestone 2 (Deep Research & Scholarly Literature Benchmarking).
State folder: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m2_3
Working directory: /home/juke/git/chaewon_ahyeon_research_review

MANDATORY INSTRUCTIONS:
1. First, read ORIGINAL_REQUEST.md at /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/ORIGINAL_REQUEST.md.
2. Read SCOPE.md at /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m2/SCOPE.md.
3. Read PROJECT.md at /home/juke/git/chaewon_ahyeon_research_review/PROJECT.md.
4. Read docs/01_research_synthesis.md at /home/juke/git/chaewon_ahyeon_research_review/docs/01_research_synthesis.md.
5. Read Survey 2 and Survey 3 handoffs in .agents/teamwork/ if needed.

YOUR MISSION:
Deeply explore the theoretical mechanics, information-theoretic grounding, and downstream benchmark methodologies:
1. Chai (2026) Entropy Proxy & Information Dynamics:
   - Formulate and analyze the Chai (2026) entropy proxy ($r = -0.89$ with repetition tolerance).
   - Information-theoretic explanation for why iEEG downstream representation saturates at 81.3 hours (1/64) and even preserves early features at 5.1 hours (1/1024).
   - High temporal resolution, high local signal-to-noise ratio, and lower effective neural manifold dimensionality in local cortical populations.
2. Representation Readout Divergence (Layer 1 vs Layer 12):
   - Analyze why in the extreme 1/1024 data regime (5.1h), Layer 1 preserves performance (-0.0039) but Layer 12 drops significantly (-0.0210).
   - Literature on feature re-use vs semantic abstraction in deep Transformer encoders (Raghu et al., Kornblith et al., Choshen et al.).
3. Held-out Reconstruction Loss vs Downstream Probe Disconnect:
   - Why held-out MAE reconstruction loss degrades (+8.5%) as data is reduced while downstream probe accuracy remains invariant ($\Delta < -0.005$).
   - Reconcile this paradox using literature from Vision MAE (He et al., Goyal et al.) and SSL representation learning: reconstruction loss optimizes pixel/sample-level high-frequency residuals, while linear probes evaluate semantic linear separability.
4. Downstream Evaluation Paradigms & Clinical Task Generalization:
   - SPEC v1 benchmark: Frozen linear probe protocol, non-inferiority margin $\Delta > -0.005$.
   - Contrast with Full Fine-tuning risks (catastrophic forgetting, overfitting on small target cohorts).
   - Clinical benchmark coverage: Mayo Clinic seizure detection, BCI motor imagery, cognitive speech decoding.

Strictly follow honorific rules: ALWAYS "안채원 선생님", "이아현 선생님" (NEVER "OO 씨" or 반말).
Save your full findings in /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m2_3/handoff.md and report completion via send_message.
