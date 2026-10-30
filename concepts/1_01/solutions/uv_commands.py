"""Map Maven/SDKMAN-style jobs to uv commands (solution)."""

COMMANDS = {
    "install-python": "uv python install",
    "sync-locked": "uv sync --locked",
    "run-tests": "uv run pytest",
    "run-script": "uv run python",
}


def command_for(task: str) -> str:
    """Return the uv command for install-python, sync-locked, run-tests, or run-script."""
    try:
        return COMMANDS[task]
    except KeyError as exc:
        known = ", ".join(sorted(COMMANDS))
        raise ValueError(f"unknown task {task!r}; expected one of: {known}") from exc


def prefers_uv_run() -> bool:
    """Should DocsDesk scripts be launched with `uv run` so they use `.venv`?"""
    return True
