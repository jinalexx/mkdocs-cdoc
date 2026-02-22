# Live Demo

The mkdocs-cdoc repository includes a working example project under `example/` that demonstrates the plugin's features with sample C source files.

## What the example covers

The example project has four source groups:

- **Core API** (`src/core/`) — `engine.h` and `engine.c` with function signatures, structs, enums, and cross-references
- **Driver API** (`src/drivers/`) — `spi.c` and `uart.c` showing multi-file groups
- **Library API** (`src/lib/`) — `igt_aux.c` and `igt_core.c` demonstrating reST doc comment parsing
- **Test API** (`src/tests/`) — five IGT-style test files with `TEST:` / `SUBTEST:` metadata, "By Category" / "By Functionality" index pages

## Configuration

The example `mkdocs.yml`:

```yaml
site_name: My Project Docs

nav:
  - Home: index.md

plugins:
  - search
  - cdoc:
      project_name: My Project
      version_file: version.json

      custom_index_pages:
        - docs/api_ref.md

      sources:
        - root: src/core
          nav_title: Core API
          output_dir: api/core
          custom_index_pages:
            - docs/api-intro.md

        - root: src/drivers
          nav_title: Driver API
          output_dir: api/drivers
          extensions: [".c"]
          custom_index_pages:
            - docs/driver-intro.md

        - root: src/lib
          nav_title: Library API
          output_dir: api/lib

        - root: src/tests
          nav_title: Test API
          output_dir: api/tests
          extensions: [".c"]
          igt:
            group_by: [category, mega_feature, sub_category, functionality]

      convert_rst: true
      convert_gtkdoc: true
      appendix_code_usages: true
```

## Build it yourself

```bash
git clone https://github.com/pawelsikora/mkdocs-cdoc.git
cd mkdocs-cdoc
pip install -e .
cd example
mkdocs serve
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) to browse the generated documentation.

## Browse online

The example is built automatically by CI and deployed alongside this documentation. You can browse it at:

**[Live Example →](../../example-site/index.html)**
