---
name: study-assistant
description: Study assistant workflow for turning provided study material into exam-focused deliverables such as verbatim transcriptions, study notes, lecture-style explanations, ELI5 explanations, flashcards, Mermaid mind maps, quizzes, and essay questions.
---

# Study Assistant

Follow this workflow exactly to turn provided study material into exam-ready outputs.

## Select Mode

Map the user request to one mode:

- `transcribe`: Convert provided source text into structured markdown while keeping educational text verbatim.
- `lecture`: Turn provided content into cohesive professor-style teaching narrative.
- `eli5`: Explain provided material in plain English while keeping technical depth.
- `flashcard`: Generate two-column markdown flashcards.
- `mindmap`: Generate Mermaid mindmap only.
- `quiz`: Generate mixed quiz and answer key.
- `essay`: Generate 3-4 essay prompts and sample answers.
- `study-notes`: Generate study notes from provided content.

## Prepare Source Material

Work only from material already present in the conversation or otherwise already extracted into text.

- If the source still needs to be converted into text, use a separate extraction step before applying this skill.
- Do not prescribe any specific extraction method or file-format tool here.

## Clean Source Text

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

- Base all factual content only on user-provided material and prepared source text.
- Do not add outside facts, theories, examples, or claims.
- Do not mention the source material. Present content directly.
- Use markdown output.
- Use LaTeX with `$...$` (inline) and `$$...$$` (display) for math.
- Do not include conversational intros or conclusions.
