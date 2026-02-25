from pathlib import Path

from docx import Document
from docx.shared import Pt

from ocrpolish.utils.docx_utils import (
    calculate_font_size,
    create_docx_from_pages,
    split_markdown_by_pages,
)


def test_split_markdown_by_pages_removes_markers() -> None:
    content = "# Page 1\nContent 1\n---\n# Page 2\nContent 2\n---\nContent 3"
    pages = split_markdown_by_pages(content)
    expected_pages = 3
    assert len(pages) == expected_pages
    for page in pages:
        body = "\n".join(page.body_lines)
        assert "---" not in body
        assert "# Page" not in body
    assert pages[0].body_lines[0] == "Content 1"
    assert pages[1].body_lines[0] == "Content 2"
    assert pages[2].body_lines[0] == "Content 3"


def test_split_markdown_by_pages_filters_empty() -> None:
    content = "Content 1\n---\n---\nContent 2"
    pages = split_markdown_by_pages(content)
    expected_pages = 2
    assert len(pages) == expected_pages
    assert pages[0].body_lines[0] == "Content 1"
    assert pages[1].body_lines[0] == "Content 2"


def test_calculate_font_size() -> None:
    # Under limit
    text_short = "Line\n" * 10
    expected_base = 10.0
    assert calculate_font_size(text_short, base_size=10, max_lines=50) == expected_base

    # Over limit
    text_long = "Line\n" * 100
    # 50 / 100 * 10 = 5.0, but capped at 6.0
    expected_min = 6.0
    assert calculate_font_size(text_long, base_size=10, max_lines=50) == expected_min

    # Mid range
    text_mid = "Line\n" * 80
    # 50 / 80 * 10 = 6.25
    expected_mid = 6.25
    assert calculate_font_size(text_mid, base_size=10, max_lines=50) == expected_mid


def test_create_docx_scaling(tmp_path: Path) -> None:
    # One short page (1 line), one very long page (100 lines)
    pages_content = ["Short page", "Long\n" * 100]
    pages = [p for c in pages_content for p in split_markdown_by_pages(c)]
    output_path = tmp_path / "scale_test.docx"
    create_docx_from_pages(pages, output_path)

    doc = Document(str(output_path))
    # We expect 2 paragraphs now (one per page) because lines are grouped
    expected_paras = 2
    assert len(doc.paragraphs) == expected_paras

    # First page should be 10pt (first paragraph)
    assert doc.paragraphs[0].runs[0].font.size == Pt(10)
    # Second page should be 6.5pt
    expected_scaled = 6.5
    assert doc.paragraphs[1].runs[0].font.size == Pt(expected_scaled)


def test_native_table_generation(tmp_path: Path) -> None:
    content = ["Header 1 | Header 2", "--- | ---", "Row 1 Col 1 | Row 1 Col 2"]
    pages = split_markdown_by_pages("\n".join(content))
    output_path = tmp_path / "table_test.docx"
    create_docx_from_pages(pages, output_path)

    assert output_path.exists()
    doc = Document(str(output_path))

    # Verify a table was created
    assert len(doc.tables) == 1
    table = doc.tables[0]
    expected_rows = 2
    expected_cols = 2
    assert len(table.rows) == expected_rows
    assert len(table.columns) == expected_cols

    # Check content
    assert table.cell(0, 0).text == "Header 1"
    assert table.cell(1, 1).text == "Row 1 Col 2"

    # Check styling (Consolas)
    assert table.cell(0, 0).paragraphs[0].runs[0].font.name == "Consolas"
