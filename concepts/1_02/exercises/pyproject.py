"""Translate Maven coordinates and diagnose a stale lockfile."""


def dependency_line(name: str, lower: str, upper: str) -> str:
    """Return a pep-style range, e.g. httpx>=0.27,<1 ."""
    raise NotImplementedError


def group_for_maven_scope(scope: str) -> str:
    """Return 'project' for compile/runtime, 'dev' for test, 'demo' for optional."""
    raise NotImplementedError


def diagnose_lock_error(message: str) -> str:
    """If uv says the lock is stale, tell the learner to run `uv lock` and commit."""
    raise NotImplementedError
