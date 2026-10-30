# 7.3 Integrated ask path: RAG, tools, approval   [NEW — no Java equivalent] [cost: mock] [~60 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/7_03/tests/test_skip.py` passes. **Still recommended.**

Official docs: [Responses API](https://platform.openai.com/docs/guides/migrate-to-responses), [function calling](https://platform.openai.com/docs/guides/function-calling). DocsDesk files: `docsdesk.v1`, `docsdesk.rag`, `docsdesk.triage`.

## 1. Concept

The **ask path** retrieves chunks, answers with citations, and logs cost. The **investigate path** runs the agent loop and stops write tools until a human sets `approved=True`. v1.0 is those two paths behind one class.

## 2. Intuition

```
question  → retrieve k → complete(Responses) → citations + cost log
incident  → tools… → propose_page ─┬─ approved? → continue
                                   └─ no → status=denied
```

Retrieval is *your* numpy index (Module 4). The model does not magically "know the repo". Write tools are *your* function, like a `@PreAuthorize` method that still needs a boolean.

## 3. Why it exists

A RAG demo without an approval gate is a chatbot. An agent demo without citations is a loop. Interviewers ask how those meet.

### The Java analogy that misleads you

`@Transactional` + a command bus looks like "the framework will orchestrate tools". Here the model proposes the next tool. Your Python still executes it, caps steps, and refuses `propose_page` when `approved` is false. There is no container-managed agent.

## 4. Step-by-step examples

**Example 1 — route intent.** Refund *how-to* → `ask`. HTTP 500 incident → `investigate`.

**Example 2 — citations required.** `DocsDeskV1.ask` returns `RagCitation` rows into retrieved chunks, not empty prose.

**Example 3 — read-only tools.** `search_docs` / `search_corpus` do not need approval.

**Example 4 — write tools.** `propose_page` and `delete_page` need approval. Denied runs still show the tool name.

**Example 5 — honesty.** `propose_page` sets `would_write`. It does not create a Confluence page.

```bash
uv run python concepts/7_03/examples.py
```

## 5. Common pitfalls

- Calling `investigate` for every question (wastes steps, needs a fake trajectory).
- `approved=True` as the default in `create_app`.
- Forgetting citations because the FakeLLM text "looks right".
- Using the Assistants API "runs" object. Sunset. Use `complete()` + your loop.

## 6. Exercises

1. **Guided:** `route_intent`.
2. **Open:** `needs_approval`, `citation_ok`.

```bash
uv run pytest concepts/7_03
```

- Hint 1: incident hints include `500`, `incident`, `investigate`, `triage`.
- Hint 2: write tools are `propose_page` and `delete_page`.
- Solution: `solutions/intent.py`, `solutions/approval.py`.

## 7. Check

1. Who retrieves — the model, or your index?
2. Predict `route_intent("POST /refunds returns 500")`.
3. Why is `@Transactional` a misleading analog for the tool loop?
4. What happens when `propose_page` runs with `approved=False`?
5. Did this demo send an email?

## Setup / troubleshooting

- Graded work: `LLM_PROVIDER=fake` and `data/embeddings/payments-api.json`.
- Rebuild vectors: `uv run python scripts/build_embedding_fixtures.py`.
- Windows console Unicode: use Windows Terminal; CI sets `PYTHONUTF8=1`.
- Apple Silicon: arm64 uv/Python. "Bad CPU type" is a Rosetta binary.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** `uv run docsdesk v1` prints one RAG ask and one approved triage. Both are simulated.

**What you learned:** citations on ask; approval on writes; the model does not get a blank check.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
