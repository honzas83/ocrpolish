# CLI Contract: Dynamic Headers and Footers for DOCX

## Enhanced Functionality for `--docx`

When the `--docx` flag is used, the system will automatically:
- Search for page numbers in formats `- X -` or `-X-`.
- Analyze the document for recurring headers and footers (80% threshold).
- Move these items into the DOCX metadata (header/footer) and remove them from the body.

## New Optional Argument

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--scan-paragraphs` | integer | `3` | The number of paragraphs at the top and bottom of each page to scan for potential headers/footers. |

## Expected Behavior
- No new flags are required to enable basic header/footer/page-number extraction; it is bundled with `--docx`.
- The extracted content will be removed from the main body paragraphs in the output DOCX.
