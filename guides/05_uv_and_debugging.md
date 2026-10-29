# 05 — uv, imports, kernels and debugging

`uv` manages the project's interpreter, environment and dependencies. `pyproject.toml` defines compatible dependency ranges; committed `uv.lock` freezes the resolved versions. Install with `uv sync --locked` so you get the same versions CI uses.

```bash
uv python install 3.12
uv sync --locked --group dev
uv run python -c "import mini_agent, pydantic; print('ready')"
uv run python scripts/doctor.py --offline
uv run pytest -q
uv run pytest --nbmake --nbmake-timeout=120 notebooks/
```

## Five common issues

1. **`ModuleNotFoundError: mini_agent`:** run `uv sync --locked --group dev` at the repository root. Choose the `.venv` kernel.
2. **`ModuleNotFoundError: pydantic`:** you're likely using system Python, not `uv`'s `.venv`.
3. **`NameError` in a notebook:** execute earlier cells in order, or restart kernel and run all.
4. **`asyncio.run() cannot be called from a running event loop`:** notebooks allow top-level `await`; use `asyncio.run()` from a normal Python process.
5. **`uv sync` cannot download dependencies:** check PyPI/network access, proxy configuration, and whether your environment uses an internal package index. Do not hardcode credentials. See [setup troubleshooting](../docs/setup/troubleshooting.md) for PATH, SSL, VPN, Apple Silicon, and WSL.

## Different commands, different jobs

- `uv sync --locked --group dev`: install the course and its development tools from `uv.lock`.
- `uv sync --locked --group dev --group demo`: also install optional Gradio.
- `uv run pytest -q`: run unit tests (Gradio tests skip if the demo group is omitted).
- `uv run ruff check src tests scripts examples` and `uv run ruff format --check ...`: lint and format.
- `uv run pyright`: type-check (install the demo group so `examples/gradio_app.py` resolves).
- `uv run pytest --nbmake notebooks/`: execute all 7 notebooks headlessly.
- `uv run python scripts/validate_notebooks.py`: older notebook runner; CI uses nbmake.

## Reproducibility note

This repository supports Python 3.11–3.13 (learners typically use 3.12). Ranges live in `pyproject.toml`; exact versions live in committed `uv.lock`. After changing dependencies, run `uv lock` and commit both files. CI fails if the lockfile is stale (`uv sync --locked`).

[Return to guide index](README.md)
