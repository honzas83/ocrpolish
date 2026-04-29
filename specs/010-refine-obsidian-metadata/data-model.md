# Data Model: Refine Obsidian Metadata

## Entities

### MetadataSchema (Pydantic Model)
Updated to reflect the removal of `correspondence_` prefixes and the focus on single-sentence summaries.

| Field | Type | Description |
|-------|------|-------------|
| title | str | Formal title of the document. |
| summary | str | Exactly one sentence summary. |
| abstract | str | Detailed overview (up to 20 sentences). |
| sender | str | Name/institution of the sender (formerly `correspondence_sender`). |
| recipient | str | Name/institution of the recipient (formerly `correspondence_recipient`). |
| transaction | str | Action/request of the correspondence (formerly `correspondence_transaction`). |
| author_name | str | Name of the author. |
| author_institution| str | Organization of the author. |
| date | str | ISO 8601 date (YYYY-MM-DD). |
| archive_code | str | Formal archive reference. |
| language | str | Primary language. |
| location_city | str | Origin city. |
| location_state | str | Origin nation-state. |
| mentioned_states | list[str] | List of nation states mentioned. |
| mentioned_organisations | list[str] | List of organizations mentioned. |
| references | list[str] | Other archive reference codes. |
| tags | list[str] | Hash-tag like keywords (numeric-only tags prefixed with `Year`). |

## Validation Rules
- **Summary**: MUST be a single sentence.
- **Tags**: MUST NOT contain spaces. Numeric tags MUST be prefixed with `Year`.
- **Empty Fields**: Any field with `""`, `[]`, or `None` MUST be excluded from the final YAML frontmatter.

## State Transitions
1. **Extraction**: Ollama extracts metadata into `MetadataSchema`.
2. **Refinement**: Python logic cleans up tags, truncates summary, and filters empty fields.
3. **Assembly**: 
    - `title` and `abstract` are moved from metadata to a `> [!abstract]` callout block.
    - Title is formatted as `# Title` inside the callout.
    - Remaining fields are formatted as YAML frontmatter.
    - Original body is cleaned of duplicate titles and leading horizontal rules.
    - Spacing: YAML + empty line + Callout + empty line + Original Body.
