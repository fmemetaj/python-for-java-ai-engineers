# 2.3 Context window and model limits   [NEW — no Java equivalent] [cost: mock] [~30 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/2_03/tests/test_skip.py` passes. **Still recommended.**

Official docs: [Conversation state](https://platform.openai.com/docs/guides/conversation-state), [gpt-4.1-mini](https://platform.openai.com/docs/models/gpt-4.1-mini).

## 1. Concept

A **context window** is the maximum number of tokens a model can see in one request: input + output + (for some models) reasoning tokens. Exceed it and the API rejects the call or the model silently drops the beginning.

## 2. Intuition

Think of a whiteboard with a fixed number of squares. Every prompt token, every prior turn you replay, and every token the model is allowed to write occupies a square. `max_output_tokens` reserves squares at the end so the model can actually answer.

```
[ pasted doc | prior turns | question | reserved output ]
|<-------------- context window ----------------------->|
```

## 3. Why it exists

Transformers attend over a finite sequence. Java heap size is a misleading analog: the JVM can GC; the window cannot. HTTP max body size is closer (a hard cap), but bytes ≠ tokens.

### The Java analogy that misleads you

`HttpServletRequest` has no "memory of the previous POST" unless you put it in a session. The context window *is* that memory budget, measured in tokens, and it includes the answer you have not generated yet.

## 4. Step-by-step examples

**Example 1 — remaining budget.** window 100, input 40, reserved output 20 → 40 left.

**Example 2 — overflow.** A 90-token doc + 20 reserved output on a 100-token window overflows.

**Example 3 — real model windows.** `gpt-4.1-mini` is 1,047,576 tokens per the model page; exercises use a tiny window so the arithmetic is visible.

**Example 4 — max output.** Requesting 8k output on a model whose `max_output_tokens` is 32k is fine; requesting more than the window minus input is not.

**Example 5 — DocsDesk pasted doc.** A 50-page dump can crowd out the question. Trim (concept 2.8) before calling.

```bash
uv run python concepts/2_03/examples.py
```

The fake cannot teach a live `context_length_exceeded` error.

## 5. Common pitfalls

- Counting only the user question.
- Forgetting reserved output and reasoning tokens.
- Assuming `previous_response_id` expands the window (it does not).

## 6. Exercises

1. **Guided:** `remaining_budget` and `would_overflow`.
2. **Open:** `max_input_for` and `clamp_output`.

```bash
uv run pytest concepts/2_03
```

- Hint 1: remaining = window - input - reserved_output; raise if negative.
- Hint 2: max input = window - reserved_output; clamp output to [0, max_output].
- Solution: `solutions/window.py`, `solutions/limits.py`.

## 7. Check

1. Does the window include output tokens?
2. Why reserve output space before sending a huge doc?
3. Is a 1M window "unlimited" for a whole repo?
4. Predict overflow: window 80, texts totalling 70 tokens, reserved 20.

## Setup / troubleshooting

- Graded tests use the course estimator, not tiktoken.
- Live errors mention context length; shrink the pasted doc first.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk pastes one page, not the entire Spring repo, so the question still fits.

**What you learned:** the window is input+output(+reasoning). Reserve output. Trim later in 2.8.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
