# CLI Contract: Metadata Extraction

## Command: `ocrpolish metadata`

Extracts metadata from Markdown files using a local Ollama instance.

### Usage
```bash
ocrpolish metadata [OPTIONS] INPUT_DIR OUTPUT_DIR
```

### Arguments
- `INPUT_DIR`: Path to the directory containing source Markdown files.
- `OUTPUT_DIR`: Path to the directory where processed files with frontmatter will be saved.

### Options
- `--model TEXT`: The Ollama model to use. (Default: `gemma4:26b`)
- `--recursive / --no-recursive`: Whether to process subdirectories. (Default: `--recursive`)
- `--ollama-url TEXT`: The URL of the Ollama server. (Default: `http://localhost:11434`)
- `--overwrite / --no-overwrite`: Whether to overwrite existing files in the output directory. (Default: `--no-overwrite`)
- `--dry-run`: If set, logs the metadata without writing files.

### Example
```bash
ocrpolish metadata ./data/input ./data/output --model gemma4:26b
```

### Expected Output
- Progress bar for file processing.
- Log of successfully processed files and any failures.
- Final summary of extraction statistics.
