# CLI Contract: Rework Filtering and Wrapping

## Command Signature

```bash
ocrpolish <input_dir> <output_dir> [OPTIONS]
```

## Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--filter-file` | `Path` | `None` | Path to a file containing patterns to exclude. No filtering occurs if omitted. |
| `--frequency-file` | `Path` | `frequency.txt` | Path for the frequency report. Relative to CWD if dir provided, else output root. |
| `--width` | `int` | `80` | Target width for line wrapping. |

## Behavior Changes

### Filtering
- **Threshold**: Matching uses a 50% word-set overlap rule ($|L \cap F| \ge 0.5 \times |L|$).
- **Case Sensitivity**: Normalization **preserves case**, making filters case-sensitive.
- **Default**: Zero lines are filtered unless a `--filter-file` is specified.

### Frequency Reporting
- **Timing**: Generated **after** filtering, but based on **unwrapped** lines.
- **Content**: Format is `TotalCount (FileCount): Verbatim`.
- **Threshold**: Only lines appearing more than 5 times total are included.
- **Exclusions**: Structural markers (page numbers) are excluded.

### Wrapping & Layout
- **Scope**: Paragraphs, lists, and bullets are all subject to wrapping.
- **Blank Lines**: Exactly one blank line is inserted after every wrapped paragraph or wrapped list item.
