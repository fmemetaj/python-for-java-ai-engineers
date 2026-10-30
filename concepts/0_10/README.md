# 0.10 First-class functions and lambdas   [Analog: functional interfaces, lambdas, method refs] [cost: mock] [~25 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_10/tests/test_skip.py` passes.

## 1. Concept

Functions are values. You can pass them, return them, and store them in lists. `lambda` builds a **single-expression** anonymous function. Anything that needs statements (loops, more than one line) should be a `def`.

## 2. Java version

```java
import java.util.List;

public class FirstClassDemo {
    public static void main(String[] args) {
        List<String> words = List.of("login", "api");
        var sorted = words.stream()
            .sorted((a, b) -> Integer.compare(a.length(), b.length()))
            .toList();
        System.out.println(sorted);
    }
}
```

`Comparator`, `Function<T,R>`, method references (`String::length`).

## 3. Python version

```python
words = ["login", "api"]
sorted(words, key=lambda word: len(word))
# or: sorted(words, key=len)
```

| Java | Python |
| --- | --- |
| `(a, b) -> …` | `lambda a, b: …` (one expression) |
| `String::length` | `str.lower` / `len` as a function value |
| `Function<T,R>` | any callable (`def`, `lambda`, object with `__call__`) |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Multi-line lambda | `lambda` is one expression | People stuff `and`/`or` into lambdas; write a `def` |
| Checked functional interface | Any callable | `key=words.sort` passes the bound method — usually you wanted `key=len` |
| Method ref on instance | `ticket.id` is a value; `Ticket.id` is a function if it is a method | Passing a *result* instead of a *function* |
| Captured effectively-final locals | Closure cells (0.9) | Late-binding in `lambdas` inside a loop: all see the last `i` |

## 5. Exercise

`apply_each`, `sort_by_length`, `make_adder` in `exercises/first_class.py`.

```bash
uv run pytest concepts/0_10
```

- Hint 1: `return [fn(value) for value in values]` or a loop.
- Hint 2: `sorted(words, key=len)` or a lambda. `make_adder` returns `lambda x: x + n`.
- Solution: `solutions/first_class.py`.

## 6. Check

1. Can `lambda` contain a `for` loop?
2. `sorted(words, key=len)` — why not `key=len()`?
3. What does `make_adder(2)(5)` return?
4. In `[lambda: i for i in range(3)]`, why do all three lambdas often return `2`?

**Real scenario:** DocsDesk sorts retrieved chunks with `key=lambda c: c.score` and maps them with `apply_each`.

**What you learned:** functions are values; Python lambdas are smaller than Java lambdas.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
