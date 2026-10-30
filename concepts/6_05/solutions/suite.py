"""Open: grade one suite case; all-true means the suite passed."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any


def grade_case(
    case: dict[str, Any],
    *,
    looks_like_injection: Callable[[str], bool],
    redact_secrets: Callable[[str, Sequence[str]], str],
) -> bool:
    """Return True when the case behaved as ``expect``.

    Kinds: direct (blocked), benign (allowed), leak (redacted), indirect
    (strip lines that look like injection; leftover text must be clean).
    """
    kind = str(case["kind"])
    expect = str(case.get("expect", ""))
    if kind == "direct":
        blocked = looks_like_injection(str(case["prompt"]))
        return blocked if expect == "blocked" else not blocked
    if kind == "benign":
        return looks_like_injection(str(case["prompt"])) is False
    if kind == "leak":
        secrets = [str(item) for item in case["secrets"]]
        redacted = redact_secrets(str(case["output"]), secrets)
        return all(secret not in redacted for secret in secrets if secret)
    if kind == "indirect":
        kept = [line for line in str(case["doc"]).splitlines() if not looks_like_injection(line)]
        leftover = "\n".join(kept)
        return looks_like_injection(leftover) is False
    raise ValueError(f"unknown kind {kind}")


def suite_ok(results: Sequence[bool]) -> bool:
    """True when every result is True and the sequence is non-empty."""
    return bool(results) and all(results)
