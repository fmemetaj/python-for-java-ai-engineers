"""2–3 minute skip check for 0.1. Replace the NotImplementedError bodies."""


def is_entry_point(dunder_name: str) -> bool:
    """Return True when a module is being executed as a script."""
    raise NotImplementedError


def repl_command() -> str:
    """Return the usual command that starts a Python REPL via uv."""
    raise NotImplementedError
