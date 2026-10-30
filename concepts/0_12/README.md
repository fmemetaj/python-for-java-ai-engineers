# 0.12 Slicing and unpacking   [NEW — no Java equivalent] [cost: mock] [~25 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_12/tests/test_skip.py` passes. **Still recommended.**

Related explainer: [notebook 01](../../notebooks/01_pythonic_essentials.ipynb).

## 1. Concept

A **slice** `seq[start:stop:step]` returns a new sequence of a half-open range. **Unpacking** writes `head, *rest = seq` (or `a, b = pair`) to bind several names at once. Slices **copy** a list; they do not view it.

## 2. Intuition

Think of a slice as "give me a window, as a new list." Indexes work like `range`: start inclusive, stop exclusive. Negative indexes count from the end (`-1` is last). Extended unpacking is "peel the first/last items and keep the middle as a list."

```
values = [10, 20, 30, 40]
values[1:3]      → [20, 30]     # copy
values[-2:]      → [30, 40]
values[::2]      → [10, 30]
head, *rest = values            # 10, [20, 30, 40]
```

## 3. Why it exists

Java has `list.subList(from, to)` (a **view** — writes write through) and no first-class `a, *rest =`. You write `get(0)` plus `subList(1, size())`. Python's slice-and-unpack is how people split headers from payloads, take the last N log lines, and swap variables (`a, b = b, a`).

## 4. Step-by-step examples

**Example 1 — half-open.** `items[0:2]` is two elements, not three.

**Example 2 — copy.** `copy = items[:]`; `copy.append(1)` leaves `items` alone. Contrast `alias = items`.

**Example 3 — step.** `items[::2]` every other; `items[::-1]` reversed copy.

**Example 4 — unpack a pair.** `level, count = ("ERROR", 3)`. Too many/few values → `ValueError`.

**Example 5 — starred unpack.** `head, *rest = lines` or `*body, last = lines`. `rest` is always a list.

```bash
uv run python concepts/0_12/examples.py
```

Docs: [common sequence operations](https://docs.python.org/3/library/stdtypes.html#common-sequence-operations).

## 5. Common pitfalls

- Slices of a **list** copy; slices of some libraries (NumPy) are views. Here we only use lists/tuples/str.
- `items[1:1]` is empty, not `items[1]`.
- `subList` in Java shares mutation; `items[1:3]` does not.
- Unpacking a generator consumes it (see 0.14).

## 6. Exercises

1. **Guided:** `tail(seq, n)` and `every_other(seq)`.
2. **Open:** `split_head(seq)` → `(head, rest)` using unpacking.

```bash
uv run pytest concepts/0_12
```

- Hint 1: `seq[-n:]` if `n` else `[]`; `seq[::2]`.
- Hint 2: `head, *rest = seq`.
- Solution: `solutions/slicing.py`.

## 7. Check

1. Does `items[1:3]` include index 3?
2. After `b = a[:]`, does `b.append(1)` change `a`?
3. `head, *rest = [1]` — what is `rest`?
4. How do you reverse a list without `reverse()`?

**Real scenario:** DocsDesk keeps the last 50 log lines with `lines[-50:]` and splits `level, *words = line.split()`.

**What you learned:** slices copy and exclude the end index; `*rest` always binds a list.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
