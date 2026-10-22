# Python for Java AI Engineers

**A practical, 60-minute Python bridge for experienced Java developers entering AI engineering.**

If you've worked with Java, Spring Boot, APIs and backend architecture, you already know how to program. The question is how Python expresses familiar ideas, and which Python patterns you'll encounter in LLM and agent projects. Let's focus on *that*.

This is a beginner-friendly **Python language bridge**, not a complete AI, LangChain or Python course. Examples use a fictional helpdesk: support tickets, knowledge-base lookup and an approval-gated response. The mini workflow is deterministic and does **not** call an LLM. You do not need API keys or paid services.

## Who this is for

- Experienced Java/JVM developers who know OOP, interfaces, exceptions, REST and concurrency.
- Engineers who want to read, troubleshoot and modify Python used in GenAI and agent applications.
- People who would rather run small examples than watch another 20-hour beginner course.

**Prerequisites:** Java programming knowledge, Python 3.11+ (or let `uv` install Python 3.12), [uv](https://docs.astral.sh/uv/getting-started/installation/) and a terminal. No prior ML expertise required.

## One-hour syllabus

| Lesson | Notebook | Time | You will practice |
| --- | --- | ---: | --- |
| 00 | [Getting started](notebooks/00_getting_started.ipynb) | 3 min | Working with a Python notebook and comparing Java types |
| 01 | [Pythonic essentials](notebooks/01_pythonic_essentials.ipynb) | 9 min | Comprehensions, dictionaries, `None`, kwargs and mutable defaults |
| 02 | [OOP, typing and Pydantic](notebooks/02_typing_pydantic.ipynb) | 12 min | Dataclasses, validation, type hints and decorators |
| 03 | [Async and streaming](notebooks/03_async_streaming.ipynb) | 12 min | Coroutines, concurrent I/O, exceptions and generators |
| 04 | [Production Python](notebooks/04_production_python.ipynb) | 9 min | Imports, uv, files, testing, installed packages |
| 05 | [Mini agent workflow](notebooks/05_mini_ai_agent.ipynb) | 12 min | A typed, async, approval-gated mock agent |
| 06 | [Readiness check](notebooks/06_readiness_check.ipynb) | 3 min | Five diagnostic questions and executable checks |
| | **Total** | **60 min** | |

Track completion in [PROGRESS.md](PROGRESS.md). **The 60 minutes exclude initial environment installation.**

## Setup (using uv)

Open a terminal in the repository root:

```bash
# Install uv first if needed: https://docs.astral.sh/uv/getting-started/installation/
uv python install 3.12
uv sync --group dev
uv run jupyter lab
```

Open `notebooks/00_getting_started.ipynb`, select the project's Python kernel if prompted, and run the cells in order. The exercises have safe-to-run starting cells and solutions directly below them, so **Run All** is also supported.

If Jupyter selects another environment, select the interpreter from `.venv` or run:

```bash
uv run python -m ipykernel install --user --name java-ai-python --display-name "Python (java-ai-python)"
```

Then select `Python (java-ai-python)` as the notebook kernel. This command registers the project's environment in your own Jupyter installation.

> The package is installed in editable mode by `uv sync`; you should be able to `import mini_agent` from any notebook. Run Jupyter from the repository root.

## Validate everything without manual clicking

```bash
uv sync --group dev
uv run pytest -q
uv run python scripts/validate_notebooks.py
uv run ruff check src tests scripts
```

On the first run `uv sync` resolves dependencies and generates `uv.lock`; commit that file to keep future installs reproducible. The notebook checker executes all seven notebooks in fresh kernels (from the repository root). CI repeats these commands on pushes and pull requests.

## How to learn effectively

1. **Java analogy:** recognize a familiar concept, then learn the Python difference.
2. **Run the code:** observe the real result rather than just reading it.
3. **Change one thing:** predict what will happen, then test your hypothesis.
4. **Attempt the checkpoint:** compare with the solution only after trying.
5. **Move on:** this is a bridge, not a mandate to memorize every Python feature.

The mini project intentionally separates validation, fake I/O tools, decision logic and approval handling. It is **agent-shaped**, not a genuine autonomous agent: it has no reasoning model, retrieval embeddings or external tool execution. The next step in a real AI project is to integrate a model behind this tested structure and measure its behavior.

## Java to Python lookup

| Java | Python |
| --- | --- |
| `List<Map<String, Object>>` | `list[dict[str, object]]` |
| Stream `filter/map` | List/dict comprehensions |
| Java `record` / DTO | `@dataclass` / Pydantic `BaseModel` |
| Annotations (similar use cases, different mechanics) | Decorators `@something` |
| `CompletableFuture` | `async` / `await` / `asyncio.gather()` |
| `Optional<T>` | `T \| None` (type annotation) |
| `try-with-resources` | `with` context manager |
| Maven / Gradle | `uv` + `pyproject.toml` |
| JUnit / Mockito | pytest / mocking |

## Limitations and next steps

One hour is sufficient for a *guided introduction*, not fluency or production certification. You'll still learn by building real projects: async cancellation, timeouts, retries, security, test mocking, dependency management and API SDK details all deserve deeper practice. This bridge focuses on reading and editing the kind of Python you'll see in AI engineering.

## Inspiration and attribution

Inspired by the **hands-on notebook teaching format** popularized in courses such as [Ed Donner's LLM Engineering](https://github.com/ed-donner/llm_engineering). All written explanations, examples and code here are original; this repository is independent and is not affiliated with or endorsed by Ed Donner.

## License

MIT. See [LICENSE](LICENSE). Contributions and corrections are welcome.
