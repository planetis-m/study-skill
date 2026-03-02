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
- exit code `0`: cache hit, skip `pdfocr` and use `read`
- exit code `3`: cache miss, continue to step 3
- exit code `1` or `2`: runtime/argument error, stop and report

On cache miss, copy `raw_path` from the JSON output and set it explicitly:
```bash
RAW_PATH=".study-assistant-cache/<key>.jsonl"
```

## 3. Populate Cache on Miss (No Pipe)

Before running `pdfocr`, request user approval for unrestricted network execution.

```bash
cache_dir=".study-assistant-cache"
mkdir -p "$cache_dir"
TMP_JSONL=".study-assistant-cache/.ocr-tmp.jsonl"

pdfocr "$PDF_INPUT" --pages:"$page_sel" > "$TMP_JSONL"
python3 scripts/ocr_cache.py validate --input-jsonl "$TMP_JSONL"
```

Interpretation:
- exit code `0`: all parsed pages are valid `status:"ok"` with non-empty text
- exit code `3`: OCR output is non-cacheable (page/parse errors or empty)
- exit code `1` or `2`: runtime/argument error, stop and report

Commit on valid output:

```bash
mv "$TMP_JSONL" "$RAW_PATH"
```

Cleanup on invalid output:

```bash
rm -f "$TMP_JSONL"
```

## 4. Reuse Across Modes

When user asks another mode for the same PDF/pages in the same session:

```bash
python3 scripts/ocr_cache.py read \
  --pdf-input "$PDF_INPUT" \
  --page-sel "$page_sel"
```

Use the JSON response fields:
- `ok_text_concat`: merged text from all cached `status:"ok"` records

Do not rerun OCR unless `check` returns a miss (`exit 3`).
Partial OCR runs are not cached.

## 5. Cache Layout

- Raw JSONL entries: `.study-assistant-cache/<key>.jsonl`

The key is derived from normalized `pdf_input + page_sel`.
