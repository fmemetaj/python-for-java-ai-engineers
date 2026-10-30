# 2.10 Prompts as versioned code + first eval   [NEW — no Java equivalent] [cost: mock] [~45 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/2_10/tests/test_skip.py` passes. **Still recommended.**

DocsDesk prompt file: `src/docsdesk/prompts/answer_from_doc.v1.txt`.

## 1. Concept

A **prompt is source code**: instructions in a versioned file, reviewed like any other string resource. An **eval** is a pytest of model *behavior* on a tiny golden set — not a vibe check and not JUnit of a pure function.

## 2. Intuition

`messages[0].content = "You are helpful"` buried in a method is an unversioned magic string. A file `answer_from_doc.v1.txt` can be diffed. Five fixtures ("auth → Bearer", …) catch a prompt edit that breaks DocsDesk.

```
prompts/answer_from_doc.v1.txt  →  instructions=
evals/cases.json                →  pytest
```

## 3. Why it exists

Java `messages.properties` is a cousin for UI strings, not for model instructions. JUnit asserts deterministic returns. LLM evals assert *contracts* (contains, schema, cost) against a fake or a recorded fixture.

### The Java analogy that misleads you

`@Value("classpath:prompt.txt")` looks done. Without a failing test when the prompt changes, you shipped a string. Evals are the missing CI gate.

## 4. Step-by-step examples

**Example 1 — load the committed prompt.** It mentions DocsDesk and forbids claiming it sent email.

**Example 2 — version in the filename.** `answer_from_doc.v1`.

**Example 3 — exact-match eval on FakeLLM script.** Five cases, all offline.

**Example 4 — a prompt regression.** Change instructions → cases fail (you will not commit that).

**Example 5 — grade `passed/failed` counts.** Never grade live wording in this module.

```bash
uv run python concepts/2_10/examples.py
```

## 5. Common pitfalls

- Editing prompts only in a notebook cell (lost on kernel restart).
- An eval set of 1 case.
- Asserting full live paragraphs.

## 6. Exercises

1. **Guided:** load a prompt file and parse its version from the filename.
2. **Open:** run a 5-case exact-match eval, return passed/failed.

```bash
uv run pytest concepts/2_10
```

- Hint 1: `Path.read_text`. Version is the stem (`answer_from_doc.v1`).
- Hint 2: exact `==` on fake answers; count mismatches.
- Solution: `solutions/prompts.py`, `solutions/eval_cases.py`.

## 7. Check

1. Why is a prompt file better than a string literal in `session.py`?
2. How many cases does this lesson's eval have?
3. Does an eval require `OPENAI_API_KEY`?
4. What happens if you "improve" the prompt and FakeLLM scripts no longer match?

## Setup / troubleshooting

- If `load_instructions` fails, you are not running from an editable checkout (`uv sync`).
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk ships `answer_from_doc.v1.txt` and prints `prompt=answer_from_doc.v1` next to the dollar amount.

**What you learned:** prompts are versioned files; evals are pytest on fixtures, not live prose.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
