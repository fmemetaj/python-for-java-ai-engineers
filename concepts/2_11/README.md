# 2.11 Reasoning models and effort settings   [NEW — no Java equivalent] [cost: mock] [~35 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/2_11/tests/test_skip.py` passes. **Still recommended.**

Official docs: [Migrate to Responses](https://platform.openai.com/docs/guides/migrate-to-responses) (reasoning items, `reasoning_effort`), [Counting tokens](https://help.openai.com/en/articles/4936856-understanding-and-counting-tokens).

## 1. Concept

**Reasoning models** spend hidden tokens planning before they speak. Those tokens are **not** the visible answer, but they count toward **output** usage and the context window. **Effort** (`none` / `low` / `medium` / `high`) trades latency and dollars for harder tasks.

## 2. Intuition

The model writes on scratch paper, then writes the postcard you see. You pay for the scratch paper. A 5-word answer can be expensive.

```
output_tokens = visible_answer_tokens + reasoning_tokens
```

## 3. Why it exists

Some tasks need internal search. Java `ExecutorService` thinking-time is not billed per thought. Here, thoughts are tokens. Starting with GPT-5.4, Chat Completions does not support tool calling with `reasoning_effort` other than `none` — another reason this course defaults to Responses.

### The Java analogy that misleads you

CPU time on a thread is not an output token. `System.nanoTime()` around a call measures *your* wait, not the hidden token bill. Always read `usage.output_tokens` / `output_tokens_details.reasoning_tokens`.

## 4. Step-by-step examples

**Example 1 — FakeLLM `reasoning_effort="none"`.** `reasoning_tokens == 0`, output is a message item only.

**Example 2 — `high`.** A `reasoning` item appears; `output_tokens` grows by 256 in the fake.

**Example 3 — visible vs billed.** visible 2 + reasoning 256 → billed output 258.

**Example 4 — latency/cost.** Higher effort → more output tokens → more USD at the output rate in `pricing.yaml`.

**Example 5 — DocsDesk.** Default effort unset (treated as none) so the skeleton stays cheap.

```bash
uv run python concepts/2_11/examples.py
```

The fake's token numbers are a teaching scale, not OpenAI's production counts.

## 5. Common pitfalls

- "The answer was short so it was cheap."
- Dropping `reasoning` Items when replaying context (migration error).
- Using Chat Completions + tools + effort ≠ none on newer models.

## 6. Exercises

1. **Guided:** map effort → fake reasoning tokens; add them to visible output.
2. **Open:** pick the cheaper effort given two token totals.

```bash
uv run pytest concepts/2_11
```

- Hint 1: none=0, low=16, medium=64, high=256 in the course fake.
- Hint 2: billed output = visible + reasoning; cheaper means fewer billed output tokens here.
- Solution: `solutions/effort.py`, `solutions/tradeoff.py`.

## 7. Check

1. Are reasoning tokens billed as input or output?
2. Can a short answer still be expensive?
3. Why does this course still prefer Responses for reasoning + tools?
4. Predict FakeLLM output_tokens for effort high vs none on the same scripted reply.

## Setup / troubleshooting

- If you opt into live keys, check the model page for effort support before setting `high`.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** turning effort to `high` on every DocsDesk FAQ would burn output tokens; leave it off for lookup, raise it for a later agent module.

**What you learned:** hidden reasoning tokens are output. Effort is a cost/latency knob. Fake numbers are for tests, not invoices.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
