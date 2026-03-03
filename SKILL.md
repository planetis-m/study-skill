---
name: study-assistant
description: Study assistant workflow for lecture-slide exam prep using the `pdfocr` CLI. Use when a task involves reading PDF slides, transcribing slide text, and generating exam-focused deliverables such as study notes, lecture-style explanations, ELI5 explanations, flashcards, Mermaid mind maps, quizzes, and essay questions.
---

# Study Assistant

Follow this workflow exactly to convert lecture material into exam-ready outputs.

## Available scripts

- `scripts/ocr_cache.py` - Manages OCR cache operations (`check`, `store`, `read`).

## Select Mode

Map the user request to one mode:

- `transcribe`: Convert PDF slides into markdown while keeping educational text verbatim.
- `lecture`: Turn provided content into cohesive professor-style teaching narrative.
- `eli5`: Explain provided material in plain English while keeping technical depth.
- `flashcard`: Generate two-column markdown flashcards.
- `mindmap`: Generate Mermaid mindmap only.
- `quiz`: Generate mixed quiz and answer key.
- `essay`: Generate 3-4 essay prompts and sample answers.
- `study-notes`: Generate study notes from provided content.

## Session OCR Cache

For PDF-based requests, avoid repeated OCR in the same session by using a local cache.

- Use only `python3 scripts/ocr_cache.py` for cache operations.
- Follow [references/ocr-cache.md](references/ocr-cache.md) for the exact command sequence.
- Re-run OCR only on cache miss or when PDF path/page selection changes.

## Process PDF Input

If the source is a PDF, always run `pdfocr` through shell execution.

Before first OCR call:

- Check availability with `command -v pdfocr`.
- If `pdfocr` is missing, attempt install by following [references/pdfocr-install.md](references/pdfocr-install.md).
- Install only to user-home absolute paths (`$HOME/.local/...`), never `./.local` in workspace.
- Retry `command -v pdfocr` after installation.
- If still missing, stop and report the failed install attempt plus the exact command/output.
- Ask user permission before every networked OCR execution:
  - Request unrestricted network/escalated execution first.
  - Do not run a sandboxed `pdfocr` attempt as a probe when network access is required.
- Do not run shell preflight checks for credentials.
  - Do not inspect environment variables, shell profiles, or filesystem files to discover API keys.
  - Run OCR directly after permission.
  - If OCR indicates auth/config failure, report the error and ask the user to configure `DEEPINFRA_API_KEY` or `api_key` in `config.json` next to the real `pdfocr` binary, then retry.

- Never read PDFs with direct file readers or ad-hoc parsers.
- Use full document extraction:
  - `pdfocr INPUT.pdf --all-pages`
- If page ranges are provided, pass them to `pdfocr`:
  - `pdfocr INPUT.pdf --pages:"8-20,22-27"`
- Parse stdout as JSONL:
  - Treat each line as one JSON object.
  - Keep `"text"` only for records with `"status":"ok"`.
  - Report pages with `"status":"error"` but continue with successful pages.
  - For cached OCR, use `python3 scripts/ocr_cache.py read` and consume the formatted text directly.

## Clean OCR Text

Before generation, remove only clear metadata:

- Instructor details
- Headers and footers
- Page numbers
- Timestamps
- Course codes

Preserve educational content (concepts, definitions, examples). If text is severely fragmented, skip that fragment instead of guessing.

## Generate Output

Read and apply mode-specific rules from [references/commands.md](references/commands.md). Use the section matching the selected mode.

Global rules across all modes:

- Base all factual content only on user-provided material and extracted OCR text.
- Do not add outside facts, theories, examples, or claims.
- Use markdown output.
- Use LaTeX with `$...$` (inline) and `$$...$$` (display) for math.
- Do not include conversational intros or conclusions.
