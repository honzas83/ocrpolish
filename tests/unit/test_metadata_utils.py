from ocrpolish.utils.metadata import parse_frontmatter, prepend_frontmatter, stringify_frontmatter


def test_parse_frontmatter_valid():
    content = "---\ntitle: Test\nauthor: John\n---\nBody content"
    metadata, body = parse_frontmatter(content)
    assert metadata == {"title": "Test", "author": "John"}
    assert body == "Body content"

def test_parse_frontmatter_no_frontmatter():
    content = "Just content"
    metadata, body = parse_frontmatter(content)
    assert metadata == {}
    assert body == "Just content"

def test_parse_frontmatter_malformed():
    content = "---\ntitle: Test\nBody content" # Missing closing ---
    metadata, body = parse_frontmatter(content)
    assert metadata == {}
    assert body == content

def test_stringify_frontmatter():
    metadata = {"title": "Test", "author": "John"}
    yaml_str = stringify_frontmatter(metadata)
    assert "---\ntitle: Test\nauthor: John\n---\n" in yaml_str

def test_prepend_frontmatter():
    content = "Existing content"
    metadata = {"title": "New"}
    result = prepend_frontmatter(content, metadata)
    assert result.startswith("---\ntitle: New\n---\n")
    assert "Existing content" in result

def test_prepend_frontmatter_merge():
    content = "---\ntitle: Old\n---\nBody"
    metadata = {"author": "New"}
    result = prepend_frontmatter(content, metadata)
    assert "title: Old" in result
    assert "author: New" in result
    assert "Body" in result
