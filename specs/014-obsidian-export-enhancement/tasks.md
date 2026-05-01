# Tasks: Obsidian Export Enhancement

**Input**: Design documents from `/specs/014-obsidian-export-enhancement/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Included as per project constitution requiring robust testing with `pytest`.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify current state and prepare environment.

- [ ] T001 [P] Run existing tests to ensure baseline stability `pytest`
- [x] T002 [P] Verify `ruff` and `mypy` pass on current codebase

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core model updates and utility functions needed by all stories.

**⚠️ CRITICAL**: These tasks update the data structures used by the processor.

- [x] T003 Update `MetadataSchema` in `ocrpolish/models/metadata.py` (add `mentioned_cities`, rename `transaction` to `correspondence`)
- [x] T004 [P] Implement `extract_last_page_header` utility in `ocrpolish/utils/metadata.py` to find `# Page XXX`
- [x] T005 [P] Implement `format_hierarchical_tag` enhancement in `ocrpolish/utils/metadata.py` to handle nesting and character normalization

**Checkpoint**: Foundation ready - Metadata schema updated and core utilities available.

---

## Phase 3: User Story 1 - Hierarchical Metadata Tags (Priority: P1) 🎯 MVP

**Goal**: Transform mentioned entities into hierarchical tags (#State/UK, #Org/EU, #City/UK/London).

**Independent Test**: Process a file with locations and verify tags in the output Markdown body.

### Tests for User Story 1

- [x] T006 [P] [US1] Add unit tests for hierarchical tag formatting (including normalization of spaces/special characters) in `tests/unit/test_metadata_utils.py`

### Implementation for User Story 1

- [x] T007 [US1] Update Ollama prompt in `ocrpolish/processor_metadata.py` to include instructions for `mentioned_cities`
- [x] T008 [US1] Implement entity-to-tag conversion logic in `ocrpolish/processor_metadata.py` using the utilities from T005
- [x] T009 [US1] Update `MetadataProcessor.process_file` to handle the new `mentioned_cities` extraction result

**Checkpoint**: User Story 1 functional - Entities are correctly converted to tags.

---

## Phase 4: User Story 2 - Clean Frontmatter and Enhanced Callout (Priority: P2)

**Goal**: Reorganize output structure: cleaner YAML, page count extraction, and enriched Callout.

**Independent Test**: Verify frontmatter order/content and presence of tags in the Callout section.

### Tests for User Story 2

- [x] T010 [P] [US2] Add unit tests for page number extraction from Markdown headers in `tests/unit/test_metadata_utils.py`
- [x] T011 [P] [US2] Add integration test for frontmatter field ordering and exclusion in `tests/unit/test_processor_metadata.py`

### Implementation for User Story 2

- [x] T012 [US2] Implement source-based page count extraction in `MetadataProcessor.process_file` within `ocrpolish/processor_metadata.py`
- [x] T013 [US2] Update `_prepare_obsidian_metadata` in `ocrpolish/processor_metadata.py` to enforce new field ordering (pages after summary) and renaming
- [x] T014 [US2] Modify `process_file` to move `mentioned_*` tags from frontmatter to a new "Mentioned Entities" section in the Callout block
- [x] T015 [US2] Update YAML stringification to strictly exclude `mentioned_*` keys from frontmatter

**Checkpoint**: User Story 2 functional - Output format matches the new Obsidian-optimized structure.

---

## Phase 5: User Story 3 - Language Consistency (Priority: P3)

**Goal**: Ensure all metadata and tags are in English by default.

**Independent Test**: Process a non-English document and verify English keys and tag prefixes.

### Implementation for User Story 3

- [x] T016 [US3] Update the system prompt in `ocrpolish/processor_metadata.py` to explicitly mandate English for all extracted fields and categories
- [x] T017 [P] [US3] Add a test case with non-English content to verify English output in `tests/unit/test_processor_metadata.py`

**Checkpoint**: All user stories complete and consistent.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final quality checks and documentation.

- [x] T018 [P] Run full quality suite: `ruff check .`, `mypy .`, `pytest`
- [x] T019 Update `README.md` or technical docs with the new metadata schema and tagging conventions
- [x] T020 Run `quickstart.md` validation to ensure the documented workflow is accurate

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Blocks all User Stories as it defines the data model.
- **User Stories (Phase 3-5)**: 
    - US1 (Phase 3) is the priority MVP.
    - US2 (Phase 4) depends on the foundational page extraction utility.
    - US3 (Phase 5) is cross-cutting but can be done after Ollama prompt updates.
- **Polish (Phase 6)**: After all implementation.

### Parallel Opportunities

- T004 and T005 can be done in parallel.
- Test tasks (T006, T010, T011) can be prepared in parallel once foundational utilities exist.
- Documentation updates (T019) can start early.

---

## Parallel Example: User Story 1

```bash
# Implement model changes and extraction logic in parallel
Task: "T007 [US1] Update Ollama prompt in ocrpolish/processor_metadata.py"
Task: "T006 [P] [US1] Add unit tests for hierarchical tag formatting in tests/unit/test_metadata_utils.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup and Foundational updates to support hierarchical tags.
2. Implement US1: Hierarchical Tags.
3. **STOP and VALIDATE**: Verify that States, Orgs, and Cities are correctly tagged in the body.

### Incremental Delivery

1. Foundation + US1 -> Hierarchical tagging capability.
2. Add US2 -> Clean frontmatter and page count extraction.
3. Add US3 -> Universal English output.
4. Final Polish.
