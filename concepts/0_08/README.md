# 0.8 `*args` / `**kwargs`   [NEW — no Java equivalent] [cost: mock] [~35 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_08/tests/test_skip.py` passes. **Still recommended.**

Related explainer: [notebook 01](../../notebooks/01_pythonic_essentials.ipynb).

## 1. Concept

A parameter named `*args` collects extra **positional** arguments into a tuple. `**kwargs` collects extra **keyword** arguments into a dict. At a call site, `*` unpacks a sequence into positional args and `**` unpacks a mapping into keywords.

## 2. Intuition

Imagine a function that can accept "the rest of the row" without declaring every column. `*args` is a box of leftover positional values. `**kwargs` is a box of leftover named values. Unpacking is the inverse: dump the box into a call.

```
join_fields("ERROR", "disk", "full", sep="|")
           \_____ positional ____/   \ keyword /
                 *fields               sep
```

## 3. Why it exists

Java `String... rest` covers leftover *positionals* of one type. It does not collect arbitrary named arguments, and you cannot unpack a `Map` into parameter names. Python libraries (pytest fixtures, Pydantic, HTTP clients, LLM SDKs) pass through `**kwargs` so wrappers stay thin. Without this, you would write a new overload every time a library adds an option.

### The Java analogy that misleads you

`String... args` looks like `*args`. It is only the positional half, and it is still a typed array. `**kwargs` has no Java counterpart. `Map<String,Object> options` is a *value* you pass as one argument — not extra parameters on the call.

## 4. Step-by-step examples

**Example 1 — collect positionals.** `def join_fields(*fields: str, sep: str = ",")` — `sep` must be passed by name because it follows `*fields`.

**Example 2 — collect keywords.** `def with_defaults(name: str, **options: object) -> dict` builds `{"name": name, **options}`.

**Example 3 — unpack a list into a call.** `greet(*["Ada", "Hi"])` is `greet("Ada", "Hi")`.

**Example 4 — unpack a dict.** `greet(**{"name": "Ada", "prefix": "Hi"})`.

**Example 5 — wrap a function.** `def apply_unpacked(fn, args, kwargs): return fn(*args, **kwargs)` is how decorators and test helpers forward arguments (see Module 0B).

```bash
uv run python concepts/0_08/examples.py
```

Docs: [function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions).

## 5. Common pitfalls

- `*args` is a tuple (immutable). Building a list? Use `list(args)`.
- A parameter after `*args` is keyword-only (`sep` above).
- `**kwargs` keys are strings. `fn(**{1: "x"})` is a `TypeError`.
- Mutating `kwargs` inside a wrapper can surprise the caller if you forgot to copy.
- Over-using `**kwargs` hides typos (`timout=5` silently stored instead of `timeout`).

## 6. Exercises

1. **Guided:** `join_fields(*fields, sep=",")`.
2. **Open:** `with_defaults` and `apply_unpacked`.

```bash
uv run pytest concepts/0_08
```

- Hint 1: `sep.join(fields)`.
- Hint 2: `{**{"name": name}, **options}` or assign then update. Call `fn(*args, **kwargs)`.
- Solution: `solutions/unpacking.py`.

## 7. Check

1. `def f(*args, extra):` — how must `extra` be passed?
2. `f(1, 2, 3)` with `def f(head, *rest)` — what is `rest`?
3. Does `**{"sep": "|"}` set a keyword named `sep`?
4. Why is `String...` not enough to model `**kwargs`?

**Real scenario:** DocsDesk forwards `timeout=` and `model=` into a client via `**options` without rewriting the wrapper each time.

**What you learned:** `* / **` collect at definition and unpack at the call; varargs is only half the story.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
