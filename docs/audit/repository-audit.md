# Repository Audit — fmemetaj/python-for-java-ai-engineers

Audit date: 2026-10-29 (Europe/Budapest). Method: anonymous `git clone` of `main` into `/workspace/ai-course/repo` (read-only; nothing pushed, no issues/PRs/comments). Commands were run in fresh uv environments on the box.
Labels: **[Verified]** = observed/executed by me · **[Proposed]** = recommendation · **[Unverified]** = assumption.

## 1. Snapshot
- [Verified] 4 commits, all on 2026-10-22 (14:46–15:45 +0200): init docs → "seven interactive lessons, mock helpdesk workflow, uv project, and CI" → editor/guides/diagrams + optional Gradio/Ollama capstone → "Rework every lesson as Java-first guided practice". Project is ~1 week old, single author, single day of work.
- [Verified] Scope declared in README: a **60-minute Python bridge for Java devs**, explicitly "not a full Python, ML, or agent course". No LLM-API content (no OpenAI/Anthropic SDK anywhere), no embeddings, RAG, evals.
- [Verified] License MIT. Acknowledges Ed Donner as format inspiration; states all content original. COVERAGE.md maps topics to Ed Donner's public `llm_engineering/guides` topic list without reproducing content. [Unverified] I did not diff text against his guides for originality.

## 2. Structure
```
.cursor/rules/learning-first.mdc   Cursor tutor rule (hints before solutions)
.github/CODEOWNERS, workflows/ci.yml
.vscode/extensions.json
assets/ bridge.svg, local-ai-flow.svg
examples/gradio_app.py (90 lines, optional demo)
guides/ 01 editor, 02 java↔python map, 03 async, 04 pydantic/decorators, 05 uv/debugging, 06 local AI lab, 07 extra foundations, README
notebooks/ 00–06 (.ipynb)
scripts/validate_notebooks.py (nbclient runner)
src/mini_agent/ models.py, tools.py, workflow.py, local_llm.py (Ollama via urllib)
tests/ test_agent.py, test_local_llm.py (HTTP mocked), test_gradio_demo.py
README.md, PROGRESS.md, COVERAGE.md, CONTRIBUTING.md, LICENSE, pyproject.toml, .python-version (3.12)
```

## 3. Lessons [Verified cell counts]
| Notebook | Topic | Cells (code) | Executes |
|---|---|---|---|
| 00_getting_started | Notebook mechanics, Java mental model | 6 (2) | PASS |
| 01_pythonic_essentials | Comprehensions, dicts, None, kwargs | 14 (6) | PASS |
| 02_typing_pydantic | Dataclasses, type hints, Pydantic, decorators | 14 (6) | PASS |
| 03_async_streaming | asyncio, gather, generators | 14 (6) | PASS |
| 04_production_python | Modules, uv, pytest, context managers | 11 (4) | PASS |
| 05_mini_ai_agent | Fake typed tools, async coordination, approval gate (deterministic) | 15 (6) | PASS |
| 06_readiness_check | Quiz + executable checks | 4 (1) | PASS |

## 4. Dependencies & tooling [Verified]
- `pyproject.toml`: `requires-python >=3.11`; runtime `pydantic>=2.10,<3`; dev group: ipykernel, jupyterlab, nbclient, nbformat, pytest, ruff; demo group: `gradio>=5.0,<7`. Hatchling build.
- Resolved today: pydantic 2.14.2, gradio 6.31.0, jupyterlab 4.6.5, pytest 9.2.0, ruff 0.17.3, nbclient 0.11.0.
- **uv.lock is NOT committed** (`uv sync` created an untracked `uv.lock`). README links "lockfile guidance" but reproducibility is range-based only.
- CI (`ci.yml`): push+PR, ubuntu, `setup-uv@v6`, Python 3.12 only; runs pytest, notebook execution, ruff. [Unverified] current CI badge status (not checked via GitHub API).
- `.gitignore` ignores `.env`, `.env.*`, keeps `!.env.example` — but **no `.env.example` exists** (fine today since no keys are needed).
- No pre-commit, no type checker (mypy/pyright), no nbstripout, no Dependabot, no issue/PR templates.
- CODEOWNERS present; README correctly states branch protection must be configured separately. [Unverified] whether a ruleset exists.

## 5. Execution results (fresh envs, no API keys) [Verified]
| Python | `pytest` (dev+demo) | notebooks | ruff |
|---|---|---|---|
| 3.12 | 15 passed | 7/7 PASS | clean |
| 3.11 | 15 passed | 7/7 PASS | – |
| 3.13 | 15 passed | 7/7 PASS | – |
- **Bug:** `uv sync --group dev` only (the README's default install) + `pytest` → collection **error** in `tests/test_gradio_demo.py` (`ModuleNotFoundError: gradio`). Fix: `pytest.importorskip("gradio")` or a marker. [Proposed]
- Nothing requires paid keys. Ollama live inference not tested (needs local daemon + ~1.3 GB model per README).

## 6. Secrets [Verified]
Regex scan of working tree and full `git log -p` for `sk-`, `ghp_`, `AKIA`, `hf_` tokens and `password=`: **no hits**. Ollama endpoint pinned to 127.0.0.1.

## 7. Classification
**Keep unchanged** [Proposed]: Java-first lesson pattern; mock-first/no-key philosophy; deterministic `mini_agent` + mocked HTTP tests; notebook-execution CI; Cursor learning-first rule; honest scope/time disclaimers; Ollama loopback safety.
**Improve** [Proposed]: commit `uv.lock` and use `uv sync --locked` in CI; CI matrix 3.11–3.13; importorskip gradio; add `.env.example` once cloud APIs arrive; add Dependabot/Renovate, pre-commit (ruff format, nbstripout), issue/PR templates; replace custom runner with `pytest --nbmake` (optional).
**Broken/outdated**: only the gradio test collection error above. No deprecated OpenAI patterns because no OpenAI code exists. [Verified]
**Missing prerequisites/content** vs. stated AI-Engineering vision: HTTP/JSON with `httpx`, env/secrets handling, LLM API fundamentals (tokens, cost), OpenAI Responses vs Chat Completions, structured outputs, tool calling, embeddings, RAG, evals, observability. Python gaps: exceptions idioms, `logging`, packaging `src/` layout explanation, typing.Protocol depth.
**Simplification**: README is long (marketing + docs mixed); 60-minute claim is unmeasured (author already labels it an estimate); three overlapping navigation docs (README/PROGRESS/guides README) could collapse.
