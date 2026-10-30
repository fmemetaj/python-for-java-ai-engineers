# A.9 Spend-capped smoke tests and sanitized fixtures   [NEW — no Java equivalent] [cost: mock] [~50 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/a_09/tests/test_skip.py` passes. **Still recommended.**

Official docs: [Pricing](https://platform.openai.com/docs/pricing). Helpers: `course_kit.upgrade.run_smoke`, `sanitize_record`. DocsDesk: `docsdesk.smoke`.

## 1. Concept

A **spend-capped smoke test** runs FakeLLM (or, live, a tiny budget) until the *next* call would exceed the cap, then **skips** the rest. A **sanitized fixture** is recorded JSON with `sk-…`, `Bearer …`, and `course-test-secret-value` replaced by `***`. Graded work never spends a live key.

## 2. Intuition

Module 6 budgets a *request*. This lesson budgets a *checklist*. WireMock recordings are the closest Java habit — and they still leak headers if you commit them raw.

```
calls: a=$0.004, b=$0.004, c=$0.004
cap: $0.01
ran: a, b    skipped: c    spent: $0.008
```

## 3. Why it exists

Live smoke without a cap is how surprise bills start (F8). Recorded fixtures without redaction are how keys land in git. Both are engineering, not "we'll be careful".

### The Java analogy that misleads you

WireMock **record-and-playback** is a partial analog for fixtures. It does not teach token USD, and it will happily serialize `Authorization`. SQL injection analogs do not apply; this is secret hygiene plus a budget.

## 4. Step-by-step examples

**Example 1 — third call skipped** at a $0.01 cap.

**Example 2 — DocsDesk smoke** prices FakeLLM usage from `data/pricing.yaml`.

**Example 3 — `sk-` redacted.**

**Example 4 — Bearer headers redacted.**

**Example 5 — honesty.** The fake cannot teach a real 429; the cap is the drill.

```bash
uv run python concepts/a_09/examples.py
uv run docsdesk smoke
```

## 5. Common pitfalls

- Running remaining calls "just this once" after the cap.
- Committing `OPENAI_API_KEY` inside a recorded JSON.
- Using a live provider in `course check ma`.
- Confusing this with Module 6's per-request budget (different layer).

## 6. Exercises

1. **Guided:** `capped(calls, cap_usd)`.
2. **Open:** `sanitize(payload)` (recursive).

```bash
uv run pytest concepts/a_09
```

- Hint 1: skip as soon as `spent + next > cap`.
- Hint 2: walk dicts/lists; regexes live in `course_kit.upgrade`.
- Solution: `solutions/smoke.py`, `solutions/sanitize.py`.

## 7. Check

1. What happens to the call that would exceed the cap?
2. May recorded fixtures include `sk-` keys?
3. Why is WireMock only a partial analog?
4. Predict: cap `$0` and one `$0.001` call — ran or skipped?
5. Does `docsdesk smoke` require `LLM_PROVIDER=fake` in this course?

## Setup / troubleshooting

- Graded smoke raises if `LLM_PROVIDER` is not `fake`.
- Never commit `.env`. Doctor reports whether the key is *set*, not the value.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** `uv run docsdesk smoke` is the elective checklist; Module 7 still uses `eval-v1` as the product gate.

**What you learned:** cap the checklist; redact fixtures; never Assistants; never commit keys.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
