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


class CacheCliError(Exception):
    def __init__(self, message: str, exit_code: int = EXIT_RUNTIME_ERROR) -> None:
        super().__init__(message)
        self.exit_code = exit_code


def to_json(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=True, separators=(",", ":"))


def normalize_pdf_input(pdf_input: str) -> str:
    value = pdf_input.strip() if pdf_input else ""
    if not value:
        raise CacheCliError("Error: --pdf-input is required.", EXIT_INVALID_ARGS)
    return str(Path(os.path.expanduser(value)).resolve())


def normalize_page_sel(page_sel: str | None) -> str:
    value = (page_sel or "").strip()
    return value if value else DEFAULT_PAGE_SEL


def build_key_and_raw_path(pdf_input: str, page_sel: str | None) -> tuple[str, Path]:
    pdf_norm = normalize_pdf_input(pdf_input)
    page_norm = normalize_page_sel(page_sel)
    seed = f"{pdf_norm}\n{page_norm}".encode("utf-8")
    key = hashlib.sha256(seed).hexdigest()[:32]
    raw_path = CACHE_DIR / f"{key}.jsonl"
    return key, raw_path


def cmd_check(args: argparse.Namespace) -> int:
    key, raw_path = build_key_and_raw_path(args.pdf_input, args.page_sel)
    cache_hit = raw_path.exists() and raw_path.stat().st_size > 0
    print(to_json({"cache_hit": cache_hit, "key": key, "raw_path": str(raw_path)}))
    return EXIT_OK if cache_hit else EXIT_CACHE_MISS


def parse_ok_texts(jsonl_path: Path) -> list[str]:
    texts: list[str] = []
    with jsonl_path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise CacheCliError(f"Error: invalid JSONL at line {line_no}: {exc.msg}", EXIT_CACHE_MISS)

            if obj.get("status") != "ok":
                raise CacheCliError(f"Error: non-ok OCR record at line {line_no}", EXIT_CACHE_MISS)

            text = obj.get("text")
            if not isinstance(text, str) or not text:
                raise CacheCliError(f"Error: missing text in ok OCR record at line {line_no}", EXIT_CACHE_MISS)
            texts.append(text)

    if not texts:
        raise CacheCliError("Error: OCR JSONL has no ok text.", EXIT_CACHE_MISS)

    return texts


def cmd_store(args: argparse.Namespace) -> int:
    _, raw_path = build_key_and_raw_path(args.pdf_input, args.page_sel)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile("wb", dir=CACHE_DIR, delete=False, prefix=".ocr-store.", suffix=".jsonl") as handle:
        tmp_path = Path(handle.name)
        for chunk in iter(lambda: sys.stdin.buffer.read(65536), b""):
            handle.write(chunk)

    try:
        parse_ok_texts(tmp_path)
        os.replace(tmp_path, raw_path)
    except CacheCliError as exc:
        if exc.exit_code == EXIT_CACHE_MISS:
            print(to_json({"stored": False}))
            return EXIT_CACHE_MISS
        raise
    finally:
        tmp_path.unlink(missing_ok=True)

    print(to_json({"stored": True}))
    return EXIT_OK


def cmd_read(args: argparse.Namespace) -> int:
    _, raw_path = build_key_and_raw_path(args.pdf_input, args.page_sel)
    if not raw_path.exists():
        raise CacheCliError(f"Error: raw cache file not found: {raw_path}", EXIT_CACHE_MISS)

    ok_texts = parse_ok_texts(raw_path)
    print(to_json({"ok_text_concat": "\n\n".join(ok_texts)}))
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scripts/ocr_cache.py",
        description="Minimal deterministic cache CLI for study-assistant OCR reuse.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Commands:\n"
            "  check        Return hit/miss for one PDF + page selection\n"
            "  store        Read OCR JSONL from stdin, validate, store on all-ok\n"
            "  read         Return concatenated text from cached all-ok JSONL\n\n"
            "Exit codes:\n"
            f"  {EXIT_OK}=success, {EXIT_RUNTIME_ERROR}=runtime error, "
            f"{EXIT_INVALID_ARGS}=invalid arguments, {EXIT_CACHE_MISS}=cache miss"
        ),
    )

    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    for name, fn, help_text in (
        ("check", cmd_check, "Check cache for one PDF/page selection."),
        ("store", cmd_store, "Read OCR JSONL from stdin, validate, store on all-ok."),
        ("read", cmd_read, "Return concatenated text from one cached all-ok JSONL entry."),
    ):
        sub = subparsers.add_parser(name, help=help_text)
        sub.add_argument("--pdf-input", required=True, help="Path to PDF.")
        sub.add_argument("--page-sel", default=DEFAULT_PAGE_SEL, help=f'Page selection (default: "{DEFAULT_PAGE_SEL}").')
        sub.set_defaults(func=fn)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except CacheCliError as exc:
        print(str(exc), file=sys.stderr)
        return exc.exit_code
    except BrokenPipeError:
        return EXIT_OK
    except Exception as exc:  # pragma: no cover
        print(f"Error: unexpected failure: {exc}", file=sys.stderr)
        return EXIT_RUNTIME_ERROR


if __name__ == "__main__":
    sys.exit(main())
