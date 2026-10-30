"""DocsDesk skeleton — a docs HTTP client that grows in later modules.

Module 1: settings, redacting logs, httpx + retries, Pydantic JSON, fake LLM.
Everything essential runs offline (`LLM_PROVIDER=fake`, fixture HTTP transport).
"""

from .client import DocsClient
from .logging_setup import RedactingFilter, configure_logging
from .models import DocPage
from .settings import Settings

__all__ = [
    "DocPage",
    "DocsClient",
    "RedactingFilter",
    "Settings",
    "configure_logging",
]
