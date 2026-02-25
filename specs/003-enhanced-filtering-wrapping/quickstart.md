# Quickstart: Enhanced OCR Filtering

This guide covers the new fuzzy statistical filtering and improved paragraph wrapping in `ocrpolish`.

## 1. Fuzzy Boilerplate Removal

Unlike the previous version which required exact matches, the new filter uses "word-set overlap". This is effective against OCR noise.

```bash
# Detect boilerplate that appears in at least 10% of files
# with a 90% word overlap.
python -m ocrpolish.cli ./input ./output --threshold 0.1 --similarity 0.9
```

## 2. Paragraph Wrapping

The tool now automatically wraps lines that start with `<` or `[` markup, and ensures a blank line separation between paragraphs.

**Input:**
```text
<PAGE 1>
[SECRET]
This is a very long line of text that should be wrapped into multiple lines to improve readability.
This is another line that continues the paragraph.
```

**Output:**
```text
<PAGE 1>

[SECRET]

This is a very long line of text that should be wrapped into multiple lines
to improve readability. This is another line that continues the paragraph.
```

## 3. Auditing Dropped Lines

Every processed file `document.md` will have a corresponding `document.md.filtered.md` in the output directory if any lines were dropped.

```bash
# View what was removed
cat ./output/document.md.filtered.md
```

## 4. Dry Run

To see what would be filtered without actually writing the cleaned files:

```bash
python -m ocrpolish.cli ./input ./output --dry-run
```
