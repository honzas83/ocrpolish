# Feature Specification: Refine Obsidian Markdown Metadata

**Feature Branch**: `010-refine-obsidian-metadata`  
**Created**: 2026-04-29  
**Status**: Draft  
**Input**: User description: "Simple obsidian changes: rename correspondence --> remove the correspondence_ prefix summary - a single sentence instead of two abstract - only in the body remove empty attributes tag 1968 --> Year1968, Obsidian does not like only number"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Metadata Cleanup and Standardization (Priority: P1)

As a researcher using Obsidian, I want my extracted markdown files to have clean, standardized metadata so that they are fully compatible with Obsidian's features and easier to read.

**Why this priority**: This is the core request, ensuring metadata is correctly formatted for the target tool (Obsidian).

**Independent Test**: Can be tested by running the metadata extraction on a sample document and verifying that the resulting markdown frontmatter has the `correspondence_` prefixes removed, no empty fields, and correctly formatted year tags.

**Acceptance Scenarios**:

1. **Given** a source document with a frontmatter key `correspondence_date`, **When** metadata is extracted, **Then** the resulting frontmatter key should be `date`.
2. **Given** a frontmatter field that is empty (e.g., `author: ""`), **When** metadata is extracted, **Then** the `author` field should be omitted from the frontmatter.
3. **Given** a tag value of `1968`, **When** metadata is extracted, **Then** the tag should be formatted as `Year1968` in the Obsidian tags section.

---

### User Story 2 - Content Structure Refinement (Priority: P2)

As a researcher, I want the summary and abstract to be presented in a specific format to improve readability and consistency across my notes.

**Why this priority**: Improves the utility of the extracted information by ensuring it fits the user's preferred layout.

**Independent Test**: Verify that the summary in the frontmatter is a single sentence and that the abstract is present in the markdown body but absent from the frontmatter.

**Acceptance Scenarios**:

1. **Given** an extracted summary consisting of multiple sentences, **When** the markdown is generated, **Then** only the first sentence (or a consolidated single sentence) should be present in the `summary` frontmatter field.
2. **Given** an extracted abstract, **When** the markdown is generated, **Then** the abstract should appear at the beginning of the file body and NOT in the YAML frontmatter.

---

### Edge Cases

- **Multiple Tags**: If there are multiple numeric tags (e.g., `1968`, `1970`), all should be prefixed with `Year`.
- **Nested Prefix**: If a key is `correspondence_subject_line`, it should become `subject_line`.
- **Empty Abstract**: If no abstract is extracted, no abstract section should be added to the body.
- **Summary Truncation**: If the summary is a single long sentence with multiple clauses, it should remain intact unless it contains period-delimited sentences.

## Assumptions

- **Rename Correspondence**: It is assumed that renaming "correspondence" refers specifically to removing the `correspondence_` prefix from YAML frontmatter keys, as this is a common pattern in metadata refinement.
- **Summary Truncation**: "Single sentence" is interpreted as taking the text up to the first period (exclusive of abbreviations) or using a consolidated sentence if the source summary is multi-sentence.
- **Abstract Placement**: The abstract will be placed at the very top of the markdown body, before any other content.
- **Empty Attributes**: An attribute is considered "empty" if its value is an empty string, an empty list, `null`, or consists only of whitespace.
- **Year Tags**: Only numeric tags consisting entirely of digits (e.g., `1968`) will be prefixed with `Year`.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST rename all frontmatter keys starting with `correspondence_` by removing that prefix (e.g., `correspondence_from` -> `from`).
- **FR-002**: The system MUST ensure the `summary` metadata field contains only a single sentence.
- **FR-003**: The system MUST remove the `abstract` field from the YAML frontmatter.
- **FR-004**: The system MUST insert the `title` and `abstract` text into an Obsidian `[!abstract]` callout block at the start of the markdown body.
- **FR-007**: The system MUST insert the extracted `title` as a level 1 header (e.g., `# Title`) inside the callout block, followed by the `abstract` text.
- **FR-008**: The system MUST ensure there is an empty line between the YAML frontmatter and the callout block, and another empty line between the callout block and the original body content.
- **FR-009**: The system MUST NOT insert a horizontal rule (`---`) after the callout block.
- **FR-010**: The system MUST aggressively clean the original document body by removing any leading horizontal rules or duplicate titles (plain text or Markdown headers) that match the extracted title.
- **FR-005**: The system MUST remove any metadata attributes (YAML keys) that have empty or null values.
- **FR-006**: The system MUST transform any numeric-only tags (e.g., `1968`) by prefixing them with `Year` (e.g., `Year1968`) to ensure Obsidian compatibility.

### Key Entities

- **Markdown File**: The final output containing YAML frontmatter and markdown body.
- **Frontmatter**: The metadata block at the top of the markdown file.
- **Tags**: Metadata labels used for organization in Obsidian.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of frontmatter keys starting with `correspondence_` are successfully renamed in the output files.
- **SC-002**: 100% of numeric tags in the output markdown are prefixed with `Year`.
- **SC-003**: Empty attributes are present in 0% of the final generated frontmatter blocks.
- **SC-004**: The `abstract` field is absent from the frontmatter in all output files where an abstract was extracted.
- **SC-005**: The `summary` field in the frontmatter never exceeds a single sentence.
