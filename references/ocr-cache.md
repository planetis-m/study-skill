# OCR Cache Procedure

Use this procedure for any mode that starts from a PDF to avoid redundant OCR execution.

## 1. Check Cache

```bash
python3 <ABSOLUTE_PATH_TO_SKILL>/scripts/ocr_cache.py check --pdf-input "path/to/file.pdf" --page-sel "1-5"
```
*(Leave `--page-sel` empty or omit it for full documents).*

**Exit codes:**
- `0`: Cache hit. Skip to **Step 3 (Read)**.
- `3`: Cache miss. Continue to **Step 2 (Store)**.
- `1` or `2`: Error. Stop and report.

## 2. Populate Cache on Miss

Run `pdfocr` and pipe its JSONL output directly into the `store` command. 
Use `--all-pages` if no page selection is provided, or `--pages:"..."` if a range is specified.

```bash
pdfocr "path/to/file.pdf" <OCR_PAGE_ARG> | python3 <ABSOLUTE_PATH_TO_SKILL>/scripts/ocr_cache.py store --pdf-input "path/to/file.pdf" --page-sel "1-5"
```

**Exit codes:**
- `0`: OCR output was successfully cached. Continue to **Step 3 (Read)**.
- `3`: OCR failed completely. Stop and report the failure to the user.
- `1` or `2`: Error. Stop and report.

## 3. Read Cached Text

```bash
python3 <ABSOLUTE_PATH_TO_SKILL>/scripts/ocr_cache.py read --pdf-input "path/to/file.pdf" --page-sel "1-5"
```

This will print the extracted document directly to stdout, organized with `<page>` markers. Consume this raw text directly for the requested study mode.

*(Note: Do not rerun OCR unless `check` returns a miss (`3`). Do not attempt to read the internal cache files directly).*
