# Quickstart: Refine Obsidian Metadata

## Overview
This feature refines the metadata extraction process to better suit Obsidian's requirements and user preferences.

## Key Changes
1. **Simplified Frontmatter**: `correspondence_` prefixes are removed.
2. **Body Integration**: The document title (`# Title`) and abstract are moved to the top of the markdown body.
3. **Obsidian Compatibility**: Numeric tags (e.g., `1968`) are automatically converted to `Year1968`.
4. **Cleaner Output**: Empty fields are omitted from the frontmatter.

## Usage
Run the metadata extraction using the `metadata` command:

```bash
python -m ocrpolish.cli metadata NATO_NPG NATO_NPG_metadata --model gemma4:e4b --pdf-dir NATO_NPG_metadata/pdf --vault-root NATO_NPG_metadata
```

The tool will automatically apply the new formatting rules.

## Verification
1. Check the frontmatter for any remaining `correspondence_` fields (there should be none).
2. Verify that the title appears as a `#` header at the very top of the body.
3. Verify that the abstract follows the title.
4. Check that a `---` horizontal rule separates the abstract from the original text.
5. Confirm that any year-like tags in the frontmatter start with `Year`.
