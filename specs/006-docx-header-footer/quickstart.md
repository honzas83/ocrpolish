# Quickstart: Dynamic Headers and Footers for DOCX

## Usage
To process OCR Markdown files and generate DOCX files with automatically extracted headers, footers, and page numbers:
```bash
python -m ocrpolish.cli data/raw data/output --docx data/docx_output
```

## Configuring Scan Depth
By default, the system scans the first and last 3 paragraphs. You can adjust this:
```bash
python -m ocrpolish.cli data/raw data/output --docx data/docx_output --scan-paragraphs 5
```

## Verifying Results
1.  **Page Numbers**: Open the generated DOCX and verify the page numbers from the Markdown (e.g., `- 5 -`) are now in the official Word header/footer.
2.  **Repeated Headers**: If a title was repeated on 80% or more of your pages, it should be in the DOCX header and gone from the body text.
3.  **Clean Body**: The text moved to the header/footer should no longer be present in the main document content.
