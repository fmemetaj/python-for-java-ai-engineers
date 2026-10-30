# 5.3 Agent memory and context management   [NEW — no Java equivalent] [cost: mock] [~45 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/5_03/tests/test_skip.py` passes. **Still recommended.**

Official docs: [Conversation state](https://platform.openai.com/docs/guides/conversation-state) (prior input tokens are still billed). Course tokenizer: four characters ≈ one token ([counting tokens](https://help.openai.com/en/articles/4936856-understanding-and-counting-tokens)).

## 1. Concept

**Agent memory** is the notes the loop re-sends so later tool rounds still know what happened. It is not a database, not Redis, and not an HTTP session. It is a budgeted list: pin the user incident, keep recent observations, drop the oldest when the token budget is gone.

## 2. Intuition

A sticky note on the on-call laptop.

```
pinned:  "POST /payments/{id}/refunds returns 500 after capture"
obs 1:   search_docs → refunds page
obs 2:   get_endpoint_spec → POST refunds
obs 3:   get_recent_errors → RefundService NPE
scratch: "NPE after capture; only captured payments refund"
```

If you paste every tool JSON forever, you blow the context window (Module 2.3) and pay for it (Module 2.6). If you drop the incident, the model forgets *why* it is looping.

## 3. Why it exists

Each `complete()` is a new HTTP call. The model does not magically remember `search_docs` from turn 1 unless you send it again (`input_items` + instructions, or `previous_response_id` which **still bills** prior input tokens). Memory is how *you* choose what is worth repeating.

Java would keep `HttpSession` or a `Map<String,Object>` on a bean. That session is not metered per character. LLM memory is.

### The Java analogy that misleads you

`HttpSession` / Spring `@SessionScope` looks like "remember this across requests". Sessions are cheap relative to tokens and they are not in the prompt. Dumping a session into the next `instructions` is how a 5-step triage becomes a 20k-token prompt. `previous_response_id` is also not free (Module 2.5).

## 4. Step-by-step examples

**Example 1 — add an observation.** `memory.add("observation", "search_docs: refunds page")`.

**Example 2 — pin the incident.** `memory.add("user", incident, pinned=True)` is never trimmed.

**Example 3 — trim oldest unpinned.** A 40-token budget drops long observations first.

**Example 4 — scratchpad.** A short joined summary, not the raw 4 KB tool JSON.

**Example 5 — do not store the whole corpus.** Retrieval belongs in Module 4's index; memory stores *what you learned*, not every chunk.

```bash
uv run python concepts/5_03/examples.py
```

The fake cannot teach a live model's attention over a long prompt. Graded tests check *your* trim and pin rules.

## 5. Common pitfalls

- Unbounded append (no budget).
- Trimming the user incident.
- Storing embeddings in "memory" (wrong module).
- Assuming `previous_response_id` is free context.

## 6. Exercises

1. **Guided:** `WorkingMemory.add` / `trim` / `used_tokens` with a pin flag.
2. **Open:** `scratchpad` — compress observations to `max_chars`.

```bash
uv run pytest concepts/5_03
```

- Hint 1: drop the oldest item with `pinned=False` until `used_tokens <= budget`.
- Hint 2: join with `" | "` and ellipsize.
- Solution: `solutions/memory.py`, `solutions/scratchpad.py`.

## 7. Check

1. What is pinned vs unpinned?
2. Predict: budget 10, three 8-token unpinned items — how many remain?
3. Does `previous_response_id` make memory free?
4. Why is `HttpSession` a misleading analog?

## Setup / troubleshooting

- Token counts use `estimate_tokens` (4 characters ≈ 1 token), not tiktoken.
- If trim never fires, your budget is larger than the fixture strings.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** `TriageDesk.investigate` pins the incident and records each tool observation under a 500-token budget.

**What you learned:** agent memory is a metered sticky note, not a session store.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
