# Research: Rework Filtering and Wrapping

## Diacritics and Punctuation Removal
- **Decision**: Use `unicodedata` for diacritics and `string.punctuation` for punctuation removal.
- **Rationale**: standard library approach ensures portability and performance. Removing punctuation is critical for OCR text where characters like `.` or `,` can be inconsistently recognized in boilerplate.
- **Update**: Character case is **preserved** (no lowercasing) to help differentiate uppercase boilerplate from document content.

## Global Frequency Counting
- **Decision**: Use a dictionary mapping the `LinePattern` (normalized word set) to a tracking object.
- **Tracking Object**:
  - `total_count`: int
  - `file_paths`: set[Path] (to count unique files)
  - `verbatim_counts`: Counter (to find most frequent verbatim form)
- **Execution Order**: Frequencies are accumulated **after** filtering but **before** wrapping. This ensures the report reflects actual content and logical lines.

## Filtering Strategy
- **Decision**: Implement a "half-of-words" threshold match ($|L \cap F| \ge 0.5 \times |L|$).
- **Rationale**: Prevents a short filter pattern from accidentally deleting a long paragraph that merely contains the pattern's words.
- **Default**: No lines are filtered by default unless a filter file is provided.

## Wrapping and Blank Lines
- **Decision**: 
  - Paragraphs: Always add blank line after if wrapped.
  - List items: Add blank line ONLY if the item was wrapped (exceeded width).
- **Implementation**: Unified layout logic in `format_blocks` to ensure consistency.

## Structural Markers
- **Decision**: Explicitly exclude page numbering patterns from the frequency report.
- **Patterns**: `# Page \d+` and `-\s*\d+\s*-`.
