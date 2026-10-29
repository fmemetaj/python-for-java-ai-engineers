## What changed

## Learning objective

What a Java developer should understand after this change, and any tradeoff (time, scope, extra dependency).

## How to verify

- [ ] `uv sync --locked --group dev --group demo`
- [ ] `uv run pytest -q`
- [ ] `uv run python scripts/validate_notebooks.py`
- [ ] `uv run ruff check src tests scripts examples`
- [ ] `uv run ruff format --check src tests scripts examples`

## Notes

Core notebooks stay independently executable and must not call paid APIs.
Keep mock workflows honest: simulated approval does not send email or change data.
