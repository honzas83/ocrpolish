# Feature Specification: Obsidian Export Enhancement

**Feature Branch**: `013-obsidian-export-enhancement`  
**Created**: 2026-04-30  
**Status**: Draft  
**Input**: User description: "Now, we will further improve the Obsidian export: We will switch the mentioned states and mentioned organizations to tags. The will get a new section in the Callout. Name the tags like #State/UK or #Org/EU . Also add the City named entity and tags like #City/UK/London . Rename the tag transaction: to correspondence: Use English for all metadata if not specified otherwise (on command line). Add number of pages attribute into the frontmatter just after the summary: field. Remove the mentioned_* fields from the frontmatter (the content will be moved to Callout)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Hierarchical Metadata Tags (Priority: P1)

As a researcher using Obsidian, I want my mentioned entities (States, Organizations, and Cities) to be automatically formatted as hierarchical tags. This allows me to use Obsidian's powerful tag filtering and graph view to explore connections between different documents based on geography and organizational involvement.

**Why this priority**: This is the core functional change requested for metadata organization, enabling the primary "Obsidian-native" experience.

**Independent Test**: Can be verified by processing a document containing known locations and organizations and checking the generated Markdown file for valid Obsidian tags (e.g., `#State/UK`, `#City/UK/London`).

**Acceptance Scenarios**:

1. **Given** a document with "United Kingdom" and "London" identified, **When** exported to Obsidian, **Then** the file should contain the tags `#State/UK` and `#City/UK/London`.
2. **Given** a document with "European Union" identified, **When** exported to Obsidian, **Then** the file should contain the tag `#Org/EU`.

---

### User Story 2 - Clean Frontmatter and Enhanced Callout (Priority: P2)

As a researcher, I want the frontmatter of my notes to be concise and focused on core document metadata, while descriptive lists of entities are moved into the body of the note (inside a Callout). This makes the note more readable and visually appealing within Obsidian.

**Why this priority**: This improves the user interface and structural organization of the generated notes, separating high-level metadata from granular entity lists.

**Independent Test**: Can be verified by inspecting the YAML frontmatter and the Callout block of a generated Markdown file to ensure `mentioned_*` fields are absent from the former and present in the latter.

**Acceptance Scenarios**:

1. **Given** an extraction result and an input Markdown file, **When** generating the Obsidian file, **Then** the frontmatter must include `pages` (extracted from the last `# Page XXX` header in the source) after `summary`, and the `mentioned_states` and `mentioned_organizations` lists must be moved to a section in the Callout block.
2. **Given** the current field `transaction`, **When** exported, **Then** it must be renamed to `correspondence` in the frontmatter.

---

### User Story 3 - Language Consistency (Priority: P3)

As a user, I want all metadata fields and extracted values to be in English by default, regardless of the source document's language, unless I specifically request a different language.

**Why this priority**: Ensures a consistent and searchable metadata schema across a diverse document collection.

**Independent Test**: Process a non-English document and verify that the frontmatter keys and entity categories (e.g., "State", "Org", "City") are in English.

**Acceptance Scenarios**:

1. **Given** a document in any language, **When** no specific language is requested, **Then** the metadata fields (e.g., `summary`, `correspondence`, `pages`) and tag prefixes (e.g., `#State/`) must be in English.

### Edge Cases

- **Missing Parent State**: If a `City` is identified but its parent `State` is not clearly identified or missing from the `mentioned_states` list, the system should either omit the state level (e.g., `#City/Unknown/London`) or try to infer it if possible.
- **Special Characters**: Entities containing spaces or special characters (e.g., "United Kingdom", "New York") must be handled correctly for tags (e.g., using hyphens or underscores: `#State/United-Kingdom` or `#State/UK` if abbreviated).
- **Missing Page Headers**: If no header matching `# Page [Number]` is found in the input Markdown, the `pages` field should either be omitted or set to a default value (e.g., total document page count if available from other metadata).
- **Missing Summary**: If the `summary` field is empty or missing, `pages` should still be placed at the top of the metadata section where `summary` would normally be.
- **Empty Entity Lists**: If no states, organizations, or cities are found, the "Tags" section in the Callout should either be omitted or display a placeholder.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST convert `mentioned_states` into hierarchical tags with the prefix `#State/` (e.g., `#State/UK`).
- **FR-002**: System MUST convert `mentioned_organizations` into hierarchical tags with the prefix `#Org/` (e.g., `#Org/EU`).
- **FR-003**: System MUST identify and extract a new named entity: `City`.
- **FR-004**: System MUST convert `City` entities into hierarchical tags including the parent state (e.g., `#City/UK/London`).
- **FR-005**: System MUST rename the frontmatter field `transaction:` to `intent:`.
- **FR-006**: System MUST add the `pages` attribute to the YAML frontmatter, positioned immediately after the `summary:` field.
- **FR-010**: System MUST extract the value for `pages` from the input Markdown by identifying the last occurrence of a header matching the pattern `# Page [Number]`.
- **FR-007**: System MUST remove all `mentioned_*` fields from the YAML frontmatter.
- **FR-008**: System MUST include a new section in the Obsidian Callout specifically for the tags generated from mentioned entities.
- **FR-009**: System MUST use English for all metadata keys and extracted entity types by default.

### Key Entities *(include if feature involves data)*

- **State**: A country or sovereign state mentioned in the document.
- **Organization**: An agency, department, or international body mentioned in the document.
- **City**: A specific city or municipality mentioned in the document, associated with a State.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of mentioned states, organizations, and cities are represented as tags in the output Markdown.
- **SC-002**: `City` tags correctly follow the `#City/<State>/<City>` hierarchy.
- **SC-003**: The YAML frontmatter contains exactly `summary`, `pages`, `intent`, and other existing core fields, in the specified order.
- **SC-004**: No `mentioned_*` fields are present in the YAML frontmatter of the final output.
- **SC-005**: All metadata keys are in English by default.
