# Feature Specification: Rework Filtering and Wrapping

**Feature Branch**: `004-rework-filtering-wrapping`  
**Created**: 2026-02-25  
**Status**: Completed  
**Input**: User description: "In this feature, we will rework the filtering. First of all, remove all filtering from the existing code. Then, in the output create a special file, that contains ordered list of pairs: (set of line words, count). Use set of line words (remove diacritics, lowercase and split) as a counting key, for output, use the most frequent verbatim string representation. For filtering, we will use a special file, that lists lines, that should be filtered (in the same sense as counting key). Use initial filtering with: DECLASSIFIED - PUBLICLY DISCLOSED NATO SECRET NATO CONFIDENTIAL In the output, everytime you wrap the paragraph, add a empty newline after it. Wrap also lists and bullets."

## Clarifications

### Session 2026-02-25
- Q: Should the frequency report be generated individually for each processed file (sidecar) or as a single consolidated report for the entire processing run? → A: One consolidated frequency report for the entire run.
- Q: Should blank lines be added after each item in a list if it was wrapped, or only after the entire list block? → A: Add blank lines after wrapped items, but not after short items.
- Q: How should the output line in the frequency report be formatted for each entry? → A: [Total Count] ([File Count]): [Verbatim String].
- Q: Should punctuation (like periods, commas, dashes) be removed during normalization to ensure better grouping of noisy lines? → A: Yes, remove all punctuation characters during normalization.
- Q: Should the frequency report include every single unique line pattern found in the archive, or only those that appear at least twice (potential boilerplate)? → A: Only include recurring patterns with a total count greater than 5.
- Q: Matching logic for filtering? → A: Use a 50% word-match threshold. A line is filtered if >= 50% of its words are contained in a filter pattern.
- Q: Case sensitivity? → A: Preserve case during normalization to help differentiate between uppercase boilerplate and normal text.
- Q: Structural markers to ignore? → A: `# Page \d+` and `-\s*\d+\s*-` (e.g., `- 5 -`).
- Q: Table handling? → A: Identify blocks starting with `|`. Align columns based on max width. Do not wrap.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Boilerplate Identification (Priority: P1)

As a researcher processing OCR'd archives, I want to see a consolidated list of recurring lines (like stamps or headers) that remain after my custom filters are applied so that I can refine my filtering strategy.

**Why this priority**: This is the core engine for the new filtering logic and provides the data needed for users to configure their filters across a collection.

**Independent Test**: Can be tested by processing a set of files and verifying the single generated frequency file contains accurate counts of repetitive lines found across all files, excluding structural markers and filtered content.

**Acceptance Scenarios**:

1. **Given** multiple OCR files with the same header "NATO SECRET", **When** processed, **Then** a single consolidated frequency file is created showing "NATO SECRET" with a count corresponding to the total number of occurrences across all files.
2. **Given** lines with minor variations (e.g., "NATO SECRET." and "NATO SECRET"), **When** counted, **Then** they are grouped under the same key (punctuation ignored) and the most frequent verbatim version is shown.
3. **Given** structural markers like "- 5 -", **When** processed, **Then** they are preserved in the document but NOT included in the frequency report.

---

### User Story 2 - Customizable Content Filtering (Priority: P1)

As a researcher, I want to exclude specific repetitive lines (boilerplate) from the processed text based on a configuration file using a robust word-matching threshold.

**Why this priority**: This fulfills the primary request to rework filtering to be more flexible and data-driven rather than hardcoded.

**Independent Test**: Can be tested by adding a line to the filter file and verifying it no longer appears in the output of a processed document, while ensuring long paragraphs containing those words are preserved.

**Acceptance Scenarios**:

1. **Given** a filter file containing "DECLASSIFIED", **When** a document containing a short line "DECLASSIFIED - PUBLICLY DISCLOSED" is processed, **Then** that line is removed (as >50% words match).
2. **Given** a long paragraph containing "DECLASSIFIED", **When** processed, **Then** the paragraph is preserved (as <50% words match).
3. **Given** no filter file, **When** processed, **Then** zero lines are filtered by default.

---

### User Story 3 - Readable Text Layout (Priority: P2)

As a reader of the processed text, I want paragraphs and lists to be properly wrapped and separated by blank lines so that the text is easy to read on modern screens.

**Why this priority**: Improves the usability and aesthetic quality of the output, which is a key requirement for the "polishing" aspect of the tool.

**Independent Test**: Can be tested by processing a long un-wrapped paragraph and verifying the output is wrapped to the target width and followed by an empty line.

**Acceptance Scenarios**:

1. **Given** a long paragraph, **When** wrapped, **Then** a single empty newline is appended after the final line of the paragraph.
2. **Given** a bulleted list with both long (wrapped) and short items, **When** processed, **Then** a blank line is added after each wrapped item, but not after the short items.

---

### User Story 4 - Aligned Table Formatting (Priority: P2)

As a reader of the processed text, I want markdown tables to have perfectly aligned columns so that tabular data is easy to scan and professional in appearance.

**Why this priority**: Enhances the visual quality of OCR documents that contain complex tables.

**Independent Test**: Can be tested by processing a document with a table containing varying cell lengths and verifying that all column separators (`|`) are vertically aligned in the output.

**Acceptance Scenarios**:

1. **Given** a markdown table with varying content lengths, **When** processed, **Then** every column is padded to the width of its longest cell.
2. **Given** a header separator line (e.g., `|---|`), **When** formatted, **Then** it is expanded to match the aligned column width.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST remove all existing hardcoded filtering logic from the codebase.
- **FR-002**: System MUST generate a single consolidated frequency report file for each processing run.
- **FR-003**: System MUST calculate line frequency using a normalized key: diacritics removed, punctuation removed, and split into a set of words. **Case MUST be preserved.**
- **FR-004**: System MUST accumulate frequencies AFTER filtering is applied, but BEFORE lines are wrapped.
- **FR-005**: System MUST output the consolidated frequency list as ordered pairs, ordered by frequency descending.
- **FR-006**: System MUST read a filter list from a specified file where each line represents a pattern to be excluded.
- **FR-007**: System MUST NOT apply any filtering by default if no filter file is provided.
- **FR-008**: System MUST apply a 0.5 threshold for filtering: a line is dropped if at least 50% of its words are found in a filter pattern.
- **FR-009**: System MUST apply line wrapping to paragraphs, lists, and bullet points, adding a blank line only after blocks that were actually wrapped.
- **FR-010**: System MUST output the frequency list as a plain text file where each line consists of the total occurrence count, the number of files it appeared in, and the most frequent verbatim string representation (Format: "TotalCount (FileCount): Verbatim"). Only patterns with a TotalCount > 5 MUST be included.
- **FR-011**: System MUST ignore structural markers in the frequency report: `# Page \d+` and `-\s*\d+\s*-`.
- **FR-012**: System MUST identify consecutive lines starting with `|` as a table block.
- **FR-013**: System MUST format table blocks by aligning column separators and padding cells to the maximum width of each column.
- **FR-014**: System MUST NOT apply word-wrapping to table blocks.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of lines meeting the 50% word-match threshold against the filter list are removed.
- **SC-002**: Frequency files accurately preserve case and group lines that differ only by punctuation or diacritics.
- **SC-003**: Every wrapped paragraph or wrapped list item in the output is followed by exactly one empty line.
- **SC-004**: Structural markers are never present in the frequency report but are preserved in the text output.
- **SC-005**: 100% of markdown tables in the output have perfectly aligned column separators.
