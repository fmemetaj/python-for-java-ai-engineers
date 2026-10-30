# Module 3 — Structured Outputs, Tool Calling, First Evals

[Analog + NEW] [cost: mock] [~4–5 h estimated] [last verified: 2026-10-30, Python 3.11–3.13]

**Objective:** get reliable typed data out of models and let models call your code safely.

**Prereqs:** Module 2 (Responses vs Chat Completions, FakeLLM, cost). Professional Java (or another typed backend language).

**Offline:** every graded exercise uses `LLM_PROVIDER=fake`, Pydantic schemas, a scripted tool loop, and pytest. No API key. Cost badge: `mock`. Optional live OpenAI uses the [Responses API](https://platform.openai.com/docs/guides/migrate-to-responses) (`client.responses.create` / `client.responses.parse`), never the sunset Assistants API. Optional Ollama stays on loopback.

Total live cost if you opt in: **not required**. Structured-output and tool-loop turns use more tokens than a single completion. Prices live in `data/pricing.yaml` (retrieved 2026-10-30 from [OpenAI pricing](https://platform.openai.com/docs/pricing)).

## Do I need this? (3 questions)

If you can answer these without looking them up, run the skip tests. **NEW** concepts (the tool-call loop, evals) are still recommended.

1. Where does Responses put a JSON Schema (`text.format`) vs Chat Completions (`response_format`)?
2. How do you pair a `function_call` with a `function_call_output`?
3. Name three eval check types, and why JUnit `assertEquals` on live prose is a trap.

Per-concept skip (2–3 minutes):

```bash
uv run pytest concepts/3_01/tests/test_skip.py
```

Pass an Analog skip test → skip that concept. Pass a NEW skip test → still read the lesson.

## Concepts in order

| ID | Lesson | Kind | Est. | Skip / exercise |
|---|---|---|---:|---|
| 3.1 | [Structured outputs](../../concepts/3_01/README.md) | Analog | 50 min | `uv run pytest concepts/3_01` |
| 3.2 | [Function/tool calling](../../concepts/3_02/README.md) | Analog | 45 min | `uv run pytest concepts/3_02` |
| 3.3 | [The tool-call loop](../../concepts/3_03/README.md) | **NEW** | 40 min | `uv run pytest concepts/3_03` |
| 3.4 | [Tool safety](../../concepts/3_04/README.md) | Analog | 40 min | `uv run pytest concepts/3_04` |
| 3.5 | [Evals 101](../../concepts/3_05/README.md) | **NEW** | 55 min | `uv run pytest concepts/3_05` |

Times are unmeasured estimates. [Tell us your actual minutes](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).

## How each lesson works

- **Analog (3.1, 3.2, 3.4):** Java snippet first (≤15 lines, compiled in CI with JDK 21) → Python equivalent → differences & pitfalls table → exercise → check.
- **NEW (3.3, 3.5):** intuition → why it exists (and the Java analogy that misleads you) → 3–5 step-by-step examples → ≥2 exercises → check.
- Starters live in `concepts/3_XX/exercises/`. They **fail** the tests on purpose. Solutions live in `concepts/3_XX/solutions/` and are validated in CI. Do not copy solutions until you have tried the hints.

The fake cannot teach live refusal rates, a model that invents a tool name, or eval variance. Graded tests check *your* schemas, loops, validation, and harness.

## Module deliverable

DocsDesk v0.3 returns a typed `TypedAnswer` with citations and can call `search_docs` / `get_endpoint_spec`. Invalid tool args are handled. An eval set of ≥15 cases passes on fake.

```bash
uv run python -m docsdesk
uv run pytest tests/test_docsdesk.py tests/test_fake_llm.py tests/test_docsdesk_eval.py
```

`LLM_PROVIDER` defaults to `fake`. Secrets still never appear in logs (Module 1).

## Module checkpoint

```bash
uv run course check m3
```

Prints pass/fail per concept, plus `docsdesk`, `fake_llm`, and `evals`. CI runs the same command against `solutions/`.

## Setup if you get stuck

PATH, `python` vs `python3`, Windows Store stub, `uv` / `.venv`, encoding, and line endings: [troubleshooting](../../docs/setup/troubleshooting.md).

- **API keys:** copy `.env.example` → `.env`. Never commit `.env`. Doctor reports whether `OPENAI_API_KEY` is set, not the value.
- **Wrong API:** `client.responses.create` / `responses.parse` only. No Assistants API. Structured outputs: `text.format`, not only Chat Completions `response_format`.
- **Tool loop stuck:** pair `function_call_output` by `call_id`; cap steps; keep `LLM_PROVIDER=fake` for graded work.
- **Eval red on fake:** do not "fix" it by pointing at a live key. The gate is your parsing/loop/validation.
- **Editor interpreter:** Command Palette → Python: Select Interpreter → `.venv`.

```bash
uv sync --locked --group dev
uv run python scripts/doctor.py --offline
```
