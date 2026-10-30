# 1.4 src layout, packaging, entry points   [Analog: Maven layout, jar, Main-Class] [cost: mock] [~20 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/1_04/tests/test_skip.py` passes.

Official docs: [src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/), [hatch build](https://hatch.pypa.io/latest/).

## 1. Concept

DocsDesk lives under `src/docsdesk/`. Tests and `concepts/` import the **installed** package (editable, via uv), not a random folder on `sys.path`. Console scripts (`course = "course_kit.cli:main"`) are the `Main-Class` analog: a named callable, not a class file.

## 2. Java version

```java
public class SrcLayoutDemo {
    public static void main(String[] args) {
        System.out.println("src/main/java/com/acme/App.java");
        System.out.println("Main-Class: com.acme.App");
    }
}
```

Maven compiles `src/main/java` into `target/classes` and records `Main-Class` in the jar manifest.

## 3. Python version

```text
src/docsdesk/__init__.py
src/docsdesk/client.py      → import docsdesk.client
src/docsdesk/__main__.py    → python -m docsdesk
```

`pyproject.toml` lists packages for hatch: `packages = ["src/docsdesk", ...]`. uv's editable install puts `src/` on the import path.

| Java | Python |
| --- | --- |
| `src/main/java/com/acme/App.java` | `src/docsdesk/__main__.py` |
| `com.acme.App` | `docsdesk` |
| `Main-Class` in MANIFEST.MF | `[project.scripts] course = "course_kit.cli:main"` |
| `mvn package` → jar | `uv build` (this course runs via editable install instead) |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Package = directory matching `com.acme` | Package = directory with `__init__.py` (or implicit namespace) | Forgetting `__init__.py` on 3.11 still works for many layouts, then surprises tooling |
| Tests live in `src/test/java` and never import `src/main` as files | pytest can import a local `docsdesk.py` **shadowing** the package | src layout exists to stop that |
| `java -jar app.jar` | `uv run python -m docsdesk` or a console script | Running `python src/docsdesk/__main__.py` breaks relative imports |

## 5. Exercise

Map `src/.../*.py` to an import name, build a `module:func` entry spec, and detect src-layout paths.

```bash
uv run pytest concepts/1_04
```

- Hint 1: strip the `src/` prefix and the `.py` suffix; replace `/` with `.`.
- Hint 2: a console script is `module:function`, like `docsdesk.__main__:main`.
- Solution: `solutions/layout.py`.

## 6. Check

1. Why not put `docsdesk/` next to `tests/` without `src/`?
2. What command runs DocsDesk as a module?
3. Where is the `course` CLI declared?
4. Predict: `python src/docsdesk/client.py` vs `uv run python -m docsdesk`.

## Setup / troubleshooting

- **`ModuleNotFoundError: docsdesk`:** run `uv sync --locked --group dev` from the **repository root**, then select `.venv`.
- **Windows:** pathlib handles `src\\docsdesk\\client.py`; the exercise also accepts `/`.
- More: [troubleshooting](../../docs/setup/troubleshooting.md).

**Real scenario:** a learner copies `client.py` into `concepts/1_04/` and imports it. Tests pass locally and fail in CI, which imports `docsdesk` from `src/`.

**What you learned:** src layout is Maven `src/main/java`; entry points are `Main-Class` for callables.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
