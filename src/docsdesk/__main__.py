"""`python -m docsdesk` — fixture page, session, then a typed tool-backed answer."""

from __future__ import annotations

from course_kit.cost import format_cost

from .assistant import DocsDesk
from .client import DocsClient
from .logging_setup import configure_logging
from .session import DeskSession
from .settings import Settings


def main() -> int:
    settings = Settings()
    logger = configure_logging(settings.secret_values())
    logger.info("provider=%s (value of OPENAI_API_KEY is never logged)", settings.llm_provider)
    with DocsClient(settings) as client:
        page = client.get_page("auth")
    session = DeskSession(f"{page.title}\n{page.body}", model=settings.openai_model)
    first = session.ask("How do clients authenticate?")
    second = session.ask("Does DocsDesk log the token?")
    print(first.summary())
    print(second.summary())
    print(f"session turns={len(session.turns)} last={format_cost(second.cost)}")
    with DocsDesk() as desk:
        typed, badge = desk.ask_with_cost("Search the docs for authentication")
        print(typed.model_dump_json())
        print(badge)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
