# 0.1 Running Python   [Analog: javac + public static void main, JShell] [cost: mock] [~20 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_01/tests/test_skip.py` passes.

Related explainer: [notebook 00](../../notebooks/00_getting_started.ipynb).

## 1. Concept

Python is an interpreted language: you run a `.py` file (or type into a REPL) and the interpreter executes it immediately. There is no `javac` step that produces a class file before you can try the program. The process entry point is not a method named `main`; it is whichever module was launched, detectable with `if __name__ == "__main__":`.

## 2. Java version

```java
public class RunningPythonDemo {
    public static void main(String[] args) {
        System.out.println("DocsDesk ready");
    }
}
```

Compile, then run: `javac RunningPythonDemo.java && java RunningPythonDemo`. JShell is a separate REPL.

## 3. Python version

```python
def main() -> None:
    print("DocsDesk ready")


if __name__ == "__main__":
    main()
```

Run: `uv run python hello.py`. REPL: `uv run python` then type expressions. Same file imported as a module does **not** call `main()`.

| Java | Python |
| --- | --- |
| `javac` then `java` | `python file.py` (syntax errors appear at import/runtime) |
| `public static void main` | `if __name__ == "__main__":` |
| JShell | `python` REPL |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| "It compiled, so it will run" | Many errors are runtime (`NameError`, `TypeError`) | A typo in a rarely-taken branch is not caught until you hit it |
| Put startup code in `main` only | Top-level code runs on **import** | Importing a module starts a server or prints junk |
| `java com.acme.App` | `python path/to/app.py` or `python -m package` | Wrong working directory → files not found |
| One `PATH` to a JDK | Project interpreter is `.venv` via `uv` | Editor uses system Python; `pydantic` is "missing" |

## 5. Exercise

Fill `exercises/skip.py` (2-minute check) and `exercises/entry.py`.

```bash
uv run pytest concepts/0_01
```

- Hint 1: `__name__` is `"__main__"` only for the launched file.
- Hint 2: compare `module_name` to the string `"__main__"`.
- Solution: `solutions/entry.py` (try the hints first).

## 6. Check

1. You import `log_stats.py`. Does its `if __name__ == "__main__":` block run?
2. You have a syntax error on line 80 of a 100-line file. When do you find out — at start, or when that line executes?
3. Why is `uv run python script.py` safer than a global `python` on PATH?
4. Predict: `python -c "import hello"` vs `python hello.py` for a file that prints at top level and again under the main guard.

## Setup / troubleshooting (Windows, macOS, Linux)

- **PATH:** install [uv](https://docs.astral.sh/uv/getting-started/installation/), restart the terminal **and** the editor. Prefer `uv run python` over a system `python`.
- **`python` not found:** macOS/Linux use `python3` or `uv run python`. Windows: `py -3.12`, not the Microsoft Store stub (`WindowsApps` in the path).
- **venv:** `uv sync --locked --group dev` creates `.venv`. Select that interpreter in Cursor/VS Code.
- **Encoding:** open text files with `encoding="utf-8"`. Windows Notepad defaults can still be ANSI; this repo is UTF-8.
- **Line endings:** this repo sets `eol=lf` in `.gitattributes`. If a shebang script fails on Linux after a Windows edit, check CRLF (`git add --renormalize .`).
- More: [docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk's CLI must print a banner only when launched, not when tests import the module.

**What you learned:** Python has no compile gate; guard startup with `if __name__ == "__main__":`.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
