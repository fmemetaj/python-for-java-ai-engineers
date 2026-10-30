# Module 4 — Embeddings, Semantic Search, RAG

[Analog + NEW] [cost: mock] [~6–7 h estimated] [last verified: 2026-10-30, Python 3.11–3.13]

**Objective:** build and *measure* a retrieval-augmented system over a real Java codebase's docs (an original Northwind Payments Spring Boot fixture).

**Prereqs:** Module 3 (typed answers, tools, evals). numpy is introduced here; no prior numpy required.

**Offline:** every graded exercise uses `LLM_PROVIDER=fake`, `FakeEmbedder` (hashing trick), and committed vectors in `data/embeddings/payments-api.json`. No API key. Cost badge: `mock`. Optional live **embeddings** use `client.embeddings.create` ([Embeddings](https://platform.openai.com/docs/guides/embeddings)). Optional live **generation** uses `client.responses.create` ([Responses](https://platform.openai.com/docs/guides/migrate-to-responses)). Never the sunset Assistants API. Optional Ollama stays on loopback.

Total live cost if you opt in: **not required**. Embedding prices live under `embeddings` in `data/pricing.yaml` (retrieved 2026-10-30 from [OpenAI pricing](https://platform.openai.com/docs/pricing)).

## Do I need this? (3 questions)

If you can answer these without looking them up, run the skip tests. **NEW** concepts (embeddings, cosine, chunking, RAG, retrieval evals) are still recommended.

1. What is an embedding, and why is `String.hashCode()` a misleading analog?
2. What does recall@5 measure that `assertEquals` on the answer string does not?
3. Who retrieves — the model, or your Python index?

Per-concept skip (2–3 minutes):

```bash
uv run pytest concepts/4_01/tests/test_skip.py
```

Pass an Analog skip test → skip that concept. Pass a NEW skip test → still read the lesson. 4.7 is optional (🟣) but still in the checkpoint.

## Concepts in order

| ID | Lesson | Kind | Est. | Skip / exercise |
|---|---|---|---:|---|
| 4.1 | [Embeddings and vector spaces](../../concepts/4_01/README.md) | **NEW** | 60 min | `uv run pytest concepts/4_01` |
| 4.2 | [Cosine similarity and normalization](../../concepts/4_02/README.md) | **NEW** | 40 min | `uv run pytest concepts/4_02` |
| 4.3 | [Chunking and metadata](../../concepts/4_03/README.md) | **NEW** | 50 min | `uv run pytest concepts/4_03` |
| 4.4 | [Vector index / search](../../concepts/4_04/README.md) | Analog | 45 min | `uv run pytest concepts/4_04` |
| 4.5 | [RAG pipeline with citations](../../concepts/4_05/README.md) | **NEW** | 60 min | `uv run pytest concepts/4_05` |
| 4.6 | [Retrieval evals](../../concepts/4_06/README.md) | **NEW** | 50 min | `uv run pytest concepts/4_06` |
| 4.7 | [Hybrid search + reranking](../../concepts/4_07/README.md) | Analog (optional) | 60 min | `uv run pytest concepts/4_07` |

Times are unmeasured estimates. [Tell us your actual minutes](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).

## How each lesson works

- **Analog (4.4, 4.7):** Java snippet first (≤15 lines, compiled in CI with JDK 21) → Python equivalent → differences & pitfalls table → exercise → check.
- **NEW (4.1–4.3, 4.5, 4.6):** intuition → why it exists (and the Java analogy that misleads you) → 3–5 step-by-step examples → ≥2 exercises → check.
- Starters live in `concepts/4_XX/exercises/`. They **fail** the tests on purpose. Solutions live in `concepts/4_XX/solutions/` and are validated in CI. Do not copy solutions until you have tried the hints.

The fake cannot teach a production embedding model's geometry, HNSW recall loss, or live citation hallucinations. Graded tests check *your* hashing embedder, cosine, chunker, assembler, and eval formulas.

## Module deliverable

DocsDesk answers over `data/corpus/payments-api` (original Spring Boot docs we wrote for this course). `uv run docsdesk eval` reports recall@5 and groundedness on the fake provider.

```bash
uv run python -m docsdesk
uv run docsdesk eval
uv run pytest tests/test_rag.py tests/test_docsdesk_rag.py
```

`LLM_PROVIDER` defaults to `fake`. Secrets still never appear in logs (Module 1).

## Module checkpoint

```bash
uv run course check m4
```

Prints pass/fail per concept, plus `rag` and `docsdesk_rag`. CI runs the same command against `solutions/`.

## Setup if you get stuck

PATH, `python` vs `python3`, Windows Store stub, `uv` / `.venv`, encoding, and line endings: [troubleshooting](../../docs/setup/troubleshooting.md).

- **numpy wheels:** `uv sync --locked` should fetch a wheel (Windows amd64, macOS x86_64/arm64, Linux). If uv compiles numpy, the Python arch is wrong (Rosetta x86_64 on Apple Silicon, or Windows ARM without a wheel). Reinstall with `uv python install 3.12` for the native arch.
- **API keys:** copy `.env.example` → `.env`. Never commit `.env`. Embeddings ≠ Responses ≠ Assistants.
- **Rebuild fixture vectors:** `uv run python scripts/build_embedding_fixtures.py`.
- **Eval red on fake:** fix chunking/index/citations, do not point at a live key.
- **Editor interpreter:** Command Palette → Python: Select Interpreter → `.venv`.

```bash
uv sync --locked --group dev
uv run python scripts/doctor.py --offline
```
