# 7.5 Cost report per 100 requests   [NEW — no Java equivalent] [cost: mock] [~45 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/7_05/tests/test_skip.py` passes. **Still recommended.**

Official docs: [OpenAI pricing](https://platform.openai.com/docs/pricing) (retrieved 2026-10-30 into `data/pricing.yaml`). DocsDesk files: `docsdesk.portfolio.build_cost_report`.

## 1. Concept

A **cost report** answers "what would 100 of these asks cost?" with a model id, a dated price table, and a list of assumptions. The number is an estimate from one FakeLLM `usage` scaled by 100, not an invoice.

## 2. Intuition

```
one fake ask → usage.input_tokens / output_tokens
             → cost_usd(model, data/pricing.yaml)
             → × 100  (no cache hits in the sample)
```

Cached input tokens are cheaper when they happen (Module 6). This report states "no cache hits" so the 100× figure is conservative.

## 3. Why it exists

Interviewers will ask what it costs. "It's just tokens" is not an answer. Java cloud bills arrive after the fact; token routing has to happen *before* `complete()`.

### The Java analogy that misleads you

AWS Cost Explorer on last month's bill is a rear-view mirror. A DocsDesk budget is a remaining-USD check *before* the next call. Do not screenshot a live dashboard you do not have.

## 4. Step-by-step examples

**Example 1 — scale.** `$0.000040 × 100 = $0.004000`.

**Example 2 — required fields.** `requests`, `model`, `usd_per_request`, `usd_per_100`, `pricing_source`, `pricing_retrieved`, `assumptions`, `provider`.

**Example 3 — source.** `https://platform.openai.com/docs/pricing`, retrieved `2026-10-30`. Never paste a price into README prose that can rot.

**Example 4 — assumptions.** Fake provider, Responses API, FakeEmbedder, nothing deployed.

**Example 5 — `uv run docsdesk cost-report`.** Prints the summary. Still mock.

```bash
uv run python concepts/7_05/examples.py
```

## 5. Common pitfalls

- Hard-coding `$0.40 / 1M` in Markdown (the YAML will change; the README will lie).
- Multiplying a *cached* call by 100 and calling it typical.
- Forgetting the model id (nano vs mini is a 4× input gap in the current table).
- Treating FakeLLM token estimates as the live tokenizer.

## 6. Exercises

1. **Guided:** `cost_per_n`.
2. **Open:** `cost_report_fields`.

```bash
uv run pytest concepts/7_05
```

- Hint 1: negative USD or n → `ValueError`.
- Hint 2: look at `CostReport.as_dict()` keys.
- Solution: `solutions/scale.py`, `solutions/fields.py`.

## 7. Check

1. Where do prices live, and what date is stamped?
2. Why state "no cache hits" on the 100× figure?
3. Is this an invoice?
4. Which API is used for generation?

## Setup / troubleshooting

- Prices: `data/pricing.yaml`. Do not commit keys there.
- Windows `cmd` `$` in strings is fine; PowerShell `$env:` is for env vars.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** the portfolio README's cost section is this report, not a screenshot of a paid dashboard.

**What you learned:** scale FakeLLM usage × 100; cite the dated price file; list assumptions.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
