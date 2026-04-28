# Tasks: Ollama Metadata Extraction

**Input**: Design documents from `/specs/008-ollama-metadata-extraction/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Initialize project dependencies (`ollama`, `pydantic`, `pyyaml`) in `pyproject.toml`
- [X] T002 Create directory structure: `ocrpolish/models/` and `ocrpolish/services/`
- [X] T003 [P] Configure quality tools for new modules (update `pyproject.toml` or config if needed)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure for metadata handling and Ollama interaction

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [P] Implement `MetadataSchema` Pydantic model in `ocrpolish/models/metadata.py`
- [X] T005 [P] Implement YAML frontmatter utility (read/write/prepend) in `ocrpolish/utils/metadata.py` using `pyyaml`
- [X] T006 Implement base `OllamaClient` wrapper for structured output in `ocrpolish/services/ollama_client.py`
- [X] T007 [P] Create mock Ollama response utility for testing in `tests/unit/test_ollama_client.py`

**Checkpoint**: Foundation ready - extraction logic and file utilities can now be integrated into the CLI.

---

## Phase 3: User Story 1 - Batch Metadata Extraction (Priority: P1) 🎯 MVP

**Goal**: Automatically extract structured metadata from a collection of Markdown files via a CLI command.

**Independent Test**: Run `ocrpolish metadata` on a sample directory and verify output files contain valid YAML frontmatter.

### Tests for User Story 1

- [X] T008 [P] [US1] Create integration test for CLI command in `tests/integration/test_metadata_command.py`
- [X] T009 [P] [US1] Create unit tests for YAML frontmatter injection in `tests/unit/test_metadata_utils.py`

### Implementation for User Story 1

- [X] T010 [US1] Implement core extraction orchestration (prompting, parsing) in `ocrpolish/services/ollama_client.py`
- [X] T011 [US1] Implement directory traversal and mirroring logic in `ocrpolish/processor_metadata.py`
- [X] T012 [US1] Add `metadata` command and options (input, output, model, url) to `ocrpolish/cli.py`
- [X] T013 [US1] Integrate `OllamaClient` and `processor` into the CLI command

**Checkpoint**: User Story 1 is functional. The system can process directories and generate metadata-enriched files.

---

## Phase 4: User Story 2 - Schema-Enforced Extraction (Priority: P2)

**Goal**: Ensure metadata strictly follows the defined schema and handles missing or non-compliant data gracefully.

**Independent Test**: Process documents with missing fields and verify that output YAML contains null/defaults without crashing.

### Tests for User Story 2

- [X] T014 [P] [US2] Create unit tests for `MetadataSchema` validation and edge cases (e.g., malformed archive codes) in `tests/unit/test_metadata_schema.py`

### Implementation for User Story 2

- [X] T015 [US2] Refine `MetadataSchema` with regex validation for `archive_code` in `ocrpolish/models/metadata.py`
- [X] T016 [US2] Implement retry logic or graceful failure for schema validation errors in `ocrpolish/services/ollama_client.py`
- [X] T017 [US2] Add logging for schema validation failures during batch processing

**Checkpoint**: Metadata extraction is now robust and schema-compliant.

---

## Phase 5: User Story 3 - Handling Non-Standard Documents (Priority: P3)

**Goal**: Correctly identify the `last_date` by scanning the entire document and providing summaries for untitled docs.

**Independent Test**: Process a multi-page document with multiple dates and verify `last_date` matches the final occurrence in the text.

### Tests for User Story 3

- [X] T018 [P] [US3] Add test cases for multi-page date extraction to `tests/integration/test_metadata_command.py`

### Implementation for User Story 3

- [X] T019 [US3] Implement chunking strategy (prioritize first 6k tokens) in `ocrpolish/processor_metadata.py`
- [X] T020 [US3] Implement secondary scan of final chunk to extract `last_date` in `ocrpolish/processor_metadata.py`
- [X] T021 [US3] Update prompt to emphasize summary generation for documents with ambiguous titles

**Checkpoint**: All user stories are complete, including multi-page context management.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T022 [P] Update `README.md` with the new `metadata` command usage
- [X] T023 Add progress bar (e.g., using `click` or `tqdm`) for batch operations in `ocrpolish/cli.py`
- [X] T024 Perform final validation sweep using `specs/008-ollama-metadata-extraction/quickstart.md`
- [X] T025 [P] Code cleanup and refactoring in `ocrpolish/services/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Phase 1.
- **User Stories (Phase 3+)**: Depend on Phase 2 completion.
- **Polish (Final Phase)**: Depends on all user stories.

### User Story Dependencies

- **US1 (P1)**: Foundation for US2 and US3.
- **US2 (P2)**: Extends US1 with validation.
- **US3 (P3)**: Extends US1/US2 with complex document handling.

### Parallel Opportunities

- T004, T005 can be done in parallel.
- Integration tests (T008) and Unit tests (T009) can be written in parallel.
- Schema validation tests (T014) can be done in parallel with other US2 work.

---

## Parallel Example: User Story 1

```bash
# Implement models and utilities simultaneously
Task: T004 Implement MetadataSchema
Task: T005 Implement YAML frontmatter utility
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup and Foundational.
2. Implement US1 to achieve "end-to-end" extraction from CLI to file.
3. Validate with basic documents.

### Incremental Delivery

1. US1 delivers core value (extraction).
2. US2 adds reliability (schema enforcement).
3. US3 adds completeness (large docs, last_date).
