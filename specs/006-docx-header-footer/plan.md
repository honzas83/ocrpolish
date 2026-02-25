# Implementation Plan: Dynamic Headers and Footers for DOCX

**Branch**: `006-docx-header-footer` | **Date**: 2026-02-25 | **Spec**: [specs/006-docx-header-footer/spec.md]
**Input**: Feature specification from `/specs/006-docx-header-footer/spec.md`

## Summary

The goal is to automatically extract page numbers and recurring headers/footers from processed OCR Markdown files and move them into the official metadata of generated DOCX files. This involves a two-pass analysis of each file: first to identify recurring text (80% threshold) and extract page numbers, and second to generate the DOCX while omitting these from the body and injecting them into the header/footer.

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**: `python-docx`, `re`, `collections.Counter`  
**Storage**: Filesystem (input/output directories)  
**Testing**: pytest, coverage  
**Target Platform**: CLI  
**Project Type**: Single project  
**Performance Goals**: <5% overhead on total generation time.  
**Constraints**: 80% threshold for repeated strings, exact matching.

## Constitution Check

- **Principle I (Quality)**: New logic will be covered by unit and integration tests.
- **Principle II (CLI)**: Enhanced `--docx` functionality and added `--scan-paragraphs`.
- **Principle V (Atomic Git)**: Implementation will be broken into independent tasks.

## Project Structure

### Documentation (this feature)

```text
specs/006-docx-header-footer/
├── plan.md              # This file
├── research.md          # Analysis strategy and decisions
├── data-model.md        # Entities for page metadata
├── quickstart.md        # Usage guide
└── contracts/           
    └── cli.md           # CLI changes
```

### Source Code (repository root)

```text
ocrpolish/
├── cli.py               # Add --scan-paragraphs
├── data_model.py        # Add scan_paragraphs to ProcessingConfig
├── utils/
    └── docx_utils.py    # (UPDATED) Implement two-pass analysis and injection
    └── metadata.py      # (NEW) Encapsulate pattern matching and counting logic

tests/
├── unit/
    └── test_metadata.py # (NEW) Test pattern extraction and threshold logic
├── integration/
    └── test_docx_metadata.py # (NEW) Test end-to-end extraction to DOCX
```

**Structure Decision**: Added `ocrpolish/utils/metadata.py` to keep extraction logic separate from Word generation code.

## Complexity Tracking

*No violations identified.*
