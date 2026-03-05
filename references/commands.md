# Mode Rules

Apply the rules in the selected section exactly.

## transcribe

Goal: Convert PDF lecture slides into structured markdown while preserving educational text verbatim.

Rules:
- Output educational text word-for-word.
- Do not summarize, paraphrase, simplify, or shorten.
- Preserve original bullet points as found in extracted text.
- Keep markdown structure consistent with slide organization.
- Remove only metadata noise (instructor info, headers/footers, page numbers, timestamps, course codes).
- Skip fragments that are too broken to read reliably.

## lecture

Goal: Transform content into an engaging professor-style lecture narrative.

Rules:
- Use authoritative academic tone, without roleplay greetings.
- Present material directly; avoid source-referential phrasing such as "the lecture", "the slides", or "the notes".
- Connect fragmented slide points into coherent flow.
- Preserve and explain technical intricacies in depth.
- Include:
  - Topic framing
  - Connected narrative across ideas
  - Deep dive on hardest concepts
  - Final synthesis of the big picture

## eli5

Goal: Explain complex material in plain English while retaining full technical substance.

Rules:
- Assume zero prior knowledge at the start.
- Build complexity gradually without dumbing down technical depth.
- Translate jargon into plain meaning when introduced.
- Avoid forced metaphors; prefer clear concrete explanations.
- Cover:
  - Core idea
  - Step-by-step mechanism breakdown
  - Jargon translation
  - Practical importance and implications

## flashcard

Goal: Generate concise, exam-ready flashcards.

Rules:
- Focus on key terms, definitions, formulas, and core concepts.
- Keep fronts short and specific.
- Keep backs concise and direct.
- Output strictly as a two-column markdown table:
  - `Front (Term/Question)`
  - `Back (Definition/Answer)`

## mindmap

Goal: Produce a hierarchical concept map.

Rules:
- Output only a ` ```mermaid ` code block, with no extra text.
- First line inside block must be exactly `mindmap`.
- Encode hierarchy with indentation only.
- Do not use bullets, node IDs, or shape wrappers.
- Use short alphanumeric labels with spaces.
- Do not use parentheses, brackets, braces, quotes, or colons in labels.

## quiz

Goal: Create practice questions that test understanding.

Rules:
- Produce 5-10 questions across main concepts.
- Mix multiple-choice (4 options) and short-answer questions.
- Favor explanation and application over memorization.
- End with an `Answer Key` section containing all correct answers.

## essay

Goal: Create exam-style essay practice.

Rules:
- Produce 3-4 essay questions.
- Keep each suitable for about a 200-word response.
- Ensure at least one conceptual/theoretical and one applied/integrative question.
- Use academic verbs such as Discuss, Evaluate, Compare and contrast, Explain.
- For each question, include a sample answer of roughly 200 words.
- Keep sample answers grounded strictly in provided material.

## study-notes

Goal: Produce exam-focused study notes from provided content.

Rules:
- Organize notes by key topics with clear headers.
- For each topic include:
  - Detailed concept explanation
  - Essential facts and definitions for exams
  - Connections to other concepts
- Prefer understanding-oriented explanations over rote memorization.
- Keep flow logical and progressive.
