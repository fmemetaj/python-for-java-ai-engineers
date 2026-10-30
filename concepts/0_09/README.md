# 0.9 Scope (LEGB), closures, `nonlocal`   [NEW — no Java equivalent] [cost: mock] [~25 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_09/tests/test_skip.py` passes. **Still recommended.**

## 1. Concept

Python looks up a name in four scopes, in order: **L**ocal, **E**nclosing, **G**lobal, **B**uilt-in (LEGB). There is **no block scope**: a name assigned anywhere in a function is local to the whole function. A nested function that reads an enclosing name is a **closure**. To *rebind* an enclosing name, declare `nonlocal`; to rebind a module name, declare `global`.

## 2. Intuition

Java's `{ }` blocks can hide a local. Python's `if` / `for` / `while` do **not** create a scope. Only `def`, `(lambda)`, comprehensions (their own local), and (in a limited way) `class` bodies do.

A closure is a function that carries its enclosing variables with it — like an anonymous class that captured `final` locals, except the captured name is a cell you can rebind with `nonlocal`.

```
def make_counter(start):        # enclosing
    n = start
    def inc():                  # local
        nonlocal n
        n += 1
        return n
    return inc
```

## 3. Why it exists

Java has method scope, block scope, and captured *effectively final* locals. It has no `nonlocal` because you cannot reassign a captured local; you mutate a one-element array or a field instead. Python chose function-level scope and explicit `nonlocal` / `global` so assignment is unambiguous: `n = 1` inside `inc` would otherwise create a new local and the counter would not move.

## 4. Step-by-step examples

**Example 1 — no block scope.** `if True: value = 1` then `value` is visible after the `if` in the same function.

**Example 2 — LEGB.** `len` resolves to the built-in unless you bind a local named `len`.

**Example 3 — closure read.** `def make_prefix(p): return lambda name: f"{p}:{name}"`.

**Example 4 — `nonlocal` rebind.** `make_counter` above. Without `nonlocal`, `n += 1` is `UnboundLocalError`.

**Example 5 — `global` is rare.** Prefer returning a value over writing a module global.

```bash
uv run python concepts/0_09/examples.py
```

Docs: [naming and binding](https://docs.python.org/3/reference/executionmodel.html#naming-and-binding).

## 5. Common pitfalls

- Treating `for i in items:` as if `i` disappeared after the loop. It remains.
- Assigning to a name anywhere in a function makes it local for the **whole** function, including lines before the assignment (`UnboundLocalError`).
- Forgetting `nonlocal` when you meant to update the enclosing counter.
- Using `global` for configuration — use a function argument or a settings object instead (Module 1).

## 6. Exercises

1. **Guided:** `make_counter(start)` returns a zero-arg function that increments and returns the count.
2. **Open:** `visible_after_if(flag)` shows that `if` does not create a scope.

```bash
uv run pytest concepts/0_09
```

- Hint 1: store `n` in the enclosing function; `nonlocal n` before `n += 1`.
- Hint 2: assign inside `if`/`else` and return the name afterwards.
- Solution: `solutions/scope.py`.

## 7. Check

1. After `for i in range(3): pass`, is `i` defined?
2. Why does `n += 1` inside a nested function raise `UnboundLocalError` without `nonlocal`?
3. Does `if True: x = 1` hide `x` from the rest of the function?
4. What does LEGB stand for?

**Real scenario:** a DocsDesk retry wrapper closes over `attempts` and increments it with `nonlocal`.

**What you learned:** no block scope; closures need `nonlocal` to rebind.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
