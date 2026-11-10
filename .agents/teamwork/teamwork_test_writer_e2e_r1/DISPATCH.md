## 2026-11-10T16:12:27Z
You are the Test Writer for the E2E Testing Track of `chaewon_ahyeon_research_review`.

Working directory: /home/juke/git/chaewon_ahyeon_research_review
Your state folder: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_test_writer_e2e_r1
Dispatch file: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_test_writer_e2e_r1/DISPATCH.md
Original request: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/ORIGINAL_REQUEST.md
Project plan: /home/juke/git/chaewon_ahyeon_research_review/PROJECT.md
Scope document: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_e2e_testing/SCOPE.md

Explorer findings to base your implementation on:
- Explorer 1 (Spec Miner): /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_spec_miner_e2e_r1_1/report.md
- Explorer 2 (Repo & Env): /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_e2e_r1_2/report.md
- Explorer 3 (Test Matrix & Design): /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_e2e_r1_3/test_design_matrix.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

STRICT CONSTRAINTS:
- Honorifics: ALWAYS use "안채원 선생님", "이아현 선생님" (NEVER "OO 씨" or 반말) in all files, comments, docstrings, error messages, and documentation.
- Write ownership: You exclusively own `/home/juke/git/chaewon_ahyeon_research_review/TEST_INFRA.md` and `/home/juke/git/chaewon_ahyeon_research_review/tests/verify_acceptance_criteria.py`.

Deliverables:
1. Create `TEST_INFRA.md` at project root covering:
   - Test philosophy (Opaque-box, requirement-driven, 4 tiers).
   - Feature Inventory mapping for F1 through F7.
   - Test architecture and runner specification (`python3 tests/verify_acceptance_criteria.py`).
   - Detailed coverage thresholds: Tier 1 (35), Tier 2 (35), Tier 3 (7), Tier 4 (5) = total 82 test cases.
2. Create and implement `tests/verify_acceptance_criteria.py`:
   - Full implementation of all 82 test cases defined in Explorer 3's `test_design_matrix.md`.
   - Standalone executable via `python3 tests/verify_acceptance_criteria.py` and compatible with `pytest`.
   - CLI flags: `--progressive` (skips or marks pending for artifacts not yet created by in-progress implementation milestones, reporting progressive pass/fail), `--tier <1|2|3|4>`, `--feature <F1..F7>`, `--verbose`.
   - Standard execution: exit code 0 on complete pass, 1 on failure.
   - Genuine test logic: verify file presence, section headers, specific numerical values (e.g. 37 subjects, 5203h, 2.88M samples, delta > -0.005), citations, adversarial critique axes, action items roadmap, git status, and strict honorific regex ("안채원 선생님", "이아현 선생님" required; "씨" and 반말 forbidden).
3. Run the test runner:
   - Execute `python3 tests/verify_acceptance_criteria.py --help`
   - Execute `python3 tests/verify_acceptance_criteria.py --progressive`
   - Verify that test execution runs cleanly and reports diagnostics properly.
4. Write `handoff.md` in your state folder with build/test execution results and layout compliance.
5. Send message to the orchestrator upon completion.
