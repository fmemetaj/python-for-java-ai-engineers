# Electives (A) — optional tracks after the capstone

[Analog + NEW] [cost: mock] [~2–3 h **each** track, estimated] [last verified: 2026-10-30, Python 3.11–3.13]

**Objective:** three optional tracks that sit *after* DocsDesk v1.0: vision inputs, hosted tools vs owned RAG, and treating SDK change as a skill. Skip any track you do not need. Nothing here is on the essential path.

**Prereqs:** Module 7 is recommended (or Module 4 for vision/hosted, Module 2 for the upgrade drill). Professional Java (or another typed backend language).

**Offline:** every graded exercise uses `LLM_PROVIDER=fake`, FakeLLM, catalog vision fixtures, and pytest. No API key. Cost badge: `mock`. Optional live OpenAI uses the [Responses API](https://platform.openai.com/docs/guides/migrate-to-responses) (`client.responses.create`), never the sunset Assistants API. Optional Ollama stays on loopback.

Total live cost if you opt in: **not required**. Image tokens and hosted tools have their own prices — read `data/pricing.yaml` (retrieved 2026-10-30 from [OpenAI pricing](https://platform.openai.com/docs/pricing)).

## Do I need this? (3 questions)

If you can answer these without looking them up, run the skip tests. **NEW** concepts are still recommended.

1. What Responses item `type` carries an image?
2. When is owned RAG a more honest CI default than hosted `file_search`?
3. Which API was sunset on 2026-08-26 and must not appear in this course?

Per-concept skip (2–3 minutes):

```bash
uv run pytest concepts/a_01/tests/test_skip.py
```

Pass an Analog skip test → skip that concept. Pass a NEW skip test → still read the lesson. All nine concepts stay in `course check ma` so CI remains honest.

## Tracks (pick any)

### A1 — Vision (~2–3 h)

| ID | Lesson | Kind | Est. | Skip / exercise |
|---|---|---|---:|---|
| A.1 | [Image inputs on the Responses API](../../concepts/a_01/README.md) | **NEW** | 50 min | `uv run pytest concepts/a_01` |
| A.2 | [Screenshot-to-answer](../../concepts/a_02/README.md) | **NEW** | 50 min | `uv run pytest concepts/a_02` |
| A.3 | [Image token economics](../../concepts/a_03/README.md) | Analog | 40 min | `uv run pytest concepts/a_03` |

### A2 — Hosted tools vs own pipeline (~2–3 h)

| ID | Lesson | Kind | Est. | Skip / exercise |
|---|---|---|---:|---|
| A.4 | [Hosted file_search vs own RAG](../../concepts/a_04/README.md) | Analog | 50 min | `uv run pytest concepts/a_04` |
| A.5 | [Fake hosted-tool loop](../../concepts/a_05/README.md) | **NEW** | 50 min | `uv run pytest concepts/a_05` |
| A.6 | [Lock-in decision record](../../concepts/a_06/README.md) | **NEW** | 40 min | `uv run pytest concepts/a_06` |

### A3 — API change as a skill (~2–3 h)

| ID | Lesson | Kind | Est. | Skip / exercise |
|---|---|---|---:|---|
| A.7 | [Pin, changelog, compatibility](../../concepts/a_07/README.md) | Analog | 40 min | `uv run pytest concepts/a_07` |
| A.8 | [SDK-upgrade drill](../../concepts/a_08/README.md) | **NEW** | 50 min | `uv run pytest concepts/a_08` |
| A.9 | [Spend-capped smoke + sanitized fixtures](../../concepts/a_09/README.md) | **NEW** | 50 min | `uv run pytest concepts/a_09` |

Times are unmeasured estimates. [Tell us your actual minutes](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).

## How each lesson works

- **Analog (A.3, A.4, A.7):** Java snippet first (≤15 lines, compiled in CI with JDK 21) → Python equivalent → differences & pitfalls table → exercise → check.
- **NEW (A.1, A.2, A.5, A.6, A.8, A.9):** intuition → why it exists (and the Java analogy that misleads you) → 3–5 step-by-step examples → ≥2 exercises → check.
- Starters live in `concepts/a_XX/exercises/`. They **fail** the tests on purpose. Solutions live in `concepts/a_XX/solutions/` and are validated in CI.

The fake cannot teach live OCR, vendor chunking, or a real 429. Graded tests check *your* item shapes, token math, stack choice, scanner, cap, and redaction.

## Module deliverable

Optional DocsDesk extras, all offline:

```bash
uv run docsdesk vision
uv run docsdesk hosted
uv run docsdesk smoke
uv run pytest tests/test_electives.py tests/test_docsdesk_electives.py
```

`LLM_PROVIDER` defaults to `fake`. Secrets still never appear in logs (Module 1). Fine-tuning, a framework survey, and the Assistants API stay out of scope (curriculum §5).

## Module checkpoint

```bash
uv run course check ma
```

Prints pass/fail per concept, plus `electives` and `docsdesk`. CI runs the same command against `solutions/`.

## Setup if you get stuck

PATH, `python` vs `python3`, Windows Store stub, `uv` / `.venv`, encoding, and line endings: [troubleshooting](../../docs/setup/troubleshooting.md) and the [FAQ](../../docs/setup/faq.md).

- **API keys:** copy `.env.example` → `.env`. Never commit `.env`. Doctor reports whether `OPENAI_API_KEY` is set, not the value.
- **Wrong API:** `client.responses.create` only. No Assistants API.
- **Vision fixtures:** `data/fixtures/vision.json` — no PNG binaries, no HTTP fetches.
- **Smoke cap:** `docsdesk smoke` refuses a non-fake provider.

```bash
uv sync --locked --group dev
uv run python scripts/doctor.py --offline
```
