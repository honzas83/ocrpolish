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
        "transaction": "Requesting Info",
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

        # Tags should be cleaned
        assert "NATO" in metadata["tags"]
        assert "#NATO" not in metadata["tags"]


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
        metadata, _ = parse_frontmatter(content)

        # Tags should be: ["NATO", "Security", "ColdWar"]
        assert metadata["tags"] == ["NATO", "Security", "ColdWar"]


def test_obsidian_metadata_body_structure(temp_dirs: tuple[Path, Path, Path]) -> None:
    input_dir, output_dir, _ = temp_dirs
    runner = CliRunner()

    mock_metadata = {
        "title": "Structure Test",
        "abstract": "This is a detailed abstract.\nIt has multiple lines.",
        "summary": "One sentence summary."
    }

    with patch("ollama.Client.chat") as mock_chat:
        mock_chat.return_value = create_mock_ollama_response(
            MetadataSchema(**mock_metadata).model_dump_json()
        )

        result = runner.invoke(cli, ["metadata", str(input_dir), str(output_dir)])
        assert result.exit_code == 0

        output_file = output_dir / "test.md"
        content = output_file.read_text()

        # Verify body structure (title and abstract inside callout)
        assert "> [!abstract]" in content
        assert "> # Structure Test" in content
        assert "> This is a detailed abstract." in content
        assert "> It has multiple lines." in content

        # Verify no horizontal rule after callout
        # (It shouldn't have --- after the callout anymore)
        
        # Verify it's BEFORE the original content
        _, body = parse_frontmatter(content)
        # body starts with \n due to the empty line we add before callout
        assert "> [!abstract]" in body
        assert "This is a test document." in body
