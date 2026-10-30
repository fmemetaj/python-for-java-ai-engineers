# 6.4 Cost control: budgets, routing, prompt caching   [NEW — no Java equivalent] [cost: mock] [~45 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/6_04/tests/test_skip.py` passes. **Still recommended.**

Official docs: [prompt caching](https://platform.openai.com/docs/guides/prompt-caching), [OpenAI pricing](https://platform.openai.com/docs/pricing). Prices: `data/pricing.yaml` (retrieved 2026-10-30). DocsDesk: `docsdesk.budget`.

## 1. Concept

A **budget** is remaining USD. **Routing** picks a cheaper model when the remainder is tight. **Prompt caching** bills matching prefix tokens at `cached_input_per_million`. A **dashboard** is the sum of `cost_usd` fields you already logged (concept 6.2) — not a SaaS.

## 2. Intuition

Cloud invoices tell you after you spent. A request budget tells you *before* `complete()`. FakeLLM still fills `usage.cached_tokens` so the Module 2 formula can show the discount offline.

```
remaining = limit - spent
if remaining < estimated: route to gpt-4.1-nano (or refuse)
cost = uncached * input_rate + cached * cached_rate + output * output_rate
```

## 3. Why it exists

Token bills surprise Java teams used to a flat VM. Module 2 taught the formula. This lesson is the control loop: cap, route, cache, then *read the logs* you already emit. There is no Spring annotation that does this.

### The Java analogy that misleads you

Metered cloud billing / AWS budgets are a loose cousin: they alert on *account* spend, usually after the fact, and they do not pick `gpt-4.1-nano` for the next Responses call. `@Cacheable` caches *your* method, not the provider's prompt-prefix cache.

## 4. Step-by-step examples

**Example 1 — remaining.** `limit=1.00`, `spent=0.40` → `0.60`.

**Example 2 — over budget.** `spent > limit` → `within_budget` is false; ProductionDesk raises `BudgetExceededError` before debiting past the cap when the next call cannot fit.

**Example 3 — route.** Tiny remainder → `gpt-4.1-nano`. Comfortable remainder → `gpt-4.1-mini`.

**Example 4 — cache discount.** 1000 cached tokens at mini rates: full input $0.000400, cached input $0.000100, **saved $0.000300**.

**Example 5 — dashboard.** Two JSON log lines, `costs_from_logs` sums `cost_usd`.

```bash
uv run python concepts/6_04/examples.py
```

## 5. Common pitfalls

- Hard-coding prices in lesson code (they live in `data/pricing.yaml`).
- Treating `cached_tokens` as free (they are cheaper, not zero).
- Routing *after* the expensive call.
- Building a dashboard from `print()` instead of JSON logs.
- Calling a live API from the graded path.

## 6. Exercises

1. **Guided:** `remaining`, `route_model`.
2. **Open:** `total_cost` of log rows and `cache_discount` in USD.

```bash
uv run pytest concepts/6_04
```

- Hint 1: nano when `remaining < estimated`, else mini; refuse when remaining cannot cover a cheap stub.
- Hint 2: saved = `cached_tokens * (input_rate - cached_rate) / 1_000_000`.
- Solution: `solutions/budget.py`, `solutions/dashboard.py`.

## 7. Check

1. Are cached input tokens free?
2. Where do prices live, and why not in this README?
3. What should happen when remaining USD cannot cover even nano?
4. How does a dashboard get per-request cost without a SaaS?
5. Does routing a live model in CI get a paid key?

## Setup / troubleshooting

- `LLM_PROVIDER=fake`. Live OpenAI is optional via `.env`; keys never committed.
- If `route_model` raises `BudgetExceededError`, that is the lesson, not a broken install.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** ProductionDesk logs `cost_usd` on every ask. `CostLedger.total()` is the in-memory dashboard.

**What you learned:** remaining budget, model routing, cached-token discount, sum-of-logs dashboard.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
