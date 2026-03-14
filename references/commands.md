# Mode Rules

Apply the rules in the selected section exactly.

## transcribe

Goal: Convert provided study material into structured markdown while preserving educational text verbatim.

Rules:
- Reproduce educational content word-for-word.
- Do not summarize, paraphrase, simplify, reorder, or shorten.
- Preserve headings, bullets, numbering, and visible structure where they can be recovered reliably.
- Keep the markdown aligned with the source organization.
- Remove only metadata noise: instructor details, headers, footers, page numbers, timestamps, and course codes.
- If a fragment is too broken to recover confidently, omit it rather than guess.

## lecture

Goal: Deliver the material as a coherent professor-style lecture.

Rules:
- Write in lecturer voice, as if teaching students directly in a university class.
- Sound academically precise, but teachable and spoken rather than like commentary on notes.
- State ideas directly. Never describe what "the material," "content," "slides," "notes," or "lecture" say.
- Do not frame the output as a study guide, recap, annotated summary, or commentary on source text.
- Turn fragmented points into one continuous explanatory narrative with smooth transitions.
- Prefer developed paragraphs; use bullets only when they are genuinely the clearest format.
- Build progressively: frame the central problem, define key concepts, mark important distinctions, then move into the harder ideas.
- Preserve full technical depth and explain intricate points clearly.
- Make likely points of confusion explicit, especially where similar terms or theories can be mistaken for one another.
- Keep the narrative cumulative so each section advances the argument instead of reading like isolated blocks.
- Include:
  - a clear opening frame of the topic and its central question
  - direct exposition of the concepts in lecturer voice
  - transitions that show how each idea leads to the next
  - deeper treatment of the hardest concepts, mechanisms, or contrasts
  - a closing synthesis of the larger picture

## eli5

Goal: Explain the material in plain English without losing technical substance.

Rules:
- Assume no prior knowledge at the start.
- Begin with the simplest correct framing, then increase complexity step by step.
- Translate jargon into plain meaning on first use, while still keeping the correct technical terms.
- Prefer clear, concrete explanation over forced metaphors or cute analogies.
- Keep the explanation accurate, substantive, and fully grounded in the provided material.
- Cover:
  - the core idea in plain terms
  - a step-by-step account of how it works
  - the meaning of key terms and jargon
  - why it matters in practice or in the larger topic

## flashcard

Goal: Generate concise, exam-ready flashcards.

Rules:
- Include only high-value terms, definitions, formulas, distinctions, and core concepts.
- Make each front a single clear prompt.
- Make each back short, direct, and sufficient for revision.
- Avoid duplicate or heavily overlapping cards.
- Output only a two-column markdown table with these exact headers:
  - `Front (Term/Question)`
  - `Back (Definition/Answer)`

## mindmap

Goal: Produce a hierarchical concept map.

Rules:
- Output only a ` ```mermaid ` code block with no extra text.
- The first line inside the block must be exactly `mindmap`.
- Represent hierarchy through indentation only.
- Do not use bullets, node IDs, connectors, or shape syntax.
- Keep labels short and readable. Use letters, numbers, and spaces only.
- Do not use parentheses, brackets, braces, quotes, punctuation, or colons in labels.

## quiz

Goal: Create practice questions that test understanding and application.

Rules:
- Produce 5-10 questions covering the main concepts.
- Mix multiple-choice questions with exactly 4 options and short-answer questions.
- Prioritize explanation, comparison, and application over recall-only questions.
- Keep questions clear, unambiguous, and answerable from the provided material.
- End with an `Answer Key` section that gives the correct answer for every question.

## essay

Goal: Create exam-style essay practice.

Rules:
- Produce 3-4 essay questions.
- Make each question suitable for a response of about 200 words.
- Include at least one conceptual or theoretical question and at least one applied or integrative question.
- Use strong academic verbs such as `Discuss`, `Evaluate`, `Compare and contrast`, and `Explain`.
- Provide a sample answer of roughly 200 words for each question.
- Keep both questions and sample answers grounded strictly in the provided material.

## study-notes

Goal: Produce exam-focused study notes from provided content.

Rules:
- Organize the notes by major topic using clear markdown headers.
- For each topic include:
  - a clear explanation of the concept
  - the essential facts, definitions, or formulas most relevant for exams
  - links to related concepts, contrasts, or dependencies
- Prioritize understanding, relationships, and exam relevance over rote listing.
- Keep the flow logical and progressive so later sections build on earlier ones.
