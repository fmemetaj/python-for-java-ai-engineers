# 3.5 Evals: golden sets, rubric checks   [NEW — no Java equivalent] [cost: mock] [~55 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/3_05/tests/test_skip.py` passes. **Still recommended.**

DocsDesk eval file: `data/evals/docsdesk_m3.json` (≥15 cases). Runner: `docsdesk.evals.run_docsdesk_eval`.

## 1. Concept

An **eval** is a frozen set of cases plus **checks** (exact, schema, rubric) you run in pytest. It catches a prompt or tool-loop regression. It is not a vibe check, and it is not JUnit of a pure function: live model text is probabilistic.

## 2. Intuition

Think of a golden set as a **contract suite**. FakeLLM makes exact match legal. A live model needs weaker checks (schema + "must contain Bearer") and a **reported** pass rate — never a fake 100% claim.

```
cases.json  →  exact | schema | rubric | invalid_args
     ↓
pytest  /  uv run course check m3
     ↓
fake: CI gate     live: "pass rate N/M (no threshold claimed)"
```

## 3. Why it exists

Shipping an LLM feature without evals is shipping untested request mapping. Prompt edits silently change answers. Tool-arg bugs only show up in production. Java shops already gate merges on tests; evals are that gate for model-shaped behavior.

### The Java analogy that misleads you

JUnit `assertEquals(expected, svc.total())` works because `total()` is deterministic. `assertEquals(expectedParagraph, llm.complete())` is a flake machine. Use exact match on **fixtures**; use schema/rubric on live optional runs. Module 2's five-case exact eval was the warm-up; this lesson scales it and adds schema + rubric + invalid-tool cases.

## 4. Step-by-step examples

**Example 1 — exact.** `"Bearer" == "Bearer"` on FakeLLM scripts. Case-fold fails on purpose so you see the difference.

**Example 2 — schema.** `Incident.model_validate(payload)` — the check is "parses", not "equals this JSON string".

**Example 3 — rubric.** Every needle must appear (case-insensitive). Good for "must mention Bearer" without pinning the sentence.

**Example 4 — 15+ committed cases, all fake.** `run_docsdesk_eval()` is the CI gate.

**Example 5 — live reporting.** `format_live_rate(12, 15)` → `live pass rate 12/15 (no threshold claimed)`. This course does **not** invent a passing score for paid APIs.

```bash
uv run python concepts/3_05/examples.py
```

## 5. Common pitfalls

- One-case evals.
- Asserting full live paragraphs.
- Calling a live API from CI (keys, cost, flakes).
- Treating a live pass rate as a gate without calibration (Module 6).
- Changing the prompt and not re-running the golden set.

## 6. Exercises

1. **Guided:** `grade_exact`, `grade_schema`, `grade_rubric`.
2. **Open:** `run_harness` over ≥15 cases (must swallow grader exceptions) and `live_rate_line`.

```bash
uv run pytest concepts/3_05
```

- Hint 1: rubric uses `.lower()` on both sides.
- Hint 2: wrap `grader(case)` in `try/except` so one boom does not abort the suite.
- Solution: `solutions/checks.py`, `solutions/harness.py`.

## 7. Check

1. When is exact match honest?
2. Why is JUnit `assertEquals` a misleading analog?
3. How many cases does DocsDesk v0.3 ship, and do they need a key?
4. What must a live summary string say about thresholds?

## Setup / troubleshooting

- `LLM_PROVIDER=fake` (default). A live key is optional and never committed.
- If `run_docsdesk_eval` raises `RuntimeError`, you exported `LLM_PROVIDER=openai` in the shell. Unset it for graded work.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** `uv run course check m3` prints `evals pass` only when the 15+ fake cases are green.

**What you learned:** golden sets + three check types; live rates are reported, not gated.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
