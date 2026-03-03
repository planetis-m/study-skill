#!/usr/bin/env python3
"""Deterministic OCR cache CLI for study-assistant."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

EXIT_OK = 0
EXIT_RUNTIME_ERROR = 1
EXIT_INVALID_ARGS = 2
EXIT_CACHE_MISS = 3

CACHE_DIR = Path(".study-assistant-cache")
DEFAULT_PAGE_SEL = "all-pages"

def to_json(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=True, separators=(",", ":"))

def build_key_and_raw_path(pdf_input: str, page_sel: str) -> tuple[str, Path]:
    if not pdf_input.strip():
        print("Error: --pdf-input is required.", file=sys.stderr)
        sys.exit(EXIT_INVALID_ARGS)
        
    pdf_norm = str(Path(pdf_input).expanduser().resolve())
    page_norm = page_sel.strip() if page_sel and page_sel.strip() else DEFAULT_PAGE_SEL
    
    seed = f"{pdf_norm}\n{page_norm}".encode("utf-8")
    key = hashlib.sha256(seed).hexdigest()[:32]
    return key, CACHE_DIR / f"{key}.jsonl"

def cmd_check(args: argparse.Namespace) -> int:
    key, raw_path = build_key_and_raw_path(args.pdf_input, args.page_sel)
    cache_hit = raw_path.exists() and raw_path.stat().st_size > 0
    print(to_json({"cache_hit": cache_hit, "key": key, "raw_path": str(raw_path)}))
    return EXIT_OK if cache_hit else EXIT_CACHE_MISS

def cmd_store(args: argparse.Namespace) -> int:
    _, raw_path = build_key_and_raw_path(args.pdf_input, args.page_sel)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    data = sys.stdin.read()
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    
    if not lines:
        print(to_json({"stored": False}))
        return EXIT_CACHE_MISS

    try:
        for line in lines:
            obj = json.loads(line)
            if obj.get("status") != "ok" or not obj.get("text"):
                raise ValueError
    except Exception:
        print(to_json({"stored": False}))
        return EXIT_CACHE_MISS

    # Atomic write to final cache path
    with tempfile.NamedTemporaryFile("w", dir=CACHE_DIR, delete=False, prefix=".ocr-store.", suffix=".jsonl", encoding="utf-8") as f:
        f.write(data)
        tmp_path = f.name
        
    os.replace(tmp_path, raw_path)
    print(to_json({"stored": True}))
    return EXIT_OK

def cmd_read(args: argparse.Namespace) -> int:
    _, raw_path = build_key_and_raw_path(args.pdf_input, args.page_sel)
    if not raw_path.exists():
        print(f"Error: raw cache file not found: {raw_path}", file=sys.stderr)
        return EXIT_CACHE_MISS

    texts = [
        json.loads(line)["text"]
        for line in raw_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    print(to_json({"ok_text_concat": "\n\n".join(texts)}))
    return EXIT_OK

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scripts/ocr_cache.py",
        description="Minimal deterministic cache CLI for study-assistant OCR reuse.",
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    
    for name, fn in (("check", cmd_check), ("store", cmd_store), ("read", cmd_read)):
        sub = subparsers.add_parser(name)
        sub.add_argument("--pdf-input", required=True)
        sub.add_argument("--page-sel", default=DEFAULT_PAGE_SEL)
        sub.set_defaults(func=fn)

    return parser

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except BrokenPipeError:
        return EXIT_OK
    except Exception as exc:
        print(f"Error: unexpected failure: {exc}", file=sys.stderr)
        return EXIT_RUNTIME_ERROR

if __name__ == "__main__":
    sys.exit(main())
