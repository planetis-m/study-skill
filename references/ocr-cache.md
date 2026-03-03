# OCR Cache Procedure

Use this procedure for any mode that starts from a PDF to avoid redundant OCR execution.

## 1. Check Cache

```bash
python3 <ABSOLUTE_PATH_TO_SKILL>/scripts/ocr_cache.py check --pdf-input "path/to/file.pdf" --page-sel "1-5"
```
*(Leave `--page-sel` empty or omit it for full documents).*

**Exit codes:**
- `0`: Cache hit. Go to **Step 2A (Read Cache)**.
- `3`: Cache miss. Go to **Step 2B (Run & Store)**.
- `1` or `2`: Error. Stop and report.

## 2A. Read Cache (On Hit)

```bash
python3 <ABSOLUTE_PATH_TO_SKILL>/scripts/ocr_cache.py read --pdf-input "path/to/file.pdf" --page-sel "1-5"
```
This will print the extracted document directly to stdout, organized with `<page>` markers. Consume this text directly for the requested study mode.

## 2B. Run OCR & Store (On Miss)

Run `pdfocr` and pipe its JSONL output directly into the `store` command. 
Use `--all-pages` if no page selection is provided, or `--pages:"..."` if a range is specified.

```bash
pdfocr "path/to/file.pdf" <OCR_PAGE_ARG> | python3 <ABSOLUTE_PATH_TO_SKILL>/scripts/ocr_cache.py store --pdf-input "path/to/file.pdf" --page-sel "1-5"
```

**Exit codes:**
- `0`: The script will automatically format and print the extracted `<page>` text directly to stdout (skipping any broken pages). **Consume this printed text directly** for the requested study mode. (Do not run the `read` command).
- `3`: OCR failed completely (no valid text). Stop and report the failure to the user.
- `1` or `2`: Error. Stop and report.
