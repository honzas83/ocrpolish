# Data Model: Rework Filtering and Wrapping

## Entities

### `LinePattern`
- **Description**: A normalized representation of a line of text used for comparison and counting.
- **Fields**:
  - `normalized_words`: `frozenset[str]` (Diacritics removed, punctuation removed, split into words). **Case preserved.**
- **Validation**:
  - Must not be empty after normalization to be counted as a pattern.

### `FrequencyReport`
- **Description**: An ordered list of recurring line patterns remaining after filtering.
- **Fields**:
  - `items`: `list[FrequencyEntry]` (Ordered by total count descending).
- **Format**: Plain text list: `TotalCount (FileCount): VerbatimString`.
- **Filtering**: Patterns with `TotalCount > 5` are included. Structural markers are ignored.

### `FrequencyEntry`
- **Fields**:
  - `total_count`: `int`
  - `file_count`: `int`
  - `most_frequent_verbatim`: `str`

### `FilterList`
- **Description**: A set of `LinePattern` objects designated for exclusion.
- **Source**: User-provided file. Empty by default.

### `ProcessingConfig` (Updated)
- **New Fields**:
  - `filter_file_path`: `Optional[Path]`
  - `frequency_file_path`: `Path` (default: `frequency.txt`). Relative to CWD if path provided, otherwise output root.

## Logic Flow

1. **Initialization**:
   - Create a global `FrequencyStore`.
   - Load `FilterList` only if path provided.

2. **Processing Loop (Per File)**:
   - Read lines.
   - **Step 1: Filter**: Drop lines if $|L \cap F| \ge 0.5 \times |L|$.
   - **Step 2: Accumulate**: Update `FrequencyStore` with remaining lines (skip structural markers).
   - **Step 3: Layout**: Wrap kept lines. Format blocks with blank line rules.
   - **Step 4: Save**: Write processed content and sidecar `.filtered.md`.

3. **Report Generation**:
   - Write `FrequencyReport` to disk.
