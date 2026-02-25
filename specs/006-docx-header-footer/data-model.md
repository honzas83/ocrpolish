# Data Model: Dynamic Headers and Footers for DOCX

## Entities

### PageMetadata
Represents the metadata extracted from a single page.
- `page_number`: optional integer (extracted from - X - or -X-)
- `header_candidates`: list of strings (first $N$ paragraphs)
- `footer_candidates`: list of strings (last $N$ paragraphs)
- `body_content`: list of strings (remaining paragraphs after extraction)

### FileProcessingContext
Stores the recurring patterns identified across all pages of a single file.
- `file_path`: string
- `header_counts`: Counter (frequency of strings in top 3 paragraphs)
- `footer_counts`: Counter (frequency of strings in bottom 3 paragraphs)
- `identified_header`: optional string (string that passed the 80% threshold)
- `identified_footer`: optional string (string that passed the 80% threshold)
- `page_metadata_list`: list of PageMetadata (for the second pass)

## Relationships
- A `FileProcessingContext` contains multiple `PageMetadata` objects.
- Each `PageMetadata` object corresponds to one page within the document.

## Validation Rules
- Page numbers MUST be extracted if they match `- X -` or `-X-` patterns.
- Repeated strings MUST meet the 80% threshold to be moved to the header/footer.
- Extracted headers/footers MUST be removed from the DOCX body.
