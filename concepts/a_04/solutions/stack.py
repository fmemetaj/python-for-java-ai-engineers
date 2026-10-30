"""Open: pick own / hosted / hybrid."""

from __future__ import annotations

from course_kit.hosted import StackDecision, choose_stack


def pick_stack(
    *,
    own_recall: float,
    hosted_available: bool,
    can_export: bool,
    can_eval: bool,
    overlap: float,
) -> StackDecision:
    """Delegate to the course helper. Prefer own when eval-able and recall >= 0.6."""
    return choose_stack(
        own_recall=own_recall,
        hosted_available=hosted_available,
        can_export=can_export,
        can_eval=can_eval,
        overlap=overlap,
    )
