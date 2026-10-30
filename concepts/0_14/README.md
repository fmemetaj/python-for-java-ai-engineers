# 0.14 Iterators, generators and `yield`   [NEW — no Java equivalent] [cost: mock] [~50 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_14/tests/test_skip.py` passes. **Still recommended.**

Related explainer: [notebook 03](../../notebooks/03_async_streaming.ipynb) (generators section).

## 1. Concept

An **iterator** is an object that produces values one at a time via `next()` until it raises `StopIteration`. A **generator** is a function that `yield`s values: calling it returns an iterator, and the function **pauses** at each `yield`. Generators are lazy and **single-use**.

## 2. Intuition

A generator is a paused function, not a collection. The first `next` runs to the first `yield` and hands you a value. The next `next` resumes right after that `yield`. Nothing after the last requested item is computed.

```
def errors(lines):
    for line in lines:          # not run until next()
        if line.startswith("E"):
            yield line          # pause; return one line
```

Draw it as a playback head on a tape, not as an `ArrayList` already in memory.

## 3. Why it exists

Logs, HTTP streams, and LLM token streams do not fit in memory. Java would use `Iterator<T>`, `Stream`, or a callback. Those work, but writing a custom `Iterator` means a class with `hasNext`/`next` and stored fields. `yield` writes the same idea as straight-line code.

### The Java analogy that misleads you

`Iterator<T>` is a **partial** analog. It is also single-pass. It is **not** a paused stack frame: you manage the cursor yourself. `Stream` is lazy too, but it is a pipeline of operations, not a function you can step through in a debugger the same way. Do not think "generator = ArrayList I have not filled yet" — after one `for` loop, a generator is empty.

## 4. Step-by-step examples

**Example 1 — `yield` one at a time.** `def countdown(n): while n: yield n; n -= 1`

**Example 2 — `for` consumes the generator.** `for item in countdown(3):` runs `next` until stop.

**Example 3 — single-use.** `g = errors(lines); list(g); list(g)` — the second list is `[]`.

**Example 4 — `take(n, items)`.** Yield the first `n` items, then stop (do not consume the rest if the source is a file — actually `for` on a file still reads incrementally).

**Example 5 — lazy file lines.** `def iter_errors(path): for line in path.open(encoding="utf-8"): ... yield`. Opening with UTF-8 matters on Windows.

```bash
uv run python concepts/0_14/examples.py
```

Docs: [yield expressions](https://docs.python.org/3/reference/expressions.html#yieldexpr).

## 5. Common pitfalls

- Calling a generator function and expecting a list. You got an iterator.
- Iterating twice and wondering where the data went.
- Using a generator after you already unpacked it (`a, *rest = gen`).
- Holding a generator while the file it reads has been closed.
- Building `list(huge_gen)` and throwing away laziness.

**When a generator beats a list:** the input is large or infinite, you might stop early, or you want to pipeline stages without materializing intermediates. Prefer a list when you need `len`, reuse, or random access.

## 6. Exercises

1. **Guided:** `iter_errors(lines)` yields lines that start with `ERROR`.
2. **Open:** `take(n, items)` and show single-use with `replay_count` (how many items a second pass produces).

```bash
uv run pytest concepts/0_14
```

- Hint 1: `for line in lines: if line.startswith("ERROR"): yield line`.
- Hint 2: `for i, item in enumerate(items): if i >= n: return; yield item`. Second pass over the same generator is empty → `0`.
- Solution: `solutions/generators.py`.

## 7. Check

1. Does `iter_errors(...)` return a list?
2. After `list(gen)`, what does a second `list(gen)` produce?
3. Why open log files with `encoding="utf-8"` on Windows?
4. When would you still return a `list` from a log helper?

**Real scenario:** DocsDesk streams a 2 GB support log and stops at the first 20 errors — a list of the whole file would be the Java-in-Python-syntax mistake.

**What you learned:** `yield` pauses a function; generators are lazy and single-use.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
