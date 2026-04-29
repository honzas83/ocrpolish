# Tasks: Refine Obsidian Metadata

**Input**: Design documents from `/specs/010-refine-obsidian-metadata/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: Unit tests are requested to verify the logic changes in metadata utilities and the processor.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and quality tool configuration

- [X] T
001 [P] Ensure development environment is ready (Python 3.12, ruff, mypy, pytest)
- [X] T
002 [P] Verify existing tests pass before starting modifications

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core model updates that both user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T
003 Update `MetadataSchema` in `ocrpolish/models/metadata.py` to remove `correspondence_` prefixes from field names (rename to `sender`, `recipient`, `transaction`)
- [X] T
004 Update `MetadataProcessor._prepare_obsidian_metadata` in `ocrpolish/processor_metadata.py` to match the new `MetadataSchema` field names

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Metadata Cleanup (Priority: P1) 🎯 MVP

**Goal**: Clean and standardize metadata for Obsidian compatibility (renaming, empty removal, year tags)

**Independent Test**: Run `metadata` command on a file with `correspondence_` fields, empty fields, and a numeric tag (e.g., `1968`). Verify output frontmatter is clean and tags are prefixed with `Year`.

### Tests for User Story 1

- [X] T
005 [P] [US1] Add unit tests for tag normalization with numeric years in `tests/unit/test_metadata_utils.py`
- [X] T
006 [P] [US1] Add unit tests for empty attribute removal in `tests/unit/test_metadata_processor.py` or a utility test

### Implementation for User Story 1

- [X] T
007 [P] [US1] Update `normalize_obsidian_tags` in `ocrpolish/utils/metadata.py` to prefix numeric-only tags with `Year`
- [X] T
008 [US1] Update `MetadataProcessor._prepare_obsidian_metadata` in `ocrpolish/processor_metadata.py` to remove keys with empty/null values from the returned dictionary
- [X] T
009 [US1] Update the Ollama prompt in `MetadataProcessor.process_file` in `ocrpolish/processor_metadata.py` to use the new field names (sender, recipient, transaction)

**Checkpoint**: User Story 1 is functional. Metadata is cleaned and Obsidian-compatible.

---

## Phase 4: User Story 2 - Content Structure (Priority: P2)

**Goal**: Refine summary length and move title/abstract to the markdown body

**Independent Test**: Run `metadata` command and verify the summary is one sentence and that `# Title` and `abstract` appear in the body, separated by `---` from the original text.

### Tests for User Story 2

- [X] T
010 [P] [US2] Add unit tests for summary truncation logic in `tests/unit/test_metadata_utils.py`
- [X] T
011 [P] [US2] Add integration test case for body structure (title/abstract/rule) in `tests/unit/test_metadata_processor.py`

### Implementation for User Story 2

- [X] T
012 [P] [US2] Implement a summary truncation utility in `ocrpolish/utils/metadata.py` to ensure single-sentence output
- [X] T
013 [US2] Update `MetadataProcessor.process_file` in `ocrpolish/processor_metadata.py` to request exactly one sentence for the summary in the prompt and apply truncation
- [X] T
014 [US2] Modify `MetadataProcessor.process_file` in `ocrpolish/processor_metadata.py` to remove `abstract` and `title` from frontmatter and prepended them to the body content
- [X] T
015 [US2] Update `MetadataProcessor.process_file` in `ocrpolish/processor_metadata.py` to insert the horizontal rule `---` after the title/abstract section

**Checkpoint**: User Story 2 is functional. Document structure matches Obsidian preferences.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and documentation

- [X] T
016 [P] Run all tests and verify 100% pass rate
- [X] T
017 [P] Run `ruff check .` and `mypy .` to ensure code quality
- [X] T
018 Validate implementation using `specs/010-refine-obsidian-metadata/quickstart.md` on real sample data
- [X] T
019 [P] Update `README.md` if any user-facing CLI behavior changed significantly (optional)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on T001-T002.
- **User Stories (Phase 3-4)**: Depend on Phase 2 completion.
  - US1 (Phase 3) is the priority.
  - US2 (Phase 4) can be done in parallel with US1 implementation but follows US1 in priority.

### Parallel Opportunities

- T001 and T002 can run in parallel.
- T003 and T004 are sequential but quick.
- US1 and US2 can be implemented in parallel by different developers once Phase 2 is done.
- Within US1: T005, T006, and T007 can start in parallel.
- Within US2: T010 and T012 can start in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup and Foundational phases.
2. Complete US1 (Metadata Cleanup).
3. Validate that metadata is correctly cleaned and tags are Obsidian-compatible.

### Incremental Delivery

1. Foundation ready.
2. US1 added (MVP).
3. US2 added (Full feature).
4. Final Polish.
