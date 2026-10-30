# 1.1 uv   [Analog: Maven/Gradle + SDKMAN] [cost: mock] [~40 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/1_01/tests/test_skip.py` passes.

Related explainer: [guide 05](../../guides/05_uv_and_debugging.md). Official docs: [astral.sh/uv](https://docs.astral.sh/uv/).

## 1. Concept

**uv** is one CLI that installs a Python interpreter, creates the project environment, resolves dependencies from `pyproject.toml`, freezes them in `uv.lock`, and runs tools inside that environment. Java developers usually split this across SDKMAN (or a company JDK image) plus Maven/Gradle.

## 2. Java version

```java
public class UvDemo {
    public static void main(String[] args) {
        System.out.println(System.getProperty("java.home"));
        System.out.println("mvn -q test");
    }
}
```

`java.home` is whichever JDK `JAVA_HOME`/`PATH` pointed at. `mvn test` uses that JDK plus the project classpath.

## 3. Python version

```text
uv python install 3.12          # SDKMAN analog: pick an interpreter
uv sync --locked --group dev    # mvn dependency:resolve + surefire classpath
uv run pytest                   # mvn -q test, using .venv
uv run python -m docsdesk       # java -jar, but no separate package step
```

| Java | Python |
| --- | --- |
| SDKMAN / company JDK | `uv python install` |
| `mvn test` / `./gradlew test` | `uv run pytest` |
| Maven Wrapper `mvnw` | committed `uv.lock` + `uv sync --locked` |
| `JAVA_HOME` | `.venv` selected by `uv run` |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| One JDK on `PATH` for every repo | Each project has its own `.venv` | Editor uses system Python; `httpx` is "missing" |
| `mvn` uses the POM in the current module | `uv` uses the `pyproject.toml` at the **repo root** | Running uv from `concepts/` creates a nested project |
| Wrapper scripts (`mvnw`) | `uv run` prefixes every tool | Calling bare `pytest` hits a different install |
| `mvn -U` to refresh snapshots | `uv sync --locked` refuses a stale lock | Changing `pyproject.toml` without `uv lock` fails CI |

## 5. Exercise

Fill `exercises/skip.py` and `exercises/uv_commands.py` — map Maven-like jobs onto uv commands.

```bash
uv run pytest concepts/1_01
```

- Hint 1: interpreter install is `uv python install`; locked deps are `uv sync --locked`.
- Hint 2: tests and scripts go through `uv run` so they see `.venv`.
- Solution: `solutions/uv_commands.py` (try the hints first).

## 6. Check

1. Why is `uv run python scripts/doctor.py` safer than `python scripts/doctor.py`?
2. What Maven command is closest to `uv sync --locked`?
3. You changed `pyproject.toml` and CI says the lockfile is outdated. What two files do you commit?
4. Predict: `uv run pytest` from a subdirectory vs from the repo root.

## Setup / troubleshooting (Windows, macOS, Linux)

- **Install:** [uv installation](https://docs.astral.sh/uv/getting-started/installation/). Restart the terminal **and** the editor so PATH updates.
- **Windows:** PowerShell installer; uv lands in `%USERPROFILE%\.local\bin`. Do not use the Microsoft Store `python` stub.
- **macOS/Linux:** `curl -LsSf https://astral.sh/uv/install.sh | sh`, then `source ~/.local/bin/env`.
- **Apple Silicon:** arm64 uv/Python. "Bad CPU type" means a Rosetta binary.
- **WSL:** install uv *inside* Linux. A Windows uv cannot manage a Linux `.venv`.
- **Proxy/SSL:** `HTTPS_PROXY`, `SSL_CERT_FILE`. Doctor: `uv run python scripts/doctor.py --offline`.
- More: [docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** a teammate clones DocsDesk, runs `python -m docsdesk`, and gets `ModuleNotFoundError: httpx` because they used system Python instead of `uv run`.

**What you learned:** uv is the JDK manager and the build tool; `uv run` is how you stay on the project interpreter.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
