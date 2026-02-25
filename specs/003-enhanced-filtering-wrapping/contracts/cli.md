# CLI Contract: Enhanced OCR Filtering

The CLI will be updated to include new flags for the enhanced filtering and wrapping features.

## Updated Arguments

| Flag | Type | Description |
|------|------|-------------|
| `--similarity` | `float` | Jaccard similarity threshold for fuzzy matching (0.0-1.0). Default: `0.9`. |
| `--dry-run` | `bool` | Process files and identify boilerplate without writing primary output files. |
| `--no-filtered` | `bool` | Disable generation of `.filtered.md` sidecar files. |

## Usage Examples

### Standard Run with Fuzzy Filtering
```bash
python -m ocrpolish.cli data/raw data/processed --threshold 0.1 --similarity 0.85
```

### Dry Run to Preview Boilerplate
```bash
python -m ocrpolish.cli data/raw data/processed --dry-run
```

### Disabling Sidecar Files
```bash
python -m ocrpolish.cli data/raw data/processed --no-filtered
```
