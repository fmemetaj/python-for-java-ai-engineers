# 05 — uv, imports, kernels and debugging

`uv` manages the project's interpreter, environment and dependencies. `pyproject.toml` defines compatible dependency ranges; committed `uv.lock` freezes the resolved versions CI and learners should use.

```bash
uv python install 3.12
uv sync --locked --group dev
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

- `uv sync --locked --group dev`: install the course and its development tools at the locked versions.
- `uv sync --locked --group dev --group demo`: also install optional Gradio.
- `uv run pytest -q`: run unit tests. Gradio demo tests skip if Gradio is not installed.
- `uv run ruff check src tests scripts examples`: lint source files.
- `uv run ruff format --check src tests scripts examples`: confirm formatting.
- `uv run python scripts/validate_notebooks.py`: execute all 7 notebooks headlessly.

## Reproducibility note

This repository supports Python 3.11–3.13. Ranges live in `pyproject.toml`; exact versions are in committed `uv.lock`. CI runs `uv sync --locked`. After changing dependencies, run `uv lock` and commit the updated lockfile. Without `--locked`, compatible versions may drift.

[Return to guide index](README.md)
