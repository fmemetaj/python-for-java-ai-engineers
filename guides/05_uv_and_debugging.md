# 05 — uv, imports, kernels and debugging

`uv` manages the project's interpreter, environment and dependencies. `pyproject.toml` defines compatible dependency ranges; `uv.lock` (if present) freezes their resolved versions.

```bash
uv python install 3.12
uv sync --group dev
uv run python -c "import mini_agent, pydantic; print('ready')"
uv run pytest -q
uv run python scripts/validate_notebooks.py
```

## Five common issues

1. **`ModuleNotFoundError: mini_agent`:** run `uv sync` at the repository root. Choose the `.venv` kernel.
2. **`ModuleNotFoundError: pydantic`:** you're likely using system Python, not `uv`'s `.venv`.
3. **`NameError` in a notebook:** execute earlier cells in order, or restart kernel and run all.
4. **`asyncio.run() cannot be called from a running event loop`:** notebooks allow top-level `await`; use `asyncio.run()` from a normal Python process.
5. **`uv sync` cannot download dependencies:** check PyPI/network access, proxy configuration, and whether your environment uses an internal package index. Do not hardcode credentials.

## Different commands, different jobs

- `uv sync --group dev`: install the course and its development tools.
- `uv sync --group dev --group demo`: also install optional Gradio.
- `uv run pytest -q`: run unit tests.
- `uv run ruff check src tests scripts examples`: lint source files.
- `uv run python scripts/validate_notebooks.py`: execute all 7 notebooks headlessly.

## Reproducibility note

This repository targets Python 3.12 and declares dependency version ranges. Commit a generated `uv.lock` after a successful `uv lock` when exact reproducibility matters; without one, compatible dependency versions may change over time.

[Return to guide index](README.md)
