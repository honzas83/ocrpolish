from pathlib import Path

from ocrpolish.core import run_processing
from ocrpolish.data_model import ProcessingConfig


def test_sidecar_output_integration(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()

    bp = "BOILERPLATE LINE"
    (input_dir / "doc1.md").write_text(f"{bp}\n\nContent 1")
    (input_dir / "doc2.md").write_text(f"{bp}\n\nContent 2")

    # Create filter file
    filter_file = tmp_path / "filters.txt"
    filter_file.write_text(f"{bp}\n")

    config = ProcessingConfig(
        input_dir=input_dir, output_dir=output_dir, save_filtered=True, filter_file_path=filter_file
    )

    run_processing(config)

    filtered1 = output_dir / "doc1.md.filtered.md"
    assert filtered1.exists()
    assert bp in filtered1.read_text()
