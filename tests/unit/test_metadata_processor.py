from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from ocrpolish.processor_metadata import MetadataProcessor
from ocrpolish.utils.metadata import parse_frontmatter


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


def test_prepare_obsidian_metadata_field_order_and_exclusion(processor: Any) -> None:
    raw_dict: dict[str, Any] = {
        "title": "Document Title",
        "summary": "This is a summary.",
        "sender": "Alice",
        "recipient": "Bob",
        "intent": "Some action",
        "mentioned_states": ["UK"],
        "mentioned_organisations": ["NATO"],
        "mentioned_cities": ["London"],
        "date": "2024-04-30",
        "author_name": "Author",
        "pages": 10,  # Manually added before calling _prepare
    }
    input_file = Path("doc.md")
    processor._get_pdf_link = MagicMock(return_value="[[doc.pdf]]")

    metadata = processor._prepare_obsidian_metadata(raw_dict, input_file)

    # Check for renaming and presence
    assert "intent" in metadata
    assert metadata["intent"] == "Some action"
    assert "pages" in metadata
    
    # Check for exclusion of mentioned_*
    assert "mentioned_states" not in metadata
    assert "mentioned_organisations" not in metadata
    assert "mentioned_cities" not in metadata

    # Check for order (summary, pages, sender, recipient, intent)
    keys = list(metadata.keys())
    # title is first in primary_keys
    assert keys[0] == "title"
    assert keys[1] == "summary"
    assert keys[2] == "pages"
    assert keys[3] == "sender"
    assert keys[4] == "recipient"
    assert keys[5] == "intent"


def test_process_file_english_consistency(processor: Any, tmp_path: Path) -> None:
    input_file = tmp_path / "french.md"
    # Even if content is French, prompt mandates English
    input_file.write_text("C'est un document en français.")
    output_file = tmp_path / "output.md"

    # Mock Ollama response (simulating LLM following English instruction)
    mock_metadata = MagicMock()
    mock_metadata.title = "French Document"
    mock_metadata.summary = "This is a document in French."
    mock_metadata.mentioned_cities = ["Paris"]
    mock_metadata.mentioned_states = ["France"]
    mock_metadata.language = "English"  # Mandated English
    mock_metadata.model_dump.return_value = {
        "title": "French Document",
        "summary": "This is a document in French.",
        "mentioned_cities": ["Paris"],
        "mentioned_states": ["France"],
        "language": "English",
    }
    processor.client.extract_structured.return_value = mock_metadata
    processor._get_pdf_link = MagicMock(return_value="[[french.pdf]]")

    processor.process_file(input_file, output_file)

    content = output_file.read_text()
    metadata, body = parse_frontmatter(content)

    assert metadata["title"] == "French Document"
    assert metadata["language"] == "English"
    # Tag should use "City" (English) and "France" (English)
    assert "#City/France/Paris" in body
