"""Module loggers and a redacting helper."""


def logger_name(module: str) -> str:
    """The logger name for a module — pass through `__name__`."""
    raise NotImplementedError


def redact(message: str, secrets: list[str]) -> str:
    """Replace each non-empty secret with `***`."""
    raise NotImplementedError
