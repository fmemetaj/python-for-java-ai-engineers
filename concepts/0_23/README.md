# 0.23 Type hints vs generics   [Analog: generics, javac type checking] [cost: mock] [~40 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_23/tests/test_skip.py` passes.

Related explainer: [notebook 02](../../notebooks/02_typing_pydantic.ipynb).

## 1. Concept

`list[int]`, `TypeVar`, and `def first(items: list[T]) -> T` are **type hints**: they document shapes for humans, pyright, and IDEs. The interpreter does **not** enforce them. That is the opposite of `List<Integer>` under javac. Use Pydantic (0.19) when untrusted data must be rejected at runtime.

## 2. Java version

```java
import java.util.List;

public class TypeHintsDemo {
    static int first(List<Integer> items) {
        return items.get(0);
    }
    public static void main(String[] args) {
        System.out.println(first(List.of(1, 2, 3)));
    }
}
```

`first(List.of("x"))` does not compile.

## 3. Python version

```python
def as_ints(values: list[str]) -> list[int]:
    return [int(value) for value in values]


T = TypeVar("T")


def first(items: list[T]) -> T:
    if not items:
        raise ValueError("empty")
    return items[0]
```

`first([1, "x"])` runs. pyright reports a list-item error. `as_ints(["x"])` raises `ValueError` because `int("x")` fails — that is runtime logic, not the type system.

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| "It compiled, so the list is Integer" | Hints are erased | A `list[int]` that actually holds strings |
| Generics on the class | `list[int]` is a hint; `list` is the type | `isinstance(x, list[int])` is wrong on older mental models — check `list` then contents |
| Bean Validation ≈ hints | Hints ≠ validation | Skipping Pydantic because "we have types" |
| IDE is optional | pyright in CI is the javac stand-in | Green pytest, red pyright (or the reverse) |

## 5. Exercise

Implement `as_ints` and `first` in `exercises/hints.py`.

```bash
uv run pytest concepts/0_23
```

- Hint 1: `[int(value) for value in values]`.
- Hint 2: raise `ValueError` when `items` is empty (truthiness, 0.5).
- Solution: `solutions/hints.py`.

## 6. Check

1. Does `def f(x: int) -> None` prevent `f("a")` at runtime?
2. What tool is the closest thing to javac here?
3. Why did `double("ab")` in `examples.py` return `"abab"`?
4. Where do you still want Pydantic?

## Setup / troubleshooting

- `uv run pyright` uses `[tool.pyright]` in `pyproject.toml` (`pythonVersion = 3.11`).
- Cursor/VS Code: Python: Select Interpreter → `.venv`, or the editor's pyright disagrees with CI.
- Windows/macOS/Linux: no platform difference for hints; PATH still matters for which Python pyright sees.

Docs: [typing](https://docs.python.org/3/library/typing.html).

**Real scenario:** DocsDesk helpers are typed for pyright; ticket JSON still goes through Pydantic.

**What you learned:** hints are static; they are not javac and not Bean Validation.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
