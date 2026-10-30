"""Solutions for the 1.2 skip check."""


def lockfile_should_be_committed() -> bool:
    """Should uv.lock be committed so CI can `uv sync --locked`?"""
    return True


def ranges_live_in_the_lockfile() -> bool:
    """Do version *ranges* belong in uv.lock rather than pyproject.toml?"""
    return False
