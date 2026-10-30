"""Solutions for the 0.1 skip check."""


def is_entry_point(dunder_name: str) -> bool:
    """Return True when a module is being executed as a script."""
    return dunder_name == "__main__"


def repl_command() -> str:
    """Return the usual command that starts a Python REPL via uv."""
    return "uv run python"
