from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ocrpolish.processor import FrequencyStore


FREQUENCY_THRESHOLD = 5


def scan_files(input_dir: Path, mask: str = "*.md") -> Iterator[Path]:
    """Recursively scan input_dir for files matching the mask."""
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    return input_dir.rglob(mask)


def get_output_path(input_file: Path, input_dir: Path, output_dir: Path) -> Path:
    """Calculate the mirrored output path for a given input file."""
    relative_path = input_file.relative_to(input_dir)
    return output_dir / relative_path


def ensure_directory_exists(path: Path) -> None:
    """Ensure the directory for the given path exists."""
    path.parent.mkdir(parents=True, exist_ok=True)


def get_filtered_path(output_path: Path) -> Path:
    """Calculate the sidecar .filtered.md path for a given output path."""
    return output_path.with_suffix(output_path.suffix + ".filtered.md")


def generate_frequency_report(report_path: Path, store: "FrequencyStore") -> None:
    """Write the consolidated frequency report to the specified path."""
    # Filter entries with total_count > FREQUENCY_THRESHOLD and sort by total_count descending
    entries = [
        entry for entry in store.patterns.values() if entry.total_count > FREQUENCY_THRESHOLD
    ]
    entries.sort(key=lambda x: x.total_count, reverse=True)

    ensure_directory_exists(report_path)
    with open(report_path, "w", encoding="utf-8") as f:
        for entry in entries:
            line = f"{entry.total_count} ({entry.file_count}): {entry.most_frequent_verbatim}\n"
            f.write(line)
