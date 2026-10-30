# 0.24 Exceptions   [Analog: exceptions, try/catch/finally] [cost: mock] [~35 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_24/tests/test_skip.py` passes.

Related explainer: [notebook 04](../../notebooks/04_production_python.ipynb).

## 1. Concept

Python uses `try` / `except` / `else` / `finally` and `raise`. There are **no checked exceptions**. Idiom is often **EAFP** ("easier to ask forgiveness than permission"): try the operation, catch the specific error. Chain causes with `raise NewError("…") from exc` (Java's `getCause()`).

## 2. Java version

```java
public class ExceptionsDemo {
    static int parse(String raw) {
        try {
            return Integer.parseInt(raw);
        } catch (NumberFormatException ex) {
            throw new IllegalArgumentException("bad status", ex);
        }
    }
    public static void main(String[] args) {
        System.out.println(parse("200"));
    }
}
```

Checked exceptions force `throws` on the method signature.

## 3. Python version

```python
class ParseError(Exception):
    pass


def parse_level(line: str) -> str:
    text = line.strip()
    if not text:
        raise ParseError("empty line")
    return text.split()[0]


def wrap_parse(line: str) -> str:
    try:
        return parse_level(line)
    except ParseError as exc:
        raise ValueError("bad log") from exc
```

`except ParseError` does not catch `ValueError`. Bare `except:` is a bug.

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| `throws IOException` | Nothing is declared | Callers discover errors from docs and tests |
| `catch (Exception e)` | Same smell | Swallows `KeyboardInterrupt` if you use bare `except:` |
| `throw new E(msg, cause)` | `raise E(msg) from exc` | Forgetting `from` loses the traceback |
| LBYL (`if file.exists()`) | EAFP (`try: open(...)`) | TOCTOU races; in Python, missing keys use `except KeyError` |
| `finally` for close | Also `with` (0.25) | Double-closing or leaking files on Windows |

## 5. Exercise

Implement `parse_level`, `parse_level_or_default`, and `wrap_parse` in `exercises/exceptions.py`.

```bash
uv run pytest concepts/0_24
```

- Hint 1: blank after `strip()` → `raise ParseError`.
- Hint 2: `raise ValueError("bad log") from exc`.
- Solution: `solutions/exceptions.py`.

## 6. Check

1. Does `def f():` need `throws ParseError`?
2. `except Exception` — does it catch `ParseError`? (`ParseError` subclasses `Exception`.)
3. What is `__cause__` after `raise ValueError() from parse_error`?
4. Why is `except:` (no type) worse than Java's `catch (Exception e)`?

## Setup / troubleshooting

- Tracebacks on Windows can look garbled without UTF-8. This repo sets `PYTHONUTF8=1` in CI; locally `chcp 65001` or set the env var.
- Open files with `encoding="utf-8"` so `UnicodeDecodeError` is the exception you expect, not a mystery.

Docs: [errors tutorial](https://docs.python.org/3/tutorial/errors.html).

**Real scenario:** DocsDesk parser raises `ParseError` for a bad log line and wraps it when the CLI must return a `ValueError` to the caller.

**What you learned:** no checked exceptions; chain with `from`; catch the narrow type.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
