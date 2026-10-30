# Module 0A — Python Fundamentals I: Core Language

[Analog + NEW] [cost: mock] [~8–9 h estimated] [last verified: 2026-10-30, Python 3.11–3.13]

**Objective:** write correct, idiomatic Python for everyday logic, understanding each construct relative to its Java counterpart or as a new idea.

**Prereqs:** professional Java (or another typed backend language). No Python required.

**Offline:** every exercise uses the standard library and pytest. No API key. Cost badge: `mock`.

## Do I need this? (3 questions)

If you can answer these in your head without looking them up, run the placement check and skip any Analog concept whose skip test passes. **NEW** concepts are still recommended: they are the places Java developers get surprised.

1. What does `def f(items=[])` do on the second call, and why?
2. Is `0` true or false in `if value:`? What about `[]` and `"0"`?
3. When would you `yield` a log line instead of returning a `list`?

Placement (15 minutes, 10 tasks):

```bash
uv run pytest placement/test_self_check.py
```

Per-concept skip (2–3 minutes):

```bash
uv run pytest concepts/0_11/tests/test_skip.py
```

Pass an Analog skip test → skip that concept. Pass a NEW skip test → still read the lesson.

## Concepts in order

| ID | Lesson | Kind | Est. | Skip / exercise |
|---|---|---|---:|---|
| 0.1 | [Running Python](../../concepts/0_01/README.md) | Analog | 20 min | `uv run pytest concepts/0_01` |
| 0.2 | [Notebooks](../../concepts/0_02/README.md) | **NEW** | 25 min | `uv run pytest concepts/0_02` |
| 0.3 | [Variables](../../concepts/0_03/README.md) | Analog | 30 min | `uv run pytest concepts/0_03` |
| 0.4 | [Built-in types](../../concepts/0_04/README.md) | Analog | 30 min | `uv run pytest concepts/0_04` |
| 0.5 | [Truthiness](../../concepts/0_05/README.md) | **NEW** | 20 min | `uv run pytest concepts/0_05` |
| 0.6 | [Control flow](../../concepts/0_06/README.md) | Analog | 30 min | `uv run pytest concepts/0_06` |
| 0.7 | [Functions](../../concepts/0_07/README.md) | Analog | 35 min | `uv run pytest concepts/0_07` |
| 0.8 | [`*args` / `**kwargs`](../../concepts/0_08/README.md) | **NEW** | 35 min | `uv run pytest concepts/0_08` |
| 0.9 | [Scope, closures, `nonlocal`](../../concepts/0_09/README.md) | **NEW** | 25 min | `uv run pytest concepts/0_09` |
| 0.10 | [First-class functions](../../concepts/0_10/README.md) | Analog | 25 min | `uv run pytest concepts/0_10` |
| 0.11 | [Collections](../../concepts/0_11/README.md) | Analog | 40 min | `uv run pytest concepts/0_11` |
| 0.12 | [Slicing and unpacking](../../concepts/0_12/README.md) | **NEW** | 25 min | `uv run pytest concepts/0_12` |
| 0.13 | [Comprehensions](../../concepts/0_13/README.md) | **NEW** | 45 min | `uv run pytest concepts/0_13` |
| 0.14 | [Iterators and generators](../../concepts/0_14/README.md) | **NEW** | 50 min | `uv run pytest concepts/0_14` |
| 0.15 | [Streams vs comprehensions](../../concepts/0_15/README.md) | Analog | 25 min | `uv run pytest concepts/0_15` |

Times are unmeasured estimates. [Tell us your actual minutes](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).

## How each lesson works

- **Analog:** Java snippet first (≤15 lines, compiled in CI with JDK 21) → Python equivalent → differences & pitfalls table → exercise → check.
- **NEW:** intuition → why it exists (and what Java does instead) → 3–5 step-by-step examples → ≥2 exercises → check. Partial Java analogs (varargs, `Iterator`, Streams) are treated as NEW so you do not over-trust them.
- Starters live in `concepts/0_XX/exercises/`. They **fail** the tests on purpose. Solutions live in `concepts/0_XX/solutions/` and are validated in CI. Do not copy solutions until you have tried the hints.
- Existing notebooks [00](../../notebooks/00_getting_started.ipynb), [01](../../notebooks/01_pythonic_essentials.ipynb), and [03](../../notebooks/03_async_streaming.ipynb) stay as optional explainers. They are reused here as material, not replaced.

## Module deliverable

`fundamentals/log_stats.py` — a typed log-file analyzer (parse, count, lazy iteration) that DocsDesk will reuse later.

```bash
uv run pytest fundamentals/test_log_stats.py
```

## Module checkpoint

```bash
uv run course check m0a
```

Prints pass/fail per concept, plus `log_stats` and placement. CI runs the same command against `solutions/`.

## Setup if you get stuck

PATH, `python` vs `python3`, Windows Store stub, `uv` / `.venv`, encoding, and line endings: [troubleshooting](../../docs/setup/troubleshooting.md). Concept 0.1 covers the same issues in lesson form.

```bash
uv sync --locked --group dev
uv run python scripts/doctor.py --offline
```
