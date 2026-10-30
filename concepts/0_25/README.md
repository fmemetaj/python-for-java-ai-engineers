# 0.25 Context managers   [NEW — no Java equivalent] [cost: mock] [~40 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_25/tests/test_skip.py` passes. **Still recommended.**

Related explainer: [notebook 04](../../notebooks/04_production_python.ipynb).

## 1. Concept

A **context manager** is an object for the `with` statement. `__enter__` runs on the way in; `__exit__` runs on the way out — including when the block raises. `contextlib.contextmanager` builds one from a generator that `yield`s once.

## 2. Intuition

`with` is a guaranteed pair of "set up" and "tear down", like a `try/finally` you cannot forget.

```
with Utf8File(path) as handle:
    handle.read()
# __exit__ closed the file even if read() raised
```

A `@contextmanager` function: code before `yield` is `__enter__`; code after `yield` (usually in `finally`) is `__exit__`.

## 3. Why it exists

Files, locks, DB sessions, and timers need teardown. Java's try-with-resources covers **using** `AutoCloseable`. Python uses the same idea for many more types (timers, monkeypatches, cd into a directory). **Writing** a manager is everyday Python; writing `AutoCloseable` is rarer in Java application code.

### The Java analogy that misleads you

Try-with-resources ≈ **using** `with open(...)`. It does **not** teach you `__enter__` / `__exit__` or `contextlib`. Also, Java closes `AutoCloseable`; Python's `__exit__` can optionally swallow exceptions by returning `True` (almost always a bad idea). Do not translate `try (var x = …)` into a class with `close()` and then forget `with`.

## 4. Step-by-step examples

**Example 1 — `with open(path, encoding="utf-8") as f:`** the stdlib manager you should already use on Windows.

**Example 2 — `@contextmanager` timer.** Yield a dict; in `finally`, store elapsed seconds.

**Example 3 — exceptions still record elapsed time.** The `finally` runs after `raise`.

**Example 4 — class-based `Utf8File`.** `__enter__` opens; `__exit__` closes. Pathlib works on Windows and POSIX; do not join paths with `\\` by hand.

**Example 5 — nested `with`.** `with a, b:` is two managers; both exit.

```bash
uv run python concepts/0_25/examples.py
```

Docs: [contextlib](https://docs.python.org/3/library/contextlib.html), [with statement](https://docs.python.org/3/reference/compound_stmts.html#with).

## 5. Common pitfalls

- Opening text files without `encoding="utf-8"` (Windows ANSI).
- Returning `True` from `__exit__` and swallowing bugs.
- Using the yielded file after the `with` block.
- `@contextmanager` functions that yield twice.
- Forgetting `finally` so a failure skips teardown.

## 6. Exercises

1. **Guided:** `timed_block()` via `contextlib`.
2. **Open:** `Utf8File` with `__enter__` / `__exit__`.

```bash
uv run pytest concepts/0_25
```

- Hint 1: `started = time.perf_counter()`; `yield data`; `finally: data["seconds"] = …`.
- Hint 2: `self.path.open(encoding="utf-8")`.
- Solution: `solutions/context.py`.

## 7. Check

1. Does `__exit__` run when the block raises?
2. Why pass `encoding="utf-8"` on Windows?
3. Try-with-resources vs writing `__enter__` — which part is new?
4. Where should DocsDesk put a "time this LLM call" helper?

## Setup / troubleshooting

- **Windows paths:** `Path("logs") / "app.log"` not `"logs\\app.log"` in portable code.
- **Permission errors:** close the handle in `__exit__` or Windows will not let you delete a temp file in the same test.
- **macOS/Linux:** encoding still matters for non-UTF-8 locales.

**Real scenario:** time a DocsDesk retrieval block and always close the UTF-8 log file.

**What you learned:** `with` is try/finally as a protocol; you can write your own.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
