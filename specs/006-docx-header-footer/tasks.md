# Tasks: Dynamic Headers and Footers for DOCX

**Input**: Design documents from `/specs/006-docx-header-footer/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and file creation

- [x] T001 [P] Create `ocrpolish/utils/metadata.py` for metadata extraction logic
- [x] T002 [P] Create `tests/unit/test_metadata.py` for unit testing extraction
- [x] T003 [P] Create `tests/integration/test_docx_metadata.py` for integration testing

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure and CLI updates

- [x] T004 Update `ocrpolish/data_model.py` to add `scan_paragraphs` to `ProcessingConfig`
- [x] T005 Update `ocrpolish/cli.py` to add the `--scan-paragraphs` command-line flag

**Checkpoint**: CLI and configuration are ready.

---

## Phase 3: User Story 1 - Page Number Extraction (Priority: P1) 🎯 MVP

**Goal**: Extract page numbers like "- 1 -" or "-1-" and move them to DOCX headers/footers.

**Independent Test**: Process a file with page numbers and verify they appear in the DOCX header/footer and are removed from the body.

### Tests for User Story 1

- [x] T006 [P] [US1] Write unit tests for page number regex extraction in `tests/unit/test_metadata.py`

### Implementation for User Story 1

- [x] T007 [US1] Implement `extract_page_number` in `ocrpolish/utils/metadata.py`
- [x] T008 [US1] Update `split_markdown_by_pages` in `ocrpolish/utils/docx_utils.py` to optionally extract and return page-level metadata
- [x] T009 [US1] Implement header/footer injection logic in `ocrpolish/utils/docx_utils.py` using `section.header` / `section.footer`

**Checkpoint**: Page numbers are successfully moved to DOCX metadata.

---

## Phase 4: User Story 2 - File-Level Header/Footer Detection (Priority: P2)

**Goal**: Identify repeated text at page tops/bottoms (80% threshold) and move to DOCX headers/footers.

**Independent Test**: Process a file with recurring headers and verify they move to the DOCX header.

### Tests for User Story 2

- [x] T010 [P] [US2] Write unit tests for frequency counting and 80% threshold logic in `tests/unit/test_metadata.py`
- [x] T011 [P] [US2] Write integration tests for end-to-end extraction in `tests/integration/test_docx_metadata.py`

### Implementation for User Story 2

- [x] T012 [US2] Implement `FileMetadataAnalyzer` in `ocrpolish/utils/metadata.py` to track frequencies across a file
- [x] T013 [US2] Update `create_docx_from_pages` in `ocrpolish/utils/docx_utils.py` to perform a Pass 1 analysis of all pages
- [x] T014 [US2] Implement Pass 2 in `create_docx_from_pages` to strip identified headers/footers from the body and inject into DOCX metadata

**Checkpoint**: Recurring headers and footers are successfully extracted and moved.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and code quality

- [x] T015 Run `ruff check .` and `ruff format .`
- [x] T016 Run `mypy .` for static type checking
- [x] T017 Run `pytest` and verify 100% success rate on new tests
- [x] T018 Update `README.md` with header/footer extraction details

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Phase 1 completion for file structure.
- **User Stories (Phase 3+)**: Depend on Phase 2 completion for CLI/config support.
- **Polish (Final Phase)**: Depends on all user stories.

### Parallel Opportunities

- T001, T002, T003 (Initial file creation)
- T006 (US1 Unit tests)
- T010, T011 (US2 Tests)

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Setup and Foundational phases.
2. Implement US1: Regex-based page number extraction.
3. Verify with unit tests.

### Incremental Delivery
1. Foundation -> Config ready.
2. US1 -> Page numbers move to headers.
3. US2 -> Recurring headers/footers move to headers based on 80% threshold.
4. Polish -> Clean code and updated docs.
