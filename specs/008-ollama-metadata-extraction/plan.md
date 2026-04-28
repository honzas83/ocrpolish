# Implementation Plan: Ollama Metadata Extraction

**Branch**: `008-ollama-metadata-extraction` | **Date**: 2026-04-28 | **Spec**: [specs/008-ollama-metadata-extraction/spec.md](spec.md)

## Summary
The `ocrpolish metadata` command extracts structured archival metadata using local Ollama LLMs. It features tag frequency accumulation for cross-document consistency, 2-pass date extraction, and strict archival normalization (Acronym preservation, Title Case).

## Technical Context
- **Backend**: Ollama (`gemma4:26b`) with Pydantic schema enforcement.
- **Frontend**: Click-based CLI with subcommands.
- **Data Integrity**: YAML frontmatter merging with double-delimiter protection.

## Project Structure (Implemented)

```text
ocrpolish/
├── cli.py               # click subcommands (clean, metadata)
├── core.py              # (Existing) Core cleaning logic
├── processor_metadata.py # Metadata extraction orchestration & Tag accumulation
├── models/
│   └── metadata.py      # MetadataSchema & LastDateSchema
├── services/
│   └── ollama_client.py # Structured output wrapper for Ollama API
└── utils/
    ├── files.py         # Alphabetical scanning & filtering
    └── metadata.py      # Frontmatter parsing/merging & XML sanitization
tests/
├── integration/
│   └── test_metadata_command.py
└── unit/
    ├── test_metadata_schema.py
    └── test_metadata_utils.py
```

## Key Implementation Details
1. **Schema Enforcement**: Uses flattened Pydantic models with required defaults to prevent Ollama Status 500 grammar errors.
2. **Tag Accumulation**: A run-wide `Counter` passes the 50 most common tags to the LLM context to ensure thematic uniformity across thousands of documents.
3. **Archival Rules**: 
   - Whitelisted acronyms (`NATO`, `SHAPE`, etc.) remain uppercase.
   - Summaries and Abstracts are independent (no shared abbreviations).
   - "N/A" values are stripped; correspondence block is omitted if empty.
4. **Frontmatter Merging**: `parse_frontmatter` ensures that existing YAML is preserved and merged with new extraction results without creating triple delimiters.
5. **XML Safety**: Added `sanitize_xml` utility to `docx_utils.py` to prevent crashes when metadata contains illegal control characters.

## Final Status
- [x] CLI Subcommands implemented.
- [x] Ollama integration with schema validation.
- [x] Tag accumulation logic.
- [x] Archival normalization rules.
- [x] Unit and Integration tests passed.
- [x] Documentation backpropagated.
