"""Open: required keys on a cost report."""

from __future__ import annotations


def cost_report_fields() -> list[str]:
    """Return the keys a hiring manager should see on the cost report."""
    return [
        "requests",
        "model",
        "usd_per_request",
        "usd_per_100",
        "pricing_source",
        "pricing_retrieved",
        "assumptions",
        "provider",
    ]
