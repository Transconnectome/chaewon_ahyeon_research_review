# BRIEFING — 2026-11-10T16:15:00Z

## Mission
Thoroughly explore and extract all empirical data, methodology, experimental results, and theoretical claims regarding 안채원 선생님's research across 4 key tracks.

## 🔒 My Identity
- Archetype: explorer
- Roles: investigator, empirical data extractor, evidence synthesizer
- Working directory: /home/juke/git/chaewon_ahyeon_research_review
- State folder: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m1_1
- Original parent: 3f74780d-a2be-4f20-9156-47d37e41530b
- Milestone: Milestone 1 (Research Synthesis & Evidence Documentation)

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Students & researchers: ALWAYS "안채원 선생님", "이아현 선생님" + 존댓말 — NEVER "OO 씨" or 반말
- Evidence over agreement: exact paths, lines, numbers, no approximations or guesses
- Write only inside state folder `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/explorer_m1_1`

## Current Parent
- Conversation ID: 3f74780d-a2be-4f20-9156-47d37e41530b
- Updated: 2026-11-10T16:02:08Z

## Investigation State
- **Explored paths**:
  - `ORIGINAL_REQUEST.md`, `PROJECT.md`, `SCOPE.md`
  - Survey handoffs 1, 2, 3 in `.agents/teamwork/`
  - `/home/juke/git/chaewon-intern-2026fall`: `hangang/reports/paper_skeleton.md`, `hangang/reports/results-table-20261107.md`, `hangang/reports/morning-table-20261108.md`, `hangang/reports/condition-verdict-20261108.md`, `hangang/reports/draft_gaps-20261109.md`, `hangang/reports/hangang_report.md`, `scaling_literature/SUBJECT_AXIS_REPORT.md`, `meetings/2026-11-09_아현쌤/README.md`
  - `/home/juke/git/DIVER-2`: `diver_pretrain/releases/diver15/README.md`, `config/diver15/README.md`, `TODO/stcpe_spera_bias.md`, `docs/archive/CHANNEL_POSITIONS_2026-08.md`, `arch/scripts/eval_coord_robustness.py`
- **Key findings**:
  - Track 1: 2-axis scaling law (37 subjects, 5,203h, 2.88M samples fixed; non-inferiority Delta > -0.005 on 1/64 (81h) and 1/1024 (5h); collapse at 2 subjects (-0.0055) vs maintained at 8 subjects (+0.0001); non-substitutability of EEG (-0.0100 loss)).
  - Track 2: KISTI 한강 GH200 strong/weak scaling, step speedup 1.60x-1.72x vs AICA, 80-87% runtime, GH200 1-node throughput = 3.8x Aurora PVC node.
  - Track 3: Dataloader I/O bottleneck & timer bug in PyTorch DDP all-reduce, LMDB sparse format (apparent 3.0 TiB vs 608 GB real), optimal worker configuration (AJILE 2, iEEG 24, EEGV2 16).
  - Track 4: ACPE & channel montage robustness, STCPE vs coordinate dropout, MNI coordinate transforms and tolerance to missing electrodes.
  - Deep empirical divergences: Layer 1 vs Layer 12 probe divergence; held-out reconstruction loss (+8.5%) vs downstream score maintenance.
- **Unexplored areas**: None for M1 Explorer 1.

## Key Decisions Made
- Structure the deliverable `handoff.md` following the strict 5-component Teamwork Handoff Protocol with comprehensive data tables, code/log references, and exact statistics.

## Artifact Index
- DISPATCH.md — incoming task dispatch
- BRIEFING.md — persistent working memory
- progress.md — liveness heartbeat
- handoff.md — final 5-component deliverable
