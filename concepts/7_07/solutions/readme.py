"""Portfolio README sections, demo length, and the self-assessment list."""

from __future__ import annotations


def readme_sections() -> list[str]:
    """Sections a hiring manager should find, in a stable order."""
    return [
        "objective",
        "architecture",
        "how to run",
        "eval report",
        "cost report",
        "threat model",
        "limitations",
        "demo",
    ]


def demo_minutes() -> int:
    """How long the walkthrough is, in minutes."""
    return 5


def self_assessment_items() -> list[str]:
    """Checklist lines the learner ticks before showing the repo."""
    return [
        "uv sync --locked from a clean clone",
        "LLM_PROVIDER=fake for graded work",
        "RAG answers include citations",
        "Write tools require an approval gate",
        "Agent loop enforces a step cap",
        "Eval report has at least 30 cases",
        "Cost per 100 requests is documented",
        "Threat model and limitations are listed",
        "Optional FastAPI uses TestClient (no Docker in CI)",
        "No secrets committed; Responses API only",
    ]
