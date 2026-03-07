---
name: study-assistant
description: Study assistant workflow for lecture-slide exam prep using the `pdfocr` CLI. Use when a task involves reading PDF slides, transcribing slide text, and generating exam-focused deliverables such as study notes, lecture-style explanations, ELI5 explanations, flashcards, Mermaid mind maps, quizzes, and essay questions.
---

# Study Assistant

Follow this workflow exactly to convert lecture material into exam-ready outputs.

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

For PDF-based requests, use the caching procedure to avoid repeated OCR execution.

- Follow [references/ocr-cache.md](references/ocr-cache.md) exactly for the correct command sequence.
- Always execute cache commands directly from your current working directory.

## Process PDF Input

If the source is a PDF, extract text exclusively through `pdfocr` shell execution.
Never read PDFs with direct file readers or ad-hoc parsers.

### Installation

Run the installation steps only when cache misses, before Step 2.

- Check with `command -v pdfocr`.
- If missing, read `references/pdfocr-install.md` and attempt installation.
- Retry `command -v pdfocr` after installation. If still missing, stop and report.

### Execution

- Request unrestricted network/escalated execution directly in the tool call.
  Do not run a sandboxed `pdfocr` attempt as a probe.
- Do not inspect environment variables, shell profiles, or filesystem files to discover API keys.
  If OCR reports an auth/config failure, report the error and ask the user to configure
  `DEEPINFRA_API_KEY` or `config.json`, then retry.

### Usage

- Full document: `pdfocr INPUT.pdf --all-pages`
- Page ranges: `pdfocr INPUT.pdf --pages:"8-20,22-27"`

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
- Do not mention the source material. Present content directly.
- Use markdown output.
- Use LaTeX with `$...$` (inline) and `$$...$$` (display) for math.
- Do not include conversational intros or conclusions.
