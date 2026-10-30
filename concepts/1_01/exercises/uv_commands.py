"""Map Maven/SDKMAN-style jobs to uv commands."""


def command_for(task: str) -> str:
    """Return the uv command for install-python, sync-locked, run-tests, or run-script."""
    raise NotImplementedError


def prefers_uv_run() -> bool:
    """Should DocsDesk scripts be launched with `uv run` so they use `.venv`?"""
    raise NotImplementedError
