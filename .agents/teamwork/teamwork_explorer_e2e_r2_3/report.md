# Technical Analysis & Fix Strategy: False Negatives and CLI Filtering Loopholes (Iteration 2)

- **Target**: `tests/verify_acceptance_criteria.py`
- **Track**: E2E Acceptance Testing (Iteration 2)
- **Author**: Explorer 3 (Read-only Investigation & Analysis)
- **State Folder**: `/home/juke/git/chaewon_ahyeon_research_review/.agents/teamwork/teamwork_explorer_e2e_r2_3`
- **Scope**: Loopholes 8, 9, 10, 11 identified by Challenger 1

---

## 1. Executive Summary

Empirical analysis of `tests/verify_acceptance_criteria.py` and Challenger 1's adversarial test suite (`tests/test_adversarial_challenge.py`) reveals four critical failure modes:
1. **Loophole 8 (`test_f3_b01`)**: Valid scholarly citations of foundational pre-2015 literature (e.g. Mikolov 2013, Jasper 1958) or sample sizes trigger false rejections because of a brittle year filter `all(2015 <= y <= 2027)`.
2. **Loophole 9 (`test_f5_b05`)**: Naive substring `.find()` on the entire document falsely rejects valid roadmaps whose introductory prose mentions planning tiers in natural non-chronological order (e.g. "장기적 비전과 중기적 과제, 그리고 단기적 실행 항목").
3. **Loophole 10 (`test_f3_b05`)**: LaTeX display math blocks (`$$...$$`) consume paired `$` delimiters and invert regex capture parity, causing adjacent Korean prose to be captured as math formulas and falsely failing on unbalanced braces in text.
4. **Loophole 11 (`FEATURE_PREFIXES`)**: CLI `--feature` filters completely exclude all Tier 4 real-world acceptance scenarios (`test_tier4_s01` through `s05`), leaving governance and stakeholder readiness unverified during feature-scoped test runs.

All four issues have been analyzed down to exact line numbers, modeled in isolated test environments, and verified with both positive and negative assertions. Ready-to-apply replacement snippets and diffs are detailed below for the Worker.

---

## 2. In-Depth Root Cause Analysis

### 2.1 Loophole 8: Pre-2015 Citation False Rejections (`test_f3_b01`)
- **File & Lines**: `tests/verify_acceptance_criteria.py:678-691`
- **Current Implementation**:
  ```python
  def test_f3_b01_valid_publication_years(self):
      """[T2-F3B-01] Verify all citation publication years fall in valid scholarly range [2015..2027]."""
      content = self.read_doc_safe("docs/02_deep_research_literature.md")
      years = [int(y) for y in re.findall(r"\b(20[12]\d)\b", content)]
      self.assertTrue(years, "No publication years found in literature review")
      self.assertTrue(
          all(2015 <= y <= 2027 for y in years),
          f"Detected invalid publication year out of range: {years}"
      )
      self.assertTrue(
          2025 in years or 2026 in years,
          "Missing contemporary 2025/2026 foundation model literature citations"
      )
  ```
- **Root Cause**:
  1. The regex `r"\b(20[12]\d)\b"` extracts any four-digit token in `[2010..2029]`.
  2. The strict assertion `all(2015 <= y <= 2027 for y in years)` immediately causes test failure if a researcher cites classic pre-2015 machine learning or neuroscience literature (e.g., Mikolov et al. 2013 Word2Vec, Krizhevsky et al. 2012 AlexNet, Bengio et al. 2003, Jasper 1958 EEG standard).
  3. Furthermore, any metric such as "2014 samples" will also fail.
- **Remediation Strategy**:
  - Broaden the valid historical scholarly range to `[1950..2027]` using regex `r"\b(19\d\d|20\d\d)\b"`.
  - Maintain the contemporary assertion `2025 in years or 2026 in years` to ensure the literature review incorporates cutting-edge foundation models.
  - This guards against hallucinated future years (e.g. 2035) while permitting genuine historical foundations.

---

### 2.2 Loophole 9: Roadmap Dependency Ordering False Rejections (`test_f5_b05`)
- **File & Lines**: `tests/verify_acceptance_criteria.py:829-838`
- **Current Implementation**:
  ```python
  def test_f5_b05_dependency_ordering_topology(self):
      """[T2-F5B-05] Verify sequential ordering: Immediate (단기) precedes Medium (중기) precedes Long (장기)."""
      content = self.read_doc_safe("docs/04_action_items_roadmap.md")
      pos_imm = content.find("단기") if "단기" in content else content.find("Immediate")
      pos_med = content.find("중기") if "중기" in content else content.find("Medium")
      pos_lng = content.find("장기") if "장기" in content else content.find("Long")
      self.assertTrue(
          0 <= pos_imm < pos_med < pos_lng,
          f"Roadmap tiers not sequentially ordered: pos_imm={pos_imm}, pos_med={pos_med}, pos_lng={pos_lng}"
      )
  ```
- **Root Cause**:
  1. `content.find(...)` searches linearly from index 0 across the entire file.
  2. If the document includes an executive overview such as *"본 문서는 장기적 비전과 중기적 과제, 그리고 단기적 실행 항목을 종합한다"*, the first occurrence of "장기" is at index 12, whereas "단기" is at index 35.
  3. Consequently, `pos_lng < pos_imm`, triggering a false negative failure despite proper chronological section headings (`## 단기`, `## 중기`, `## 장기`).
- **Remediation Strategy**:
  - Restrict the positional search to actual Markdown headings using `re.search(r"^#+\s*.*(?:단기|Immediate)", content, re.MULTILINE | re.IGNORECASE)` and corresponding patterns for 중기/Medium and 장기/Long.
  - Assert that all three section headers exist (`assertIsNotNone`), and that their header start positions satisfy `pos_imm < pos_med < pos_lng`.

---

### 2.3 Loophole 10: LaTeX Display Math `$$` Desynchronization (`test_f3_b05`)
- **File & Lines**: `tests/verify_acceptance_criteria.py:723-734`
- **Current Implementation**:
  ```python
  def test_f3_b05_latex_math_syntax_validity(self):
      """[T2-F3B-05] Verify valid syntax and balanced braces in inline LaTeX scaling formulas."""
      content = self.read_doc_safe("docs/02_deep_research_literature.md")
      math_blocks = re.findall(r"\$([^\$]+)\$", content)
      self.assertGreaterEqual(len(math_blocks), 2, "Insufficient mathematical formulations in literature review")
      for block in math_blocks:
          self.assertEqual(
              block.count("{"),
              block.count("}"),
              f"Unbalanced braces in LaTeX formula: ${block}$"
          )
  ```
- **Root Cause**:
  1. Standard LaTeX display math uses `$$ ... $$` (two pairs of `$` signs).
  2. The regex `r"\$([^\$]+)\$"` matches from the 2nd `$` to the 3rd `$`, leaving the 4th `$` open.
  3. The next capture starts at the 4th `$` and matches up to the opening `$` of the next inline formula (`$...$`).
  4. As a result, the intervening natural language prose is captured as a "math block". If that prose contains Korean curly brackets or explanatory braces (e.g. `{설명 은`), the test crashes with unbalanced braces on ordinary prose text.
- **Remediation Strategy**:
  - Two-stage extraction:
    1. Extract all display math blocks via `re.findall(r"\$\$(.+?)\$\$", content, re.DOTALL)`.
    2. Strip all display math blocks using `re.sub(r"\$\$(.+?)\$\$", "", content, flags=re.DOTALL)`.
    3. Extract all inline math blocks from the stripped content using `re.findall(r"(?<!\$)\$([^\$\n]+)\$(?!\$)", clean_content)`.
  - Combine both lists: `all_blocks = display_blocks + inline_blocks`.
  - Verify that `len(all_blocks) >= 2` and every block has balanced `{` and `}` braces.

---

### 2.4 Loophole 11: Tier 4 Exclusion in CLI `FEATURE_PREFIXES`
- **File & Lines**: `tests/verify_acceptance_criteria.py:1169-1178`
- **Current Implementation**:
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
- **Root Cause**:
  1. `build_filtered_suite` iterates over all test classes (including `TestTier4AcceptanceScenarios`).
  2. However, when `--feature <FEAT>` is supplied, method names must match at least one prefix in `FEATURE_PREFIXES[<FEAT>]`.
  3. Because `FEATURE_PREFIXES` contains zero `test_tier4_` prefixes, every single Tier 4 test (`test_tier4_s01`..`s05`) is skipped whenever a developer filters by feature.
- **Remediation Strategy**:
  - Map specific Tier 4 scenario tests into their semantically relevant features:
    - **F1**: `test_tier4_s02` (Lab governance & honorific compliance), `test_tier4_s04` (NeuroAI 2027 workshop readiness)
    - **F2**: `test_tier4_s04` (Empirical figures and evaluation setup)
    - **F3**: `test_tier4_s03` (Publication readiness audit: markdown headers and table formatting)
    - **F4**: `test_tier4_s01` (Fulfillment of core adversarial criteria R2)
    - **F5**: `test_tier4_s04` (Action item roadmap milestone & NeuroAI 11/20 deadline)
    - **F6**: `test_tier4_s01` (Git init & README), `test_tier4_s03` (Markdown hygiene), `test_tier4_s05` (Transconnectome runner check)
    - **F7**: `test_tier4_` (All 5 acceptance criteria scenarios)

---

## 3. Exact Code Fix Strategy & Drop-in Replacement Snippets for Worker

### 3.1 Replacement Snippet 1: Loophole 8 (`test_f3_b01_valid_publication_years`)
**Target File**: `tests/verify_acceptance_criteria.py`  
**Target Lines**: 678-691

```python
<<<<
    def test_f3_b01_valid_publication_years(self):
        """[T2-F3B-01] Verify all citation publication years fall in valid scholarly range [2015..2027]."""
        content = self.read_doc_safe("docs/02_deep_research_literature.md")
        years = [int(y) for y in re.findall(r"\b(20[12]\d)\b", content)]
        self.assertTrue(years, "No publication years found in literature review")
        self.assertTrue(
            all(2015 <= y <= 2027 for y in years),
            f"Detected invalid publication year out of range: {years}"
        )
        self.assertTrue(
            2025 in years or 2026 in years,
            "Missing contemporary 2025/2026 foundation model literature citations"
        )
====
    def test_f3_b01_valid_publication_years(self):
        """[T2-F3B-01] Verify citation publication years fall in valid scholarly range [1950..2027] with contemporary papers."""
        content = self.read_doc_safe("docs/02_deep_research_literature.md")
        years = [int(y) for y in re.findall(r"\b(19\d\d|20\d\d)\b", content)]
        self.assertTrue(years, "No publication years found in literature review")
        self.assertTrue(
            all(1950 <= y <= 2027 for y in years),
            f"Detected invalid publication year out of range [1950..2027]: {years}"
        )
        self.assertTrue(
            2025 in years or 2026 in years,
            "Missing contemporary 2025/2026 foundation model literature citations"
        )
>>>>
```

---

### 3.2 Replacement Snippet 2: Loophole 10 (`test_f3_b05_latex_math_syntax_validity`)
**Target File**: `tests/verify_acceptance_criteria.py`  
**Target Lines**: 723-734

```python
<<<<
    def test_f3_b05_latex_math_syntax_validity(self):
        """[T2-F3B-05] Verify valid syntax and balanced braces in inline LaTeX scaling formulas."""
        content = self.read_doc_safe("docs/02_deep_research_literature.md")
        math_blocks = re.findall(r"\$([^\$]+)\$", content)
        self.assertGreaterEqual(len(math_blocks), 2, "Insufficient mathematical formulations in literature review")
        for block in math_blocks:
            self.assertEqual(
                block.count("{"),
                block.count("}"),
                f"Unbalanced braces in LaTeX formula: ${block}$"
            )
====
    def test_f3_b05_latex_math_syntax_validity(self):
        """[T2-F3B-05] Verify valid syntax and balanced braces in LaTeX scaling formulas (display and inline)."""
        content = self.read_doc_safe("docs/02_deep_research_literature.md")
        # Extract display math blocks ($$...$$) first to prevent parser desynchronization
        display_blocks = re.findall(r"\$\$(.+?)\$\$", content, re.DOTALL)
        # Strip display math blocks before extracting inline math blocks ($...$)
        clean_content = re.sub(r"\$\$(.+?)\$\$", "", content, flags=re.DOTALL)
        inline_blocks = re.findall(r"(?<!\$)\$([^\$\n]+)\$(?!\$)", clean_content)
        all_blocks = display_blocks + inline_blocks

        self.assertGreaterEqual(
            len(all_blocks),
            2,
            f"Insufficient mathematical formulations in literature review: found {len(all_blocks)} < 2"
        )
        for block in all_blocks:
            self.assertEqual(
                block.count("{"),
                block.count("}"),
                f"Unbalanced braces in LaTeX formula: {block.strip()}"
            )
>>>>
```

---

### 3.3 Replacement Snippet 3: Loophole 9 (`test_f5_b05_dependency_ordering_topology`)
**Target File**: `tests/verify_acceptance_criteria.py`  
**Target Lines**: 829-838

```python
<<<<
    def test_f5_b05_dependency_ordering_topology(self):
        """[T2-F5B-05] Verify sequential ordering: Immediate (단기) precedes Medium (중기) precedes Long (장기)."""
        content = self.read_doc_safe("docs/04_action_items_roadmap.md")
        pos_imm = content.find("단기") if "단기" in content else content.find("Immediate")
        pos_med = content.find("중기") if "중기" in content else content.find("Medium")
        pos_lng = content.find("장기") if "장기" in content else content.find("Long")
        self.assertTrue(
            0 <= pos_imm < pos_med < pos_lng,
            f"Roadmap tiers not sequentially ordered: pos_imm={pos_imm}, pos_med={pos_med}, pos_lng={pos_lng}"
        )
====
    def test_f5_b05_dependency_ordering_topology(self):
        """[T2-F5B-05] Verify sequential ordering: Immediate (단기) precedes Medium (중기) precedes Long (장기)."""
        content = self.read_doc_safe("docs/04_action_items_roadmap.md")
        m_imm = re.search(r"^#+\s*.*(?:단기|Immediate)", content, re.MULTILINE | re.IGNORECASE)
        m_med = re.search(r"^#+\s*.*(?:중기|Medium)", content, re.MULTILINE | re.IGNORECASE)
        m_lng = re.search(r"^#+\s*.*(?:장기|Long)", content, re.MULTILINE | re.IGNORECASE)
        self.assertIsNotNone(m_imm, "Missing Immediate/단기 roadmap section heading (e.g. '## 단기')")
        self.assertIsNotNone(m_med, "Missing Medium/중기 roadmap section heading (e.g. '## 중기')")
        self.assertIsNotNone(m_lng, "Missing Long/장기 roadmap section heading (e.g. '## 장기')")
        pos_imm, pos_med, pos_lng = m_imm.start(), m_med.start(), m_lng.start()
        self.assertTrue(
            pos_imm < pos_med < pos_lng,
            f"Roadmap section headers not sequentially ordered: pos_imm={pos_imm}, pos_med={pos_med}, pos_lng={pos_lng}"
        )
>>>>
```

---

### 3.4 Replacement Snippet 4: Loophole 11 (`FEATURE_PREFIXES`)
**Target File**: `tests/verify_acceptance_criteria.py`  
**Target Lines**: 1169-1178

```python
<<<<
FEATURE_PREFIXES = {
    "F1": ("test_f1_", "test_f1_b", "test_tier3_01", "test_tier3_02"),
    "F2": ("test_f2_", "test_f2_b", "test_tier3_01", "test_tier3_03"),
    "F3": ("test_f3_", "test_f3_b", "test_tier3_04"),
    "F4": ("test_f4_", "test_f4_b", "test_tier3_02", "test_tier3_03", "test_tier3_04", "test_tier3_05"),
    "F5": ("test_f5_", "test_f5_b", "test_tier3_05", "test_tier3_06"),
    "F6": ("test_f6_", "test_f6_b", "test_tier3_06", "test_tier3_07"),
    "F7": ("test_f7_", "test_f7_b", "test_tier3_07"),
}
====
FEATURE_PREFIXES = {
    "F1": ("test_f1_", "test_f1_b", "test_tier3_01", "test_tier3_02", "test_tier4_s02", "test_tier4_s04"),
    "F2": ("test_f2_", "test_f2_b", "test_tier3_01", "test_tier3_03", "test_tier4_s04"),
    "F3": ("test_f3_", "test_f3_b", "test_tier3_04", "test_tier4_s03"),
    "F4": ("test_f4_", "test_f4_b", "test_tier3_02", "test_tier3_03", "test_tier3_04", "test_tier3_05", "test_tier4_s01"),
    "F5": ("test_f5_", "test_f5_b", "test_tier3_05", "test_tier3_06", "test_tier4_s04"),
    "F6": ("test_f6_", "test_f6_b", "test_tier3_06", "test_tier3_07", "test_tier4_s01", "test_tier4_s03", "test_tier4_s05"),
    "F7": ("test_f7_", "test_f7_b", "test_tier3_07", "test_tier4_"),
}
>>>>
```

---

## 4. Empirical Verification Evidence

### 4.1 Positive Verification Results
All four proposed fixes were monkeypatched into `verify_acceptance_criteria.py` and evaluated in memory:
1. **Loophole 8 Resolution**:
   - Tested document citing Mikolov et al. (2013) + contemporary 2026 papers.
   - Result: 0 failures (previously failed with `Detected invalid publication year out of range: [2026, 2025, 2013]`).
2. **Loophole 9 Resolution**:
   - Tested document with intro sentence `"본 문서는 장기적 비전과 중기적 과제, 그리고 단기적 실행 항목을 종합한다"` followed by valid sections `## 1. 단기 과제`, `## 2. 중기 과제`, `## 3. 장기 과제`.
   - Result: 0 failures (previously failed with `pos_lng < pos_imm`).
3. **Loophole 10 Resolution**:
   - Tested document containing display math `$$\nL(N,T)=...\n$$` followed by natural Korean prose with unbalanced brace (`{설명 은`) and inline math `$a=b$`.
   - Result: 0 failures (captured 1 display block + 1 inline block = 2 blocks; Korean text ignored).
4. **Loophole 11 Resolution**:
   - Tested filtered test suite construction for F1..F7:
     - F1: 2 Tier 4 tests (`s02`, `s04`)
     - F2: 1 Tier 4 test (`s04`)
     - F3: 1 Tier 4 test (`s03`)
     - F4: 1 Tier 4 test (`s01`)
     - F5: 1 Tier 4 test (`s04`)
     - F6: 3 Tier 4 tests (`s01`, `s03`, `s05`)
     - F7: 5 Tier 4 tests (`s01`..`s05`)
   - Every single feature now includes its relevant real-world acceptance scenarios.
5. **Baseline Suite Compatibility**:
   - `python3 tests/verify_acceptance_criteria.py --progressive` execution produced:
     `TOTAL: 82 tests, 38 PASS, 0 FAIL, 44 PEND/SKIP, Code 0`. Zero regressions.

### 4.2 Negative Verification Results (Integrity & Protection)
To ensure the fixes do not introduce false positives or loosen necessary constraints:
1. **Hallucinated Future Years**: Literature with year `2035` failed with `Detected invalid publication year out of range` (Expected FAIL).
2. **Missing Contemporary Literature**: Literature with only `2013` and `2019` failed with `Missing contemporary 2025/2026 foundation model literature citations` (Expected FAIL).
3. **Genuinely Inverted Roadmaps**: Roadmaps with `## 장기` preceding `## 단기` failed with `Roadmap section headers not sequentially ordered` (Expected FAIL).
4. **Genuinely Corrupt LaTeX**: Formulas with unmatched braces (e.g. `$$\nL=\frac{1}{2\n$$`) failed with `Unbalanced braces in LaTeX formula` (Expected FAIL).

---

## 5. Instructions for Testing Track Worker

When implementing these fixes in `tests/verify_acceptance_criteria.py`:
1. Open `tests/verify_acceptance_criteria.py`.
2. Apply the four replacement snippets specified in Section 3:
   - Line 678: `test_f3_b01_valid_publication_years`
   - Line 723: `test_f3_b05_latex_math_syntax_validity`
   - Line 829: `test_f5_b05_dependency_ordering_topology`
   - Line 1169: `FEATURE_PREFIXES`
3. Also apply the complementary fixes for Loopholes 1–7 (Honorifics, monotonicity, link anchors, table placeholders) as directed by the other Explorers / Sub-Orchestrator.
4. Execute validation suite:
   ```bash
   # 1. Progressive suite execution
   python3 tests/verify_acceptance_criteria.py --progressive

   # 2. Feature-filtered execution checks
   for feat in F1 F2 F3 F4 F5 F6 F7; do
       python3 tests/verify_acceptance_criteria.py --feature $feat --progressive
   done
   ```
5. Ensure zero regressions across existing milestones.
