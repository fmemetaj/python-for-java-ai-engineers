# 2.4 Sampling, temperature, nondeterminism   [NEW — no Java equivalent] [cost: mock] [~35 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/2_04/tests/test_skip.py` passes. **Still recommended.**

Official docs: [Responses create](https://platform.openai.com/docs/api-reference/responses/create) (`temperature`).

## 1. Concept

**Sampling** is how a model picks the next token from a probability distribution. **Temperature** scales that distribution: higher → more random, lower → more peaked. Even temperature `0` is not a Java `HashMap` lookup — live APIs can still vary.

## 2. Intuition

A Java method with no `Random` is deterministic. An LLM is closer to rolling a weighted die each token. Temperature 0 is "almost always the highest-weight face". Temperature 1 is the model's native weights. Temperature 2 is a noisy die.

```
next token ~ softmax(logits / temperature)
```

You do not need the formula in production. You need the engineering consequence: **tests cannot assert exact live wording**.

## 3. Why it exists

If the model always picked `argmax`, every DocsDesk answer would be the same bland sentence. Sampling lets you trade variety against reliability. Java `Random` + a seed is a partial analog for *your* FakeLLM, not for the hosted API.

### The Java analogy that misleads you

`Math.random()` plus a seed in tests is reproducible. Hosted LLM sampling is not a seeded `Random` you control. FakeLLM ignores temperature so CI stays green. That is honest: the fake cannot teach live variance.

## 4. Step-by-step examples

**Example 1 — FakeLLM is deterministic.** Same prompt → same `output_text`.

**Example 2 — temperature is a request field.** Responses and Chat Completions both accept it.

**Example 3 — compare temperatures.** `1.2` is more random than `0.2`.

**Example 4 — eval style.** Grade cost math and JSON shape, never `"the" vs "The"` of a live model.

**Example 5 — DocsDesk.** Default fake answers are stable; optional live calls may differ across reruns.

```bash
uv run python concepts/2_04/examples.py
```

## 5. Common pitfalls

- Asserting exact assistant prose in pytest against a live key.
- Setting temperature and assuming seed-like reproducibility.
- Using high temperature for extraction tasks (wait for Module 3 structured outputs).

## 6. Exercises

1. **Guided:** compare temperatures; document that FakeLLM is deterministic.
2. **Open:** choose an assertion strategy (`behavior` vs `forbidden`).

```bash
uv run pytest concepts/2_04
```

- Hint 1: more random means strictly greater temperature.
- Hint 2: grading `usage` / cost / schema is `behavior`; grading live wording is `forbidden`.
- Solution: `solutions/sampling.py`, `solutions/eval_style.py`.

## 7. Check

1. Does temperature 0 guarantee identical live responses?
2. Why does CI use FakeLLM?
3. What should a pytest assert on a cost calculator?
4. Predict: two live calls, temperature 1.0, same prompt — same string?

## Setup / troubleshooting

- Flaky live tests? You opted into `openai`. Switch back to `LLM_PROVIDER=fake`.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk's graded tests never compare full sentences from a hosted model.

**What you learned:** sampling is why LLM tests grade behavior, not wording. The fake hides latency and variance on purpose.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
