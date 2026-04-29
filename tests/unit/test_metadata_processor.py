from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from ocrpolish.processor_metadata import MetadataProcessor


@pytest.fixture
def mock_ollama() -> MagicMock:
    return MagicMock()


@pytest.fixture
def processor(mock_ollama: MagicMock, tmp_path: Path) -> MetadataProcessor:
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return MetadataProcessor(mock_ollama, output_dir)


def test_prepare_obsidian_metadata_removes_empty_fields(processor: Any) -> None:
    raw_dict: dict[str, Any] = {
        "title": "Test Title",
        "summary": "One sentence.",
        "author_name": "",
        "date": None,
        "tags": [],
        "language": "English",
    }
    input_file = Path("test.md")

    # We need to mock _get_pdf_link because it's called in _prepare_obsidian_metadata
    processor._get_pdf_link = MagicMock(return_value="[[test.pdf]]")

    metadata = processor._prepare_obsidian_metadata(raw_dict, input_file)

    assert "title" in metadata
    assert "summary" in metadata
    assert "language" in metadata
    assert "source" in metadata  # Added by the processor

    # Empty/None/Empty list should be removed
    assert "author_name" not in metadata
    assert "date" not in metadata
    assert "tags" not in metadata


def test_prepare_obsidian_metadata_renames_correspondence(processor: Any) -> None:
    raw_dict: dict[str, Any] = {
        "title": "Letter",
        "correspondence_sender": "Alice",
        "correspondence_recipient": "Bob",
    }
    input_file = Path("letter.md")
    processor._get_pdf_link = MagicMock(return_value="[[letter.pdf]]")

    metadata = processor._prepare_obsidian_metadata(raw_dict, input_file)

    assert "sender" in metadata
    assert metadata["sender"] == "Alice"
    assert "recipient" in metadata
    assert metadata["recipient"] == "Bob"
    assert "correspondence_sender" not in metadata


def test_process_file_body_structure(processor: Any, tmp_path: Path) -> None:
    input_file = tmp_path / "input.md"
    input_file.write_text("Original content")
    output_file = tmp_path / "output.md"

    # Mock Ollama response
    mock_metadata = MagicMock()
    mock_metadata.title = "The Title"
    mock_metadata.abstract = "The Abstract."
    mock_metadata.summary = "The Summary."
    mock_metadata.tags = ["tag1"]
    mock_metadata.model_dump.return_value = {
        "title": "The Title",
        "abstract": "The Abstract.",
        "summary": "The Summary.",
        "tags": ["tag1"],
    }
    processor.client.extract_structured.return_value = mock_metadata

    # Mock _get_pdf_link
    processor._get_pdf_link = MagicMock(return_value="[[source.pdf]]")

    processor.process_file(input_file, output_file)

    assert output_file.exists()
    content = output_file.read_text()

    # Check frontmatter (should have title and summary, but NOT abstract)
    assert "title: The Title" in content
    assert "abstract: " not in content
    assert "summary: The Summary." in content

    # Check body structure (inside callout)
    assert "> [!abstract]" in content
    assert "> # The Title" in content
    assert "> The Abstract." in content
    assert "Original content" in content

    # Verify order
    lines = content.splitlines()
    callout_idx = next(i for i, line in enumerate(lines) if "> [!abstract]" in line)
    title_idx = next(i for i, line in enumerate(lines) if "> # The Title" in line)
    abstract_idx = next(i for i, line in enumerate(lines) if "> The Abstract." in line)
    body_idx = next(i for i, line in enumerate(lines) if "Original content" in line)

    assert callout_idx < title_idx < abstract_idx < body_idx
