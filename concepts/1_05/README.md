# 1.5 ruff and pyright   [Analog: Checkstyle/Spotless, javac] [cost: mock] [~20 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/1_05/tests/test_skip.py` passes.

Official docs: [ruff](https://docs.astral.sh/ruff/), [pyright](https://github.com/microsoft/pyright).

## 1. Concept

**ruff** lints and formats (Checkstyle + Spotless in one fast tool). **pyright** type-checks hints (the closest thing to `javac`'s type errors). Neither is the interpreter: a file can be ruff-clean, pyright-clean, and still raise `TypeError` at runtime if you skip Pydantic at a boundary.

## 2. Java version

```java
public class LintDemo {
    public static void main(String[] args) {
        String title = "Tickets API";
        System.out.println(title.length());
    }
}
```

`javac` rejects `String title = 3;`. Checkstyle comments on unused imports. Spotless rewrites formatting.

## 3. Python version

```bash
uv run ruff check src tests scripts examples concepts placement fundamentals
uv run ruff format --check src tests scripts examples concepts placement fundamentals
uv run pyright
```

| Java | Python |
| --- | --- |
| Checkstyle | `ruff check` |
| Spotless / google-java-format | `ruff format` |
| `javac` type errors | `pyright` (editor + CI) |
| Error Prone at compile | not equivalent — runtime remains dynamic |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| "It compiled, types are fine" | pyright is optional unless CI runs it | Shipping `str` where `int` was hinted |
| Checkstyle on `src/main/java` only | ruff must include `concepts/` and `src/` | Lesson files drift from the style the course teaches |
| Format in the IDE, maybe | `ruff format --check` in CI | CRLF / quote style bikeshedding on Windows |
| Generics erased but still compile-checked | hints are **not** runtime | See 0.23; Pydantic is the boundary |

## 5. Exercise

Route each issue to `ruff` or `pyright`, and state that pyright is **not** runtime enforcement.

```bash
uv run pytest concepts/1_05
```

- Hint 1: unused import and line length are ruff; a `str` passed where `int` was hinted is pyright.
- Hint 2: the interpreter still accepts `count: int = "1"`.
- Solution: `solutions/lint.py`.

## 6. Check

1. Which tool would flag an unused `import os`?
2. Which tool would flag `def f(x: int) -> None` called as `f("1")`?
3. Does fixing pyright errors stop `TypeError` in production?
4. Why does this course run both in CI on 3.11–3.13?

## Setup / troubleshooting

- **Editor:** `.vscode/settings.json` already points at `.venv` and ruff. Install the Ruff extension.
- **pyright missing `gradio`:** install `--group demo` or ignore `examples/gradio_app.py` locally; CI installs demo.
- **Windows:** ruff handles UTF-8; keep files LF (`core.autocrlf` / `.gitattributes`).
- More: [troubleshooting](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk adds a helper with an unused import. ruff fails CI before a type error ever would. pyright then catches a `None` passed to `DocPage.slug`.

**What you learned:** ruff is style/hygiene; pyright is static types; the interpreter still does not care until Pydantic (or a crash) does.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
