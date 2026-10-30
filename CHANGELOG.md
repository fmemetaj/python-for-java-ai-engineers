# Changelog

This project versions the *course*, not a library API. Dates are UTC.

## 0.6.0 — 2026-10-30

**Electives (A) + whole-course QA** — Optional tracks A.1–A.9 (vision, hosted tools vs owned RAG, API-change skill) after Module 7, plus a Start-here path, setup FAQ, and Markdown link check. Offline `FakeLLM` + vision catalog fixtures. No GitHub Release or git tag is created for this changelog entry.

### Electives (A)

- Three optional tracks (~2–3 h each) under `modules/a-electives/` and `concepts/a_XX/`. `uv run course check ma` (solutions in CI).
- **A1 Vision:** Responses `input_image` items, screenshot-to-answer on catalog fixtures, image token economics (low=85, high=tiles; images bill as input).
- **A2 Hosted vs own:** `file_search` vs Module 4 RAG, a two-step fake hosted-tool loop, lock-in decision record (`assistants: false`).
- **A3 API change as a skill:** lockfile pin + fake changelog, sunset-string scanner (Assistants 2026-08-26; 0.x `ChatCompletion.create`), spend-capped smoke + sanitized fixtures.
- `uv run docsdesk vision` / `hosted` / `smoke`. Graded work stays on `LLM_PROVIDER=fake`. Never Assistants. Keys are never committed.

### Whole-course QA

- Top-level **Start here**: install uv → `uv sync --locked --group dev` → `scripts/doctor.py --offline` → concept 0.1.
- [docs/setup/faq.md](docs/setup/faq.md) for Windows / macOS / Linux (Store stub, PATH, Apple Silicon, WSL, proxy/SSL).
- `scripts/check_markdown_links.py` plus `tests/test_markdown_links.py` — relative README/lesson links must resolve.
- Course map, CHANGELOG, troubleshooting, and `course check` targets updated through Module 7 and Electives.

## 0.5.0 — 2026-10-30

**Module 7 "Capstone: DocsDesk v1.0"** — Concepts 7.1–7.7. DocsDesk v1.0 composes RAG with citations, an approval-gated agent loop, evals as a CI gate (≥30 fake cases), tracing, cost budgets, and an optional FastAPI wrapper, plus a rubric, milestones, self-assessment, and portfolio/README guide. Offline `FakeLLM` + `FakeEmbedder`. No GitHub Release or git tag is created for this changelog entry.

### Module 7 — Capstone: DocsDesk v1.0

- Concepts 7.1–7.7 (2 Analog, 5 NEW) under `concepts/7_XX/`. Milestones: briefs, architecture, integrated ask path, eval report, cost report, threat model, portfolio README/demo.
- `uv run course check m7` (solutions in CI).
- `docsdesk.v1.DocsDeskV1`: retrieve → cite → budget/cache/JSON logs; `investigate()` uses the Module 5 loop and denies write tools until `approved=True`. `propose_page` is simulated (`would_write`).
- `docsdesk.portfolio`: three original briefs (own-repo, pr-review, log-triage), `run_v1_eval` (≥30 cases from M3–M6 + injection), `build_cost_report` (100× FakeLLM usage against `data/pricing.yaml`), threat rows, limitations, self-assessment.
- `uv run docsdesk v1` / `eval-v1` / `cost-report` / `portfolio`.
- Optional FastAPI `/v1/ask` and `/v1/investigate` (TestClient, no bound port). `deploy/Dockerfile` remains a sketch; CI does not `docker build`. Never Assistants. Keys are never committed.
- Learner-facing rubric, architecture diagram, demo script, and portfolio guide under `modules/7-capstone/`.

## 0.4.0 — 2026-10-30

**Module 6 "Evals, Observability, Production"** — Concepts 6.1–6.6. DocsDesk v0.6: LLM-as-judge with calibration, a CI eval gate that fails on an injected regression, JSON logs with request ids and per-request cost, TTL cache, budgets and prompt-cache discount, an injection suite, and an optional FastAPI wrapper. Offline `FakeLLM` (and Module 4's `FakeEmbedder` where retrieval is reused). No GitHub Release or git tag is created for this changelog entry.

### Module 6 — Evals, Observability, Production

- Concepts 6.1–6.6 (3 Analog, 3 NEW) under `concepts/6_XX/`. 6.6 is optional (FastAPI + container sketch).
- `uv run course check m6` (solutions in CI).
- `docsdesk.judge` / `docsdesk.gate`: scripted LLM-as-judge, agreement vs labels, `eval_gate`, `inject_regression`.
- Observability: `LLMResponse.request_id` (OpenAI SDK `_request_id` analog), ContextVar MDC, JSON log lines with `cost_usd`.
- Performance: in-process TTL cache, timeout helper, `asyncio.gather` (cooperative I/O).
- Cost control: remaining budget, nano/mini routing, cached-token discount from `data/pricing.yaml`, log dashboard.
- Security: direct/indirect injection detectors, secret redaction, `data/evals/docsdesk_injection.json`.
- `uv run docsdesk eval-prod` and `uv run docsdesk eval-injection`.
- Optional FastAPI (`uv sync --locked --group prod`) tested with in-process TestClient — no bound port. `deploy/Dockerfile` is a sketch; CI does not `docker build`. Never Assistants. Keys are never committed.

## 0.3.0 — 2026-10-30

**v0.3 "RAG + agents"** — Modules 4 and 5. DocsDesk v0.5: RAG over an original Spring Boot payments-api fixture, then a from-scratch triage agent with a scripted 5-step fake trajectory. Offline `FakeEmbedder` + `FakeLLM` trajectories. No GitHub Release or git tag is created for this changelog entry.

### Module 4 — Embeddings, Semantic Search, RAG

- Concepts 4.1–4.7 (2 Analog, 5 NEW) under `concepts/4_XX/`. 4.7 is optional advanced (hybrid BM25 + vectors, reranking, hosted file_search lock-in sidebar).
- `uv run course check m4` (solutions in CI).
- `course_kit.rag`: hashing-trick `FakeEmbedder`, cosine / L2-norm / top-k (numpy), size vs structure-aware chunking, in-memory `VectorIndex`, BM25 hybrid fusion.
- Precomputed fixture vectors `data/embeddings/payments-api.json`; rebuild with `scripts/build_embedding_fixtures.py`.
- Original corpus `data/corpus/payments-api` (Northwind Payments Spring Boot docs + Javadoc excerpt).
- DocsDesk RAG pipeline: retrieve → assemble context → FakeLLM answer with citations (`src/docsdesk/rag.py`).
- `uv run docsdesk eval` reports recall@5 and groundedness (`data/evals/docsdesk_m4.json`).
- Live embeddings remain optional via `.env` (`client.embeddings.create`); generation still uses the Responses API. Never Assistants. Keys are never committed.

### Module 5 — Agents and Orchestration from Scratch

- Concepts 5.1–5.6 (3 Analog, 3 NEW) under `concepts/5_XX/`. 5.5–5.6 are optional (framework comparison, MCP).
- `uv run course check m5` (solutions in CI).
- `course_kit.agent`: workflow-vs-agent classifier, `run_agent_loop` (max steps, approval stop), budgeted `AgentMemory`, in-process `AgentTrace` spans, a thin `Agent`/`Runner` facade (OpenAI Agents SDK *names* only — package not added), `FakeMcpServer` JSON-RPC.
- FakeLLM `trajectories=` replays multi-step tool scripts; the graded refund-500 path is five deterministic `complete()` turns.
- DocsDesk triage mode (`src/docsdesk/triage.py`): investigate → tools → `propose_page` human gate (simulated `would_write`). `uv run docsdesk triage` / `uv run docsdesk eval-agent`.
- Agent evals `data/evals/docsdesk_m5.json` check task success, step count, approval denial, and the step cap.
- Live generation remains optional via `.env` (`client.responses.create`). Never Assistants. Keys are never committed.

## 0.2.0 — 2026-10-30

**v0.2 "First LLM feature"** — Modules 2 and 3. DocsDesk v0.3: typed answers, tools, cost tracking, and a 15-case eval. Offline `FakeLLM`. No GitHub Release or git tag is created for this changelog entry.

### Module 2 — LLM API Fundamentals

- Concepts 2.1–2.11 (5 Analog, 6 NEW) under `concepts/2_XX/`.
- `uv run course check m2` (solutions in CI).
- `course_kit.cost` + dated `data/pricing.yaml` (source: https://platform.openai.com/docs/pricing, retrieved 2026-10-30).
- FakeLLM Chat Completions shape, streaming events, `previous_response_id` billing, reasoning items.
- DocsDesk multi-turn session over a pasted doc, printing tokens and USD (`src/docsdesk/session.py`).
- Versioned prompt `src/docsdesk/prompts/answer_from_doc.v1.txt`.

### Module 3 — Structured Outputs, Tool Calling, First Evals

- Concepts 3.1–3.5 (3 Analog, 2 NEW) under `concepts/3_XX/`.
- `uv run course check m3` (solutions in CI).
- Structured outputs: JSON Schema from Pydantic, Responses `text.format` vs Chat Completions `response_format`, refusal handling.
- FakeLLM scripted `function_call` / `function_call_output` turns (`call_id`) and structured JSON.
- DocsDesk typed `TypedAnswer` with citations; tools `search_docs` and `get_endpoint_spec`.
- Tool safety: allow-list, strict argument validation, simulated approval, idempotency. Invalid tool args are handled.
- Eval harness `data/evals/docsdesk_m3.json` (≥15 cases) passes on fake; live pass rate is reported with no threshold claimed.

## 0.1.0 — 2026-10-30

**v0.1 "Fundamentals"** — Modules 0A, 0B, and 1. Offline, no AI cost. This section documents what already shipped on `main` before Module 2; it is changelog-only (no retroactive tag).

### Module 0A — Python Fundamentals I

- Concepts 0.1–0.15 (8 Analog, 7 NEW) as Java-first or NEW-template lessons.
- Placement check and `fundamentals/log_stats.py` deliverable.
- `uv run course check m0a`.
- Original notebooks 00–06 kept as optional explainers.

### Module 0B — Python Fundamentals II

- Concepts 0.16–0.29 (9 Analog, 5 NEW): classes, typing, exceptions, context managers, decorators, modules, threads, asyncio.
- `fundamentals/tool_registry.py` deliverable.
- `uv run course check m0b`.

### Module 1 — Python Engineering & Tooling

- Concepts 1.1–1.12 (11 Analog, 1 NEW — virtual environments).
- DocsDesk skeleton: settings, redacting logs, httpx + retries, Pydantic JSON, `FakeLLM`.
- `uv run course check m1`.
- JDK 21 Java-snippet compile step in CI; starters fail / solutions pass.

### Tooling that landed with v0.1

- Committed `uv.lock`; CI matrix Python 3.11–3.13 × Ubuntu, macOS, Windows; ruff, pyright, pytest, nbmake.
- `course` CLI, `scripts/doctor.py --offline`, `.env.example` (keys never committed).
