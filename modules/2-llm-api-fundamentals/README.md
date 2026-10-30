# Module 2 — LLM API Fundamentals

[Analog + NEW] [cost: mock] [~7–8 h estimated] [last verified: 2026-10-30, Python 3.11–3.13]

**Objective:** call an LLM correctly and cheaply, and understand tokens, cost, state, and the two OpenAI API styles (Responses vs Chat Completions).

**Prereqs:** Module 1 (or equivalent: uv project, httpx, pytest, env config). Professional Java (or another typed backend language).

**Offline:** every graded exercise uses `LLM_PROVIDER=fake`, `data/pricing.yaml`, and pytest. No API key. Cost badge: `mock`. Optional live OpenAI uses the [Responses API](https://platform.openai.com/docs/guides/migrate-to-responses) (`client.responses.create`), never the sunset Assistants API. Optional Ollama stays on loopback.

Total live cost if you opt in: **not required**. At prices in `data/pricing.yaml` (retrieved 2026-10-30 from [OpenAI pricing](https://platform.openai.com/docs/pricing)), a handful of short gpt-4.1-mini turns is typically well under a few cents — still optional.

## Do I need this? (3 questions)

If you can answer these without looking them up, run the skip tests. **NEW** concepts (tokens, windows, sampling, cost, prompts, reasoning) are still recommended.

1. What is a token, and which `usage` fields are input vs output vs cached?
2. Name three differences between Chat Completions and Responses, plus one cost implication of `previous_response_id`.
3. Where do USD rates live in this repo, and why must they be dated?

Per-concept skip (2–3 minutes):

```bash
uv run pytest concepts/2_01/tests/test_skip.py
```

Pass an Analog skip test → skip that concept. Pass a NEW skip test → still read the lesson.

## Concepts in order

| ID | Lesson | Kind | Est. | Skip / exercise |
|---|---|---|---:|---|
| 2.1 | [LLM client from env](../../concepts/2_01/README.md) | Analog | 25 min | `uv run pytest concepts/2_01` |
| 2.2 | [Tokens and tokenization](../../concepts/2_02/README.md) | **NEW** | 40 min | `uv run pytest concepts/2_02` |
| 2.3 | [Context window](../../concepts/2_03/README.md) | **NEW** | 30 min | `uv run pytest concepts/2_03` |
| 2.4 | [Sampling and temperature](../../concepts/2_04/README.md) | **NEW** | 35 min | `uv run pytest concepts/2_04` |
| 2.5 | [Provider abstraction](../../concepts/2_05/README.md) | Analog | 30 min | `uv run pytest concepts/2_05` |
| 2.6 | [Token economics](../../concepts/2_06/README.md) | **NEW** | 45 min | `uv run pytest concepts/2_06` |
| 2.7 | [Responses vs Chat Completions](../../concepts/2_07/README.md) | Analog | 75 min | `uv run pytest concepts/2_07` |
| 2.8 | [Conversation state](../../concepts/2_08/README.md) | Analog | 45 min | `uv run pytest concepts/2_08` |
| 2.9 | [Streaming](../../concepts/2_09/README.md) | Analog | 30 min | `uv run pytest concepts/2_09` |
| 2.10 | [Prompts as code + first eval](../../concepts/2_10/README.md) | **NEW** | 45 min | `uv run pytest concepts/2_10` |
| 2.11 | [Reasoning models](../../concepts/2_11/README.md) | **NEW** | 35 min | `uv run pytest concepts/2_11` |

Times are unmeasured estimates. [Tell us your actual minutes](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).

## How each lesson works

- **Analog:** Java snippet first (≤15 lines, compiled in CI with JDK 21) → Python equivalent → differences & pitfalls table → exercise → check.
- **NEW:** intuition → why it exists (and the Java analogy that misleads you) → 3–5 step-by-step examples → ≥2 exercises → check.
- Starters live in `concepts/2_XX/exercises/`. They **fail** the tests on purpose. Solutions live in `concepts/2_XX/solutions/` and are validated in CI. Do not copy solutions until you have tried the hints.

The fake cannot teach live latency, tokenizer drift, cache-hit rates, or temperature variance. Graded tests check *your* parsing, arithmetic, and loops.

## Module deliverable

DocsDesk answers from a pasted document, prints tokens and USD per call, and keeps a multi-turn session on `FakeLLM` (`previous_response_id` still bills prior input).

```bash
uv run python -m docsdesk
uv run pytest tests/test_docsdesk.py tests/test_fake_llm.py tests/test_cost.py
```

`LLM_PROVIDER` defaults to `fake`. Secrets still never appear in logs (Module 1).

## Module checkpoint

```bash
uv run course check m2
```

Prints pass/fail per concept, plus `docsdesk`, `fake_llm`, and `cost`. CI runs the same command against `solutions/`.

## Setup if you get stuck

PATH, `python` vs `python3`, Windows Store stub, `uv` / `.venv`, encoding, and line endings: [troubleshooting](../../docs/setup/troubleshooting.md).

- **API keys:** copy `.env.example` → `.env`. Never commit `.env`. Doctor reports whether `OPENAI_API_KEY` is set, not the value.
- **Wrong API:** `client.responses.create` only. No Assistants API, no `openai.ChatCompletion.create`.
- **Bill looks wrong:** prices are in `data/pricing.yaml` (dated). Stored state still bills input tokens.
- **Editor interpreter:** Command Palette → Python: Select Interpreter → `.venv`.

```bash
uv sync --locked --group dev
uv run python scripts/doctor.py --offline
```
