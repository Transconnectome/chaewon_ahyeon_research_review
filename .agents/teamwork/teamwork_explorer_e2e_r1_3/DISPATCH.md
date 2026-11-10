## 2026-11-10T16:03:55Z
You are Explorer 3 (Test Matrix & Design Specialist) for the E2E Testing Track of `chaewon_ahyeon_research_review`.

Working directory: /home/juke/git/chaewon_ahyeon_research_review
Your state folder: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_e2e_r1_3
Dispatch file: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_e2e_r1_3/DISPATCH.md
Original request: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/ORIGINAL_REQUEST.md
Project plan: /home/juke/git/chaewon_ahyeon_research_review/PROJECT.md
Scope document: /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_e2e_testing/SCOPE.md

Tasks:
1. Read `ORIGINAL_REQUEST.md`.
2. Analyze the 7 features in `PROJECT.md` and the 4 tiers in `SCOPE.md`.
3. Design the detailed test case catalog and implementation structure for `TEST_INFRA.md` and `tests/verify_acceptance_criteria.py`:
   - Tier 1: Feature Coverage (>=5 test methods per feature for F1 through F7, total >= 35)
   - Tier 2: Boundary & Corner Cases (>=5 test methods per feature for F1 through F7, total >= 35, including strict honorific validation that "안채원 선생님" and "이아현 선생님" are used everywhere, and "씨" or 반말 are banned)
   - Tier 3: Cross-Feature Interactions (>= 7 pairwise integration tests)
   - Tier 4: Real-World Application Scenarios (>= 5 application-level acceptance tests)
   Total test cases: >= 82 tests.
4. Define test assertions, input fixtures, expected outputs, and pass/fail semantics.
5. Write your design report to `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_e2e_r1_3/test_design_matrix.md`.
6. Write a complete handoff to `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_e2e_r1_3/handoff.md`.
7. Message the orchestrator when finished. Do not modify or write source code.
