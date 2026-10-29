<p align="center"><img src="assets/bridge.svg" alt="Illustrated bridge from Java development to Python AI engineering" width="100%"></p>

<h1 align="center">Python for Java AI Engineers</h1>
<p align="center"><strong>A practical, estimated ~60-minute bridge from the Java you know to Python you'll use in AI engineering.</strong></p>
<p align="center"><a href="https://github.com/fmemetaj/python-for-java-ai-engineers/actions/workflows/ci.yml"><img src="https://github.com/fmemetaj/python-for-java-ai-engineers/actions/workflows/ci.yml/badge.svg" alt="CI checks"></a> <img src="https://img.shields.io/badge/Python-3.11%E2%80%933.13-3776ab" alt="Python 3.11 to 3.13"> <img src="https://img.shields.io/badge/study-estimated_60_min-446f61" alt="Estimated 60 minutes"> <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="MIT license"></a></p>

> **You already know how to program.** Learn the Python-specific patterns that turn up in AI projects, without re-learning basic programming.

Seven hands-on **Jupyter notebooks**, Java comparisons, short exercises, a targeted `guides/` directory, and an **optional Gradio + Ollama local AI demo**. No paid API keys. Lesson times are **estimates** — [tell us your time](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).

## Start here

```bash
uv python install 3.12
uv sync --locked --group dev
uv run jupyter lab
```

Open [Lesson 00](notebooks/00_getting_started.ipynb) and select the interpreter in this repository's `.venv`.

| I want to... | Go to |
| --- | --- |
| Start the estimated ~60-minute core | **[Lesson 00](notebooks/00_getting_started.ipynb)** |
| Check whether I'm ready / skip ahead | **[Lesson 06 readiness check](notebooks/06_readiness_check.ipynb)** |
| Use Cursor, including AI tutor rules | **[Cursor configuration](guides/01_editor_setup.md#cursor)** |
| Use VS Code or another IDE | [Editor alternatives](guides/01_editor_setup.md) |
| Fix a confusing concept | [Guides](guides/README.md) |
| Try a live local model in a small UI | [Optional Gradio + Ollama lab](guides/06_local_ai_lab.md) |
| Track lesson completion | [Progress checklist](PROGRESS.md) |
| See the proposed longer course | [Planning docs](docs/README.md) |

**Cursor and VS Code:** open the repository *folder*, install the recommended Python and Jupyter extensions, use **Python: Select Interpreter**, then choose `.venv/Scripts/python.exe` on Windows or `.venv/bin/python` on macOS/Linux. Use the matching notebook kernel. Cursor includes a [learning-first rule](.cursor/rules/learning-first.mdc). [Exact editor instructions](guides/01_editor_setup.md). **Cursor is optional**; browser-based JupyterLab works on its own.

## A real lesson, not just a cell to run

Every core notebook begins with **why the concept matters**, then a familiar **Java example**, then the runnable **Python counterpart**. There are predictions, common mistakes, small exercises and a checkpoint. Completing a lesson means *understanding the explanation and attempting the exercise*, not merely selecting Run All.

The **~60-minute schedule is an estimate** for experienced Java developers, not a measured guarantee. If a lesson took much longer or much less, [open a feedback issue](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml). Extra depth lives in [guides](guides/README.md) and the [coverage audit](COVERAGE.md). Optional subjects such as Docker and pickle security are in the [extra foundations reference](guides/07_extra_python_foundations.md).

## Seven focused lessons (estimated)

| Lesson | What you will learn | Est. |
| --- | --- | ---: |
| [00 · Getting Started](notebooks/00_getting_started.ipynb) | Notebook mechanics and Java mental model | 3 min |
| [01 · Pythonic Essentials](notebooks/01_pythonic_essentials.ipynb) | Comprehensions, dictionaries, `None`, kwargs | 9 min |
| [02 · OOP, Typing & Pydantic](notebooks/02_typing_pydantic.ipynb) | Dataclasses, types, runtime validation, decorators | 12 min |
| [03 · Async & Streaming](notebooks/03_async_streaming.ipynb) | Coroutines, concurrent I/O, generators | 12 min |
| [04 · Production Python](notebooks/04_production_python.ipynb) | Modules, `uv`, tests, context managers | 9 min |
| [05 · Mini Workflow](notebooks/05_mini_ai_agent.ipynb) | Typed fake tools, async coordination, approval | 12 min |
| [06 · Readiness Check](notebooks/06_readiness_check.ipynb) | Questions and executable checks | 3 min |
| | **Estimated core learning time** | **~60 min** |

Times estimate active learning; **environment installation and the optional capstone are excluded**. Run the examples, change one thing, predict what will happen, and attempt the checkpoint.

## Optional local AI lab, with a real model if you want

<p align="center"><img src="assets/local-ai-flow.svg" alt="Gradio, Pydantic, mock or local LLM, human review and simulated approval" width="100%"></p>

After Lesson 06, open a tiny **support-ticket response assistant** in your browser:

```bash
uv sync --locked --group dev --group demo
uv run --group demo python examples/gradio_app.py
```

The interface defaults to **Mock (no model)** and requires no API key or Ollama server. For actual *local inference*, install [Ollama](https://ollama.com/download), run `ollama pull llama3.2:1b` (roughly 1.3 GB), and select **Ollama (local model)** in the Gradio app. See the [optional 15–25-minute lab](guides/06_local_ai_lab.md); downloading and initial setup can take longer.

**Scope:** the ticket is fictional, AI text is a draft and must be reviewed, and **approval is simulated only**. The code never sends an email, updates a real ticket, or publishes the local Gradio URL.

## Java concepts and Python counterparts

| Java | Python |
| --- | --- |
| `List<Map<String,Object>>` | `list[dict[str, object]]` |
| Streams | Comprehensions and generators |
| Java records / Bean Validation | Dataclasses and Pydantic |
| Interfaces | `Protocol` or abstract base classes |
| `CompletableFuture` (I/O) | `async`, `await`, `asyncio.gather` |
| Annotations (some overlapping use cases) | Executable decorators |
| Try-with-resources | `with` context managers |
| Maven/Gradle | `uv` and `pyproject.toml` |
| JUnit | `pytest` |

This is a **language bridge**, not a full Python, ML, or agent course. The mandatory workflow is deterministic and *agent-shaped*, not autonomous. Type hints don't validate values at runtime; Pydantic does. The optional LLM output is validated but its content is not guaranteed correct.

A longer, still-offline-first expansion (DocsDesk, LLM APIs, RAG, evals) is **proposed only** in [docs/](docs/README.md). It is not the current syllabus.

## Verify locally

```bash
uv sync --locked --group dev --group demo
uv run pytest -q
uv run python scripts/validate_notebooks.py
uv run ruff check src tests scripts examples
uv run ruff format --check src tests scripts examples
```

CI runs these steps on Python 3.11, 3.12, and 3.13 without contacting a real model; Ollama HTTP responses are mocked in tests. Exact versions are in `uv.lock`. See [lockfile and troubleshooting guidance](guides/05_uv_and_debugging.md).

## Acknowledgments

Thank you to **[Ed Donner (@ed-donner)](https://github.com/ed-donner)** for the approachable, hands-on, notebook-first teaching approach exemplified by his [LLM Engineering repository](https://github.com/ed-donner/llm_engineering). That philosophy inspired the **format** here; all text, exercises, diagrams, and code are original. This project is **independent and is not affiliated with or endorsed by Ed Donner**.

Contributions welcome: [CONTRIBUTING.md](CONTRIBUTING.md). Licensed under [MIT](LICENSE).

## Community collaboration and review

This is a **public, read-only-by-default repository** for visitors. Everyone may fork, suggest changes and submit a pull request; **only people granted GitHub write permissions can push directly**. See [CONTRIBUTING.md](CONTRIBUTING.md).

The maintainer controls the main branch. [CODEOWNERS](.github/CODEOWNERS) identifies the intended reviewer; branch-protection/ruleset enforcement must also be configured in the repository's GitHub Settings and is **not implied** by the file alone.
