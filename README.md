# Study Assistant Skill

`study-assistant` is an installable Agent Skill designed for exam prep from lecture slides. It is optimized for PDF slides and uses the `pdfocr` CLI to extract and process text.

## Features

It provides a single workflow with multiple modes to help you study:
- `transcribe`: Exact text transcription from slides.
- `lecture`: Translates slides into a cohesive professor-style narrative.
- `eli5`: Explains complex material in plain English.
- `flashcard`: Generates concise, two-column flashcards.
- `mindmap`: Generates Mermaid-syntax concept maps.
- `quiz`: Creates practice questions and answer keys.
- `essay`: Creates 3-4 essay prompts with sample answers.
- `study-notes`: Generates structured, exam-focused study notes.

*Note: The skill automatically caches OCR results locally during your session. If you run multiple modes on the same PDF, it reuses the text to save time and API costs.*

## Requirements

- **`pdfocr`**: The skill requires `pdfocr` to extract text. *(If it is missing, the agent will automatically attempt to install it for you).*
- **DeepInfra API Key**: Required for the OCR engine.
  - Set it via the `DEEPINFRA_API_KEY` environment variable (recommended).
  - Alternatively, provide it via a `config.json` file next to the `pdfocr` executable.

## Installation

### Using Codex
Codex recommends installing non-built-in skills using the `$skill-installer`. Prompt Codex with:

```text
$skill-installer install the skill from repo planetis-m/study-assistant with path .
```
*(If the skill does not appear immediately, restart Codex).*

### Manual Install
Clone directly into your agent's scanned skills path (e.g., `~/.agents/skills`):

```bash
git clone https://github.com/planetis-m/study-assistant.git ~/.agents/skills/study-assistant
```

## Usage Examples

Invoke the skill explicitly using `$study-assistant` in your prompts:

```text
Use $study-assistant in transcribe mode for lecture1.pdf and keep text verbatim.
```

```text
Use $study-assistant in study-notes mode for lecture1.pdf.
```

```text
Use $study-assistant in quiz mode on this transcribed content: ...
```
