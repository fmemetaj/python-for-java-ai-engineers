# 1.3 Virtual environments (`.venv`)   [NEW — no Java equivalent] [cost: mock] [~25 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/1_03/tests/test_skip.py` passes. **Still recommended.**

Official docs: [venv](https://docs.python.org/3/library/venv.html), [uv python environments](https://docs.astral.sh/uv/pip/environments/).

## 1. Concept

A **virtual environment** is a per-project copy of a Python interpreter plus its own `site-packages` directory (libraries). DocsDesk's `.venv` can have `httpx` 0.28 while another repo on the same laptop has 0.27. The course always uses the `.venv` that `uv sync` creates at the repository root.

## 2. Intuition

Think of `.venv` as a **project-private JDK install**, not as a classpath entry. The binary lives at `.venv/bin/python` (macOS/Linux) or `.venv\Scripts\python.exe` (Windows). `uv run` launches that binary without you "activating" anything.

```
repo/
  pyproject.toml
  uv.lock
  .venv/                 # gitignored; created by uv sync
    bin/python           # or Scripts\python.exe
    lib/.../site-packages/httpx
  src/docsdesk/
```

## 3. Why it exists

Python packages install into *an interpreter*, not into a zip of jars you pass to one shared runtime. Two projects that both `pip install` into the same global Python will fight (dependency hell). A venv isolates installs so DocsDesk's `pydantic` 2.x cannot break a random system tool that still wants 1.x.

Java usually shares one JDK and isolates with **per-project classpaths** (Maven `target/`, Gradle configurations). That is the misleading analog: a classpath is a list of jars *for one JVM*. A venv is a whole interpreter tree. Mixing them in your head produces "I installed httpx, why can't Jupyter see it?" — you installed it into a different interpreter.

### The Java analogy that misleads you

`CLASSPATH` / Maven compile classpath is **not** a venv. Adding a jar to a module does not install a second `java` binary. `JAVA_HOME` per project (SDKMAN `.sdkmanrc`) is closer, but still shares a global Maven local repo (`~/.m2`). Python's `.venv` has its own copies of wheels. Do not "fix" `ModuleNotFoundError` by copying files into a global `site-packages`.

## 4. Step-by-step examples

**Example 1 — `.venv` is a directory.** After `uv sync --locked --group dev`, either `.venv/bin/python` or `.venv/Scripts/python.exe` exists. That file is the course interpreter.

**Example 2 — detecting the venv.** `sys.prefix != sys.base_prefix` means "this process is inside a virtual environment." Doctor uses the same idea.

**Example 3 — two projects, two httpx versions.** Project A syncs `httpx==0.27.2`. Project B syncs `0.28.1`. They cannot collide because each `.venv` has its own `site-packages`.

**Example 4 — `uv run` vs activate.** `uv run pytest` finds `.venv` from the project root. You do **not** need `source .venv/bin/activate`. Activation is optional sugar; it is also how people accidentally mix shells.

**Example 5 — Windows vs POSIX vs WSL.** Windows stores the interpreter in `Scripts\python.exe`. macOS/Linux use `bin/python`. A WSL shell cannot use a Windows `.venv` (and the reverse). Clone, sync, and run entirely on one side of the boundary.

```bash
uv run python concepts/1_03/examples.py
```

## 5. Common pitfalls

- Selecting the system interpreter in Cursor/VS Code (`Python: Select Interpreter` → `.venv`).
- Running `pip install httpx` with a global `python` (installs in the wrong place; the lockfile is ignored).
- Mixing WSL paths with a Windows venv.
- Committing `.venv/` (large, OS-specific, never portable).
- Creating a second venv inside `concepts/` by running `uv init` in a subdirectory.

## 6. Exercises

1. **Guided:** `venv_python(root, system)` returns the Windows or POSIX interpreter path; `in_virtualenv(prefix, base_prefix)` detects a venv.
2. **Open:** `diagnose_import_error(using_venv=...)` tells the learner either "you are not on `.venv`" or "run `uv sync --locked --group dev`".

```bash
uv run pytest concepts/1_03
```

- Hint 1: Windows → `.venv/Scripts/python.exe`; otherwise `.venv/bin/python`. Use `pathlib.Path`.
- Hint 2: `prefix != base_prefix` means in-venv. If not in a venv, say so; if in a venv but import failed, the package was never synced.
- Solution: `solutions/virtualenv.py`.

## 7. Check

1. Is `.venv` a classpath, or a second interpreter?
2. Why does `pip install` without uv make CI lie (green locally, red in GitHub)?
3. What breaks if you open the repo in WSL but the venv was created by Windows Python?
4. Should `.venv` be committed? Should `uv.lock`?

## Setup / troubleshooting

- **PATH:** after installing uv, restart the editor. GUI apps keep the old PATH.
- **Windows Store stub:** if `python` points at `WindowsApps`, doctor warns. Use `uv run python` or `py -3.12`.
- **macOS:** `python3` exists, `python` often does not. uv still installs its own CPython.
- **Activation not required:** prefer `uv run`. If you activate, deactivate before switching projects.
- More: [troubleshooting](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk's `httpx` import fails in a notebook because the kernel is `Python 3.12.8` (Homebrew) instead of `.venv`. Selecting the venv kernel fixes it; reinstalling httpx globally would not.

**What you learned:** a venv is a per-project interpreter, not a classpath. `uv run` is how you stay inside it.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
