# 0.6 Control flow   [Analog: if, enhanced for, while, switch patterns] [cost: mock] [~30 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_06/tests/test_skip.py` passes.

## 1. Concept

Python branches with `if` / `elif` / `else`, loops with `for item in iterable` and `while`, and structural pattern matching with `match` (3.10+). There is no C-style `for (int i = 0; i < n; i++)`. Use `range`. A `for` can have `else`, which runs when the loop did **not** `break`.

## 2. Java version

```java
public class ControlFlowDemo {
    static String label(int status) {
        return switch (status) {
            case 200 -> "ok";
            case 400, 404 -> "client";
            case 500 -> "server";
            default -> "other";
        };
    }
    public static void main(String[] args) {
        int sum = 0;
        for (int i = 1; i <= 3; i++) sum += i;
        System.out.println(label(404) + " " + sum);
    }
}
```

## 3. Python version

```python
def label(status: int) -> str:
    match status:
        case 200:
            return "ok"
        case 400 | 404:
            return "client"
        case 500:
            return "server"
        case _:
            return "other"


total = 0
for i in range(1, 4):
    total += i
```

`if` / `elif` is the everyday form. `match` is the `switch`-like form (PEP 634).

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| `for (i=0; i<n; i++)` | `for i in range(n):` | `range(1, n)` excludes `n` |
| Enhanced `for (T x : xs)` | `for x in xs:` | Iterating a dict yields **keys**, not pairs |
| `switch` on ints / patterns | `match` / `case` | `case 400 | 404` is OR, not bitwise intent |
| No `for/else` | `else` on `for`/`while` runs if no `break` | People read it as "loop failed" — it means "completed" |
| Braces required | Indentation is syntax | Mixing tabs/spaces; copy-paste from Slack |

## 5. Exercise

`exercises/flow.py`: `label_status`, `sum_to`, `first_error` (use `for`/`else` or an equivalent).

```bash
uv run pytest concepts/0_06
```

- Hint 1: `range(1, n + 1)` includes `n`.
- Hint 2: `for level in levels: ... else: return None`.
- Solution: `solutions/flow.py`.

## 6. Check

1. What does `list(range(3))` produce?
2. When does `for ... else` run the `else`?
3. `for key in {"a": 1, "b": 2}:` — what is `key`?
4. Is `elif` required, or could you stack `if`/`if`?

**Real scenario:** walk DocsDesk log levels until the first `ERROR`; if none, return `None` (the `for`/`else` case).

**What you learned:** no C-style `for`; `range` is half-open; `match` is the switch analog.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
