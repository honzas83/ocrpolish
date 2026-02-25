# Quickstart: Rework Filtering and Wrapping

The `ocrpolish` tool now provides more powerful filtering and improved output formatting for OCR text.

## Core Features

1. **Boilerplate Identification**: See a list of all recurring lines across your documents.
2. **Customizable Filtering**: Provide a file containing lines you want to exclude.
3. **Improved Wrapping**: Lists and bullets are wrapped to your target width, with clean paragraph separation.

## Basic Usage

Run `ocrpolish` as usual to process your documents:

```bash
ocrpolish ./data/raw ./data/processed
```

By default, this will:
1. Generate `data/processed/frequency.txt` with a list of all repetitive lines.
2. Remove default classification stamps.
3. Wrap all paragraphs, lists, and bullets to 80 characters.
4. Add blank lines between blocks.

## Custom Filtering

1. **Review the Frequency Report**: Open `data/processed/frequency.txt` to find common boilerplate like headers or footers.
2. **Create a Filter File**: Copy the lines you want to remove into a text file (e.g., `my_filters.txt`).
3. **Apply the Filter**:

```bash
ocrpolish ./data/raw ./data/processed --filter-file my_filters.txt
```

### Example Filter File Content

```text
ANNEX A
APPENDIX 1
PAGE 1
NATO SECRET
```

## Advanced Options

| Feature | Option | Description |
|---------|--------|-------------|
| **Target Width** | `--width 100` | Wrap text to 100 characters instead of 80. |
| **Output File** | `--frequency-file report.txt` | Save the frequency list to a different file name. |
| **Audit Filtered** | `--no-filtered` | Disable generation of the `.filtered.md` sidecar files if not needed. |
