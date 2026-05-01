# Research: Obsidian Export Enhancement

## Decision: Metadata Schema Updates
- **Decision**: Update `MetadataSchema` in `ocrpolish/models/metadata.py`.
- **Rationale**: 
    - Rename `transaction` to `correspondence` as requested.
    - Add `mentioned_cities: list[str]` to capture cities.
    - `pages` will NOT be in `MetadataSchema` because it is extracted directly from the source Markdown headers, not by the LLM. It will be added to the frontmatter during the processing phase.
- **Alternatives considered**: Keeping `transaction` for backward compatibility, but the user explicitly requested renaming.

## Decision: Hierarchical Tag Format
- **Decision**: Implement hierarchical tags in `ocrpolish/processor_metadata.py` and `ocrpolish/utils/metadata.py`.
- **Format**:
    - `#State/UK`
    - `#Org/EU`
    - `#City/UK/London`
- **Rationale**: This follows Obsidian's hierarchical tag convention and the user's specific examples.
- **Special Characters**: Spaces in names will be replaced with hyphens (e.g., `#State/United-Kingdom`).

## Decision: Page Extraction Logic
- **Decision**: Use a regex to find all headers matching `# Page \d+` and pick the last one.
- **Rationale**: The user specified "the last # Page XXX header".
- **Implementation**: 
    ```python
    page_headers = re.findall(r"^# Page (\d+)", content, re.MULTILINE)
    pages = int(page_headers[-1]) if page_headers else None
    ```

## Decision: Frontmatter and Callout Structure
- **Decision**: 
    1. `pages` field placed immediately after `summary` in YAML.
    2. Remove all `mentioned_*` from YAML.
    3. Create a "Mentioned Entities" (or similar) section in the Callout to store the hierarchical tags.
- **Rationale**: User explicitly requested this structural change to keep the frontmatter clean.

## Decision: Default Language
- **Decision**: Force "English" in the Ollama prompt for all metadata unless overridden.
- **Rationale**: Requirement FR-009.
