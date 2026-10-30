# 0.21 Duck typing   [NEW — no Java equivalent] [cost: mock] [~30 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_21/tests/test_skip.py` passes. **Still recommended.**

Related explainer: [notebook 02](../../notebooks/02_typing_pydantic.ipynb).

## 1. Concept

**Duck typing** means a function cares about **behaviour** (methods and attributes), not a declared type. If `obj` has `read()`, you can stream it — even if it never heard of `io.IOBase`.

## 2. Intuition

"If it walks like a duck and quacks like a duck, it is a duck for this function." There is no `implements Duck` at runtime. The call either works or raises `AttributeError` / `TypeError`.

```
line_count(obj)
    has line_count()?  → call it
    else has .lines?   → len(obj.lines)
    else               → TypeError
```

## 3. Why it exists

Java needs a named type (`interface`, superclass) before a method can accept two unrelated classes. That is safe and verbose. Python libraries (files, HTTP clients, pytest's `tmp_path`) accept anything that matches a small surface. You get fewer types to invent — and later, fewer guarantees unless you add a `Protocol` (0.22) for the type checker.

### The Java analogy that misleads you

`Object` plus `instanceof` is not duck typing. Reflection (`getMethod("read")`) is the closest JVM cousin, and you would not use it for ordinary APIs. Do not think "duck typing = skip types forever". Production Python still adds Protocols and Pydantic at the edges.

## 4. Step-by-step examples

**Example 1 — two unrelated classes, one function.** A `Path` and a fake `Reader` both have `read()` in your tests.

**Example 2 — `getattr(obj, "read", None)`** plus `callable(...)` instead of `isinstance`.

**Example 3 — `len(obj.lines)`** as a fallback shape for log batches.

**Example 4 — failure mode.** `line_count(object())` raises `TypeError` with a useful message — fail loud, like a missing interface, not a `null`.

**Example 5 — files on Windows.** A "file-like" object still needs `encoding="utf-8"` when *you* open a real path. Duck typing does not fix the console code page.

```bash
uv run python concepts/0_21/examples.py
```

Docs: [glossary — duck-typing](https://docs.python.org/3/glossary.html#term-duck-typing).

## 5. Common pitfalls

- Catching `AttributeError` too broadly and hiding typos (`obj.raed()`).
- Assuming `read` exists because a similar class in Java implemented `InputStream`.
- Using duck typing for untrusted JSON — that is a Pydantic job (0.19).
- `hasattr` is true for non-callable attributes named `read`. Check `callable`.

## 6. Exercises

1. **Guided:** `line_count(obj)` — method first, then `.lines`.
2. **Open:** `can_stream(obj)` — true iff `read` is callable.

```bash
uv run pytest concepts/0_21
```

- Hint 1: `getattr(obj, "line_count", None)` then `callable`.
- Hint 2: same pattern for `read`.
- Solution: `solutions/duck.py`.

## 7. Check

1. Must `MemoryLog` subclass `FileLog` before `line_count` works?
2. What exception should a function raise when the duck does not quack?
3. Why is `callable(getattr(obj, "read", None))` safer than `hasattr(obj, "read")`?
4. Where does duck typing stop and Pydantic start?

**Real scenario:** DocsDesk accepts any object that can `search(query) -> list[str]` in tests, including a fake in-memory retriever that is not in the production class tree.

**What you learned:** runtime Python dispatches on behaviour; declare a Protocol when you want the editor to catch mismatches.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
