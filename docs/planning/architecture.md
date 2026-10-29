# Proposed Repository Architecture
All items **[Proposed]** unless labelled. Goal: extend the existing repo (keep Part 0 = current 7 notebooks), not rebuild.

## Layout
```
pyproject.toml / uv.lock (committed) / .python-version
.env.example                 # OPENAI_API_KEY=, LLM_PROVIDER=fake|ollama|openai, OPENAI_MODEL=
src/course_kit/
  llm/ base.py (Protocol LLMClient), fake.py (deterministic, recorded fixtures), ollama.py, openai_client.py
  cost.py (token→$ from a dated pricing table in data/pricing.yaml with source URL)
  rag/ chunking.py, vectorstore.py (in-memory numpy), embeddings_fake.py
src/mini_agent/              # existing, unchanged
modules/
  00-python-bridge/ notebooks 00–06 (moved from notebooks/ with redirects in README)
  01-python-for-ai-services/  02-llm-api-fundamentals/  03-structured-tools-evals/  04-embeddings-rag/  05-agents/  06-evals-observability-prod/  07-capstone/  electives/
  (aligned with curriculum.md 2026-10-29; running project `src/docsdesk/` grows per module)
placement/self_check.py  scripts/doctor.py  data/pricing.yaml
    each: README.md, NN_*.ipynb, exercises/, solutions/, tests/
tests/ (unit) ; fixtures/recorded/*.json (sanitized API responses)
scripts/
.github/ workflows/ci.yml, workflows/live-smoke.yml (manual, uses secret), ISSUE_TEMPLATE/, PULL_REQUEST_TEMPLATE.md, dependabot.yml
.cursor/rules/, .vscode/{extensions,settings}.json, .devcontainer/ (optional Codespaces)
```

## Principles
1. **Provider switch via env**: notebooks call `get_client()`; default `fake` so every notebook executes in CI and for learners without keys. Java analogy: Spring profiles / interface + `@Primary` test bean.
2. **Deterministic fakes**: `FakeLLM` returns canned Responses-API-shaped objects (output items, usage tokens) from fixtures; also scripted tool-call sequences to teach the agent loop. Recorded fixtures are captured once with a real key and committed after scrubbing.
3. **Pinned deps**: ranges in pyproject, exact versions in committed `uv.lock`; CI `uv sync --locked`. Pin `openai` major (`openai>=3,<4`; current PyPI 3.41.0 [Verified 2026-10-29]).
4. **Testing**: pytest for `src/`; `pytest --nbmake modules/` (or keep the existing nbclient script) with `LLM_PROVIDER=fake`; exercise autograding via tests that import learner code from `exercises/`; `solutions/` validated in CI.
5. **CI**: matrix Python 3.11/3.12/3.13 × ubuntu (+ windows weekly); ruff check + format check; nbstripout check; link check (lychee) weekly; `live-smoke.yml` only `workflow_dispatch` with `OPENAI_API_KEY` secret and a spend cap.
6. **Secrets**: `.env.example` only; `python-dotenv`; GitHub secret scanning + push protection enabled; never print keys.
7. **Governance**: ruleset on `main`: PR required, 1 approval from CODEOWNERS, required status checks, no force-push, linear history. Contributors via fork PRs only (owner retains sole admin).
8. **Editors**: keep `.cursor/rules`; add `.vscode/settings.json` (interpreter `.venv`, ruff formatter, pytest); devcontainer for zero-install.
