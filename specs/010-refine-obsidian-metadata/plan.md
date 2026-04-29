# Implementation Plan: Refine Obsidian Metadata

**Branch**: `010-refine-obsidian-metadata` | **Date**: 2026-04-29 | **Spec**: [specs/010-refine-obsidian-metadata/spec.md](spec.md)
**Input**: Feature specification from `/specs/010-refine-obsidian-metadata/spec.md`

## Summary

The goal of this feature is to refine the metadata extraction output for better Obsidian compatibility and document structure. This involves renaming frontmatter keys, simplifying the summary to a single sentence, moving the title and abstract into an Obsidian callout block at the start of the body, removing empty attributes, and formatting numeric tags.

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**: `pydantic`, `ollama`, `pyyaml`, `click`  
**Storage**: Filesystem (input/output directories)  
**Testing**: `pytest`, `coverage`  
**Target Platform**: CLI (cross-platform Python)
**Project Type**: Single project
**Performance Goals**: Minimal overhead on top of LLM extraction.  
**Constraints**: Recursive processing, directory mirroring, Obsidian metadata limitations.
**Scale/Scope**: Impacts the `metadata` command and its core processing logic.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Quality-Driven Python Development**: YES. Using Python 3.12, ruff, mypy, and pytest.
- **Principle II: CLI-First Interface**: YES. Part of the `ocrpolish` CLI.
- **Principle III: Recursive Directory Processing**: YES. Handled by `MetadataProcessor`.
- **Principle IV: Data Isolation**: YES. Data remains in `data/`.
- **Principle V: Atomic Git Workflow**: YES. Each task will be committed separately.

## Project Structure

### Documentation (this feature)

```text
specs/010-refine-obsidian-metadata/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
ocrpolish/
├── models/
│   └── metadata.py      # MetadataSchema updates
├── utils/
│   └── metadata.py      # tag normalization and formatting updates
└── processor_metadata.py # core processing logic updates

tests/
├── unit/
│   ├── test_metadata_utils.py
│   └── test_metadata_processor.py
```

**Structure Decision**: Single project. Modifications are confined to existing metadata processing modules.

## Complexity Tracking

*No constitution violations detected.*
