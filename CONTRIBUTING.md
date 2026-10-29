# Contributing

Thanks for helping Java developers learn Python for AI engineering.

- Report inaccuracies with a clear reproducer, Python version, OS and the lesson number. Prefer the [issue forms](.github/ISSUE_TEMPLATE/).
- Keep the **core course around an estimated 60 minutes**. Place optional longer explanations in `guides/` and optional projects in `examples/`. Proposed future modules live in [docs/](docs/README.md) and are not the current syllabus.
- Keep notebooks independently executable and avoid network calls in mandatory lessons.
- Avoid paid APIs, personal data, hidden credentials and real external write operations.
- Run:

  ```bash
  uv sync --locked --group dev --group demo
  uv run pytest -q
  uv run python scripts/validate_notebooks.py
  uv run ruff check src tests scripts examples
  uv run ruff format --check src tests scripts examples
  ```

- Follow the learning-first style: concise context, Java analogy, runnable Python example, meaningful checkpoint.
- If you are inspired by another educational resource, link it and write your own examples rather than reproducing its lesson text.

The optional Ollama path is not tested against live model inference in CI; use mocked HTTP responses in automatic tests.

## Pull requests and maintainer review

1. **Fork** the public repository and create a branch in your fork.
2. Make a small, explained change, with tests where behavior changes.
3. Open a **pull request** into `main`. The maintainer reviews it before deciding whether to merge.
4. Outside contributors are not given repository write access by submitting pull requests.

The `.github/CODEOWNERS` file requests maintainer review, but **does not by itself prevent direct pushes**. Required reviews and no-force-push rules need an active GitHub branch ruleset. Repo owner: Settings → Rules → Rulesets → Add a ruleset for `main`. Also enable secret scanning and push protection in Settings → Code security.
