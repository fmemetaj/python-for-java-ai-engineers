"""2–3 minute skip check for 1.2."""


def lockfile_should_be_committed() -> bool:
    """Should uv.lock be committed so CI can `uv sync --locked`?"""
    raise NotImplementedError


def ranges_live_in_the_lockfile() -> bool:
    """Do version *ranges* belong in uv.lock rather than pyproject.toml?"""
    raise NotImplementedError
