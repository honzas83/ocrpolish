# Data Model: Tag Grouping Prefixes (Updated v2)

This feature introduces global constants for tag categorization with support for disabling prefixes.

## Global Constants

Defined in `ocrpolish/data_model.py`:

| Constant | Default Value | Type | Description |
|----------|---------------|------|-------------|
| `TAG_PREFIX_TOPIC` | `"Topics"` | `str \| None` | Root for taxonomy-based topics |
| `TAG_PREFIX_ENTITY` | `"Entities"` | `str \| None` | Root for named entities |
| `TAG_PREFIX_TAG` | `"Tags"` | `str \| None` | Root for LLM-assigned keywords |

## Entities

### Grouped Tags (Output Structure)

All tags in the Obsidian output are formatted based on the global constants:

| Source Model Field | Constant Reference | Result if `str` | Result if `None` |
|-------------------|-------------------|-----------------|------------------|
| `topic_tags`      | `TAG_PREFIX_TOPIC` | `#Topics/TopicName` | `#TopicName` |
| `entity_tags`     | `TAG_PREFIX_ENTITY` | `#Entities/EntityName` | `#EntityName` |
| `conceptual_tags` | `TAG_PREFIX_TAG`   | `#Tags/TagName` | `#TagName` |

## Constraints & Rules

1. **Centralized Control**: Prefixes MUST be sourced from the global constants.
2. **Conditional Prefixing**: If a constant is `None`, the system MUST NOT apply the root prefix to that group. It still MUST apply a leading `#` and normal normalization.
3. **Idempotency**: The system MUST NOT double-prefix tags, even if they already start with the string defined in the constant.
