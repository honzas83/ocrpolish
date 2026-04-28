# Quickstart: Ollama Metadata Extraction

## Prerequisites
1.  **Ollama Installed**: Ensure Ollama is installed and running on your system.
2.  **Model Pulled**: Pull the required model:
    ```bash
    ollama pull gemma4:26b
    ```
3.  **Dependencies**: Install the required Python packages:
    ```bash
    pip install ollama pydantic pyyaml click
    ```

## Basic Usage

To extract metadata from a directory of Markdown files and save them to an output directory:

```bash
ocrpolish metadata ./my_ocr_files ./output_with_metadata
```

## Advanced Options

### Use a different model
```bash
ocrpolish metadata ./input ./output --model llama3.1
```

### Specify Ollama server location
If Ollama is running on a different machine or port:
```bash
ocrpolish metadata ./input ./output --ollama-url http://192.168.1.10:11434
```

### Dry Run
To see what metadata would be extracted without writing any files:
```bash
ocrpolish metadata ./input ./output --dry-run
```

## Verifying Output
Open any file in the output directory. You should see a YAML block at the top:

```markdown
---
archive_code: NPG/D(77)12
author: John Doe
date: '1977-05-12'
language: English
title: Letter to the Committee
...
---

Rest of the document content...
```
