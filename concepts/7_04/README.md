# 7.4 Eval report (≥30 cases) as a CI gate   [NEW — no Java equivalent] [cost: mock] [~55 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/7_04/tests/test_skip.py` passes. **Still recommended.**

Official docs: [OpenAI evals](https://platform.openai.com/docs/guides/evaluation). DocsDesk files: `data/evals/docsdesk_m7.json`, `docsdesk.portfolio.run_v1_eval`.

## 1. Concept

The capstone **eval report** is one bundle: Module 3 goldens, Module 4 retrieval, Module 5 agent, Module 6 judge/gate, and the injection suite. The rubric wants **≥30 cases**, all green on FakeLLM. That number is a CI gate, not a live-model SLA.

## 2. Intuition

```
m3 golden + schema + tools     18
m4 recall@5 / groundedness     10
m5 agent success / step cap     4
m6 judge + extra goldens        5
injection suite                 7
                              ----
                               44  (≥30)
```

Counts are from the committed fixtures. If you add cases, keep them offline.

## 3. Why it exists

A README that says "it usually works" is not evidence. A pytest that fails when you mutate `expected_answer` is.

### The Java analogy that misleads you

Surefire "44 tests, 0 failures" is honest for `RefundService`. It is not honest for a live `gpt-4.1-mini` paragraph. The capstone gate is 100% **on the fake**. Live optional runs *report a rate* and claim no bar (Module 3 / 6).

## 4. Step-by-step examples

**Example 1 — merge counts.** `(18,18)+(10,10)+(4,4) → (32,32)`.

**Example 2 — bar.** `meets_capstone_bar(29, 29)` is false (too few). `meets_capstone_bar(44, 43)` is false (a miss).

**Example 3 — run the harness.** `run_v1_eval(provider="fake")` prefixes ids (`m3:exact-auth`) so suites do not collide.

**Example 4 — injected regression.** Mutating one golden still fails Module 6's gate; the capstone bundle includes that suite.

**Example 5 — live key.** `LLM_PROVIDER=openai` raises on this harness. Do not "fix" a red fake by exporting a key.

```bash
uv run python concepts/7_04/examples.py
```

## 5. Common pitfalls

- Counting the same `exact-auth` twice without a prefix and thinking you have 30 unique behaviors. Prefixing is fine — they are different harnesses.
- Putting a live judge in CI.
- Claiming "≥30" while shipping 18 goldens and a screenshot.

## 6. Exercises

1. **Guided:** `merge_counts`.
2. **Open:** `meets_capstone_bar` (min 30, all passed, reject impossible counts).

```bash
uv run pytest concepts/7_04
```

- Hint 1: empty parts → `(0, 0)`.
- Hint 2: `passed > total` is a `ValueError`, not `False`.
- Solution: `solutions/report.py`, `solutions/gate.py`.

## 7. Check

1. Why is 29/29 not enough?
2. What does this course claim about live pass rates?
3. Why prefix `m3:` on case ids?
4. Should you export `OPENAI_API_KEY` to make a red fake green?

## Setup / troubleshooting

- `uv run docsdesk eval-v1` prints the bundle. Exit 0 only when the gate passes.
- If retrieval is red: rebuild `data/embeddings/payments-api.json`, do not switch provider.
- Windows: long pytest output — `uv run pytest --tb=line`.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** `tests/test_docsdesk_v1.py` asserts `report.total >= 30` and zero failures on fake.

**What you learned:** ≥30 offline cases, 100% on FakeLLM, no live SLA.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
