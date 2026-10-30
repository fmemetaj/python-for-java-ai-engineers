# 4.3 Chunking and metadata   [NEW — no Java equivalent] [cost: mock] [~50 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/4_03/tests/test_skip.py` passes. **Still recommended.**

## 1. Concept

**Chunking** cuts a document into retrieval units. Each chunk carries **metadata** (path, heading, whether it is code). The unit you retrieve is the unit the model will see.

## 2. Intuition

A whole 40-page Markdown file is a bad vector: the question only needs one section, and the rest is noise. A 20-character shard is also bad: it loses the heading that said "Refunds". You want a paragraph-or-section sized bite, plus enough overlap that a sentence on a boundary is not lost.

```
# Refunds            ← heading metadata
## Partial refunds   ← keep with its body
```java ... ```     ← a fence must stay one chunk
```

## 3. Why it exists

Embedding APIs take a string, not a Git repo. You must choose the string. Java `split("\\n")` or `substring(0, 500)` will bisect Javadoc and Markdown fences. Structure-aware chunking walks headings and treats fenced code as atomic — like not splitting a Java method in the middle of a brace.

### The Java analogy that misleads you

`String.substring(0, n)` looks like pagination. It is how production RAG quietly loses `@PostMapping` because the fence started at character 480. Lucene *field* mapping (title vs body) is closer to metadata than to chunking.

## 4. Step-by-step examples

**Example 1 — size windows.** `chunk_by_size` cuts every `max_chars` with overlap. Simple, and it *will* split a fence.

**Example 2 — the bug.** A Javadoc fence longer than `max_chars` comes back as two chunks, neither of which compiles as an example.

**Example 3 — preserve fences.** `chunk_preserving_fences` emits the whole ` ```java ...``` ` as `is_code=True`.

**Example 4 — headings.** `chunk_structured` splits on `#` / `##` (when not inside a fence) and copies the heading into metadata.

**Example 5 — ids.** `chunk_id` is `{stem}:{index}` so citations can point at `PaymentController:1`.

```bash
uv run python concepts/4_03/examples.py
```

The fake cannot teach a tokenizer-aware token budget. Graded tests check fences and ids.

## 5. Common pitfalls

- Overlap ≥ max_chars (infinite loop).
- Splitting inside fences.
- Dropping path/heading, then being unable to cite.
- One chunk per file for a 2 kB doc (wastes the index) or one chunk per line (noise).

## 6. Exercises

1. **Guided:** `chunk_by_size(text, max_chars, overlap)` with ids `{path stem}:{i}`.
2. **Open (fix the bug):** `chunk_preserving_fences` must not bisect ` ``` ` blocks.

```bash
uv run pytest concepts/4_03
```

- Hint 1: step `max_chars - overlap`; reject overlap ≥ max_chars.
- Hint 2: find fence spans first; window only the prose in between.
- Solution: `solutions/size.py`, `solutions/fences.py`.

## 7. Check

1. Why overlap?
2. What metadata do you store besides the text?
3. Predict: a 900-char fence, max_chars=240, naive vs preserving — how many code chunks?
4. Is a heading inside a fence a real Markdown heading?

## Setup / troubleshooting

- Corpus path: `data/corpus/payments-api/docs`. Use UTF-8 (fences include Java).
- Windows: do not split on `\\` only — `path.replace("\\", "/")`.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk's structure-aware chunker keeps `PaymentController`'s Java fence intact so `@PostMapping` is retrievable.

**What you learned:** the chunk is the retrieval atom; fences and headings are structure, not characters.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
