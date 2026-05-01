# Quickstart: Obsidian Export Enhancement

This feature improves how metadata and mentioned entities are exported to Obsidian Markdown files.

## New Metadata Fields
- `pages`: Extracted from `# Page XXX` headers in the input file.
- `intent`: Renamed from `transaction`.
- `mentioned_cities`: New entity extraction for cities.

## Hierarchical Tagging
Mentioned entities are now converted to tags in the following format:
- States: `#State/United-Kingdom`
- Organizations: `#Org/NATO`
- Cities: `#City/United-Kingdom/London` (Note: LLM extracts city with its correct state).

## Usage
Run the metadata processor as usual:
```bash
python -m ocrpolish.cli metadata data/input data/output --vault-root /path/to/vault
```

The output Markdown files will now feature a cleaner frontmatter (no `mentioned_*` fields) and an enhanced Callout section containing the hierarchical tags.
