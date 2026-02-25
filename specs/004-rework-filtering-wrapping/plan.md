# Implementation Plan: Rework Filtering and Wrapping

**Branch**: `004-rework-filtering-wrapping` | **Date**: 2026-02-25 | **Spec**: [specs/004-rework-filtering-wrapping/spec.md](spec.md)
**Input**: Feature specification from `/specs/004-rework-filtering-wrapping/spec.md`

## Summary

The objective is to replace the current hardcoded filtering logic with a flexible, data-driven system. This includes generating a consolidated frequency report for repetitive lines across all documents (TotalCount > 5) and implementing a customizable filter file. The text wrapping logic will be refined to ensure proper paragraph separation and support for wrapping lists and bullets, with specific rules for blank line placement after wrapped items.

Technical approach:
1. **Normalization**: Use a "set of words" approach (lowercase, no diacritics, punctuation removed) to identify identical content.
2. **Frequency Counting**: Track total occurrences and file occurrences of these normalized keys.
3. **Filtering**: Load exclusion patterns from a file and skip lines matching these patterns. No filtering by default if no file provided.
4. **Wrapping**: Update the `Processor` to append a blank line after each wrapped block (paragraphs and list items).

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**: `click`, `textwrap`, `unicodedata` (stdlib), `collections.Counter` (stdlib), `re` (stdlib)
**Storage**: Filesystem (input/output directories, consolidated `frequency.txt`)  
**Testing**: pytest, coverage  
**Target Platform**: CLI (cross-platform Python)
**Project Type**: Single project
**Performance Goals**: Efficiently process archives while maintaining global frequency and file tracking state.
**Constraints**: Recursive processing, directory mirroring.
**Scale/Scope**: Local CLI tool for text processing.

## Constitution Check

- [x] **Python Development**: Implementation in Python 3.12 using standard tools.
- [x] **CLI-First**: Feature is exposed via the existing CLI with new options.
- [x] **Recursive Processing**: Maintained by the core processor logic.
- [x] **Data Isolation**: All test data remains in the `data/` directory.
- [x] **Atomic Git Workflow**: Tasks will be broken down into logical commits.

## Project Structure

### Documentation (this feature)

```text
specs/004-rework-filtering-wrapping/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── cli.md
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```text
ocrpolish/
├── cli.py               # CLI entry point (add filter/frequency options)
├── processor.py         # Core logic (normalization, wrapping, filtering)
├── core.py              # Processing orchestration
└── utils/
    ├── nlp.py           # Advanced normalization (diacritics, punctuation)
    └── files.py         # File handling and report generation
```

**Structure Decision**: Single project structure. Logic resides within the `ocrpolish/` package.

## Complexity Tracking

*No violations identified.*
