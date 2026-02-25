# Tasks: Rework Filtering and Wrapping

**Feature Branch**: `004-rework-filtering-wrapping`
**Implementation Plan**: [specs/004-rework-filtering-wrapping/plan.md](plan.md)

## Implementation Strategy

We will follow an incremental delivery approach, prioritizing the foundational normalization logic and the core frequency counting engine.

1.  **MVP (US1)**: Implement the frequency counting engine and consolidated report generation. This provides immediate value by helping identify boilerplate.
2.  **Filtering (US2)**: Replace hardcoded filters with the new data-driven filter matching system.
3.  **Layout (US3)**: Enhance the wrapping logic to support lists/bullets and the refined blank line rules.

## Phase 1: Setup

- [x] T001 Prepare test data directory with multiple OCR samples in `data/test/normalization`
- [x] T002 Create a base test suite for the new filtering and wrapping logic in `tests/integration/test_reworked_logic.py`

## Phase 2: Foundational

- [x] T003 [P] Implement advanced normalization (lowercase, diacritics, punctuation) in `ocrpolish/utils/nlp.py`
- [x] T004 [P] Update `ProcessingConfig` to include `filter_file_path` and `frequency_file_path` in `ocrpolish/data_model.py`
- [x] T005 [P] Define `LinePattern` and `FrequencyEntry` data classes in `ocrpolish/data_model.py`

## Phase 3: User Story 1 - Boilerplate Identification (Priority: P1)

**Story Goal**: Generate a consolidated frequency report for recurring lines across all documents.
**Independent Test**: Process a directory of files and verify `frequency.txt` contains correctly formatted entries for lines appearing > 5 times.

- [x] T006 [P] [US1] Implement `FrequencyStore` to track total counts, file counts, and verbatim forms in `ocrpolish/processor.py`
- [x] T007 [US1] Implement "Pass 1" accumulation logic to walk files and update `FrequencyStore` in `ocrpolish/core.py`
- [x] T008 [US1] Implement frequency report generation (TotalCount > 5, sorted) in `ocrpolish/utils/files.py`
- [x] T009 [US1] Update `run_processing` to execute Pass 1 and generate the report in `ocrpolish/core.py`
- [x] T010 [US1] Add CLI options `--frequency-file` in `ocrpolish/cli.py`

## Phase 4: User Story 2 - Customizable Content Filtering (Priority: P1)

**Story Goal**: Exclude specific repetitive lines based on a user-provided filter file.
**Independent Test**: Provide a filter file and verify that matching lines are removed from the output and saved to `.filtered.md`.

- [x] T011 [US2] Remove existing hardcoded noisy boilerplate logic from `ocrpolish/processor.py`
- [x] T012 [US2] Implement `FilterList` loading logic from a plain text file in `ocrpolish/processor.py`
- [x] T013 [US2] Update `clean_lines` to use `FilterList` matching (set of words) in `ocrpolish/processor.py`
- [x] T014 [US2] Ensure no filtering occurs by default if no filter file is provided in `ocrpolish/core.py`
- [x] T015 [US2] Add CLI option `--filter-file` and remove deprecated thresholds in `ocrpolish/cli.py`

## Phase 5: User Story 3 - Readable Text Layout (Priority: P2)

**Story Goal**: Wrap paragraphs, lists, and bullets with refined blank line placement.
**Independent Test**: Process a file with long list items and verify they are wrapped with a blank line following them.

- [x] T016 [US3] Update `should_protect_line` to allow wrapping for lists and bullets in `ocrpolish/processor.py`
- [x] T017 [US3] Modify `wrap_lines` to return whether a wrap actually occurred for each block in `ocrpolish/processor.py`
- [x] T018 [US3] Update output loop in `clean_lines` to append a blank line after every wrapped paragraph or wrapped list item in `ocrpolish/processor.py`
- [x] T019 [US3] Verify that short list items (unwrapped) do NOT receive a following blank line in `ocrpolish/processor.py`

## Phase 6: Polish & Cross-cutting Concerns

- [x] T020 [P] Run `ruff check .` and `ruff format .` to ensure code quality
- [x] T021 [P] Run `mypy .` to verify type safety
- [x] T022 Run full integration test suite `pytest tests/` and verify coverage

## Dependencies

1. Foundational tasks (T003-T005) must precede all User Stories.
2. US1 (T006-T010) provides the basis for identifying boilerplate.
3. US2 (T011-T015) uses the normalization logic from US1 for filtering.
4. US3 (T016-T019) is largely independent but should follow filtering.

## Parallel Execution Examples

- **Normalization & Data Model**: T003, T004, and T005 can be implemented in parallel.
- **Reporting & Logic**: T006 and T008 can be drafted in parallel while T007/T009 orchestrate them.
- **Quality Checks**: T020 and T021 can run in parallel at any point after implementation.
