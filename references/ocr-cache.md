# OCR Cache Procedure

Use this procedure for any mode that starts from a PDF.

All cache functions must go through `python3 scripts/ocr_cache.py`.

## 1. Validate Input and Normalize Page Selection

```bash
if [ ! -f "$PDF_INPUT" ]; then
  echo "PDF not found: $PDF_INPUT" >&2
  exit 1
fi

page_sel="$PAGE_SELECTION"
if [ -z "$page_sel" ]; then
  page_sel="all-pages"
fi
```

## 2. Check Cache

```bash
python3 scripts/ocr_cache.py check \
  --pdf-input "$PDF_INPUT" \
  --page-sel "$page_sel"
```

Interpretation:
- exit code `0`: cache hit, skip `pdfocr`
- exit code `3`: cache miss, continue to step 3
- exit code `1` or `2`: runtime/argument error, stop and report

The command prints JSON to stdout with `cache_hit`, `key`, and `raw_path`.

## 3. Populate Cache on Miss

Before running `pdfocr`, request user approval for unrestricted network execution.

Run OCR and pipe stdout directly into the cache script:

```bash
set -o pipefail
pdfocr "$PDF_INPUT" --pages:"$page_sel" | python3 scripts/ocr_cache.py store \
  --pdf-input "$PDF_INPUT" \
  --page-sel "$page_sel"
```

## 4. Reuse Across Modes

When user asks another mode for the same PDF/pages in the same session:

```bash
python3 scripts/ocr_cache.py read \
  --pdf-input "$PDF_INPUT" \
  --page-sel "$page_sel"
```

Use the JSON response fields:
- `ok_pages`: list of successful page text payloads
- `error_pages`: list of OCR/page parsing errors
- `ok_text_concat`: merged text from all `status:"ok"` records

Do not rerun OCR unless `check` returns a miss (`exit 3`).

## 5. Cache Layout

- Raw JSONL entries: `.study-assistant-cache/<key>.jsonl`

The key is derived from normalized `pdf_input + page_sel`.
