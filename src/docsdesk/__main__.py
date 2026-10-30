"""`python -m docsdesk` — demo, or `uv run docsdesk eval` for retrieval metrics."""

from __future__ import annotations

import sys

from course_kit.cost import format_cost

from .assistant import DocsDesk
from .client import DocsClient
from .logging_setup import configure_logging
from .session import DeskSession
from .settings import Settings


def _demo() -> int:
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
    from .rag import RagDesk

    rag = RagDesk()
    answer = rag.ask("How do I refund a captured payment?")
    print(answer.model_dump_json())
    return 0


def _eval() -> int:
    from .retrieval_eval import print_report, run_retrieval_eval

    report = run_retrieval_eval()
    print_report(report)
    return 0 if report.ok else 1


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args[:1] == ["eval"]:
        return _eval()
    return _demo()


if __name__ == "__main__":
    raise SystemExit(main())
