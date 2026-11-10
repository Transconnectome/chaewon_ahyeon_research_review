# Scope: Milestone 5 — Repository Assembly, Executive README, E2E Acceptance, & GitHub Transconnectome Publication

## Mission
모든 연구 산출물(M1~M4)을 총괄 통합하는 최상위 `README.md`를 작성하고, E2E 검증 테스트 스위트(`tests/verify_acceptance_criteria.py`)의 82개 전 테스트(Tiers 1~4) 및 14개 적대적 스트레스 테스트(Tier 5)를 100% 통과시킨 후, 로컬 Git 저장소 초기화·커밋을 거쳐 GitHub `Transconnectome` 조직에 원격 저장소를 생성하고 성공적으로 푸시하여 프로젝트를 최종 완수한다.

## Architecture & Code Layout
- Target Deliverables:
  - `/home/juke/git/chaewon_ahyeon_research_review/README.md` (최상위 총괄 보고서)
  - `/home/juke/git/chaewon_ahyeon_research_review/.gitignore`
  - Git repository: `git init`, `git add`, `git commit`
  - GitHub Remote: `https://github.com/Transconnectome/chaewon_ahyeon_research_review`
- Working Directory: `/home/juke/git/chaewon_ahyeon_research_review`
- State Folder: `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/sub_orch_m5`

## Feature Inventory Coverage
- F6: Git Repository Structuring & Transconnectome Push
- F7: E2E Acceptance Criteria Verification

## Inputs & Authoritative Sources
1. Prior Milestone Deliverables:
   - M1: `docs/01_research_synthesis.md`
   - M2: `docs/02_deep_research_literature.md`
   - M3: `docs/03_adversarial_review.md`
   - M4: `docs/04_action_items_roadmap.md`
2. Test Suite & Infra:
   - `TEST_INFRA.md`
   - `TEST_READY.md`
   - `tests/verify_acceptance_criteria.py`
   - `tests/test_adversarial_challenge.py`
3. Environment & Tools:
   - `git`
   - `gh` CLI (`/home/juke/.local/bin/gh`, logged in as `snuconnectome` with `admin:org` / `repo` permissions)
4. Original Request & Project Plan:
   - `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/ORIGINAL_REQUEST.md`
   - `/home/juke/git/chaewon_ahyeon_research_review/PROJECT.md`

## Milestones (Internal to M5)
1. Explorer -> Worker -> Reviewer -> Challenger -> Auditor cycle.
2. Produce comprehensive `README.md` and `.gitignore`.
3. Run and pass 100% of strict E2E tests (`python3 tests/verify_acceptance_criteria.py` - all 82 tests pass) and adversarial stress tests (`python3 tests/test_adversarial_challenge.py` - 14 tests pass).
4. Initialize git repository, stage files, and create clean initial commit.
5. Check / create remote repository under GitHub `Transconnectome` org and push to `main`.
6. Verify remote publication via `gh repo view Transconnectome/chaewon_ahyeon_research_review`.

## Honorific Rules
- Students & researchers: ALWAYS "안채원 선생님", "이아현 선생님" + 존댓말 — NEVER "OO 씨" or 반말.
