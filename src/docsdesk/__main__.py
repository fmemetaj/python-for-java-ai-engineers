"""`python -m docsdesk` — print one fixture page. No network, no paid API."""

from __future__ import annotations

from course_kit.llm import get_client

from .client import DocsClient
from .logging_setup import configure_logging
from .settings import Settings


def main() -> int:
    settings = Settings()
    logger = configure_logging(settings.secret_values())
    logger.info("provider=%s (value of OPENAI_API_KEY is never logged)", settings.llm_provider)
    with DocsClient(settings) as client:
        page = client.get_page("auth")
    summary = get_client(settings.llm_provider).complete(f"{page.title}\n{page.body}").output_text
    print(f"{page.title}: {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
