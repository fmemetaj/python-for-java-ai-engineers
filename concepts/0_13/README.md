# 0.13 List/dict/set comprehensions   [NEW — no Java equivalent] [cost: mock] [~45 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_13/tests/test_skip.py` passes. **Still recommended.**

Related explainer: [notebook 01](../../notebooks/01_pythonic_essentials.ipynb). Concept 0.15 compares these to Java Streams.

## 1. Concept

A comprehension builds a collection from an iterable in one expression: transform, optionally filter. Square brackets → list, `{k: v ...}` → dict, `{x ...}` → set. They are **eager**: the whole result exists when the line finishes.

## 2. Intuition

Read a list comprehension left-to-right as English: *"message for each row in rows if the level is ERROR."*

```
[row["message"] for row in rows if row["level"] == "ERROR"]
 \___ result __/  \___ source ___/  \______ filter ______/
```

A nested comprehension is two loops. If you cannot say it in one breath, use a `for` loop.

## 3. Why it exists

Java Streams (`filter`/`map`/`collect`) are a pipeline object. Python wanted the same idea as **syntax**, not a fluent API. That is shorter for simple maps and filters. It is worse for multi-step pipelines (no named intermediate, easy to nest too deep). 0.15 is the "when to choose which style" lesson.

You would do this in Java with a Stream or a `for` + `add`. Both are fine. The Python-specific skill is knowing when a comprehension stays readable.

## 4. Step-by-step examples

**Example 1 — list, map only.** `[line.upper() for line in lines]`

**Example 2 — list, filter.** `[line for line in lines if line.startswith("ERROR")]`

**Example 3 — dict.** `{row["id"]: row["message"] for row in rows}` — last key wins on duplicates.

**Example 4 — set.** `{row["level"] for row in rows}` unique levels.

**Example 5 — flatten (limit).** `[tag for row in rows for tag in row["tags"]]` is two `for`s. A third `for` is usually a readability bug.

```bash
uv run python concepts/0_13/examples.py
```

Docs: [list displays](https://docs.python.org/3/reference/expressions.html#list-displays).

## 5. Common pitfalls

- Nesting until nobody can parse it. Two `for`s is the usual maximum.
- Side effects inside a comprehension (`print`, `append`). Use a loop.
- Dict comprehension with duplicate keys: silent overwrite.
- A set comprehension drops order.
- `[f() for _ in items]` if `f` is expensive — you wanted a generator (0.14).

## 6. Exercises

1. **Guided:** `error_messages(rows)` list comprehension (port a Java `for` + `Map` filter).
2. **Open:** `index_by_id` (dict) and `unique_levels` (set).

```bash
uv run pytest concepts/0_13
```

- Hint 1: `[row["message"] for row in rows if row["level"] == "ERROR"]`.
- Hint 2: `{row["id"]: row["message"] for row in rows}` and `{row["level"] for row in rows}`.
- Solution: `solutions/comprehensions.py`.

## 7. Check

1. Is a list comprehension lazy?
2. What happens if two rows share an id in `index_by_id`?
3. When should you refuse a comprehension and write a loop?
4. `{x for x in items}` vs `[x for x in items]`?

**Real scenario:** DocsDesk turns raw log dicts into error messages and an id→message index in two lines.

**What you learned:** comprehensions are eager readable map/filter; stop nesting.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
