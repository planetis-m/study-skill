# Study Assistant Skill

`study-assistant` is an installable Agent Skill for exam prep from study material that is already available as text.

## Features

It provides a single workflow with multiple modes to help you study:
- `transcribe`: Exact text transcription from provided material.
- `lecture`: Translates provided material into a cohesive professor-style narrative.
- `eli5`: Explains complex material in plain English.
- `flashcard`: Generates concise, two-column flashcards.
- `mindmap`: Generates Mermaid-syntax concept maps.
- `quiz`: Creates practice questions and answer keys.
- `essay`: Creates 3-4 essay prompts with sample answers.
- `study-notes`: Generates structured, exam-focused study notes.

If the source material is not yet available as text, run a separate extraction step before invoking `study-assistant`.

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
Use $study-assistant in transcribe mode on this extracted lecture text and keep it verbatim.
```

```text
Use $study-assistant in study-notes mode on this extracted lecture text.
```

```text
Use $study-assistant in quiz mode on this transcribed content: ...
```
