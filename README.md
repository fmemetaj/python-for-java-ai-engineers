<p align="center"><img src="assets/bridge.svg" alt="Illustrated bridge from Java development to Python AI engineering" width="100%"></p>

<h1 align="center">Python for Java AI Engineers</h1>
<p align="center"><strong>A practical, 60-minute bridge from the Java you know to Python you'll use in AI engineering.</strong></p>
<p align="center"><a href="https://github.com/fmemetaj/python-for-java-ai-engineers/actions/workflows/ci.yml"><img src="https://github.com/fmemetaj/python-for-java-ai-engineers/actions/workflows/ci.yml/badge.svg" alt="CI checks"></a> <img src="https://img.shields.io/badge/Python-3.12-3776ab" alt="Python 3.12"> <img src="https://img.shields.io/badge/study-60_minutes-446f61" alt="60 minutes"> <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="MIT license"></a></p>

> **You already know how to program.** Learn the Python-specific patterns that turn up in AI projects, without re-learning basic programming.

Seven hands-on **Jupyter notebooks**, Java comparisons, short exercises, a targeted `guides/` directory, and an **optional Gradio + Ollama local AI demo**. No paid API keys, Java-to-Python conversion service, or previous machine-learning experience required.

## Start here

| I want to... | Go to |
| --- | --- |
| Start the 60-minute course | **[Lesson 00](notebooks/00_getting_started.ipynb)** |
| Use Cursor, including AI tutor rules | **[Cursor configuration](guides/01_editor_setup.md#cursor)** |
| Use VS Code or another IDE | [Editor alternatives](guides/01_editor_setup.md) |
| Fix a confusing concept | [Six targeted guides](guides/README.md) |
| Try a live local model in a small UI | [Optional Gradio + Ollama lab](guides/06_local_ai_lab.md) |
| Track lesson completion | [Progress checklist](PROGRESS.md) |

## Seven focused lessons (60 minutes)

| Lesson | What you will learn | Time |
| --- | --- | ---: |
| [00 · Getting Started](notebooks/00_getting_started.ipynb) | Notebook mechanics and Java mental model | 3 min |
| [01 · Pythonic Essentials](notebooks/01_pythonic_essentials.ipynb) | Comprehensions, dictionaries, `None`, kwargs | 9 min |
| [02 · OOP, Typing & Pydantic](notebooks/02_typing_pydantic.ipynb) | Dataclasses, types, runtime validation, decorators | 12 min |
| [03 · Async & Streaming](notebooks/03_async_streaming.ipynb) | Coroutines, concurrent I/O, generators | 12 min |
| [04 · Production Python](notebooks/04_production_python.ipynb) | Modules, `uv`, tests, context managers | 9 min |
| [05 · Mini Workflow](notebooks/05_mini_ai_agent.ipynb) | Typed fake tools, async coordination, approval | 12 min |
| [06 · Readiness Check](notebooks/06_readiness_check.ipynb) | Questions and executable checks | 3 min |
| | **Total core learning time** | **60 min** |

Times estimate active learning for engineers comfortable with Java; **environment installation and the optional capstone are excluded**. Run the examples, change one thing, predict what will happen, and attempt the checkpoint.

## Install once using uv

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then from the repository root:

```bash
uv python install 3.12
uv sync --group dev
uv run jupyter lab
```

Open [Lesson 00](notebooks/00_getting_started.ipynb) and select the interpreter in this repository's `.venv`.

**Cursor and VS Code:** open the repository *folder*, install the recommended Python and Jupyter extensions, use **Python: Select Interpreter**, then choose `.venv/Scripts/python.exe` on Windows or `.venv/bin/python` on macOS/Linux. Use the matching notebook kernel. Cursor includes a [learning-first rule](.cursor/rules/learning-first.mdc) that explains Python concepts in Java terms and gives hints instead of automatically completing exercises. [Exact editor instructions](guides/01_editor_setup.md). **Cursor is optional**; browser-based JupyterLab works on its own.

## Optional local AI lab, with a real model if you want

<p align="center"><img src="assets/local-ai-flow.svg" alt="Gradio, Pydantic, mock or local LLM, human review and simulated approval" width="100%"></p>

After Lesson 06, open a tiny **support-ticket response assistant** in your browser to see Python types, async code, HTTP APIs, validation, Gradio callbacks and an approval gate working together:

```bash
uv sync --group dev --group demo
uv run --group demo python examples/gradio_app.py
```

The interface defaults to **Mock (no model)** and requires no API key or Ollama server. For actual *local inference*, install [Ollama](https://ollama.com/download), run `ollama pull llama3.2:1b` (roughly 1.3 GB), and select **Ollama (local model)** in the Gradio app. See the [optional 15–25-minute lab](guides/06_local_ai_lab.md); downloading and initial setup can take longer.

**Scope:** the ticket is fictional, AI text is a draft and must be reviewed, and **approval is simulated only**. The code never sends an email, updates a real ticket, or publishes the local Gradio URL.

## Guides: read only when needed

A short reference library, inspired by the helpfulness of course companion guides:

1. [Editor configuration: Cursor, VS Code, Jupyter](guides/01_editor_setup.md)
2. [Java ↔ Python mental model](guides/02_java_python_map.md)
3. [Async, await, gather and generators](guides/03_async_and_streaming.md)
4. [Pydantic, type hints and decorators](guides/04_pydantic_and_decorators.md)
5. [uv, imports, kernel issues and debugging](guides/05_uv_and_debugging.md)
6. [Gradio/Ollama optional local AI lab](guides/06_local_ai_lab.md)

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

## Verify locally

```bash
uv sync --group dev --group demo
uv run pytest -q
uv run python scripts/validate_notebooks.py
uv run ruff check src tests scripts examples
```

The [CI workflow](.github/workflows/ci.yml) runs these steps without contacting a real model; Ollama HTTP responses are mocked in tests. Dependency bounds are declared in `pyproject.toml`; see [lockfile and reproducibility guidance](guides/05_uv_and_debugging.md).

## Acknowledgments

Thank you to **[Ed Donner (@ed-donner)](https://github.com/ed-donner)** for the approachable, hands-on, notebook-first teaching approach exemplified by his [LLM Engineering repository](https://github.com/ed-donner/llm_engineering). That philosophy inspired the **format** here; all text, exercises, diagrams, and code are original. This project is **independent and is not affiliated with or endorsed by Ed Donner**.

Contributions welcome: [CONTRIBUTING.md](CONTRIBUTING.md). Licensed under [MIT](LICENSE).
