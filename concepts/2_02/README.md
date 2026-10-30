# 2.2 Tokens and tokenization   [NEW — no Java equivalent] [cost: mock] [~40 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/2_02/tests/test_skip.py` passes. **Still recommended.**

Official docs: [Understanding and counting tokens](https://help.openai.com/en/articles/4936856-understanding-and-counting-tokens).

## 1. Concept

A **token** is the billing and context unit of an LLM call. It is not a word, not a character, and not a Java `char`. OpenAI bills **input** (prompt) tokens, **output** (completion) tokens, and sometimes **cached input** tokens at a different rate.

## 2. Intuition

Imagine feeding the model a stream of puzzle pieces. English often lands near 4 characters per token, but `https://`, code, and CJK split differently. `usage.input_tokens` is the billable count *after* the real tokenizer runs — not `text.split().length`.

```
"DocsDesk auth"  →  course estimate  (len+3)//4
                 →  real BPE (tiktoken) would differ slightly
```

## 3. Why it exists

HTTP APIs bill by a stable unit that is cheaper to count than Unicode words and closer to model internals than bytes. Java metering (API Gateway request count, CloudWatch bytes) does not map. You cannot `String.split("\\s+")` your way to a correct invoice.

### The Java analogy that misleads you

`String.length()` and `split("\\s+")` look like "size of the prompt". They are not. A 10-word Java identifier dumped into a prompt can be many tokens. Tests that assert `len(words) == usage.input_tokens` will fail against a live tokenizer.

## 4. Step-by-step examples

**Example 1 — course estimator.** `estimate_tokens("abcd")` is 1. Empty string is 0.

**Example 2 — words ≠ tokens.** `"one two three four"` is 4 whitespace words; the course estimator uses characters.

**Example 3 — punctuation and URLs.** `"https://docs.internal.test/auth"` is one "word" and many characters.

**Example 4 — Responses usage names.** `input_tokens` / `output_tokens` (Chat Completions still says `prompt_tokens` / `completion_tokens`).

**Example 5 — cached input.** Cached tokens are still input tokens; they are just cheaper. They count toward the context window.

```bash
uv run python concepts/2_02/examples.py
```

The fake cannot teach a production BPE tokenizer. Live OpenAI uses a different split; always read `response.usage`.

## 5. Common pitfalls

- Treating tokens as words or as UTF-16 `char` counts.
- Forgetting output tokens (and reasoning tokens inside output).
- Comparing models by sticker price without token counts.
- Logging raw prompts that contain secrets "because it's just tokens".

## 6. Exercises

1. **Guided:** implement `estimate_tokens` (4 characters ≈ 1 token) and compare it to a whitespace split.
2. **Open:** parse a Responses-shaped `usage` payload, including `cached_tokens`.

```bash
uv run pytest concepts/2_02
```

- Hint 1: `max(1, (len(text) + 3) // 4)` for non-empty text; 0 if empty.
- Hint 2: `input_tokens_details.cached_tokens` nests under usage in the real API; the course payload flattens it to `cached_tokens`.
- Solution: `solutions/tokens.py`, `solutions/usage.py`.

## 7. Check

1. Are tokens words?
2. Which usage field is the billing unit for the prompt?
3. Do cached tokens count toward the context window?
4. Why does DocsDesk print `usage` instead of `len(prompt.split())`?

## Setup / troubleshooting

- No tiktoken install is required for graded work.
- If you experiment live, read `response.usage` — never estimate a production bill from this course helper.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk prints `tokens in=` from FakeLLM `usage` so you can see the bill before a real key exists.

**What you learned:** tokens are the billing unit; words are a bad analog; always read `usage`.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
