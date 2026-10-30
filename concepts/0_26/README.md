# 0.26 Decorators   [NEW — no Java equivalent] [cost: mock] [~45 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_26/tests/test_skip.py` passes. **Still recommended.**

Related explainer: [notebook 02](../../notebooks/02_typing_pydantic.ipynb).

## 1. Concept

A **decorator** is a callable that takes a function (or class) and returns a replacement. `@timed` above `def f` means `f = timed(f)` — that assignment **runs at definition time**. Decorators can wrap calls, register tools, retry, or time work.

## 2. Intuition

Think "function factory that wraps another function", not "label on a method".

```
@retry(3)
def flaky():
    ...
# is
def flaky():
    ...
flaky = retry(3)(flaky)
```

`retry(3)` runs first and returns a decorator. That decorator runs with `flaky` and returns the wrapper that callers actually invoke.

## 3. Why it exists

Cross-cutting behaviour (timing, retries, registration) would otherwise be copy-pasted into every function. Java uses annotations *plus* a framework that *later* reads them (Spring, Jakarta). Python decorators **are** the framework: they execute in your process when the module is imported.

### The Java analogy that misleads you

`@Override` / `@Deprecated` / Spring `@Service` look like `@retry`. They are **metadata**. The JVM or Spring processes them. A Python decorator is an ordinary function call that can replace the function, start a thread, or fill a registry. `@tool("search")` in DocsDesk **registers** the function as a side effect. That cannot be `@Override`.

## 4. Step-by-step examples

**Example 1 — identity decorator.** `def banner(fn): return fn` then `@banner`. Nothing changes, but `banner(fn)` already ran.

**Example 2 — wrap the call.** Inner function calls `fn(*args, **kwargs)` and returns a modified result.

**Example 3 — `functools.wraps`.** Copy `__name__` and `__doc__` so pytest and logs show `add`, not `wrapped`.

**Example 4 — `@timed`.** Return `(result, seconds)` using `time.perf_counter()`.

**Example 5 — `@retry(times)`.** A decorator *with arguments* is a factory. Loop, catch `Exception`, re-raise the last one. Used later for flaky I/O, never to hide programming errors in tests.

```bash
uv run python concepts/0_26/examples.py
```

Docs: [glossary — decorator](https://docs.python.org/3/glossary.html#term-decorator), [functools.wraps](https://docs.python.org/3/library/functools.html#functools.wraps).

## 5. Common pitfalls

- Forgetting `return wrapper` — `@deco` then becomes `None`.
- Forgetting `*args, **kwargs` — keyword-only calls break.
- Skipping `wraps` — `__name__` is `wrapped`.
- `@retry` on a non-idempotent function (charging a card twice).
- Confusing decorator syntax `@retry(3)` (factory) with `@retry` (the decorator itself).

## 6. Exercises

1. **Guided:** `timed(fn)` → `(result, elapsed)`.
2. **Open:** `retry(times)` factory that re-raises after the last failure.

```bash
uv run pytest concepts/0_26
```

- Hint 1: `wraps(fn)` on the inner function; `perf_counter` around `fn(...)`.
- Hint 2: `for _ in range(times): try: return fn(...) except Exception as exc: last = exc`.
- Solution: `solutions/decorators.py`.

## 7. Check

1. When does `timed(add)` run — at import or at each call?
2. Why is a Java annotation a bad mental model?
3. What does `@retry(3)` return *before* it sees the function?
4. How will the 0B tool registry use a decorator?

## Setup / troubleshooting

- No extra packages. If `wraps` is missing, you are on a broken install — re-run `uv sync --locked --group dev`.
- Debugger "jumps" into `wrapped` first; `wraps` keeps the original name in stack traces.

**Real scenario:** `@registry.register("classify")` on a DocsDesk tool — registration is a real function call at import.

**What you learned:** `@deco` is `f = deco(f)` and it runs code; annotations do not.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
