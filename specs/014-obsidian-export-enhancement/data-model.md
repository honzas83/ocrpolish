# Data Model: Obsidian Export Enhancement

## MetadataSchema (Updated)
The Pydantic model for structured metadata extraction.

| Field | Type | Description |
|-------|------|-------------|
| title | str | Formal title of the document. |
| summary | str | Exactly one sentence summary. |
| abstract | str | Detailed overview (up to 20 sentences). |
| author_name | str | Name of individual author. |
| author_institution | str | Responsible organization. |
| date | str | ISO 8601 date (YYYY-MM-DD). |
| archive_code | str | Formal archive reference code. |
| language | str | Default "English". |
| location_city | str | Document origin city. |
| location_state | str | Document origin state. |
| sender | str | Correspondence sender. |
| recipient | str | Correspondence recipient. |
| intent | str | Action/purpose of the letter (Renamed from transaction). |
| mentioned_states | list[str] | Full names of nation states mentioned. |
| mentioned_organisations | list[str] | Organizations mentioned. |
| mentioned_cities | list[str] | Cities mentioned. |
| references | list[str] | Other archive reference codes mentioned. |
| tags | list[str] | Arbitrary keywords (3-8). |

## Frontmatter Structure (Output)
The YAML block at the top of the generated Markdown file.

1. `title`
2. `summary`
3. `pages` (Extracted from source Markdown headers)
4. `sender`
5. `recipient`
6. `intent`
7. `author_name`
6. `author_institution`
7. `date`
8. `archive_code`
9. `language`
10. `location_city`
11. `location_state`
12. `source` (Link to PDF)

## Callout Structure (Output)
The Obsidian callout at the top of the note body.

- **Title** (Optional header)
- **Abstract** (Body text)
- **Mentioned Entities** (Section with hierarchical tags: `#State/`, `#Org/`, `#City/`)
- **Categories/Topics** (Optional section for LLM-extracted topics)
- **Tags** (Section for flat tags)
