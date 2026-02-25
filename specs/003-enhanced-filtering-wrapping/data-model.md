# Data Model: Enhanced OCR Filtering

## Entities

### ProcessingConfig (Updated)
The runtime configuration will be extended to support fuzzy matching and dry-run modes.

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `similarity_threshold` | `float` | Jaccard similarity threshold for word-set overlap. | `0.9` |
| `min_file_frequency` | `float` | Minimum fraction of files a line must appear in to be dropped. | `0.1` |
| `dry_run` | `bool` | If true, do not write primary output, only logs and filtered files. | `False` |
| `save_filtered` | `bool` | If true, save dropped lines to `.filtered.md`. | `True` |

### BoilerplateCandidate
Represents a line identified as potential boilerplate across the corpus.

| Field | Type | Description |
|-------|------|-------------|
| `word_set` | `frozenset[str]` | The unique set of normalized words in the line. |
| `raw_line` | `str` | The first occurrence of the line as seen in the corpus. |
| `file_count` | `int` | Number of unique files this word-set was found in. |
| `is_dropped` | `bool` | Final decision based on frequency and similarity. |

## State Transitions
1. **Pass 1 (Counting)**: Collect `word_set` from every line in every file. Count unique file occurrences.
2. **Analysis**: Mark `BoilerplateCandidate` as `is_dropped` if `file_count / total_files > min_file_frequency`.
3. **Pass 2 (Cleaning)**: For each line in a file, calculate Jaccard similarity against all `is_dropped` candidates. If similarity > `similarity_threshold`, drop the line and add to sidecar.
