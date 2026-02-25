# Research: Dynamic Headers and Footers for DOCX

## Decision: Two-Pass File-Level Analysis
- **Rationale**: To identify repeated strings at the top/bottom of pages across a whole file (with an 80% threshold), the tool must first scan all pages of that file to collect candidates and their frequencies before performing the final DOCX generation.
- **Implementation**: 
  - Pass 1: Scan each page, extract the first/last $N$ paragraphs, and update a frequency counter for that specific file.
  - Pass 2: During DOCX generation, check each page's first/last paragraphs against the identified "global" headers/footers and move them if they meet the threshold.

## Decision: Header/Footer Implementation in `python-docx`
- **Rationale**: `python-docx` supports accessing and modifying headers and footers via `section.header` and `section.footer`. 
- **Details**: 
  - We will use the `different_first_page_header_footer` property if we want to handle the first page specifically, but the requirement suggests a consistent header/footer based on repeated strings across the *entire* document (80% threshold).
  - Page numbers will be extracted and placed in the header/footer. 

## Decision: Page Number Extraction
- **Rationale**: Use regex `r"^\s*-\s*(\d+)\s*-\s*$"` and `r"^\s*-(\d+)-\s*$"` to detect standalone page numbers.
- **Cleanup**: If a line matches, the entire line is removed from the body content.

## Decision: Handling "Minor Variations" in Repeated Strings
- **Rationale**: For the initial implementation, we will use **exact string matching** (after stripping whitespace) to identify repeated headers/footers.
- **Alternatives considered**: Fuzzy matching (e.g., Levenshtein distance). 
- **Reasoning**: Exact matching is faster and less prone to false positives in the first iteration. We can reconsider if OCR noise makes exact matching too brittle.

## Decision: Performance Optimization
- **Rationale**: Since we are already splitting Markdown by pages in `ocrpolish/utils/docx_utils.py`, we can perform the first pass during that split or immediately after.
- **Constraint**: Must ensure it doesn't exceed the 5% performance impact target.
