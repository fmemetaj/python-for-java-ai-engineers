# Course progress

Check each lesson when you've run the examples and attempted its checkpoint. Times in the README are **estimates**, not a stopwatch. Install time and the optional lab are extra.

## Module 0A — Python Fundamentals I

Start at [modules/0a-fundamentals/README.md](modules/0a-fundamentals/README.md). Analog concepts can be skipped on a passing skip test. **NEW** concepts are still recommended.

- [ ] [0.1 Running Python](concepts/0_01/README.md) — Analog
- [ ] [0.2 Notebooks](concepts/0_02/README.md) — NEW
- [ ] [0.3 Variables](concepts/0_03/README.md) — Analog
- [ ] [0.4 Built-in types](concepts/0_04/README.md) — Analog
- [ ] [0.5 Truthiness](concepts/0_05/README.md) — NEW
- [ ] [0.6 Control flow](concepts/0_06/README.md) — Analog
- [ ] [0.7 Functions](concepts/0_07/README.md) — Analog
- [ ] [0.8 `*args` / `**kwargs`](concepts/0_08/README.md) — NEW
- [ ] [0.9 Scope and closures](concepts/0_09/README.md) — NEW
- [ ] [0.10 First-class functions](concepts/0_10/README.md) — Analog
- [ ] [0.11 Collections](concepts/0_11/README.md) — Analog
- [ ] [0.12 Slicing and unpacking](concepts/0_12/README.md) — NEW
- [ ] [0.13 Comprehensions](concepts/0_13/README.md) — NEW
- [ ] [0.14 Generators](concepts/0_14/README.md) — NEW
- [ ] [0.15 Streams vs comprehensions](concepts/0_15/README.md) — Analog
- [ ] [Placement check](placement/README.md)
- [ ] [Deliverable: `fundamentals/log_stats.py`](fundamentals/README.md)
- [ ] `uv run course check m0a`

## Module 0B — Python Fundamentals II

Start at [modules/0b-fundamentals/README.md](modules/0b-fundamentals/README.md). Analog concepts can be skipped on a passing skip test. **NEW** concepts are still recommended.

- [ ] [0.16 Classes and objects](concepts/0_16/README.md) — Analog
- [ ] [0.17 Properties](concepts/0_17/README.md) — Analog
- [ ] [0.18 Dunder methods](concepts/0_18/README.md) — NEW
- [ ] [0.19 Dataclasses and Pydantic](concepts/0_19/README.md) — Analog
- [ ] [0.20 Inheritance and MRO](concepts/0_20/README.md) — Analog
- [ ] [0.21 Duck typing](concepts/0_21/README.md) — NEW
- [ ] [0.22 Protocol and ABCs](concepts/0_22/README.md) — Analog
- [ ] [0.23 Type hints vs generics](concepts/0_23/README.md) — Analog
- [ ] [0.24 Exceptions](concepts/0_24/README.md) — Analog
- [ ] [0.25 Context managers](concepts/0_25/README.md) — NEW
- [ ] [0.26 Decorators](concepts/0_26/README.md) — NEW
- [ ] [0.27 Modules and packages](concepts/0_27/README.md) — Analog
- [ ] [0.28 Threads and executors](concepts/0_28/README.md) — Analog
- [ ] [0.29 GIL and asyncio](concepts/0_29/README.md) — NEW
- [ ] [Deliverable: `fundamentals/tool_registry.py`](fundamentals/README.md)
- [ ] `uv run course check m0b`
- [ ] [06 · Readiness Check](notebooks/06_readiness_check.ipynb)

## Module 1 — Python Engineering & Tooling

Start at [modules/1-engineering-tooling/README.md](modules/1-engineering-tooling/README.md). Analog concepts can be skipped on a passing skip test. **NEW** concept 1.3 is still recommended.

- [ ] [1.1 uv](concepts/1_01/README.md) — Analog
- [ ] [1.2 pyproject.toml and uv.lock](concepts/1_02/README.md) — Analog
- [ ] [1.3 Virtual environments](concepts/1_03/README.md) — NEW
- [ ] [1.4 src layout and entry points](concepts/1_04/README.md) — Analog
- [ ] [1.5 ruff and pyright](concepts/1_05/README.md) — Analog
- [ ] [1.6 Logging](concepts/1_06/README.md) — Analog
- [ ] [1.7 Config and secrets](concepts/1_07/README.md) — Analog
- [ ] [1.8 pytest](concepts/1_08/README.md) — Analog
- [ ] [1.9 Mocking](concepts/1_09/README.md) — Analog
- [ ] [1.10 httpx](concepts/1_10/README.md) — Analog
- [ ] [1.11 JSON ↔ Pydantic](concepts/1_11/README.md) — Analog
- [ ] [1.12 Retries with backoff](concepts/1_12/README.md) — Analog
- [ ] [Deliverable: `src/docsdesk`](modules/1-engineering-tooling/README.md)
- [ ] `uv run course check m1`

## Original notebooks (optional explainers)

- [ ] [00 · Getting Started](notebooks/00_getting_started.ipynb)
- [ ] [01 · Pythonic Essentials](notebooks/01_pythonic_essentials.ipynb)
- [ ] [02 · OOP, Typing & Pydantic](notebooks/02_typing_pydantic.ipynb)
- [ ] [03 · Async & Streaming](notebooks/03_async_streaming.ipynb)
- [ ] [04 · Production Python](notebooks/04_production_python.ipynb)
- [ ] [05 · Mini Workflow](notebooks/05_mini_ai_agent.ipynb)
- [ ] [06 · Readiness Check](notebooks/06_readiness_check.ipynb)

## Optional showcase (after the core notebooks)

- [ ] [Open the Gradio app in Mock mode](guides/06_local_ai_lab.md)
- [ ] Try Ollama with `llama3.2:1b` locally (optional)
- [ ] Extend one category and add a test

## Troubleshooting notes

Start with [docs/setup/troubleshooting.md](docs/setup/troubleshooting.md) or `uv run python scripts/doctor.py --offline`. Use the [topic guides](guides/README.md) only when a concept is unclear.

## How to mark a lesson complete

- [ ] Read the Java analogy and Python explanation **before** executing code.
- [ ] Predict at least one result, run it, and understand why it happened.
- [ ] Edit the **Your turn** example and verify the assertion.
- [ ] Explain one language difference in your own words.

If a lesson's estimate was wildly off, [send feedback with the minutes you actually spent](.github/ISSUE_TEMPLATE/lesson-feedback.yml).
