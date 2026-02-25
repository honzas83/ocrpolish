# Research: Enhanced OCR Filtering and Paragraph Wrapping

## Problem: Statistical Filtering with Fuzzy Matching

Current implementation uses exact string matching for identifying global headers/footers. This is brittle as OCR often has minor variations (e.g., "Page 1" vs "Page 2" or "Confidential" vs "Confldential").

### Decision: Jaccard Similarity on Word Sets

**What was chosen**: Jaccard similarity between sets of words.
**Rationale**:
- It ignores word order, which is often scrambled in OCR.
- It handles "overlap and specificity" by looking at the intersection divided by the union.
- Easy to implement and relatively efficient for short lines.

**Implementation Detail**:
- For each line, tokenize into a set of lowercased words (excluding stop words if necessary, but for headers/footers, all words usually matter).
- Calculate "Overlap" as $|A \cap B| / \min(|A|, |B|)$ to find if one line is mostly contained in another.
- Calculate "Specificity" as the rarity of the words in the overlap.

### Decision: Inverted Index for Global Frequency

**What was chosen**: An inverted index mapping word sets (or hashes) to file counts.
**Rationale**: Comparing every line in every file against every other line is $O(N^2)$ and doesn't scale.
**Alternative**: MinHash/LSH (Locality Sensitive Hashing) was considered but might be overkill for the expected number of lines and files (thousands, not millions).

## Problem: Data Preservation (Filtered Output)

### Decision: Sidecar Filtered Files

**What was chosen**: Create `<filename>.filtered.md` in the output directory.
**Rationale**: Preserves the original context and allows easy `diff` between cleaned and raw text.

## Problem: Paragraph Wrapping with Newlines

### Decision: Update `wrap_lines` and `clean_lines`

**What was chosen**:
1. Modify `wrap_lines` to ensure it treats lines starting with `<` or `[` as wrappable (removing them from `should_protect_line` if they were there, or explicitly including them).
2. Modify the final pass in `clean_lines` to ensure that every wrapped block is followed by an extra newline.
