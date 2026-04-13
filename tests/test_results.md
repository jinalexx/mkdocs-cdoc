# Area 5: Multi-Source Groups & Navigation - Test Results

## TC-001: Multiple source groups generate separate navigation sections

**What we tested and why:** The plugin is configured with 4 source groups in mkdocs.yml. We wanted to verify that each group appears as a separate section in the navigation menu. This is the core feature of Area 5 — if groups do not appear separately, the entire multi-source functionality is broken.

**Preconditions:** Plugin installed, mkdocs serve running, 4 source groups defined in mkdocs.yml

**Steps:**
1. Open http://127.0.0.1:8000 in browser
2. Click on API Reference menu
3. Check the dropdown sections

**Expected Result:** Core API, Driver API, Library API, Test API appear as separate sections

**Actual Result:** All 4 groups (Core API, Driver API, Library API, Test API) appeared correctly as separate navigation sections

**Status:** PASS

---

## TC-002: Extension filter excludes non-matching file types

**What we tested and why:** The src/drivers group is configured with extensions: [".c"], meaning only .c files should be included. We wanted to verify that if a .h file is added to that folder, the plugin correctly ignores it. This is important because including wrong file types could pollute the documentation with unintended content.

**Preconditions:** mkdocs serve running, src/drivers configured with extensions: [".c"]

**Steps:**
1. Add a .h file (test_driver.h) to src/drivers folder
2. Restart mkdocs serve
3. Navigate to Driver API section in browser

**Expected Result:** test_driver.h should NOT appear in Driver API navigation

**Actual Result:** test_driver.h was not shown in Driver API section, only spi.c and uart.c were visible

**Status:** PASS

---

## TC-003: nav_title configuration reflects correctly in navigation

**What we tested and why:** Each source group has a nav_title value in mkdocs.yml which defines how it appears in the navigation menu. We wanted to verify that changing this value is correctly reflected in the browser. This ensures that teams can customize their documentation structure as needed.

**Preconditions:** mkdocs serve running, nav_title set to "Core API" in mkdocs.yml

**Steps:**
1. Change nav_title value from "Core API" to "Core API Modified" in mkdocs.yml
2. Restart mkdocs serve
3. Check navigation in browser

**Expected Result:** Navigation section title should update to "Core API Modified"

**Actual Result:** Navigation updated correctly to show "Core API Modified"

**Status:** PASS

---

## TC-004: Output directories created for each source group

**What we tested and why:** The plugin is configured with 4 source groups, each with a different output_dir value. We wanted to verify that after building the site, each group creates its own separate folder. This is important because if two groups write to the same folder, files could overwrite each other and documentation would be incomplete or incorrect.

**How mkdocs build works:** Unlike mkdocs serve which only displays the site temporarily in the browser without saving files to disk, mkdocs build generates real HTML, CSS and JavaScript files and saves them to the example/site/ folder. This allowed us to read the generated files programmatically with pytest and verify the output directory structure.

**Preconditions:** mkdocs build completed successfully, 4 source groups configured in mkdocs.yml with output_dir values: api/core, api/drivers, api/lib, api/tests

**Steps:**
1. Run mkdocs build to generate the static site files
2. Navigate to example/site/api/ directory
3. Check if all 4 expected output directories exist

**Expected Result:** Directories core, drivers, lib, and tests should all exist under site/api/

**Actual Result:** All 4 output directories were created correctly and matched the output_dir values defined in mkdocs.yml

**Status:** PASS

---

## TC-005: Cross-references between source groups exist in generated HTML

**What we tested and why:** The plugin generates documentation from 4 separate source groups. We wanted to verify that pages in one group contain hyperlinks pointing to related pages in other groups. This is important because without cross-references, a developer reading Core API documentation cannot easily navigate to related Driver API or Library API pages. It makes the documentation harder to use.

**How we tested it:** We opened the generated HTML files for Core API pages and searched for any hyperlinks containing "api/drivers", "api/lib" or "api/tests" in their href attribute. We checked both the group index page and individual source file pages.

**Preconditions:** mkdocs build completed successfully

**Steps:**
1. Run mkdocs build to generate static HTML files
2. Open site/api/core/index.html
3. Search for hyperlinks pointing to other groups
4. Open site/api/core/engine.c/index.html
5. Repeat the search

**Expected Result:** Generated HTML pages should contain hyperlinks referencing pages from other source groups

**Actual Result:** No cross-group hyperlinks found in any Core API pages. Only a self-referencing anchor link was present (href="#core-api")

**Status:** FAIL

**Notes:** Cross-references between groups may only appear when explicitly defined using role syntax in source code comments such as :func: or :struct:. This is not done in the example project, which may explain the absence of cross-group links. Further investigation needed.

---

## Automated Tests - pytest

**File:** tests/test_navigation.py

**What was tested and why:** We wrote automated tests to verify the configuration and structure of the plugin without manually checking every file. Automated tests are repeatable and can be run any time the code changes to catch regressions.

- **test_source_groups_have_nav_titles:** Verifies that every source group in mkdocs.yml has a nav_title defined. If someone accidentally removes a nav_title, this test will catch it.
- **test_source_groups_have_output_dirs:** Verifies that every source group has an output_dir defined. Without output_dir, the plugin does not know where to write generated files.
- **test_source_directories_exist:** Verifies that all source directories referenced in mkdocs.yml actually exist on disk. If a directory is renamed or deleted but mkdocs.yml is not updated, this test will fail.
- **test_output_directories_created:** Verifies that after running mkdocs build, all 4 expected output directories exist under site/api/.
- **test_cross_references_exist_in_html:** Checks whether Core API pages contain hyperlinks to other source groups in the generated HTML.

**Results:**
- test_source_groups_have_nav_titles: PASS
- test_source_groups_have_output_dirs: PASS
- test_source_directories_exist: PASS
- test_output_directories_created: PASS
- test_cross_references_exist_in_html: FAIL

**Total: 4 passed, 1 failed**

---

## Observation: File watcher inconsistency with PyCharm

**Description:** When mkdocs.yml was modified and saved via PyCharm (Cmd+S), mkdocs serve did not detect the change and did not rebuild. The change was only detected when the file was modified directly via terminal using the sed command.

**Possible cause:** PyCharm saves files using a temporary file + rename approach, which may not trigger mkdocs file watcher correctly. Direct file modification via terminal triggers the watcher as expected.

**Impact:** Developers or testers using PyCharm may not see live updates when editing mkdocs.yml, leading to confusion during testing.

**Severity:** Minor

---

## Static Analysis

**What we tested and why:** Static analysis examines source code without executing it, identifying potential bugs, code quality issues, and style violations before they cause real problems at runtime. We ran three industry-standard tools on the plugin source code.

### flake8 - Style and Convention Checking
**Command:** flake8 mkdocs_cdoc/ --count --statistics
**Result:** 0 issues found
**Interpretation:** The codebase fully complies with Python style conventions. No formatting or style violations detected.

### pylint - Code Quality Analysis
**Command:** pylint mkdocs_cdoc/
**Score:** 9.77/10
**Most significant findings:**

1. **parser.py line 238 - Too many branches (67/12):** A single function contains 67 decision points. This is extremely complex and difficult to maintain. If a bug exists here, it will be very hard to find and fix.

2. **plugin.py line 870 - File opened without encoding:** When opening files without specifying encoding, the plugin may behave differently on Windows vs Mac/Linux machines. This could cause unexpected characters or crashes on some systems.

3. **plugin.py lines 1474, 1551 - Unused variables:** Variables are declared but never used. This is dead code that adds confusion without any benefit.

4. **plugin.py line 1588, 1602 - Catching too general exception:** The code catches all exceptions without distinction. This can hide real bugs because even unexpected errors are silently swallowed.

**Interpretation:** Despite a high score, the complexity issues in parser.py represent a maintainability risk. The more branches a function has, the harder it is to test all possible paths.

### mypy - Type Checking
**Command:** mypy mkdocs_cdoc/ --ignore-missing-imports
**Result:** No issues found in 5 source files
**Interpretation:** All function signatures and variable types are consistent. No type-related bugs detected.

### Summary
| Tool | Issues Found | Score |
|------|-------------|-------|
| flake8 | 0 | Clean |
| pylint | 48 warnings | 9.77/10 |
| mypy | 0 | Clean |