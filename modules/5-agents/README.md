# Module 5 — Agents and Orchestration from Scratch

[Analog + NEW] [cost: mock] [~5–6 h estimated] [last verified: 2026-10-30, Python 3.11–3.13]

**Objective:** write and debug an agent loop you fully understand, and know when *not* to use an agent.

**Prereqs:** Module 4 (RAG). Module 3 (tool loop, approval).

**Offline:** every graded exercise uses `LLM_PROVIDER=fake` and a scripted FakeLLM **trajectory** (five deterministic LLM turns for DocsDesk triage). No API key. Cost badge: `mock`. Optional live generation uses `client.responses.create` ([Responses](https://platform.openai.com/docs/guides/migrate-to-responses)). Never the sunset Assistants API. Optional Ollama stays on loopback.

Total live cost if you opt in: **not required**. Prices still live in `data/pricing.yaml` (retrieved 2026-10-30 from [OpenAI pricing](https://platform.openai.com/docs/pricing)).

## Do I need this? (3 questions)

If you can answer these without looking them up, run the skip tests. **NEW** concepts (workflow vs agent, memory, MCP) are still recommended.

1. When is a fixed RAG pipeline enough, and when do you need an agent?
2. What stops a confused model from calling tools forever?
3. Who executes `propose_page` — the model, or your Python, after a human gate?

Per-concept skip (2–3 minutes):

```bash
uv run pytest concepts/5_01/tests/test_skip.py
```

Pass an Analog skip test → skip that concept. Pass a NEW skip test → still read the lesson. 5.5 and 5.6 are optional (🟣) but still in the checkpoint.

## Concepts in order

| ID | Lesson | Kind | Est. | Skip / exercise |
|---|---|---|---:|---|
| 5.1 | [Workflow vs agent](../../concepts/5_01/README.md) | **NEW** | 35 min | `uv run pytest concepts/5_01` |
| 5.2 | [The agent loop](../../concepts/5_02/README.md) | Analog | 60 min | `uv run pytest concepts/5_02` |
| 5.3 | [Memory and context](../../concepts/5_03/README.md) | **NEW** | 45 min | `uv run pytest concepts/5_03` |
| 5.4 | [Tracing agent runs](../../concepts/5_04/README.md) | Analog | 45 min | `uv run pytest concepts/5_04` |
| 5.5 | [One framework comparison](../../concepts/5_05/README.md) | Analog (optional) | 60 min | `uv run pytest concepts/5_05` |
| 5.6 | [MCP tools](../../concepts/5_06/README.md) | **NEW** (optional) | 45 min | `uv run pytest concepts/5_06` |

Times are unmeasured estimates. [Tell us your actual minutes](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).

## How each lesson works

- **Analog (5.2, 5.4, 5.5):** Java snippet first (≤15 lines, compiled in CI with JDK 21) → Python equivalent → differences & pitfalls table → exercise → check.
- **NEW (5.1, 5.3, 5.6):** intuition → why it exists (and the Java analogy that misleads you) → 3–5 step-by-step examples → ≥2 exercises → check.
- Starters live in `concepts/5_XX/exercises/`. They **fail** the tests on purpose. Solutions live in `concepts/5_XX/solutions/` and are validated in CI. Do not copy solutions until you have tried the hints.

The fake cannot teach live latency, a surprising tool choice, or a hosted MCP server. Graded tests check *your* classifier, loop cap, memory trim, spans, facade, and JSON-RPC.

## Module deliverable

DocsDesk **triage mode**: a multi-step investigation of `POST /payments/{id}/refunds returns 500 after capture`, with a human approval gate on `propose_page` (simulated `would_write`, nothing is sent).

```bash
uv run python -m docsdesk triage
uv run docsdesk eval-agent
uv run pytest tests/test_course_agent.py tests/test_docsdesk_triage.py
```

`LLM_PROVIDER` defaults to `fake`. Secrets still never appear in logs (Module 1).

## Module checkpoint

```bash
uv run course check m5
```

Prints pass/fail per concept, plus `agent` and `triage`. CI runs the same command against `solutions/`.

## Setup if you get stuck

PATH, `python` vs `python3`, Windows Store stub, `uv` / `.venv`, encoding, and line endings: [troubleshooting](../../docs/setup/troubleshooting.md).

- **Trajectory stuck on turn 1:** reuse the same `FakeLLM` instance. Each `complete()` advances one scripted turn.
- **Cap never fires:** the script must keep returning `tools`; a final `message` turn stops with `done`.
- **Approval still executes `propose_page`:** both the loop `approve=` flag *and* `ToolRunner.approved` must be false to deny.
- **API keys:** copy `.env.example` → `.env`. Never commit `.env`. Generation uses Responses, never Assistants.
- **Editor interpreter:** Command Palette → Python: Select Interpreter → `.venv`.

```bash
uv sync --locked --group dev
uv run python scripts/doctor.py --offline
```
