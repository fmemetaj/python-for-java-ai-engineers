# Module 0B — Python Fundamentals II: Objects, Typing, Errors, Runtime Model

[Analog + NEW] [cost: mock] [~8–9 h estimated] [last verified: 2026-10-30, Python 3.11–3.13]

**Objective:** design Python code the Pythonic way rather than the Java way: data classes, protocols, type hints, exceptions, context managers, decorators, modules, and the concurrency model.

**Prereqs:** Module 0A (or the 0A placement check). Professional Java (or another typed backend language).

**Offline:** every exercise uses the standard library, Pydantic, and pytest. No API key. Cost badge: `mock`.

## Do I need this? (3 questions)

If you can answer these in your head without looking them up, run the per-concept skip tests. **NEW** concepts are still recommended: they are the places Java developers get surprised.

1. Why is a Python decorator **not** a Java annotation? (What runs, and when?)
2. Do type hints (`list[int]`) reject a `list[str]` at runtime the way `List<Integer>` does at compile time?
3. Why does `asyncio.gather` make ten fake HTTP calls finish sooner, but **not** make a CPU-heavy loop finish sooner?

Per-concept skip (2–3 minutes):

```bash
uv run pytest concepts/0_16/tests/test_skip.py
```

Pass an Analog skip test → skip that concept. Pass a NEW skip test → still read the lesson.

## Concepts in order

| ID | Lesson | Kind | Est. | Skip / exercise |
|---|---|---|---:|---|
| 0.16 | [Classes and objects](../../concepts/0_16/README.md) | Analog | 45 min | `uv run pytest concepts/0_16` |
| 0.17 | [Properties](../../concepts/0_17/README.md) | Analog | 20 min | `uv run pytest concepts/0_17` |
| 0.18 | [Dunder methods](../../concepts/0_18/README.md) | **NEW** | 40 min | `uv run pytest concepts/0_18` |
| 0.19 | [Dataclasses and Pydantic](../../concepts/0_19/README.md) | Analog | 35 min | `uv run pytest concepts/0_19` |
| 0.20 | [Inheritance and MRO](../../concepts/0_20/README.md) | Analog | 25 min | `uv run pytest concepts/0_20` |
| 0.21 | [Duck typing](../../concepts/0_21/README.md) | **NEW** | 30 min | `uv run pytest concepts/0_21` |
| 0.22 | [Protocol and ABCs](../../concepts/0_22/README.md) | Analog | 35 min | `uv run pytest concepts/0_22` |
| 0.23 | [Type hints vs generics](../../concepts/0_23/README.md) | Analog | 40 min | `uv run pytest concepts/0_23` |
| 0.24 | [Exceptions](../../concepts/0_24/README.md) | Analog | 35 min | `uv run pytest concepts/0_24` |
| 0.25 | [Context managers](../../concepts/0_25/README.md) | **NEW** | 40 min | `uv run pytest concepts/0_25` |
| 0.26 | [Decorators](../../concepts/0_26/README.md) | **NEW** | 45 min | `uv run pytest concepts/0_26` |
| 0.27 | [Modules and packages](../../concepts/0_27/README.md) | Analog | 30 min | `uv run pytest concepts/0_27` |
| 0.28 | [Threads and executors](../../concepts/0_28/README.md) | Analog | 25 min | `uv run pytest concepts/0_28` |
| 0.29 | [GIL and asyncio](../../concepts/0_29/README.md) | **NEW** | 60 min | `uv run pytest concepts/0_29` |

Times are unmeasured estimates. [Tell us your actual minutes](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).

## How each lesson works

- **Analog:** Java snippet first (≤15 lines, compiled in CI with JDK 21) → Python equivalent → differences & pitfalls table → exercise → check.
- **NEW:** intuition → why it exists (and what Java does instead) → 3–5 step-by-step examples → ≥2 exercises → check. Partial Java analogs (try-with-resources, annotations, `CompletableFuture`) are treated as NEW so you do not over-trust them.
- Starters live in `concepts/0_XX/exercises/`. They **fail** the tests on purpose. Solutions live in `concepts/0_XX/solutions/` and are validated in CI. Do not copy solutions until you have tried the hints.
- Existing notebooks [02](../../notebooks/02_typing_pydantic.ipynb), [03](../../notebooks/03_async_streaming.ipynb), [04](../../notebooks/04_production_python.ipynb), [05](../../notebooks/05_mini_ai_agent.ipynb), and [06](../../notebooks/06_readiness_check.ipynb) stay as optional explainers. They are reused here as material, not replaced.

## Module deliverable

`fundamentals/tool_registry.py` — a `Protocol`-typed tool registry with decorator-based registration. The same pattern is wired into `src/mini_agent/registry.py` so the helpdesk simulation can look up tools by name.

```bash
uv run pytest fundamentals/test_tool_registry.py
```

Existing `mini_agent` tests must still pass (`uv run pytest tests/test_agent.py`).

## Module checkpoint

```bash
uv run course check m0b
```

Prints pass/fail per concept, plus `tool_registry`. CI runs the same command against `solutions/`. After this module, also run the original [readiness check 06](../../notebooks/06_readiness_check.ipynb), then continue with [Module 1](../1-engineering-tooling/README.md).

## Setup if you get stuck

PATH, `python` vs `python3`, Windows Store stub, `uv` / `.venv`, encoding, and line endings: [troubleshooting](../../docs/setup/troubleshooting.md).

- **Editor interpreter:** Command Palette → Python: Select Interpreter → `.venv`. Otherwise pyright reports `pydantic` missing and type hints look broken.
- **Windows files:** always `open(..., encoding="utf-8")`. Context-manager lessons (0.25) and module imports (0.27) fail in confusing ways with the system ANSI code page.
- **Notebook vs script:** notebooks allow top-level `await`. In `.py` files use `asyncio.run(main())` under `if __name__ == "__main__":` (0.29).
- **GIL:** threads (0.28) overlap I/O; they do not parallelize CPU-bound Python. `asyncio` (0.29) is cooperative concurrent I/O, not multithreading.

```bash
uv sync --locked --group dev
uv run python scripts/doctor.py --offline
```
