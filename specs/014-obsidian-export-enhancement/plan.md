# Implementation Plan: Obsidian Export Enhancement

**Branch**: `014-obsidian-export-enhancement` | **Date**: 2026-04-30 | **Spec**: [specs/014-obsidian-export-enhancement/spec.md](spec.md)
**Input**: Feature specification from `/specs/014-obsidian-export-enhancement/spec.md`

## Summary
Enhance the Obsidian export by transforming mentioned entities (States, Organizations, Cities) into hierarchical tags, cleaning up the YAML frontmatter, and adding a page count attribute extracted directly from the source Markdown headers.

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**: `click`, `ollama`, `pydantic`, `pyyaml`  
**Storage**: Filesystem (input/output directories)  
**Testing**: `pytest`, `coverage`  
**Target Platform**: CLI (cross-platform Python)
**Project Type**: Single project
**Performance Goals**: Maintain current processing speed (~5-10s per document for Ollama extraction).
**Constraints**: Recursive processing, directory mirroring, Obsidian-compatible Markdown output.
**Scale/Scope**: Updating the metadata extraction and formatting logic in the core processor.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] I. Quality-Driven Python Development (Using ruff, mypy, pytest)
- [x] II. CLI-First Interface (Extending existing `metadata` command)
- [x] III. Recursive Directory Processing (Supported by `MetadataProcessor`)
- [x] IV. Data Isolation (Data in `data/`, gitignored)
- [x] V. Atomic Git Workflow (Logical commits for each task)

## Project Structure

### Documentation (this feature)

```text
specs/014-obsidian-export-enhancement/
├── plan.md              # This file
├── research.md          # Decisions and rationale
├── data-model.md        # Updated MetadataSchema and output structure
├── quickstart.md        # Usage overview
└── tasks.md             # Implementation tasks (Phase 2)
```

### Source Code (repository root)

```text
ocrpolish/
├── models/
│   └── metadata.py      # MetadataSchema updates
├── utils/
│   └── metadata.py      # Formatting and extraction utilities
├── processor_metadata.py # Main logic for extraction and formatting
└── cli.py               # CLI command entry point

tests/
├── unit/
│   ├── test_metadata_utils.py
│   └── test_processor_metadata.py
```

**Structure Decision**: Single project structure, extending existing core modules.

## Complexity Tracking

*No constitution violations identified.*
