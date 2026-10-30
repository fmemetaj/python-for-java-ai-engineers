"""Translate Maven coordinates and diagnose a stale lockfile (solution)."""

SCOPE_TO_GROUP = {
    "compile": "project",
    "runtime": "project",
    "test": "dev",
    "optional": "demo",
}


def dependency_line(name: str, lower: str, upper: str) -> str:
    """Return a pep-style range, e.g. httpx>=0.27,<1 ."""
    return f"{name}>={lower},<{upper}"


def group_for_maven_scope(scope: str) -> str:
    """Return 'project' for compile/runtime, 'dev' for test, 'demo' for optional."""
    try:
        return SCOPE_TO_GROUP[scope]
    except KeyError as exc:
        raise ValueError(f"unknown Maven scope {scope!r}") from exc


def diagnose_lock_error(message: str) -> str:
    """If uv says the lock is stale, tell the learner to run `uv lock` and commit."""
    lowered = message.lower()
    if "lock" in lowered and ("out of date" in lowered or "outdated" in lowered):
        return "run uv lock and commit uv.lock"
    return "see docs/setup/troubleshooting.md"
