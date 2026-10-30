# Module 6 — Evals, Observability, Production

[Analog + NEW] [cost: mock] [~5–6 h estimated] [last verified: 2026-10-30, Python 3.11–3.13]

**Objective:** make DocsDesk shippable: measured, observable, secure, and within budget.

**Prereqs:** Module 5 (agents, traces). Module 3 (evals 101, tool safety). Professional Java (or another typed backend language).

**Offline:** every graded exercise uses `LLM_PROVIDER=fake`, FakeLLM, fixture embeddings from Module 4 where retrieval is involved, and pytest. No API key. Cost badge: `mock`. Optional live OpenAI uses the [Responses API](https://platform.openai.com/docs/guides/migrate-to-responses) (`client.responses.create`), never the sunset Assistants API. Optional Ollama stays on loopback. Docker and bound ports are optional and are skipped in CI.

Total live cost if you opt in: **not required**. Judge calls use extra tokens. Prices live in `data/pricing.yaml` (retrieved 2026-10-30 from [OpenAI pricing](https://platform.openai.com/docs/pricing)).

## Do I need this? (3 questions)

If you can answer these without looking them up, run the skip tests. **NEW** concepts (judge/gates, cost control, prompt injection) are still recommended.

1. Why is JUnit `assertEquals` a misleading analog for a live LLM-as-judge?
2. Where does OpenAI put the HTTP request id, and why log it next to `cost_usd`?
3. Why is SQL injection a misleading analog for prompt injection?

Per-concept skip (2–3 minutes):

```bash
uv run pytest concepts/6_01/tests/test_skip.py
```

Pass an Analog skip test → skip that concept. Pass a NEW skip test → still read the lesson. 6.6 is optional (🟣) but still in the checkpoint.

## Concepts in order

| ID | Lesson | Kind | Est. | Skip / exercise |
|---|---|---|---:|---|
| 6.1 | [Eval strategy, LLM-as-judge, CI gates](../../concepts/6_01/README.md) | **NEW** | 60 min | `uv run pytest concepts/6_01` |
| 6.2 | [Observability](../../concepts/6_02/README.md) | Analog | 45 min | `uv run pytest concepts/6_02` |
| 6.3 | [Performance: cache, timeouts, gather](../../concepts/6_03/README.md) | Analog | 45 min | `uv run pytest concepts/6_03` |
| 6.4 | [Cost control](../../concepts/6_04/README.md) | **NEW** | 45 min | `uv run pytest concepts/6_04` |
| 6.5 | [Prompt injection and leakage](../../concepts/6_05/README.md) | **NEW** | 60 min | `uv run pytest concepts/6_05` |
| 6.6 | [FastAPI + container](../../concepts/6_06/README.md) | Analog (optional) | 60 min | `uv run pytest concepts/6_06` |

Times are unmeasured estimates. [Tell us your actual minutes](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).

## How each lesson works

- **Analog (6.2, 6.3, 6.6):** Java snippet first (≤15 lines, compiled in CI with JDK 21) → Python equivalent → differences & pitfalls table → exercise → check.
- **NEW (6.1, 6.4, 6.5):** intuition → why it exists (and the Java analogy that misleads you) → 3–5 step-by-step examples → ≥2 exercises → check.
- Starters live in `concepts/6_XX/exercises/`. They **fail** the tests on purpose. Solutions live in `concepts/6_XX/solutions/` and are validated in CI. Do not copy solutions until you have tried the hints.

The fake cannot teach live judge variance, real prompt-cache hit rates, or a production collector. Graded tests check *your* gate, JSON logs, TTL cache, budget math, and injection suite.

## Module deliverable

DocsDesk v0.6: a CI eval gate that fails on an injected regression, an injection suite that passes, and per-request `cost_usd` on a JSON log line with `request_id`.

```bash
uv run docsdesk eval-prod
uv run docsdesk eval-injection
uv run python -m docsdesk
uv run pytest tests/test_docsdesk_prod.py
```

`LLM_PROVIDER` defaults to `fake`. Secrets still never appear in logs (Module 1). FastAPI is optional (`uv sync --locked --group prod`); tests use TestClient and never bind a port. `deploy/Dockerfile` is a sketch — CI does not `docker build`.

## Module checkpoint

```bash
uv run course check m6
```

Prints pass/fail per concept, plus `prod` and `evals`. CI runs the same command against `solutions/`.

## Setup if you get stuck

PATH, `python` vs `python3`, Windows Store stub, `uv` / `.venv`, encoding, and line endings: [troubleshooting](../../docs/setup/troubleshooting.md).

- **API keys:** copy `.env.example` → `.env`. Never commit `.env`. Doctor reports whether `OPENAI_API_KEY` is set, not the value.
- **Wrong API:** `client.responses.create` only. No Assistants API.
- **Gate red on fake:** do not "fix" it by pointing at a live key. Mutating `expected_answer` is supposed to fail the gate.
- **Port 8000:** only if you opt into uvicorn. Windows `netstat -ano | findstr :8000`; macOS/Linux `lsof -i :8000`. Bind `127.0.0.1`, never `0.0.0.0` for this course.
- **Docker Desktop** (Windows/macOS) or the Docker engine (Linux) is optional. CI skips it.
- **Editor interpreter:** Command Palette → Python: Select Interpreter → `.venv`.

```bash
uv sync --locked --group dev
uv run python scripts/doctor.py --offline
```
