# Contributing

Thanks for helping Java developers learn Python for AI engineering.

- Report inaccuracies with a clear reproducer, Python version, OS, and the lesson number. Setup failures: paste `uv run python scripts/doctor.py --offline` (no secrets).
- Keep the **core notebooks tightly scoped**. Put optional longer explanations in `guides/` and optional projects in `examples/`. If a change alters lesson length, update the README estimates — those numbers are unmeasured guesses, not a timed guarantee.
- Keep notebooks independently executable and avoid network calls in mandatory lessons.
- Avoid paid APIs, personal data, hidden credentials, and real external write operations.
- Original work only. If another educational resource inspired you, link it and write your own examples.
- Follow the learning-first style: concise context, Java analogy (and where it breaks), runnable Python, meaningful checkpoint.

## Checks

From the repository root, using the committed lockfile:

```bash
uv sync --locked --group dev
uv run python scripts/doctor.py --offline
uv run pytest -q
uv run ruff check src tests scripts examples concepts placement fundamentals
uv run ruff format --check src tests scripts examples concepts placement fundamentals
uv run course check m0a --solutions
uv run course check m0b --solutions
uv run course check m1 --solutions
uv run course check m2 --solutions
uv run course check m3 --solutions
uv run course check m4 --solutions
uv run pytest --nbmake --nbmake-timeout=120 notebooks/ concepts/0_02/hidden_state.ipynb
```

Install the optional demo group before pyright on `examples/gradio_app.py` and before Gradio tests actually run (otherwise they skip):

```bash
uv sync --locked --group dev --group demo
uv run pyright
uv run pytest -q
```

The optional Ollama path is not tested against live model inference in CI; use mocked HTTP responses.

Issue templates: bug, lesson feedback (including actual minutes), and lesson proposal. See [docs/planning](docs/planning/course-strategy.md) before proposing large curriculum changes.

## Pull requests and maintainer review

1. **Fork** the public repository and create a branch in your fork.
2. Make a small, explained change, with tests where behavior changes.
3. Open a **pull request** into `main`. The maintainer reviews it before deciding whether to merge.
4. Outside contributors are not given repository write access by submitting pull requests.

The `.github/CODEOWNERS` file requests maintainer review, but **does not by itself prevent direct pushes**. Required reviews and no-force-push rules need an active GitHub branch ruleset. Repo owner: Settings → Rules → Rulesets → Add a ruleset for `main`.
