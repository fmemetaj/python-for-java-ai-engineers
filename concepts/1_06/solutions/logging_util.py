"""Module loggers and a redacting helper (solution)."""


def logger_name(module: str) -> str:
    """The logger name for a module — pass through `__name__`."""
    return module


def redact(message: str, secrets: list[str]) -> str:
    """Replace each non-empty secret with `***`."""
    redacted = message
    for secret in secrets:
        if secret:
            redacted = redacted.replace(secret, "***")
    return redacted
