import os
import yaml


def test_source_groups_have_nav_titles():
    """Test that all source groups have nav_title defined"""
    with open("example/mkdocs.yml", "r") as f:
        config = yaml.safe_load(f)

    sources = config["plugins"][1]["cdoc"]["sources"]

    for source in sources:
        assert "nav_title" in source, f"Source {source.get('root')} is missing nav_title"


def test_source_groups_have_output_dirs():
    """Test that all source groups have output_dir defined"""
    with open("example/mkdocs.yml", "r") as f:
        config = yaml.safe_load(f)

    sources = config["plugins"][1]["cdoc"]["sources"]

    for source in sources:
        assert "output_dir" in source, f"Source {source.get('root')} is missing output_dir"


def test_source_directories_exist():
    """Test that all source directories actually exist on disk"""
    with open("example/mkdocs.yml", "r") as f:
        config = yaml.safe_load(f)

    sources = config["plugins"][1]["cdoc"]["sources"]

    for source in sources:
        path = os.path.join("example", source["root"])
        assert os.path.isdir(path), f"Source directory {path} does not exist"


def test_output_directories_created():
    """Test that each source group creates its own output directory after build"""
    expected_dirs = ["core", "drivers", "lib", "tests"]

    for dir_name in expected_dirs:
        path = os.path.join("example", "site", "api", dir_name)
        assert os.path.isdir(path), f"Output directory {path} was not created"


def test_cross_references_exist_in_html():
    """Test that cross-references between groups exist in generated HTML"""
    core_index = os.path.join("example", "site", "api", "core", "index.html")

    assert os.path.exists(core_index), "Core API index.html not found"

    with open(core_index, "r") as f:
        content = f.read()

    assert "api/drivers" in content or "api/lib" in content, \
        "No cross-references to other groups found in Core API index"