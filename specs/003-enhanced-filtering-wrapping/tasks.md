# Tasks: Enhanced OCR Filtering and Paragraph Wrapping

**Input**: Design documents from `/specs/003-enhanced-filtering-wrapping/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli.md

**Tests**: Tests are explicitly included to verify functional requirements (FR-001 to FR-007) and success criteria.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Update `ocrpolish/data_model.py` with new `ProcessingConfig` fields (`similarity_threshold`, `dry_run`, etc.)
- [X] T002 Update `ocrpolish/cli.py` to support new arguments (`--similarity`, `--dry-run`, `--no-filtered`)
- [X] T003 [P] Add unit test for `ProcessingConfig` validation in `tests/unit/test_data_model.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure for fuzzy matching and word-set processing

**⚠️ CRITICAL**: Statistical filtering and sidecar file handling MUST be implemented before user stories can be fully verified.

- [X] T004 Implement word-set normalization and overlap coefficient utility in `ocrpolish/utils/nlp.py`
- [X] T005 [P] Create unit tests for fuzzy matching in `tests/unit/test_nlp_utils.py`
- [X] T006 Implement sidecar file writing utility in `ocrpolish/utils/files.py`
- [X] T007 [P] Create unit tests for sidecar file generation in `tests/unit/test_file_utils.py`

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Clean Paragraph Separation (Priority: P1) 🎯 MVP

**Goal**: Implement wrapping for tag-like markup and ensure blank line separation.

### Tests for User Story 1

- [X] T008 [P] [US1] Create integration test for markup wrapping in `tests/integration/test_markup_wrapping.py`
- [X] T009 [P] [US1] Create unit test for paragraph separation logic in `tests/unit/test_paragraph_separation.py`

### Implementation for User Story 1

- [X] T010 [US1] Update `should_protect_line` in `ocrpolish/processor.py` to allow wrapping for lines starting with `<` or `[`
- [X] T011 [US1] Update `clean_lines` in `ocrpolish/processor.py` to insert blank lines between wrapped blocks
- [X] T012 [US1] Modify `wrap_lines` in `ocrpolish/processor.py` to handle tag-like markup specifically

**Checkpoint**: User Story 1 functional and testable.

---

## Phase 4: User Story 2 - Statistical Boilerplate Removal (Priority: P2)

**Goal**: Implement fuzzy statistical filtering based on word-set overlap across the corpus.

### Tests for User Story 2

- [X] T013 [P] [US2] Create integration test for fuzzy boilerplate detection in `tests/integration/test_fuzzy_boilerplate.py`
- [X] T014 [P] [US2] Create unit test for global frequency counting with fuzzy matching in `tests/unit/test_frequency_counter.py`

### Implementation for User Story 2

- [X] T015 [US2] Update Pass 1 in `ocrpolish/core.py` to use word-set hashing for global frequency counting
- [X] T016 [US2] Implement fuzzy matching logic in `clean_lines` (Pass 2) using `similarity_threshold` from `ocrpolish/processor.py`
- [X] T017 [US2] Add logic to `ocrpolish/core.py` to identify `BoilerplateCandidate` sets from the corpus

**Checkpoint**: User Story 2 functional and testable.

---

## Phase 5: User Story 3 - Data Preservation (Priority: P3)

**Goal**: Save filtered lines to sidecar files and support dry-run mode.

### Tests for User Story 3

- [X] T018 [P] [US3] Create integration test for dry-run mode in `tests/integration/test_dry_run.py`
- [X] T019 [P] [US3] Create integration test for sidecar file content in `tests/integration/test_sidecar_output.py`

### Implementation for User Story 3

- [X] T020 [US3] Update `run_processing` in `ocrpolish/core.py` to respect the `dry_run` flag
- [X] T021 [US3] Implement sidecar file creation for dropped lines in `ocrpolish/core.py`
- [X] T022 [US3] Ensure `clean_lines` returns dropped lines alongside cleaned output for sidecar processing

**Checkpoint**: All user stories functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T023 [P] Update `README.md` with new CLI arguments and fuzzy filtering documentation
- [X] T024 Run `ruff check .` and `mypy .` to ensure code quality
- [X] T025 [P] Performance profiling for fuzzy matching on 100+ files
- [X] T026 Validate all success criteria (SC-001 to SC-004) using `quickstart.md` examples

**Final Status**: Implementation complete and verified.
