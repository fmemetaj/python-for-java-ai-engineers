# 2.6 Token economics and cost calculation   [NEW — no Java equivalent] [cost: mock] [~45 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/2_06/tests/test_skip.py` passes. **Still recommended.**

Official docs: [Pricing](https://platform.openai.com/docs/pricing) (retrieved 2026-10-30 into `data/pricing.yaml`).

## 1. Concept

LLM calls are **metered**. USD = uncached input × input rate + cached input × cached rate + output × output rate, with rates **per 1 million tokens**. Never hard-code prices in prose.

## 2. Intuition

Cloud egress bills gigabytes; this bills tokens. Cached input is a discount on *repeated prefix* tokens, not free memory. Reasoning tokens (2.11) sit inside `output_tokens`.

```
cost = (in - cached)/1e6 * P_in + cached/1e6 * P_cached + out/1e6 * P_out
```

## 3. Why it exists

Without a calculator, "the bill tripled" is a mystery. Java reserved-instance pricing is a loose analog; there is no Maven plugin that prints `$0.001200` from `usage`.

### The Java analogy that misleads you

AWS invoice line items feel similar. `previous_response_id` feels like a server session that "already paid". It is not: **all previous input tokens in the chain are billed again as input**.

## 4. Step-by-step examples

**Example 1 — gpt-4.1-mini 1000 in / 500 out.** `$0.40` and `$1.60` per 1M → `$0.001200`.

**Example 2 — 800 cached of those 1000.** uncached 200 × 0.40 + 800 × 0.10 + 500 × 1.60 per 1M → `$0.000960`.

**Example 3 — gpt-5-mini 1M fully cached input, 0 out.** `$0.025`.

**Example 4 — replay vs stored.** Replaying the full transcript and using `previous_response_id` both bill prior input.

**Example 5 — DocsDesk prints `format_cost`.** Learners see `$` per turn without a key.

```bash
uv run python concepts/2_06/examples.py
```

The fake cannot teach a live invoice delay or cache-hit rate.

## 5. Common pitfalls

- Using output price for input (or the reverse).
- Treating cached tokens as *not* input.
- Assuming `store=true` is a cost optimization rather than a storage flag.

## 6. Exercises

1. **Guided:** `cost_of(usage, model)` against `data/pricing.yaml` via the same arithmetic as `course_kit.cost`.
2. **Open:** explain a "bill tripled" replay: billed input is the sum of every turn's prompt tokens when you resend history.

```bash
uv run pytest concepts/2_06
```

- Hint 1: load rates from the course table; do not hard-code 0.40 in the solution if you can call `load_pricing()`.
- Hint 2: `billed_input_after_replay([1200, 400, 400])` is 2000 if each turn resends everything so far... actually we'll define it as sum of each turn's *full* prompt size.
- Solution: `solutions/costing.py`, `solutions/replay.py`.

## 7. Check

1. Where do prices live, and what is their source URL?
2. Are cached tokens billed at the input rate?
3. Does `previous_response_id` zero out old input tokens?
4. Hand-compute example 1.

## Setup / troubleshooting

- If numbers drift, update `data/pricing.yaml` and the "retrieved" date — not the README.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** a teammate enabled `previous_response_id` to "save money" and the bill rose because each turn still billed the growing chain.

**What you learned:** dated YAML prices, cached vs uncached, stored state is not free.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
