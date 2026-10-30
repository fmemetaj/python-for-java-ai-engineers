# 4.5 RAG pipeline with citations   [NEW — no Java equivalent] [cost: mock] [~60 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/4_05/tests/test_skip.py` passes. **Still recommended.**

Official docs: generation uses the [Responses API](https://platform.openai.com/docs/guides/migrate-to-responses). Embeddings stay on the [Embeddings API](https://platform.openai.com/docs/guides/embeddings). Never Assistants.

## 1. Concept

**RAG** (retrieval-augmented generation) is retrieve → assemble context → generate an answer that **cites** the retrieved chunks. The model does not search; your code does.

## 2. Intuition

You would not let a junior engineer answer a Spring question from memory if the Javadoc is on disk. You paste the relevant sections into the prompt, then ask. Citations are the footnotes: every claim should point at a `chunk_id` you actually retrieved.

```
question
  → embed (FakeEmbedder)
  → VectorIndex.search / hybrid
  → assemble [chunk_id] + text  (character budget)
  → FakeLLM.complete  (Responses-shaped)
  → RagAnswer { answer, citations[] }
```

## 3. Why it exists

A 128k context window is not a license to dump the repo. Retrieval picks the 5 chunks that might matter. Citations make the answer auditable — the same reason a Javadoc `@link` exists, except the model will happily invent a link unless you constrain it.

### The Java analogy that misleads you

A Spring service chain (`Controller → Service → Repository`) looks like the pipeline. The misleading part is **who chooses the repository query**: in Spring, you wrote the SQL. In RAG, cosine (or hybrid) chooses the rows, and the model may still ignore them. Treating RAG as "the LLM has our docs" is how people skip groundedness (4.6).

## 4. Step-by-step examples

**Example 1 — retrieve.** `RagDesk.retrieve("How do I refund a captured payment?")` should include stem `refunds`.

**Example 2 — assemble.** `assemble_context(hits)` labels each block `[refunds:0]`. A budget drops the tail.

**Example 3 — generate.** FakeLLM returns a scripted JSON answer. Live path would be `client.responses.create` with that context in `instructions` or `input`. Not Assistants. Not Chat Completions unless you are migrating (Module 2).

**Example 4 — citations from hits.** DocsDesk attaches `RagCitation(chunk_id, path, quote)` from the retrieved rows so a scripted model cannot cite a chunk it never saw.

**Example 5 — refuse to cite the rest of the corpus.** If a chunk was not retrieved, it must not appear in `citations`.

```bash
uv run python concepts/4_05/examples.py
```

The fake cannot teach a live model that quotes a chunk and then contradicts it. Graded tests check *your* assembler and citation filter.

## 5. Common pitfalls

- Stuffing the whole file into the prompt "to be safe" (cost + lost needle).
- Citing `payments.md` because you know it exists, not because it was retrieved.
- Using Assistants file_search in the graded path (lock-in; 4.7 discusses it as optional).
- Forgetting the character budget so context overflows the window (Module 2).

## 6. Exercises

1. **Guided:** `assemble_context(chunks, budget)` with `[id]` labels, stopping at the budget.
2. **Open:** `cite_only_retrieved(proposed_ids, retrieved_ids)` — drop invented citations.

```bash
uv run pytest concepts/4_05
```

- Hint 1: join with blank lines; if the next block would exceed budget and you already have one block, stop.
- Hint 2: keep order of `proposed_ids` but only those in the retrieved set.
- Solution: `solutions/assemble.py`, `solutions/citations.py`.

## 7. Check

1. Who runs the search — the model or your Python?
2. Which API generates the answer in this course?
3. Why attach citations from hits even when FakeLLM already "knows" the answer?
4. Predict: budget 10, two 80-char chunks — how many blocks?

## Setup / troubleshooting

- `uv run python -m docsdesk` prints a RAG answer after the Module 3 demo.
- Graded: `LLM_PROVIDER=fake`. Live generation: Responses. Live embeddings: Embeddings API.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk v0.4 answers Northwind Payments questions with citations into `data/corpus/payments-api`.

**What you learned:** RAG is a pipeline you own; citations must be a subset of retrieval.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
