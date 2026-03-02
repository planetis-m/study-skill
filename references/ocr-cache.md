# OCR Cache Procedure

Use this procedure for any mode that starts from a PDF.

## 1. Build Cache Key

POSIX shell:

```bash
pdf_abs="$(realpath "$PDF_INPUT")"
pdf_size="$(stat -c %s "$pdf_abs" 2>/dev/null || stat -f %z "$pdf_abs")"
pdf_mtime="$(stat -c %Y "$pdf_abs" 2>/dev/null || stat -f %m "$pdf_abs")"
page_sel="${PAGE_SELECTION:-all-pages}"
cache_key="$(printf '%s|%s|%s|%s\n' "$pdf_abs" "$page_sel" "$pdf_size" "$pdf_mtime" | sha256sum | awk '{print $1}')"
cache_dir=".study-skill-cache"
mkdir -p "$cache_dir"
cache_text="$cache_dir/$cache_key.txt"
cache_err="$cache_dir/$cache_key.errors.txt"
cache_meta="$cache_dir/$cache_key.meta"
```

## 2. Check Cache

```bash
if [ -s "$cache_text" ]; then
  echo "OCR cache hit: $cache_text"
  # Reuse this text for analyze/lecture/eli5/flashcard/mindmap/quiz/essay outputs.
fi
```

If `cache_text` exists and is non-empty, skip `pdfocr`.

## 3. Populate Cache on Miss

Run OCR:

```bash
# all pages
pdfocr "$pdf_abs" --all-pages
# or selected pages
pdfocr "$pdf_abs" --pages:"$page_sel"
```

Parse JSONL and write:
- successful page text (concatenate with blank line separators) to `cache_text`
- failed page details to `cache_err`
- key inputs and command to `cache_meta`

## 4. Reuse Across Modes

When user asks another mode for the same PDF/pages in the same session:
- recompute key
- load `cache_text`
- do not rerun OCR unless cache miss

## 5. Invalidation

Treat as miss when any of these change:
- file path
- page selection
- file size
- file mtime
