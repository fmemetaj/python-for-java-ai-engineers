# 6.1 Eval strategy, LLM-as-judge, CI gates   [NEW — no Java equivalent] [cost: mock] [~60 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/6_01/tests/test_skip.py` passes. **Still recommended.**

Official docs: [OpenAI evals](https://platform.openai.com/docs/guides/evaluation). DocsDesk files: `data/evals/docsdesk_m6.json`, `docsdesk.gate`, `docsdesk.judge`.

## 1. Concept

An **eval strategy** is how you decide a prompt, tool, or model change is safe to merge. Module 3 gave you golden cases. This lesson adds an **LLM-as-judge** (a second model scores an answer) and a **CI gate** (a frozen pass rate that fails the build).

## 2. Intuition

Think of three layers, not one test class:

```
offline golden (exact / schema / rubric)  →  CI must be 100% on FakeLLM
LLM-as-judge (score 1–5 vs a rubric)     →  only after you calibrate it
live optional run                         →  report a rate, claim no bar
```

Calibration means: on a labeled set, the judge's pass/fail **agrees** with the labels. An uncalibrated judge in CI is a flake machine.

## 3. Why it exists

Prompt edits silently change answers. A judge catches "sounds fine but missed Bearer". A gate catches "I tweaked the prompt and 3 of 15 exact cases died". Java shops already fail the merge on red tests; this is that gate for model-shaped behavior.

### The Java analogy that misleads you

JUnit `assertEquals(expected, svc.total())` is honest because `total()` is deterministic. `assertEquals(paragraph, llm.complete())` flakes. `assertTrue(gpt_judge.score(answer) >= 4)` flakes **and** can rubber-stamp a wrong answer if you never measured agreement. Module 3 already warned you; this lesson is the production version: calibrate, then gate.

## 4. Step-by-step examples

**Example 1 — golden still exact-matches on FakeLLM.** `"Bearer token" == "Bearer token"`. Case-fold still fails.

**Example 2 — judge scores a fixture.** FakeLLM returns `{"score": 5, "pass": true}` for the auth answer. Threshold 4 → pass.

**Example 3 — calibration.** Four predictions vs four labels; `agreement_rate` is `3/4 = 0.75`. You would not ship a 0.75 judge as a 100% CI gate.

**Example 4 — CI gate on the baseline.** `eval_gate(report, min_pass_rate=1.0)` is true for the committed fake set.

**Example 5 — injected regression.** Change `expected_answer` on `exact-auth` to `"WRONG"`. The same FakeLLM still returns the real sentence. The gate goes red. That is the Module 6 acceptance test.

```bash
uv run python concepts/6_01/examples.py
```

## 5. Common pitfalls

- Putting a live judge in CI with no labels (cost, flakes, self-grading).
- Exact-matching live prose.
- Claiming a live pass-rate threshold (this course never does).
- Calibrating on the same 3 cases you then gate on (train/test leakage, even for a judge).
- Forgetting `LLM_PROVIDER=fake` so the gate tries to call a paid API.

## 6. Exercises

1. **Guided:** `verdict_passes`, `agreement_rate`.
2. **Open:** `gate_ok` and `inject_wrong_answer` (the gate must fail after the mutation).

```bash
uv run pytest concepts/6_01
```

- Hint 1: agreement is `sum(pred is label) / len(labels)`.
- Hint 2: copy each case dict; only the matching `id` gets a new `expected_answer`.
- Solution: `solutions/judge.py`, `solutions/gate.py`.

## 7. Check

1. When is exact match an honest CI gate?
2. What does "calibrate a judge" mean in one sentence?
3. Why is JUnit `assertEquals` a misleading analog for a live judge?
4. What happens to `eval_gate` when one golden expected string is mutated?
5. Does this course claim a passing score for paid APIs?

## Setup / troubleshooting

- `LLM_PROVIDER=fake` (default). A live key is optional and never committed.
- If a gate raises `RuntimeError` about live eval, you exported `LLM_PROVIDER=openai`. Unset it.
- Windows: `set LLM_PROVIDER=fake`. PowerShell: `$env:LLM_PROVIDER="fake"`. macOS/Linux: `export LLM_PROVIDER=fake`.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** `uv run course check m6` prints `prod pass` only when the fake gate and the injection suite are green.

**What you learned:** golden + calibrated judge + a CI gate that fails on an injected regression.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
