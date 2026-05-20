# Tasks: Tag Grouping Prefixes (v2)

**Input**: Design documents from `/specs/021-tag-grouping-prefixes/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing. This version focuses on global configurable constants and support for `None` to disable prefixes.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and design review

- [X] T001 Review updated implementation plan (v2) and data model in `specs/021-tag-grouping-prefixes/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [X] T002 [P] Define `TAG_PREFIX_TOPIC`, `TAG_PREFIX_ENTITY`, and `TAG_PREFIX_TAG` as configurable constants in `ocrpolish/data_model.py`.
- [X] T003 Update `prefix_tag` in `ocrpolish/utils/metadata.py` to handle `None` (opt-out) and ensure it uses `normalize_tag_component`.

---

## Phase 3: User Story 1 - Configurable Topics Prefix (Priority: P1) 🎯 MVP

**Goal**: Group taxonomy topics under a configurable root, with opt-out support.

**Independent Test**: Set `TAG_PREFIX_TOPIC = "Topics"` and verify `#Topics/...`. Set to `None` and verify `#Category/Topic`.

### Tests for User Story 1

- [X] T004 [P] [US1] Update `tests/unit/test_tag_prefixing.py` to verify Topic prefixing using the global constant and handle `None`.

### Implementation for User Story 1

- [X] T005 [US1] Update `MetadataProcessor.process_file` in `ocrpolish/processor_metadata.py` to use `TAG_PREFIX_TOPIC` from `ocrpolish.data_model`.

**Checkpoint**: User Story 1 functional and testable with configuration.

---

## Phase 4: User Story 2 - Configurable Entities Prefix (Priority: P1)

**Goal**: Group entities under a configurable root, with plural Plural default.

**Independent Test**: Set `TAG_PREFIX_ENTITY = "Entities"` and verify `#Entities/State/...`.

### Tests for User Story 2

- [X] T006 [P] [US2] Update `tests/unit/test_tag_prefixing.py` to verify Entity prefixing using the global constant and handle `None`.

### Implementation for User Story 2

- [X] T007 [US2] Update `MetadataProcessor.process_file` in `ocrpolish/processor_metadata.py` to use `TAG_PREFIX_ENTITY` and refine entity grouping logic to handle the root prefix.

**Checkpoint**: User Story 2 functional and testable with configuration.

---

## Phase 5: User Story 3 - Configurable Tags Prefix (Priority: P2)

**Goal**: Group flat tags under a configurable root.

**Independent Test**: Set `TAG_PREFIX_TAG = "Tags"` and verify `#Tags/Keyword`.

### Tests for User Story 3

- [X] T008 [P] [US3] Update `tests/unit/test_tag_prefixing.py` to verify Assigned tag prefixing using the global constant and handle `None`.

### Implementation for User Story 3

- [X] T009 [US3] Update `MetadataProcessor.process_file` in `ocrpolish/processor_metadata.py` to use `TAG_PREFIX_TAG`.

**Checkpoint**: All user stories functional and testable with global configuration.

---

## Phase 6: Integration & Validation

**Purpose**: Final verification and cleanup across the project.

- [X] T010 [P] Refactor `tests/unit/test_tag_prefixing_integration.py` and other integration tests to import and use the global constants.
- [X] T011 [P] Run all project tests: `pytest`
- [X] T012 [P] Perform static analysis: `ruff check .` and `mypy .`
- [X] T013 Verify `quickstart.md` validation scenarios, specifically the "Disabling a Prefix Group" section.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: T002 and T003 are prerequisites for all User Stories.
- **User Stories (Phase 3+)**: Can proceed in priority order (US1 -> US2 -> US3).
- **Validation (Phase 6)**: Depends on all user stories being complete.

---

## Implementation Strategy

### Configuration-First

1. Complete Phase 2 first to establish the `data_model` constants.
2. For each User Story, update tests to reflect the desired configuration behavior.
3. Update implementation and verify against tests.

### Regression Testing

- Integration tests MUST be updated to use the constants to avoid brittle tests that fail when prefixes are reconfigured.
