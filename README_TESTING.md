# QA Testing - Area 5: Multi-Source Groups & Navigation

## About This Project
This repository is a fork of [mkdocs-cdoc](https://github.com/pawelsikora/mkdocs-cdoc), 
a MkDocs plugin that generates API documentation from C/C++ source code comments.

As part of my Software Testing course at WSB Merito University, I was assigned 
to test Area 5: Multi-Source Groups & Navigation.

## What I Tested
The plugin supports multiple source directories, each generating a separate 
navigation section. I tested whether this feature works correctly by verifying:

- Navigation sections are generated correctly for each source group
- Extension filters include only the correct file types
- nav_title configuration reflects correctly in the output
- Output directories are created as configured
- Cross-references between groups exist in generated HTML

## Test Results
See [tests/test_results.md](tests/test_results.md) for full manual and automated test results.

## Automated Tests
```bash
pytest tests/test_navigation.py -v
```

## Static Analysis
```bash
flake8 mkdocs_cdoc/ --count --statistics
pylint mkdocs_cdoc/
mypy mkdocs_cdoc/ --ignore-missing-imports
```

## Key Findings
- TC-001 to TC-004: PASS
- TC-005: FAIL - No cross-references between source groups found in generated HTML
- Static analysis score: 9.77/10 (pylint)
- Observation: PyCharm file watcher inconsistency with mkdocs serve