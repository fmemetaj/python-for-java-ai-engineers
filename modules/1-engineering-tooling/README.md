# Module 1 — Python Engineering & Tooling

[Analog + NEW] [cost: mock] [~6–7 h estimated] [last verified: 2026-10-30, Python 3.11–3.13]

**Objective:** structure, build, configure, test, and integrate a Python service the way a Java engineer expects from Maven + Spring + JUnit.

**Prereqs:** Module 0A and 0B (or the placement check). Professional Java (or another typed backend language).

**Offline:** every graded exercise uses the standard library, pytest, httpx `MockTransport`, pydantic-settings, and `LLM_PROVIDER=fake`. No API key. Cost badge: `mock`. A live OpenAI key is optional and unused by CI; if you ever opt in, call the [Responses API](https://platform.openai.com/docs/guides/migrate-to-responses), never the sunset Assistants API.

## Do I need this? (3 questions)

If you can answer these without looking them up, run the skip tests. **NEW** concept 1.3 is still recommended: virtualenvs are where Java developers get surprised.

1. What is the Maven analog of `uv sync --locked`? Where do version ranges live vs exact pins?
2. Why is `.venv` **not** a classpath?
3. How do you translate a JUnit 5 + Mockito test that calls a JSON HTTP API into pytest + httpx with a timeout?

Per-concept skip (2–3 minutes):

```bash
uv run pytest concepts/1_01/tests/test_skip.py
```

Pass an Analog skip test → skip that concept. Pass the NEW skip test → still read the lesson.

## Concepts in order

| ID | Lesson | Kind | Est. | Skip / exercise |
|---|---|---|---:|---|
| 1.1 | [uv](../../concepts/1_01/README.md) | Analog | 40 min | `uv run pytest concepts/1_01` |
| 1.2 | [pyproject.toml and uv.lock](../../concepts/1_02/README.md) | Analog | 25 min | `uv run pytest concepts/1_02` |
| 1.3 | [Virtual environments](../../concepts/1_03/README.md) | **NEW** | 25 min | `uv run pytest concepts/1_03` |
| 1.4 | [src layout and entry points](../../concepts/1_04/README.md) | Analog | 20 min | `uv run pytest concepts/1_04` |
| 1.5 | [ruff and pyright](../../concepts/1_05/README.md) | Analog | 20 min | `uv run pytest concepts/1_05` |
| 1.6 | [Logging](../../concepts/1_06/README.md) | Analog | 20 min | `uv run pytest concepts/1_06` |
| 1.7 | [Config and secrets](../../concepts/1_07/README.md) | Analog | 25 min | `uv run pytest concepts/1_07` |
| 1.8 | [pytest](../../concepts/1_08/README.md) | Analog | 45 min | `uv run pytest concepts/1_08` |
| 1.9 | [Mocking](../../concepts/1_09/README.md) | Analog | 30 min | `uv run pytest concepts/1_09` |
| 1.10 | [httpx](../../concepts/1_10/README.md) | Analog | 40 min | `uv run pytest concepts/1_10` |
| 1.11 | [JSON ↔ Pydantic](../../concepts/1_11/README.md) | Analog | 30 min | `uv run pytest concepts/1_11` |
| 1.12 | [Retries with backoff](../../concepts/1_12/README.md) | Analog | 25 min | `uv run pytest concepts/1_12` |

Times are unmeasured estimates. [Tell us your actual minutes](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).

## How each lesson works

- **Analog:** Java snippet first (≤15 lines, compiled in CI with JDK 21) → Python equivalent → differences & pitfalls table → exercise → check.
- **NEW (1.3 only):** intuition → why it exists (and the classpath analogy that misleads you) → 5 step-by-step examples → ≥2 exercises → check.
- Starters live in `concepts/1_XX/exercises/`. They **fail** the tests on purpose. Solutions live in `concepts/1_XX/solutions/` and are validated in CI. Do not copy solutions until you have tried the hints.

## Module deliverable

`src/docsdesk/` — a DocsDesk skeleton: `Settings` (env / `.env`, `SecretStr`), redacting logs, an httpx client against an in-process mock docs service, Pydantic `DocPage`, retries, and `course_kit.llm.FakeLLM` (Responses-shaped, offline).

```bash
uv run python -m docsdesk
uv run pytest tests/test_docsdesk.py tests/test_fake_llm.py
```

A test asserts secrets never appear in logs. `LLM_PROVIDER` defaults to `fake`.

## Module checkpoint

```bash
uv run course check m1
```

Prints pass/fail per concept, plus `docsdesk` and `fake_llm`. CI runs the same command against `solutions/`.

## Setup if you get stuck

PATH, `python` vs `python3`, Windows Store stub, `uv` / `.venv`, encoding, and line endings: [troubleshooting](../../docs/setup/troubleshooting.md).

- **Lockfile:** after editing `pyproject.toml`, run `uv lock` and commit `uv.lock`. CI uses `uv sync --locked`.
- **API keys:** copy `.env.example` → `.env`. Never commit `.env`. Doctor reports whether `OPENAI_API_KEY` is set, not the value.
- **httpx hanging:** set a timeout; graded tests use `MockTransport` and must not touch the network.
- **Editor interpreter:** Command Palette → Python: Select Interpreter → `.venv`.

```bash
uv sync --locked --group dev
uv run python scripts/doctor.py --offline
```
