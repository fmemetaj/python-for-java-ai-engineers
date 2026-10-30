# 1.2 pyproject.toml, groups, lockfile   [Analog: pom.xml / build.gradle, scopes, lockfiles] [cost: mock] [~25 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/1_02/tests/test_skip.py` passes.

Official docs: [pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/), [uv lockfiles](https://docs.astral.sh/uv/concepts/projects/layout/).

## 1. Concept

`pyproject.toml` is the project file: Python version, runtime dependencies, optional groups, scripts. **Ranges** live there (`httpx>=0.27,<1`). `uv.lock` is the committed freeze of exact versions, like a Gradle lockfile or a checked-in `pom.xml` with `<version>` pins plus a dependency tree.

## 2. Java version

```java
public class PyprojectDemo {
    public static void main(String[] args) {
        System.out.println("pom.xml compile scope -> project.dependencies");
        System.out.println("pom.xml test scope -> dependency-groups.dev");
    }
}
```

Maven `<scope>test</scope>` does not ship in the jar. Python **dependency groups** (`dev`, `demo`) are the same idea: installed on demand, not part of the default runtime.

## 3. Python version

```toml
[project]
requires-python = ">=3.11"
dependencies = ["httpx>=0.27,<1"]

[dependency-groups]
dev = ["pytest>=8.3,<10", "ruff>=0.9,<1"]
demo = ["gradio>=5.0,<7"]
```

`uv sync --locked --group dev` installs runtime + `dev`. Omit `--group demo` and Gradio stays out — CI has a job that proves that path still tests.

| Java | Python |
| --- | --- |
| `pom.xml` coordinates + ranges | `[project] dependencies` |
| `<scope>test</scope>` | `[dependency-groups] dev` |
| Gradle lock / Dependabot PRs | committed `uv.lock` |
| `mvn -q` uses the POM you just edited | `uv sync --locked` **fails** if the lock is stale |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| SNAPSHOT versions refresh | Lockfile is exact; CI uses `--locked` | Editing pyproject without `uv lock` breaks the pipeline |
| `provided` scope | No perfect analog; extras/groups instead | Putting pytest in `dependencies` bloats learner installs |
| One `pom.xml` per module | This course has **one** project at the repo root | Nested `uv init` in `concepts/` forks the lock |
| Checking in `target/` | Checking in `.venv/` | Lock yes, venv no (`.gitignore`) |

## 5. Exercise

Convert Maven-like coordinates into a PEP 508 line, map scopes to groups, and diagnose a stale-lock error.

```bash
uv run pytest concepts/1_02
```

- Hint 1: `httpx>=0.27,<1` is name + lower bound + exclusive upper bound.
- Hint 2: Maven `test` → group `dev`; `compile` → `project`.
- Solution: `solutions/pyproject.py`.

## 6. Check

1. Where do version *ranges* live? Where do *exact* versions live?
2. Why does CI run `uv sync --locked` instead of unlocked `uv sync`?
3. Should `uv.lock` be gitignored like `node_modules`? Why not?
4. You added `httpx` to pyproject and forgot `uv lock`. What happens in CI?

## Setup / troubleshooting

- **Stale lock:** `uv lock` then commit **both** `pyproject.toml` and `uv.lock`.
- **Windows line endings:** this repo uses `eol=lf`. A lockfile with CRLF can produce noisy diffs; `git add --renormalize .`.
- **Corporate index:** configure uv via env/config — never put index credentials in `pyproject.toml`.
- More: [troubleshooting](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk adds `httpx`. A PR updates only `pyproject.toml`. Ubuntu CI fails with "lockfile is out of date" while the author's machine still works because they ran unlocked `uv sync`.

**What you learned:** ranges in pyproject, pins in the committed lock, groups instead of Maven scopes.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
