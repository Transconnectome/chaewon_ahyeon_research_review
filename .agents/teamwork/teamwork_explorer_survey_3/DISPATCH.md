# Dispatch: Survey Explorer 3 (이아현 선생님 Research & Infrastructure Investigation)

## Objective
Investigate all research details, hypotheses, data, code, and experimental results shared by 이아현 선생님, as well as the GitHub Transconnectome environment and repository requirements.

## Inputs
- ORIGINAL_REQUEST: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/ORIGINAL_REQUEST.md
- Teams database: `~/.agents/registry/chavis_teams/teams.db`
- Local repositories or file paths mentioned in messages
- GitHub Transconnectome org status (`gh repo list Transconnectome` or git config)
- Working directory: /home/juke/git/chaewon_ahyeon_research_review
- State folder: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_survey_3

## Scope & Instructions
1. Extract all messages and shared files from 이아현 선생님 in Teams.
2. Identify:
   - Research topic, core hypotheses, and scientific questions.
   - Datasets used, methodologies, models, analytical frameworks, and current results.
   - Joint research points or overlaps with 안채원 선생님's work.
3. Check Transconnectome organization access on GitHub via `gh` CLI (`gh auth status`, `gh repo list Transconnectome`, etc.).
4. Output a detailed report to `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_survey_3/handoff.md`.
5. Strictly adhere to honorific rule: "이아현 선생님".


## 2026-11-10T15:48:38Z
You are teamwork_explorer_survey_3.
Your task is to conduct an in-depth investigation into all research details, hypotheses, data, code, and experimental results shared by 이아현 선생님, along with the GitHub Transconnectome environment and repository requirements.

Working directory: /home/juke/git/chaewon_ahyeon_research_review
State folder: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_survey_3
Original request: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/ORIGINAL_REQUEST.md
Dispatch details: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_survey_3/DISPATCH.md

Instructions:
1. Read ORIGINAL_REQUEST.md and DISPATCH.md.
2. Query Teams data (`~/.agents/registry/chavis_teams/teams.db` and related paths) for all communications from 이아현 선생님.
3. Check local git repositories in `~/git/` or on connectome/servers if referenced.
4. Extract the core scientific questions, hypotheses, datasets, models, metrics, and empirical findings. Also identify research overlap/synergy with 안채원 선생님.
5. Check GitHub Transconnectome organization status (`gh auth status`, `gh repo list Transconnectome`, etc.).
6. Synthesize findings into `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_survey_3/handoff.md`.
7. Strictly adhere to the honorific rule: ALWAYS "이아현 선생님", "안채원 선생님" (NEVER "OO 씨" or 반말).
8. When complete, send a message to parent notifying completion.
