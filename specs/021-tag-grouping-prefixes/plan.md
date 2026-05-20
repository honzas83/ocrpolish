# Implementation Plan: Tag Grouping Prefixes (v2)

**Branch**: `021-tag-grouping-prefixes` | **Date**: 2026-05-20 | **Spec**: [specs/021-tag-grouping-prefixes/spec.md](specs/021-tag-grouping-prefixes/spec.md)
**Input**: Feature specification from `/specs/021-tag-grouping-prefixes/spec.md`

## Summary

This feature refines the tag organization in the Obsidian vault using global configurable constants defined in `ocrpolish/data_model.py`. The prefixes are `Topics`, `Entities`, and `Tags`. A key requirement is that if any of these constants is set to `None`, the corresponding group will remain unprefixed. The implementation will ensure proper normalization, idempotency, and opt-out support via the `None` value.

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**: click, pydantic, pyyaml, ollama  
**Constants File**: `ocrpolish/data_model.py` (added `TAG_PREFIX_*` constants)
**Refactored Helper**: `prefix_tag` in `ocrpolish/utils/metadata.py`
**Refactored Processor**: `MetadataProcessor` in `ocrpolish/processor_metadata.py`
**Testing**: Refactored `tests/unit/test_tag_prefixing.py` and `tests/unit/test_tag_prefixing_integration.py`

## Constitution Check

- **Python Development**: PASSED
- **CLI-First**: PASSED
- **Recursive Processing**: PASSED
- **Data Isolation**: PASSED (Config separated from logic)
- **Atomic Git Workflow**: PASSED

## Project Structure

### Documentation (this feature)

```text
specs/021-tag-grouping-prefixes/
├── plan.md              # This file
├── research.md          # Implementation analysis (Global Constants + None support)
├── data-model.md        # Tag hierarchy structure and opt-out rules
├── quickstart.md        # Verification and disablement steps
└── checklists/
    └── requirements.md  # Spec quality checklist
```

### Source Code (repository root)

```text
ocrpolish/
├── data_model.py        # Centralized constants: TAG_PREFIX_TOPIC, TAG_PREFIX_ENTITY, TAG_PREFIX_TAG
├── processor_metadata.py    # Refactored to use data_model constants
└── utils/
    └── metadata.py          # prefix_tag() updated to handle None root_prefix
```

**Structure Decision**: Global configuration driven implementation.

## Complexity Tracking

*No violations.*
