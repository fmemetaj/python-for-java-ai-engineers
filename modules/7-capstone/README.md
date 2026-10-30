# Module 7 — Capstone: DocsDesk v1.0

[Analog + NEW] [cost: mock] [~8–12 h estimated] [last verified: 2026-10-30, Python 3.11–3.13]

**Objective:** a portfolio project you can defend in an interview: DocsDesk v1.0 composes RAG with citations, an approval-gated agent loop, evals as a CI gate, tracing, cost budgets, and an optional FastAPI wrapper.

**Prereqs:** Modules 0A–6 (or enough of them that you can run `uv run course check m6 --solutions`). Professional Java (or another typed backend language).

**Offline:** every graded exercise uses `LLM_PROVIDER=fake`, FakeLLM, FakeEmbedder fixture vectors, and pytest. No API key. Cost badge: `mock`. Optional live OpenAI uses the [Responses API](https://platform.openai.com/docs/guides/migrate-to-responses) (`client.responses.create`), never the sunset Assistants API. Optional Ollama stays on loopback. Docker and bound ports are optional and are skipped in CI.

Total live cost if you opt in: **not required**. Prices live in `data/pricing.yaml` (retrieved 2026-10-30 from [OpenAI pricing](https://platform.openai.com/docs/pricing)).

## Do I need this? (3 questions)

If you can answer these without looking them up, run the skip tests. **NEW** concepts (briefs, integrated ask path, eval/cost/threat reports) are still recommended.

1. What six artifacts does the capstone rubric require?
2. Why is JUnit `assertEquals` a misleading analog for a live LLM eval gate?
3. What happens when `propose_page` runs with `approved=False`?

Per-concept skip (2–3 minutes):

```bash
uv run pytest concepts/7_01/tests/test_skip.py
```

Pass an Analog skip test → skip that concept. Pass a NEW skip test → still read the lesson.

## Concepts in order (milestones)

| ID | Lesson | Kind | Est. | Skip / exercise |
|---|---|---|---:|---|
| 7.1 | [Capstone briefs](../../concepts/7_01/README.md) | **NEW** | 45 min | `uv run pytest concepts/7_01` |
| 7.2 | [Architecture of v1.0](../../concepts/7_02/README.md) | Analog | 50 min | `uv run pytest concepts/7_02` |
| 7.3 | [Integrated ask path](../../concepts/7_03/README.md) | **NEW** | 60 min | `uv run pytest concepts/7_03` |
| 7.4 | [Eval report as a CI gate](../../concepts/7_04/README.md) | **NEW** | 55 min | `uv run pytest concepts/7_04` |
| 7.5 | [Cost report per 100](../../concepts/7_05/README.md) | **NEW** | 45 min | `uv run pytest concepts/7_05` |
| 7.6 | [Threat model](../../concepts/7_06/README.md) | **NEW** | 50 min | `uv run pytest concepts/7_06` |
| 7.7 | [Portfolio README + demo](../../concepts/7_07/README.md) | Analog | 45 min | `uv run pytest concepts/7_07` |

Times are unmeasured estimates. [Tell us your actual minutes](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml). The remaining hours in the 8–12 h band are the portfolio write-up for *your* brief.

## How each lesson works

- **Analog (7.2, 7.7):** Java snippet first (≤15 lines, compiled in CI with JDK 21) → Python equivalent → differences & pitfalls table → exercise → check.
- **NEW (7.1, 7.3–7.6):** intuition → why it exists (and the Java analogy that misleads you) → 3–5 step-by-step examples → ≥2 exercises → check.
- Starters live in `concepts/7_XX/exercises/`. They **fail** the tests on purpose. Solutions live in `concepts/7_XX/solutions/` and are validated in CI. Do not copy solutions until you have tried the hints.

The fake cannot teach live latency, a real IdP approval, or a production collector. Graded tests check *your* composition, counts, cost math, and checklist.

## Pick a brief

All three briefs are original. Graded CI stays on the payments-api fixture so you never need a private repo.

| Id | Product | Write tools? |
|---|---|---|
| `own-repo` | DocsDesk over **your** public Java/Spring docs | no |
| `pr-review` | Review a fixture Spring PR with citations | yes (simulated) |
| `log-triage` | Parse a log line, then the agent loop | yes (simulated) |

Details: [PORTFOLIO.md](PORTFOLIO.md). Architecture: [architecture.md](architecture.md). Demo script: [DEMO.md](DEMO.md).

## Rubric (acceptance)

| # | Bar | PASS when |
|---|---|---|
| 1 | Clean clone | `uv sync --locked` then tests, no extra undocumented steps |
| 2 | Offline | `LLM_PROVIDER=fake`; no key required |
| 3 | Eval report | ≥30 cases; `uv run docsdesk eval-v1` exits 0 |
| 4 | Cost | documented USD per 100 requests with model, price date, assumptions |
| 5 | Limitations | listed; writes are simulated; no real deploy |
| 6 | Citations | `ask()` returns retrieved-chunk citations |
| 7 | Approval | write tools deny when `approved=False` |
| 8 | Secrets | none committed; logs redact known secrets |
| 9 | API | Responses / embeddings only — never Assistants |
| 10 | Optional HTTP | FastAPI TestClient; Docker skipped in CI |

## Module deliverable

DocsDesk v1.0: `DocsDeskV1` in `src/docsdesk/v1.py`.

```bash
uv run docsdesk v1
uv run docsdesk eval-v1
uv run docsdesk cost-report
uv run docsdesk portfolio
uv run pytest tests/test_docsdesk_v1.py
```

`LLM_PROVIDER` defaults to `fake`. Secrets still never appear in logs (Module 1). FastAPI is optional (`uv sync --locked --group prod`); tests use TestClient and never bind a port. `deploy/Dockerfile` is a sketch — CI does not `docker build`.

## Module checkpoint

```bash
uv run course check m7
```

Prints pass/fail per concept, plus `v1` and `evals`. CI runs the same command against `solutions/`.

## Self-assessment

Tick these before you share the repo. Same list: `uv run docsdesk portfolio`.

- [ ] `uv sync --locked` from a clean clone
- [ ] `LLM_PROVIDER=fake` for graded work
- [ ] RAG answers include citations
- [ ] Write tools require an approval gate
- [ ] Agent loop enforces a step cap
- [ ] Eval report has at least 30 cases
- [ ] Cost per 100 requests is documented
- [ ] Threat model and limitations are listed
- [ ] Optional FastAPI uses TestClient (no Docker in CI)
- [ ] No secrets committed; Responses API only

## Setup if you get stuck

PATH, `python` vs `python3`, Windows Store stub, `uv` / `.venv`, encoding, and line endings: [troubleshooting](../../docs/setup/troubleshooting.md).

- **API keys:** copy `.env.example` → `.env`. Never commit `.env`. Doctor reports whether `OPENAI_API_KEY` is set, not the value.
- **Wrong API:** `client.responses.create` only. No Assistants API.
- **Eval red on fake:** do not "fix" it by pointing at a live key.
- **Port 8000:** only if you opt into uvicorn. Windows `netstat -ano | findstr :8000`; macOS/Linux `lsof -i :8000`. Bind `127.0.0.1`.
- **Docker Desktop** (Windows/macOS) or the Docker engine (Linux) is optional. CI skips it.
- **Editor interpreter:** Command Palette → Python: Select Interpreter → `.venv`.

```bash
uv sync --locked --group dev
uv run python scripts/doctor.py --offline
```
