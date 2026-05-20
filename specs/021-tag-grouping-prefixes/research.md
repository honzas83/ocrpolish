# Research: Tag Grouping Prefixes (Updated v2)

**Feature**: [specs/021-tag-grouping-prefixes/spec.md](specs/021-tag-grouping-prefixes/spec.md)

## Current Implementation Analysis

The current implementation (v1) successfully added `#Topic/`, `#Entity/`, and `#Tags/` prefixes in `MetadataProcessor`.

## Decision: Global Configurable Constants & Opt-out

### Decision: Centralize Prefixes in `ocrpolish/data_model.py`
- **Rationale**: To unify singular/plural terms (Topics, Entities, Tags) and allow easy changes in one place.
- **Unified Terms**:
  - `TAG_PREFIX_TOPIC = "Topics"`
  - `TAG_PREFIX_ENTITY = "Entities"`
  - `TAG_PREFIX_TAG = "Tags"`

### Decision: Support `None` for Opt-out
- **Requirement**: "If the constant is None, do not prefix the corresponding group."
- **Implementation**: The `prefix_tag` helper function will be updated to check if `root_prefix` is `None`. If it is, it will return the normalized tag with a leading `#` but WITHOUT any root prefix.

## Implementation Strategy Refinement
1. **Define Constants**: Add the prefix constants to `ocrpolish/data_model.py` as type `str | None`.
2. **Update Helper**: Modify `prefix_tag` in `ocrpolish/utils/metadata.py` to handle the `None` case.
3. **Refactor Processor**: Update `MetadataProcessor` to use the constants from `ocrpolish.data_model`.
4. **Update Tests**: Refactor tests to import and verify both prefixed and unprefixed (via `None`) scenarios.

## Alternatives Considered
- **Empty String vs None**: `None` is more explicit for "disabled" than an empty string, which might be accidentally passed. We will support both: if `root_prefix` is falsy, no root prefix is added.
