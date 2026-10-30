# 0.5 Truthiness and falsy values   [NEW — no Java equivalent] [cost: mock] [~20 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_05/tests/test_skip.py` passes. **Still recommended.**

Related explainer: [notebook 01](../../notebooks/01_pythonic_essentials.ipynb).

## 1. Concept

In a boolean context (`if`, `while`, `and`, `or`, `not`, `bool(x)`), every object is **truthy** or **falsy**. You do not have to write `if items.size() > 0`. You write `if items:`.

## 2. Intuition

Python asks an object "are you empty / zero / missing?" instead of requiring a `boolean` expression. The built-in falsy values are a short list; everything else is truthy.

Falsy: `None`, `False`, `0`, `0.0`, `0j`, `""`, `[]`, `{}`, `set()`, `range(0)`.

Truthy examples: `True`, `1`, `"0"`, `"false"`, `[0]`, `{"ok": None}`.

## 3. Why it exists

Java's `if` condition must be `boolean`. `if (list)` does not compile. You write `if (list != null && !list.isEmpty())`. Python's truthiness collapses the common "is there something here?" check. That is shorter — and it hides the difference between `None` and `[]` if you are not careful.

## 4. Step-by-step examples

**Example 1 — empty collections are falsy.** `if not tickets:` means "no tickets" for both `[]` and (accidentally) `None`.

**Example 2 — zero is falsy, the string `"0"` is not.** `if count:` is wrong when `0` is a valid measurement.

**Example 3 — `or` for defaults.** `title = incoming or "untitled"` uses the first truthy value. `incoming = ""` becomes `"untitled"`.

**Example 4 — `and` returns an operand.** `user and user.get("id")` returns `None` if `user` is `None`, else the id. Readable in small doses.

**Example 5 — prefer explicit checks when `0` or `""` are valid.** `if value is None:` (see 0.4) or `if len(items) == 0:`.

```bash
uv run python concepts/0_05/examples.py
```

Official rules: [truth value testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing).

## 5. Common pitfalls

- Treating `0` as "missing" when it is a count.
- `if user:` is False for `{}` even if "empty dict" is a valid payload.
- `incoming or default` turns `""` into the default; use `if incoming is None` when empty string is data.
- Custom classes are truthy unless they define `__bool__` or `__len__`.

## 6. Exercises

1. **Guided:** `keep_truthy(values)` — filter with Python truthiness.
2. **Open:** `first_present(*values)` — first truthy value, or `None`.

```bash
uv run pytest concepts/0_05
```

- Hint 1: `bool(x)` or `if x:`.
- Hint 2: walk the values; return the first one that is true in a boolean context.
- Solution: `solutions/truthy.py`.

## 7. Check

1. `if "0":` — enter the block or skip?
2. `if []:` — enter or skip?
3. `status = 0; message = status or "unknown"` — what is `message`?
4. When must you write `if value is None` instead of `if not value`?

**Real scenario:** a DocsDesk filter `if ticket["tags"]:` drops tickets whose tags are an empty list — sometimes that is correct, sometimes you needed `is not None`.

**What you learned:** `if items:` is idiomatic; it is not a Java boolean, and `0`/`""`/`[]` are false.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
