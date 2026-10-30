# 0.7 Functions   [Analog: methods, overloading, builders] [cost: mock] [~35 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_07/tests/test_skip.py` passes.

Related explainer: [notebook 01](../../notebooks/01_pythonic_essentials.ipynb).

## 1. Concept

`def` defines a function. Parameters can have defaults. Callers may pass arguments by position or by name (`name="DocsDesk"`). There is no method overloading; one function plus defaults (or `*args` in 0.8) replaces most overloads. **Default argument values are evaluated once, at definition time** — a mutable default is a shared object.

## 2. Java version

```java
public class FunctionsDemo {
    static String greet(String name, String prefix) {
        return prefix + ", " + name;
    }
    static String greet(String name) {
        return greet(name, "Hello");
    }
    public static void main(String[] args) {
        System.out.println(greet("Ada"));
        System.out.println(greet("Ada", "Hi"));
    }
}
```

Overloads + a builder for optional fields. Java evaluates argument expressions at each call.

## 3. Python version

```python
def greet(name: str, prefix: str = "Hello") -> str:
    return f"{prefix}, {name}"


greet("Ada")
greet("Ada", prefix="Hi")
```

Broken default (do not do this):

```python
def add_tag(tag: str, tags: list[str] = []) -> list[str]:  # shared list
    tags.append(tag)
    return tags
```

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Overload `greet(String)` / `greet(String, String)` | One `def` with defaults | Two `def greet` — the second **replaces** the first |
| Builder for optional args | Keyword arguments | Positional after a keyword: `SyntaxError` |
| New list every call | Default `[]` is created **once** | `add_tag("a"); add_tag("b")` → `["a", "b"]` |
| `void` vs return | Missing `return` yields `None` | `x = do_stuff()` is silently `None` |

**Acceptance for this module:** you can explain why `def f(x=[])` is a bug.

## 5. Exercise

Implement `greet` and `add_tag` in `exercises/functions.py`. `add_tag` must **not** leak state across calls.

```bash
uv run pytest concepts/0_07
```

- Hint 1: default `tags` to `None`, then assign a new list inside the function.
- Hint 2: `tags = [] if tags is None else tags`, then append on a copy or the provided list as specified in the docstring.
- Solution: `solutions/functions.py`.

## 6. Check

1. Two `def greet` in one file — which one runs?
2. `def f(x=[]): x.append(1); return x` — second call returns?
3. `greet(prefix="Hi", name="Ada")` — valid?
4. What does a function return if it has no `return`?

**Real scenario:** a DocsDesk helper `def parse(line, acc=[])` silently aggregates every test case into one list.

**What you learned:** keyword args replace most overloads; never default a parameter to `[]` or `{}`.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
