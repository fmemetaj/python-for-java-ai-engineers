# 0.18 Dunder methods / data model   [NEW — no Java equivalent] [cost: mock] [~40 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_18/tests/test_skip.py` passes. **Still recommended.**

Related explainer: [notebook 02](../../notebooks/02_typing_pydantic.ipynb).

## 1. Concept

**Dunder** (double-underscore) methods hook your class into Python syntax: `==`, `repr()`, `len()`, `for`, `+`. They are the language's data model, not optional sugar.

## 2. Intuition

Built-in operations are messages sent to the object. `money == other` becomes `money.__eq__(other)`. `len(batch)` becomes `batch.__len__()`. `cents, currency = money` iterates `__iter__`. You do not call these names in application code; you implement them so the syntax works.

```
obj == other     →  obj.__eq__(other)
repr(obj)        →  obj.__repr__()
len(obj)         →  obj.__len__()
a + b            →  a.__add__(b)
for x in obj     →  obj.__iter__()
```

## 3. Why it exists

Java puts this behaviour on a handful of methods (`equals`, `hashCode`, `toString`) plus interfaces (`Comparable`, `Iterable`). Python uses one consistent protocol for *every* operator. That is how `dict` keys, `if batch:`, and `money + money` stay uniform.

### The Java analogy that misleads you

`toString` / `equals` / `hashCode` cover **three** dunders (`__str__`/`__repr__`, `__eq__`, `__hash__`). They do **not** cover `+`, `len`, iteration, context managers, or `[]`. Implementing `equals` in Java does not make `a + b` compile. Implementing `__eq__` in Python still leaves `__hash__` as `None` if you are not careful with mutability — another trap.

## 4. Step-by-step examples

**Example 1 — default `==` is identity.** Two `Ticket(1, "A")` objects are not `==` until you write `__eq__`.

**Example 2 — `__repr__` for logs.** `Money(199, "USD")` should print as `Money(199, 'USD')`, a copy-pasteable debug form. Use `!r` in the f-string.

**Example 3 — `__eq__` returns `NotImplemented` for other types** so Python can try the right-hand side, instead of raising.

**Example 4 — `__iter__` makes unpacking work.** `cents, currency = money`.

**Example 5 — `__add__` is an operator protocol.** Different currencies raise `ValueError`. `__bool__` / `__len__` make `if batch:` follow truthiness (0.5).

```bash
uv run python concepts/0_18/examples.py
```

Docs: [data model](https://docs.python.org/3/reference/datamodel.html).

## 5. Common pitfalls

- Implementing `__eq__` on a mutable object used as a dict key without `__hash__`.
- `__str__` vs `__repr__`: logs and pytest diffs use `repr`.
- Returning `False` from `__eq__` for unknown types instead of `NotImplemented`.
- Forgetting `__len__` and writing `if batch.lines:` when you wanted `if batch:`.
- Encoding: `repr` of a UTF-8 string is fine; printing to a Windows console still needs `PYTHONUTF8=1` (CI sets this).

## 6. Exercises

1. **Guided:** `Money` with `__repr__`, `__eq__`, `__iter__`, `__add__`.
2. **Open:** `LineBatch` with `__len__` and `__bool__` (empty is false).

```bash
uv run pytest concepts/0_18
```

- Hint 1: `return f"Money({self.cents!r}, {self.currency!r})"`.
- Hint 2: `if not isinstance(other, Money): return NotImplemented`.
- Solution: `solutions/dunder.py`.

## 7. Check

1. Without `__eq__`, is `Money(1) == Money(1)` true?
2. What should `__eq__` return for a `str` other?
3. Why implement `__repr__` before `__str__`?
4. Does `__add__` mutate `self` or return a new `Money`?

**Real scenario:** DocsDesk `Money` for token-cost math — `__eq__` / `__repr__` / `__add__` instead of a pile of `getCents()` helpers.

**What you learned:** operators are methods with reserved names; `equals`/`toString` is only a slice of the data model.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
