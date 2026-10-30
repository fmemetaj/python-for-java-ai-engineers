# 0.27 Modules and packages   [Analog: packages, classpath, import] [cost: mock] [~30 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_27/tests/test_skip.py` passes.

Related explainer: [notebook 04](../../notebooks/04_production_python.ipynb).

## 1. Concept

A **module** is a `.py` file (or a C extension). A **package** is a directory of modules, historically with `__init__.py`. `import mini_agent` loads `src/mini_agent/__init__.py` because `uv` put `src` on the path. Circular imports fail at runtime, not at compile time.

## 2. Java version

```java
package com.docsdesk;

public class ModulesDemo {
    public static void main(String[] args) {
        System.out.println(ModulesDemo.class.getName());
    }
}
```

Packages match directories on the classpath. `import com.docsdesk.ModulesDemo` is a type import.

## 3. Python version

```python
import mini_agent
from mini_agent.models import Ticket
```

`mini_agent.tools` is the file `tools.py`. There is no `import static`. Relative imports (`from .models import Ticket`) work only inside a package.

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Classpath + JAR | `sys.path` + `.venv` via `uv run` | Editor uses system Python; `import mini_agent` fails |
| `com.acme.Foo` matches folders | File name **is** the module | `tools.py` vs `tool.py` typos |
| Cycles often fail at compile | Cycles fail when the name is used | `partially initialized module` |
| One public class per file | Many names per module | Star imports (`from x import *`) wreck the namespace |
| `\\` vs `/` on Windows | `import` always uses dots | Never `import mini_agent\\tools` |

## 5. Exercise

Implement `module_stem`, `is_dunder_init`, and `package_parts` in `exercises/modules.py`.

```bash
uv run pytest concepts/0_27
```

- Hint 1: strip the `.py` suffix; reject other names.
- Hint 2: `dotted.split(".")`.
- Solution: `solutions/modules.py`.

## 6. Check

1. Is `log_stats.py` a module?
2. Why does `uv run python` find `mini_agent` when `python` might not?
3. What goes wrong with a circular import between `tools.py` and `workflow.py`?
4. Should `__init__.py` re-export everything?

## Setup / troubleshooting

- **PATH / venv:** always `uv run python` / `uv run pytest` from the repo root.
- **Windows:** the Microsoft Store `python` stub is not this project. Doctor warns about `WindowsApps`.
- **WSL:** do not import a Windows-path checkout from Linux Python.
- **Encoding:** `.py` files in this repo are UTF-8 (`PYTHONUTF8=1`).

Docs: [modules tutorial](https://docs.python.org/3/tutorial/modules.html).

**Real scenario:** DocsDesk as `src/mini_agent/` with `from .registry import ToolRegistry` — same pattern you will use in Module 1.

**What you learned:** a file is a module; `uv run` is the classpath.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
