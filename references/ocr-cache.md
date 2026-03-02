# OCR Cache Procedure

Use this procedure for any mode that starts from a PDF.

## 1. Set Cache Paths

POSIX shell:

```bash
cache_dir=".study-assistant-cache"
mkdir -p "$cache_dir"
cache_raw="$cache_dir/current.raw.jsonl"
cache_meta="$cache_dir/current.meta"
page_sel="$PAGE_SELECTION"
if [ -z "$page_sel" ]; then
  page_sel="all-pages"
fi
```

## 2. Check Cache

```bash
cache_hit="no"
if [ -s "$cache_raw" ]; then
  if [ -f "$cache_meta" ]; then
    if grep -Fqx "pdf_input=$PDF_INPUT" "$cache_meta"; then
      if grep -Fqx "page_sel=$page_sel" "$cache_meta"; then
        cache_hit="yes"
      fi
    fi
  fi
fi
if [ "$cache_hit" = "yes" ]; then
  echo "OCR cache hit: $cache_raw"
fi
```

If cache hit, skip `pdfocr`.

## 3. Populate Cache on Miss

Before running `pdfocr`, request user approval for unrestricted network execution.

Write metadata, then run OCR:

```bash
printf 'pdf_input=%s\npage_sel=%s\n' "$PDF_INPUT" "$page_sel" > "$cache_meta"
if [ "$page_sel" = "all-pages" ]; then
  pdfocr "$PDF_INPUT" --all-pages > "$cache_raw"
else
  pdfocr "$PDF_INPUT" --pages:"$page_sel" > "$cache_raw"
fi
```

## 4. Reuse Across Modes

When user asks another mode for the same PDF/pages in the same session:
- load `cache_raw`
- read JSONL lines directly:
  - use `status:"ok"` lines as content source (`text` field)
  - report `status:"error"` lines with page/error info
- do not rerun OCR unless cache miss

## 5. Invalidation

Treat as miss when any of these change:
- `PDF_INPUT` path
- page selection
