# Handoff Report — False Negative and CLI Filtering Loopholes (Iteration 2)

- **Track**: E2E Acceptance Testing (Iteration 2)
- **Explorer**: Explorer 3 (Read-only Investigation & Analysis)
- **Target File**: `tests/verify_acceptance_criteria.py`
- **Scope**: Loopholes 8, 9, 10, 11 (False negatives and CLI filtering)
- **Working Directory**: `/home/juke/git/chaewon_ahyeon_research_review`
- **State Folder**: `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_e2e_r2_3`
- **Reference Analysis**: `.agents/teamwork/teamwork_explorer_e2e_r2_3/report.md`

---

## 1. Observation

Direct code inspection of `/home/juke/git/chaewon_ahyeon_research_review/tests/verify_acceptance_criteria.py` and empirical execution of `tests/test_adversarial_challenge.py` revealed:

1. **Loophole 8 (`test_f3_b01_valid_publication_years`, lines 678–691)**:
   - Verbatim code:
     ```python
     years = [int(y) for y in re.findall(r"\b(20[12]\d)\b", content)]
     self.assertTrue(years, "No publication years found in literature review")
     self.assertTrue(
         all(2015 <= y <= 2027 for y in years),
         f"Detected invalid publication year out of range: {years}"
     )
     ```
   - Observed failure: In `tests/test_adversarial_challenge.py:test_challenge_false_negative_pre_2015_scholarly_citation`, a document citing Mikolov et al. (2013) alongside contemporary 2025/2026 works triggers `2015 <= 2013 <= 2027 -> False`, causing false rejection of valid scholarly literature.

2. **Loophole 9 (`test_f5_b05_dependency_ordering_topology`, lines 829–838)**:
   - Verbatim code:
     ```python
     pos_imm = content.find("단기") if "단기" in content else content.find("Immediate")
     pos_med = content.find("중기") if "중기" in content else content.find("Medium")
     pos_lng = content.find("장기") if "장기" in content else content.find("Long")
     self.assertTrue(
         0 <= pos_imm < pos_med < pos_lng,
         f"Roadmap tiers not sequentially ordered: pos_imm={pos_imm}, pos_med={pos_med}, pos_lng={pos_lng}"
     )
     ```
   - Observed failure: In `tests/test_adversarial_challenge.py:test_challenge_false_negative_roadmap_ordering_sentence`, an intro sentence stating `"본 문서는 장기적 비전과 중기적 과제, 그리고 단기적 실행 항목을 종합한다"` causes `pos_lng (12) < pos_imm (35)`, failing `0 <= pos_imm < pos_med < pos_lng` despite correct subsequent section headings (`## 단기`, `## 중기`, `## 장기`).

3. **Loophole 10 (`test_f3_b05_latex_math_syntax_validity`, lines 723–734)**:
   - Verbatim code:
     ```python
     math_blocks = re.findall(r"\$([^\$]+)\$", content)
     self.assertGreaterEqual(len(math_blocks), 2, "Insufficient mathematical formulations in literature review")
     for block in math_blocks:
         self.assertEqual(
             block.count("{"),
             block.count("}"),
             f"Unbalanced braces in LaTeX formula: ${block}$"
         )
     ```
   - Observed failure: In `tests/test_adversarial_challenge.py:test_challenge_false_negative_display_math_desync`, display math `$$...$$` desynchronizes dollar sign parity. Korean natural prose between the closing `$$` and the next inline `$a=b$` is captured as `block`. An unmatched brace in Korean prose (e.g. `{설명 은`) causes false failure on prose rather than formula.

4. **Loophole 11 (`FEATURE_PREFIXES`, lines 1169–1178)**:
   - Verbatim code:
     ```python
     FEATURE_PREFIXES = {
         "F1": ("test_f1_", "test_f1_b", "test_tier3_01", "test_tier3_02"),
         "F2": ("test_f2_", "test_f2_b", "test_tier3_01", "test_tier3_03"),
         "F3": ("test_f3_", "test_f3_b", "test_tier3_04"),
         "F4": ("test_f4_", "test_f4_b", "test_tier3_02", "test_tier3_03", "test_tier3_04", "test_tier3_05"),
         "F5": ("test_f5_", "test_f5_b", "test_tier3_05", "test_tier3_06"),
         "F6": ("test_f6_", "test_f6_b", "test_tier3_06", "test_tier3_07"),
         "F7": ("test_f7_", "test_f7_b", "test_tier3_07"),
     }
     ```
   - Observed failure: Running `python3 tests/verify_acceptance_criteria.py --feature <FEAT>` filters out all methods not matching prefixes. Because none of the prefixes match `test_tier4_s01`..`s05`, zero Tier 4 tests ever execute when filtering by feature.

---

## 2. Logic Chain

1. **Scholarly Citation Inclusivity**:
   - *Observation*: EEG and ML foundational literature frequently spans 1950–2014 (e.g. Jasper 1958, Mikolov 2013).
   - *Inference*: The assertion `all(2015 <= y <= 2027)` creates brittle false rejections.
   - *Resolution*: Broadening to `[1950..2027]` using `r"\b(19\d\d|20\d\d)\b"` while maintaining `2025 in years or 2026 in years` allows historical references while enforcing contemporary foundation models.

2. **Heading Scoping for Topological Ordering**:
   - *Observation*: Natural Korean prose often mentions long-term, medium-term, and short-term goals in non-chronological order.
   - *Inference*: Whole-file substring matching binds to the first mention in prose rather than structural sections.
   - *Resolution*: Matching Markdown headers specifically (`r"^#+\s*.*(?:단기|Immediate)"`) isolates section headers from introductory prose.

3. **LaTeX Delimiter Parity Isolation**:
   - *Observation*: Single regex `\$([^\$]+)\$` fails on multiline display math `$$...$$` and misinterprets following prose.
   - *Inference*: Display math blocks must be stripped before scanning for inline math blocks.
   - *Resolution*: Two-stage extraction: extract `$$...$$` with `re.DOTALL`, strip them, then extract `(?<!\$)\$([^\$\n]+)\$(?!\$)`. Combine both lists for brace checking.

4. **Tier 4 Scenario Coverage in Feature Filtering**:
   - *Observation*: Developers use `--feature F<N>` to test specific features, but currently miss all governance and acceptance checks.
   - *Inference*: Tier 4 scenarios correspond directly to specific project features (F1: honorific governance s02 & workshop s04; F2: workshop evaluation s04; F3: publication formatting s03; F4: core request criteria s01; F5: roadmap timeline s04; F6: git & distribution s01, s03, s05; F7: all acceptance scenarios s01..s05).
   - *Resolution*: Add corresponding `test_tier4_` prefixes to `FEATURE_PREFIXES` in `verify_acceptance_criteria.py`.

---

## 3. Caveats

- **Scope Boundary**: This handoff specifically covers Loopholes 8, 9, 10, 11. Loopholes 1–7 (honorific student surnames, banmal leaks, untracked root files, KISTI monotonicity, contract vulnerability completeness, broken link anchors, and body placeholders) are handled by fellow track Explorers/Workers.
- **Unbuilt Milestone Documents**: Milestones M2 (`02_deep_research_literature.md`), M3 (`03_adversarial_review.md`), and M4 (`04_action_items_roadmap.md`) are currently pending in the workspace. Fixes were verified against both the progressive suite and simulated isolated documents matching downstream specifications.
- **Read-Only Investigation**: As an Explorer, no edits were made directly to `tests/verify_acceptance_criteria.py`. All code snippets are ready for Worker implementation.

---

## 4. Conclusion

The exact code fix strategy and drop-in replacements for Loopholes 8, 9, 10, and 11 have been designed, empirically simulated, and validated with zero regressions against the existing test suite:
- **Loophole 8**: `test_f3_b01` updated to `[1950..2027]` range + `2025/2026` presence.
- **Loophole 9**: `test_f5_b05` updated to regex header matching (`r"^#+\s*.*(?:단기|Immediate)"`).
- **Loophole 10**: `test_f3_b05` updated to two-stage display/inline math extraction and combined brace checking.
- **Loophole 11**: `FEATURE_PREFIXES` updated to include Tier 4 scenarios across F1 through F7.

Full replacement code snippets with line numbers and diffs are documented in:
`/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_e2e_r2_3/report.md`.

---

## 5. Verification Method

To verify these findings and the proposed fixes:

```bash
# 1. Inspect technical analysis report and replacement snippets
cat /home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_e2e_r2_3/report.md

# 2. Run monkeypatched empirical verification script
python3 -c '
import importlib.util, re, tempfile, unittest
from pathlib import Path

p = Path("/home/juke/git/chaewon_ahyeon_research_review/tests/verify_acceptance_criteria.py")
spec = importlib.util.spec_from_file_location("vac", p)
vac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vac)

def fixed_test_f3_b01(self):
    content = self.read_doc_safe("docs/02_deep_research_literature.md")
    years = [int(y) for y in re.findall(r"\b(19\d\d|20\d\d)\b", content)]
    self.assertTrue(years and all(1950 <= y <= 2027 for y in years) and (2025 in years or 2026 in years))

def fixed_test_f5_b05(self):
    content = self.read_doc_safe("docs/04_action_items_roadmap.md")
    m_imm = re.search(r"^#+\s*.*(?:단기|Immediate)", content, re.M | re.I)
    m_med = re.search(r"^#+\s*.*(?:중기|Medium)", content, re.M | re.I)
    m_lng = re.search(r"^#+\s*.*(?:장기|Long)", content, re.M | re.I)
    self.assertTrue(m_imm and m_med and m_lng and m_imm.start() < m_med.start() < m_lng.start())

def fixed_test_f3_b05(self):
    content = self.read_doc_safe("docs/02_deep_research_literature.md")
    disp = re.findall(r"\$\$(.+?)\$\$", content, re.DOTALL)
    clean = re.sub(r"\$\$(.+?)\$\$", "", content, flags=re.DOTALL)
    inl = re.findall(r"(?<!\$)\$([^\$\n]+)\$(?!\$)", clean)
    all_b = disp + inl
    self.assertTrue(len(all_b) >= 2 and all(b.count("{") == b.count("}") for b in all_b))

vac.TestTier2BoundaryCases.test_f3_b01_valid_publication_years = fixed_test_f3_b01
vac.TestTier2BoundaryCases.test_f5_b05_dependency_ordering_topology = fixed_test_f5_b05
vac.TestTier2BoundaryCases.test_f3_b05_latex_math_syntax_validity = fixed_test_f3_b05

vac.FEATURE_PREFIXES = {
    "F1": ("test_f1_", "test_f1_b", "test_tier3_01", "test_tier3_02", "test_tier4_s02", "test_tier4_s04"),
    "F2": ("test_f2_", "test_f2_b", "test_tier3_01", "test_tier3_03", "test_tier4_s04"),
    "F3": ("test_f3_", "test_f3_b", "test_tier3_04", "test_tier4_s03"),
    "F4": ("test_f4_", "test_f4_b", "test_tier3_02", "test_tier3_03", "test_tier3_04", "test_tier3_05", "test_tier4_s01"),
    "F5": ("test_f5_", "test_f5_b", "test_tier3_05", "test_tier3_06", "test_tier4_s04"),
    "F6": ("test_f6_", "test_f6_b", "test_tier3_06", "test_tier3_07", "test_tier4_s01", "test_tier4_s03", "test_tier4_s05"),
    "F7": ("test_f7_", "test_f7_b", "test_tier3_07", "test_tier4_"),
}

code = vac.run_tests_with_reporting(progressive=True)
assert code == 0, "Progressive test suite must pass with 0 failures"
print("Independent Verification PASSED cleanly.")
'
```
