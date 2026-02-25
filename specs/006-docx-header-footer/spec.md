# Feature Specification: Dynamic Headers and Footers for DOCX

**Feature Branch**: `006-docx-header-footer`  
**Created**: 2026-02-25  
**Status**: Draft  
**Input**: User description: "Can you add header and footer to DOCX containing the page numbers extracted from the page in format - X - or -X-? And, at the same time, look for strings, that are repeated at the top of the page in the first few paragraphs that can also be part of the page and include them into the page header. The same for footer. The repeated strings must be determined on the file-level"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Page Number Extraction (Priority: P1)

As a researcher, I want the system to find page numbers within my documents (e.g., "- 5 -") and move them into the official Word header/footer, so that the document looks professional and the main body is clean.

**Why this priority**: Essential for maintaining document structure and accessibility.

**Independent Test**: Can be tested by processing a Markdown file containing "- 1 -" on page 1 and "- 2 -" on page 2, then verifying the generated DOCX has these numbers in the header/footer and they are removed from the body.

**Acceptance Scenarios**:

1. **Given** a Markdown file with the text "- 1 -" at the bottom of the first page, **When** processed with `--docx`, **Then** the DOCX should have "1" in the footer/header and "- 1 -" should be absent from the body.
2. **Given** a Markdown file with the text "-1-" at the top of a page, **When** processed, **Then** the DOCX should have "1" in the header and "-1-" should be absent from the body.

---

### User Story 2 - File-Level Header/Footer Detection (Priority: P2)

As a researcher, I want the system to identify recurring text at the top and bottom of pages within a single document (like a report title or classification marker) and move it into the header/footer.

**Why this priority**: Significant improvement in readability and formatting quality for documents with consistent internal metadata.

**Independent Test**: Can be tested by creating a multi-page Markdown file where "SECRET - UNCLASSIFIED" appears in the first paragraph of every page. Verify it moves to the DOCX header.

**Acceptance Scenarios**:

1. **Given** a 3-page Markdown file where the first paragraph of every page is "REPORT 2024", **When** processed, **Then** "REPORT 2024" should be in the DOCX header and removed from the body of each page.
2. **Given** a 3-page Markdown file where the last paragraph of every page is "ARCHIVE 1234", **When** processed, **Then** "ARCHIVE 1234" should be in the DOCX footer and removed from the body.

---

### Edge Cases

- **Inconsistent Page Numbers**: What happens if only some pages have the "- X -" marker? (Assumption: Only the pages with markers get them in the header/footer; body is cleaned only where found).
- **False Positives**: What if a hyphenated list item or math expression looks like "- 1 -"? (Assumption: Only lines that consist *entirely* of the page marker or have it as a distinct paragraph/standalone line are extracted).
- **Minor Variations**: What if the repeated string has extra spaces or minor character differences? (Assumption: Use exact match for now, or very high similarity, within the first/last few paragraphs).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST extract page numbers from patterns matching `- X -` or `-X-` (where X is a number).
- **FR-002**: System MUST identify strings that are repeated at the top of pages (within the first 3 paragraphs) across at least 80% of the document's pages.
- **FR-003**: System MUST identify strings that are repeated at the bottom of pages (within the last 3 paragraphs) across the document.
- **FR-004**: System MUST perform detection on a per-file basis (file-level analysis).
- **FR-005**: System MUST move the extracted page numbers and identified repeated strings into the DOCX header or footer.
- **FR-006**: System MUST remove the extracted text from the main body of the DOCX to prevent duplication.
- **FR-007**: Repeated header/footer detection MUST be configurable regarding the number of paragraphs to scan (default: 3).

### Key Entities *(include if feature involves data)*

- **Page Metadata**: Information extracted from the page (page number, detected header text, detected footer text).
- **File Processing Context**: Stores the recurring patterns identified across all pages of a single file.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of page numbers matching the specified patterns are successfully extracted to DOCX metadata.
- **SC-002**: Standard document headers (classification, titles) repeated on 90% or more of pages are moved to the header in the output.
- **SC-003**: DOCX output body contains no duplicate text that has been moved to headers/footers.
- **SC-004**: No more than 5% performance impact on total DOCX generation time for standard 50-page documents.
