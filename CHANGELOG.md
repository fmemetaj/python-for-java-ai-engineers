# Changelog

This project versions the *course*, not a library API. Dates are UTC.

## 0.2.0 — 2026-10-30

Start of **release v0.2** ("First LLM feature"). Module 2 only; Module 3 is not in this drop.

### Added

- Module 2 — LLM API Fundamentals: concepts 2.1–2.11 (5 Analog, 6 NEW) under `concepts/2_XX/`.
- `uv run course check m2` (solutions in CI).
- `course_kit.cost` + dated `data/pricing.yaml` (source: https://platform.openai.com/docs/pricing, retrieved 2026-10-30).
- FakeLLM Chat Completions shape, streaming events, `previous_response_id` billing, reasoning items.
- DocsDesk multi-turn session over a pasted doc, printing tokens and USD (`src/docsdesk/session.py`).
- Versioned prompt `src/docsdesk/prompts/answer_from_doc.v1.txt`.

No GitHub Release or git tag is created for this changelog entry.

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
