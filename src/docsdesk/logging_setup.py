"""Module loggers with secret redaction. Java analogy: Logback + a masking converter."""

from __future__ import annotations

import logging
from collections.abc import Iterable

LOGGER_NAME = "docsdesk"


class RedactingFilter(logging.Filter):
    """Replace known secret substrings in a log record before it is emitted."""

    def __init__(self, secrets: Iterable[str]) -> None:
        super().__init__()
        self._secrets = [secret for secret in secrets if secret]

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        for secret in self._secrets:
            message = message.replace(secret, "***")
        record.msg = message
        record.args = ()
        return True


def configure_logging(
    secrets: Iterable[str],
    *,
    level: int = logging.INFO,
    handler: logging.Handler | None = None,
) -> logging.Logger:
    """Return the `docsdesk` logger with a redacting filter attached to its handler."""
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)
    logger.propagate = False
    if handler is None:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    handler.addFilter(RedactingFilter(secrets))
    logger.handlers.clear()
    logger.addHandler(handler)
    return logger
