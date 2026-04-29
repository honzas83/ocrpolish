# Research: Refine Obsidian Metadata

## Decision: Rename `correspondence_` prefixes
- **Action**: Update `MetadataSchema` in `ocrpolish/models/metadata.py` to use `sender`, `recipient`, and `transaction` directly, or rename them during the preparation phase in `MetadataProcessor`.
- **Selected**: Update `MetadataSchema` to use the shorter names directly. This simplifies the prompt and the resulting dictionary.
- **Rationale**: Reduces complexity and aligns with the desired final output format early in the pipeline.

## Decision: Single-sentence summary
- **Action**: Update the Ollama prompt in `MetadataProcessor.process_file` to request "exactly one sentence" for the summary.
- **Enforcement**: Add a utility function to truncate the summary to the first sentence if the LLM provides more.
- **Rationale**: Ensures strict adherence to the requirement even if the LLM fails to follow the prompt exactly.

## Decision: Abstract and Title placement
- **Action**: Modify `MetadataProcessor.process_file` to:
    1. Remove `abstract` from the frontmatter dictionary.
    2. Insert `# {title}` as the first line of the body.
    3. Insert the `abstract` text immediately after the title.
    4. Insert a horizontal rule `---` after the abstract.
- **Rationale**: Matches the user's request for Obsidian note structure.

## Decision: Remove empty attributes
- **Action**: Update `MetadataProcessor._prepare_obsidian_metadata` to filter out any keys with empty/null values.
- **Rationale**: Keeps the frontmatter clean and focused.

## Decision: Year tags formatting
- **Action**: Update `normalize_obsidian_tags` in `ocrpolish/utils/metadata.py` to detect numeric-only strings and prefix them with `Year`.
- **Rationale**: Fixes Obsidian's limitation with purely numeric tags.
