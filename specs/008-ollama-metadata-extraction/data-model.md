# Data Model: Metadata Extraction

## MetadataSchema (Pydantic Model)

The `MetadataSchema` defines the structure of the metadata extracted by the LLM and stored in the YAML frontmatter. All fields are required with defaults to ensure compatibility with local LLM grammar engines.

| Field | Type | Description |
|-------|------|-------------|
| `title` | `str` | The formal title of the document. Extracted carefully from first two pages. |
| `summary` | `str` | Concise summary (exactly two sentences). Independent entity. |
| `abstract` | `str` | Detailed overview (superset of summary, max 20 sentences). Independent entity. |
| `author_name` | `str` | The individual who wrote the document. |
| `author_institution` | `str` | The organization or institution responsible. |
| `date` | `str` | The primary date of the document (ISO 8601: `YYYY-MM-DD`). |
| `archive_code` | `str` | Code in format `NPG/D(77)12`. |
| `language` | `str` | Primary language of the document (default: "English"). |
| `location_city` | `str` | The city where the document originated. |
| `location_state` | `str` | The nation-state where the document originated (inferred from city if possible). |
| `correspondence_sender` | `str` | Sender of the letter (flattened for LLM grammar). |
| `correspondence_recipient` | `str` | Recipient of the letter (flattened for LLM grammar). |
| `correspondence_transaction` | `str` | Purpose or action imposed by the letter (flattened). |
| `mentioned_states` | `List[str]` | Full names of national states mentioned. |
| `mentioned_organisations`| `List[str]` | Organizations mentioned (e.g., NATO, European Community). |
| `references` | `List[str]` | Other archive reference codes mentioned (e.g., C-M(55)15). |
| `tags` | `List[str]` | 3-8 specific thematic tags to interconnect documents. |

### Field Ordering in YAML
The output YAML frontmatter is strictly ordered:
1. `title`, `summary`, `abstract`, `author_name`, `author_institution`
2. `correspondence` (a nested block containing `sender`, `recipient`, `transaction` if valid)
3. `date`, `archive_code`, `language`, `location_city`, `location_state`
4. `mentioned_states`, `mentioned_organisations`, `references`, `tags`

### Validation & Transformation Rules
- **Acronyms**: Preserve uppercase for whitelisted acronyms: `NATO, NPG, DPC, NAC, SHAPE, SACEUR, SACLANT, WP`.
- **Title Case**: All names, titles, and cities are converted to Title Case if extracted in ALL CAPS.
- **Independence**: Abbreviations defined in `summary` must be redefined in `abstract`.
- **Empty Fields**: "N/A" is invalid; fields are left empty if data is missing. The `correspondence` block is omitted if all its sub-fields are empty or "N/A".
- **Date Extraction**: 2-pass logic; if date is missing from first 6000 chars of a large document, scan the last 6000 chars.

### State Transitions
- **Input**: Raw Markdown text (OCR output).
- **Intermediate**: Flattened Pydantic model validated against Ollama JSON output.
- **Transformation**: Title Case normalization, Acronym preservation, Correspondence nesting.
- **Output**: Clean YAML frontmatter (exactly one `---` block) prepended to the Markdown content.
