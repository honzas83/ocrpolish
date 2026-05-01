from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from ocrpolish.cli import cli
from ocrpolish.models.metadata import MetadataSchema
from ocrpolish.utils.metadata import parse_frontmatter
from tests.unit.test_ollama_client import create_mock_ollama_response


@pytest.fixture
def temp_dirs(tmp_path: Path) -> tuple[Path, Path, Path]:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    vault_root = tmp_path / "vault"
    input_dir.mkdir()
    output_dir.mkdir()
    vault_root.mkdir()

    # Create a dummy markdown file
    md_file = input_dir / "test.md"
    md_file.write_text("This is a test document.")

    return input_dir, output_dir, vault_root


def test_obsidian_metadata_renaming(temp_dirs: tuple[Path, Path, Path]) -> None:
    input_dir, output_dir, _ = temp_dirs
    runner = CliRunner()

    # Mock data with field names from the new schema
    mock_metadata = {
        "title": "Renaming Test",
        "sender": "Sender Name",
        "recipient": "Recipient Name",
        "intent": "Requesting Info",
        "tags": ["#NATO", "#Security"],
    }

    with patch("ollama.Client.chat") as mock_chat:
        mock_chat.return_value = create_mock_ollama_response(
            MetadataSchema(**mock_metadata).model_dump_json()
        )

        result = runner.invoke(cli, ["metadata", str(input_dir), str(output_dir)])
        assert result.exit_code == 0

        output_file = output_dir / "test.md"
        assert output_file.exists()

        content = output_file.read_text()
        metadata, body = parse_frontmatter(content)

        # Verify no prefix
        assert "correspondence_sender" not in metadata
        assert metadata["sender"] == "Sender Name"
        assert metadata["recipient"] == "Recipient Name"
        assert metadata["intent"] == "Requesting Info"

        # Tags should be cleaned and present in the body
        assert "tags" not in metadata
        assert "#NATO #Security" in body


def test_obsidian_metadata_relative_source(temp_dirs: tuple[Path, Path, Path]) -> None:
    input_dir, output_dir, vault_root = temp_dirs
    runner = CliRunner()

    # Place input file deep in vault
    # vault/Notes/Research/test.md
    notes_dir = vault_root / "Notes" / "Research"
    notes_dir.mkdir(parents=True)
    md_file = notes_dir / "test.md"
    md_file.write_text("Content")

    # Assume PDF is in vault/Attachments/test.pdf
    attach_dir = vault_root / "Attachments"
    attach_dir.mkdir()

    mock_metadata = {"title": "Path Test"}

    with patch("ollama.Client.chat") as mock_chat:
        mock_chat.return_value = create_mock_ollama_response(
            MetadataSchema(**mock_metadata).model_dump_json()
        )

        # Run with --vault-root and --pdf-dir
        result = runner.invoke(
            cli,
            [
                "metadata",
                str(notes_dir),
                str(output_dir),
                "--vault-root",
                str(vault_root),
                "--pdf-dir",
                str(attach_dir),
            ],
        )
        assert result.exit_code == 0

        output_file = output_dir / "test.md"
        assert output_file.exists()

        content = output_file.read_text()
        metadata, _ = parse_frontmatter(content)

        # Expected relative path from vault root to PDF is Attachments/test.pdf
        assert metadata["source"] == "[[Attachments/test.pdf]]"


def test_obsidian_metadata_tags(temp_dirs: tuple[Path, Path, Path]) -> None:
    input_dir, output_dir, _ = temp_dirs
    runner = CliRunner()

    mock_metadata = {"title": "Tag Test", "tags": ["#NATO", " #Security ", "Cold War"]}

    with patch("ollama.Client.chat") as mock_chat:
        mock_chat.return_value = create_mock_ollama_response(
            MetadataSchema(**mock_metadata).model_dump_json()
        )

        result = runner.invoke(cli, ["metadata", str(input_dir), str(output_dir)])
        assert result.exit_code == 0

        output_file = output_dir / "test.md"
        content = output_file.read_text()
        metadata, body = parse_frontmatter(content)

        # Tags should not be in frontmatter
        assert "tags" not in metadata
        # Tags should be in body callout: ["#NATO", "#Security", "#ColdWar"]
        assert "#NATO #Security #ColdWar" in body


def test_obsidian_metadata_entities(temp_dirs: tuple[Path, Path, Path]) -> None:
    input_dir, output_dir, _ = temp_dirs
    runner = CliRunner()

    mock_metadata = {
        "title": "Entity Test",
        "mentioned_states": ["United Kingdom", "United States"],
        "mentioned_organisations": ["NATO"],
        "mentioned_cities": ["London, United Kingdom", "Washington, United States"],
        "location_state": "Germany"
    }

    with patch("ollama.Client.chat") as mock_chat:
        mock_chat.return_value = create_mock_ollama_response(
            MetadataSchema(**mock_metadata).model_dump_json()
        )

        result = runner.invoke(cli, ["metadata", str(input_dir), str(output_dir)])
        assert result.exit_code == 0

        output_file = output_dir / "test.md"
        content = output_file.read_text()
        metadata, body = parse_frontmatter(content)

        # Excluded from frontmatter
        assert "mentioned_states" not in metadata
        assert "mentioned_organisations" not in metadata
        assert "mentioned_cities" not in metadata

        # Present in body callout
        assert "## Mentioned Entities" in body
        assert "#State/United-Kingdom" in body
        assert "#State/United-States" in body
        assert "#Org/NATO" in body
        # Should NOT use location_state (Germany) but the state provided in the city string
        assert "#City/United-Kingdom/London" in body
        assert "#City/United-States/Washington" in body
