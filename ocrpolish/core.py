from pathlib import Path
from ocrpolish.data_model import ProcessingConfig
from ocrpolish.processor import FrequencyStore, load_filter_list, filter_lines, wrap_lines, format_blocks
from ocrpolish.utils.files import (
    ensure_directory_exists,
    generate_frequency_report,
    get_filtered_path,
    get_output_path,
    scan_files,
)
from ocrpolish.utils.logging import get_logger


def run_processing(config: ProcessingConfig) -> None:
    """Coordinate the OCR post-processing."""
    logger = get_logger()

    # Load filter list
    filter_list = load_filter_list(config.filter_file_path)
    if filter_list:
        logger.info(f"Loaded {len(filter_list)} filter patterns from {config.filter_file_path}")
    else:
        logger.info("No filter file provided or file empty. Proceeding without filtering.")

    freq_store = FrequencyStore()
    files = list(scan_files(config.input_dir, config.input_mask))

    logger.info(f"Processing {len(files)} files...")

    for input_file in files:
        output_path = get_output_path(input_file, config.input_dir, config.output_dir)

        with open(input_file, encoding="utf-8") as f:
            lines = f.readlines()

        # 1. Filter lines
        filtered_lines, dropped = filter_lines(lines, filter_list)

        # 2. Accumulate frequencies for KEPT lines
        for line in filtered_lines:
            freq_store.update(line, input_file)

        # 3. Wrap and format kept lines
        if not filtered_lines:
            cleaned = []
        else:
            blocks = wrap_lines(filtered_lines, config)
            cleaned = format_blocks(blocks)

        # 4. Save primary output
        if not config.dry_run:
            ensure_directory_exists(output_path)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(cleaned) + "\n")
            logger.debug(f"Processed {input_file} -> {output_path}")

        # 5. Save sidecar filtered lines
        if config.save_filtered and dropped:
            filtered_path = get_filtered_path(output_path)
            ensure_directory_exists(filtered_path)
            with open(filtered_path, "w", encoding="utf-8") as f:
                f.write("\n".join(dropped) + "\n")
            logger.debug(f"Saved filtered lines to {filtered_path}")

    # Pass 2: Generation of Frequency Report (AFTER all processing)
    logger.info("Generating consolidated frequency report...")
    report_path = config.frequency_file_path
    if not report_path.parents or report_path.parent == Path("."):
        report_path = config.output_dir / report_path

    generate_frequency_report(report_path, freq_store)
    logger.info(f"Frequency report saved to {report_path}")

    logger.info("Processing complete")
