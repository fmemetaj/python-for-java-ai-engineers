"""Prompt-injection and leakage checks. SQL injection is a misleading analog.

A SQL engine has a parser that separates code from data. An LLM does not:
instructions, retrieved docs, and user text share one token stream. Treating
``IGNORE PREVIOUS INSTRUCTIONS`` like ``'; DROP TABLE`` will miss *indirect*
injection inside a document you retrieved.

Official: OWASP Top 10 for Large Language Model Applications
https://owasp.org/www-project-top-10-for-large-language-model-applications/
(version numbers change; read the current project page). This lesson drills
prompt injection, sensitive-information disclosure, and excessive agency
(tool allow-lists from Module 3). It does not claim a complete threat model.

Graded work is offline. Nothing is sent, emailed, or deployed.
"""

from __future__ import annotations

from collections.abc import Sequence

# Synthetic markers used by the fixture suite. These are detector strings,
# not a payload cookbook.
_DIRECT_MARKERS = (
    "ignore previous instructions",
    "ignore all previous",
    "dump the system prompt",
    "reveal your instructions",
    "exfiltrate",
    "print the api key",
    "call delete_page",
)


def looks_like_injection(text: str) -> bool:
    """True when the user (or a doc line) asks the model to override instructions."""
    lowered = text.lower()
    return any(marker in lowered for marker in _DIRECT_MARKERS)


def redact_secrets(text: str, secrets: Sequence[str]) -> str:
    """Replace known secret substrings. Empty secrets are skipped."""
    redacted = text
    for secret in secrets:
        if secret:
            redacted = redacted.replace(secret, "***")
    return redacted


def output_leaks_secret(text: str, secrets: Sequence[str]) -> bool:
    return any(secret and secret in text for secret in secrets)


def strip_injected_instructions(doc_body: str) -> str:
    """Drop retrieved-doc lines that look like instructions (indirect injection)."""
    kept = [line for line in doc_body.splitlines() if not looks_like_injection(line)]
    return "\n".join(kept)


def classify_prompt(text: str) -> str:
    """Return ``injection`` or ``ok``. Used by ProductionDesk before any LLM call."""
    return "injection" if looks_like_injection(text) else "ok"


__all__ = [
    "classify_prompt",
    "looks_like_injection",
    "output_leaks_secret",
    "redact_secrets",
    "strip_injected_instructions",
]
