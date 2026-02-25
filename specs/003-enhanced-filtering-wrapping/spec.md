# Feature Specification: Enhanced OCR Filtering and Paragraph Wrapping

**Feature Branch**: `003-enhanced-filtering-wrapping`  
**Created**: 2026-02-16  
**Status**: Draft  
**Input**: User description: "After the paragraph is wrapped, add a newline to separate the following paragraph For statistical filtering, do not use the exact match, but use the set of words on the line and the overlap and specificity of this overlap -- if it occur in multiple files multiple times, it is candidate to drop. If there are some lines dropped from the source, create an additional output file containing the filtered lines so that no information is lost. Wrap also lines, that start with markup, also add newline."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Clean Paragraph Separation (Priority: P1)

As a researcher, I want my OCR-processed text to have clear paragraph boundaries and proper wrapping so that the text is readable and correctly formatted for analysis.

**Why this priority**: Correct paragraph structure is the fundamental goal of this post-processing tool.

**Independent Test**: Process a file with long, unwrapped paragraphs and verify that they are wrapped to a standard width and separated by exactly one blank line.

**Acceptance Scenarios**:

1. **Given** a text file with long lines representing single paragraphs, **When** processed, **Then** lines are wrapped and a blank line is inserted between the end of one paragraph and the start of the next.
2. **Given** lines that start with markup (e.g., `<PAGE>`, `[Header]`), **When** processed, **Then** these lines are also subject to wrapping logic and followed by a newline if they represent a block of text.

---

### User Story 2 - Statistical Boilerplate Removal (Priority: P2)

As a researcher processing thousands of OCR files, I want to automatically remove recurring headers, footers, and other boilerplate that appears across many files so that I only see the unique content.

**Why this priority**: Reduces noise in large-scale text analysis.

**Independent Test**: Process a set of files containing the same recurring "Confidential" footer and verify that the footer is removed from the primary output.

**Acceptance Scenarios**:

1. **Given** a collection of files where certain word sets appear frequently across different files, **When** statistical filtering is enabled, **Then** lines matching these word sets (based on overlap/specificity) are removed from the main output.
2. **Given** a line that is similar but not identical to a recurring boilerplate line (e.g., "Page 1" vs "Page 2"), **When** processed, **Then** the statistical filter correctly identifies the recurring pattern and removes it.

---

### User Story 3 - Data Preservation for Filtered Content (Priority: P3)

As a researcher, I want to ensure that no information is lost during filtering, so I can audit what was removed.

**Why this priority**: Compliance and auditability; ensuring no "false positives" result in permanent data loss.

**Independent Test**: Process a file where lines are dropped and verify that a secondary file is created containing exactly those dropped lines.

**Acceptance Scenarios**:

1. **Given** a processing run that filters out 5 lines of boilerplate, **When** completed, **Then** a sidecar file is created containing those 5 lines with their original context or file reference.

---

### Edge Cases

- **Mixed Markup and Text**: How should the system handle lines that start with markup but contain very little text?
- **Small Corpus**: How does statistical filtering behave when only a few files are processed (low sample size)?
- **High Overlap but Unique Content**: How to avoid dropping lines that are legitimately frequent but important (e.g., common greetings in correspondence)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST wrap lines to a configurable width (defaulting to a standard, e.g., 80 characters).
- **FR-002**: System MUST ensure that every wrapped paragraph is followed by exactly one blank line (two newlines).
- **FR-003**: System MUST identify and wrap lines starting with tag-like markup characters (specifically `<` or `[`).
- **FR-004**: System MUST implement a fuzzy statistical filter that identifies candidate lines for removal based on word-set overlap across a corpus of files.
- **FR-005**: The statistical filter MUST use a high-precision default threshold, dropping lines with >90% word overlap that appear in more than 10% of the files in the corpus.
- **FR-006**: System MUST create a companion "filtered" output file for every source file that had lines removed, containing the dropped content.
- **FR-007**: System MUST allow users to run the statistical filter in a "dry run" mode to preview what will be dropped.

### Key Entities *(include if feature involves data)*

- **Word Set**: A collection of unique words from a single line, used for fuzzy comparison.
- **Corpus Statistics**: A global map of word sets and their frequency across all files in the current run.
- **Filtered Output File**: A secondary file containing lines that were excluded from the primary output.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of wrapped paragraphs in the output are separated by a blank line.
- **SC-002**: The statistical filter identifies and removes at least 90% of identical recurring boilerplate across a test set of 100 files.
- **SC-003**: No more than 1% of unique, non-boilerplate lines are accidentally removed (False Positive Rate).
- **SC-004**: For every line removed from the main output, that exact line is present in the corresponding filtered output file.
