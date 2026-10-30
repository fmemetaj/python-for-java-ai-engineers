## Summary

<!-- What changed, and why a Java developer taking this course should care. -->

## Learning impact

- [ ] Notebooks still run independently (no new paid APIs or required network calls)
- [ ] Optional depth stayed in `guides/` or `examples/`
- [ ] README time estimates were updated if lesson length changed

## Checks

Run from the repository root:

- [ ] `uv sync --locked --group dev`
- [ ] `uv run python scripts/doctor.py --offline`
- [ ] `uv run pytest -q` (Gradio tests skip unless the demo group is installed)
- [ ] `uv run ruff check src tests scripts examples concepts placement fundamentals`
- [ ] `uv run ruff format --check src tests scripts examples concepts placement fundamentals`
- [ ] `uv run course check m0a --solutions` / `m0b` / `m1` / `m2` / `m3` / `m4` / `m5` / `m6` / `m7` / `ma --solutions` (when those modules change)
- [ ] `uv run python scripts/check_markdown_links.py`
- [ ] `uv run pyright` (install `--group demo` so `examples/gradio_app.py` type-checks)
- [ ] `uv run pytest --nbmake --nbmake-timeout=120 notebooks/`

Optional demo coverage: `uv sync --locked --group dev --group demo`

## Notes

<!-- OS, Python version, and doctor output if this PR is setup-related. -->
