"""API-change skill: changelogs, sunset scanners, spend-capped smoke tests.

The course treats SDK upgrades as an engineering drill (F1), not a surprise.
Graded work scans strings and runs FakeLLM. It never spends a live key.

Official docs: https://platform.openai.com/docs/guides/migrate-to-responses
Assistants sunset: 2026-08-26 (technical-review.md, verified 2026-10-29).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .loader import repo_root

CHANGELOG_PATH = Path("data") / "changelogs" / "sdk_fake.json"

# 0.x Chat Completions helper and the Assistants surface. Current
# `client.chat.completions.create` is still supported; do not flag it.
SUNSET_PATTERNS: tuple[tuple[str, str], ...] = (
    ("openai.ChatCompletion.create", "removed 0.x Chat Completions helper"),
    ("openai.ChatCompletion.acreate", "removed 0.x Chat Completions helper"),
    ("beta.assistants", "Assistants API sunset 2026-08-26"),
    ("client.beta.threads", "Assistants threads sunset 2026-08-26"),
    ("Assistants API", "Assistants API sunset 2026-08-26"),
)

SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"sk-[A-Za-z0-9_-]{8,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._\-]+"),
    re.compile(r"course-test-secret-value"),
)


@dataclass(frozen=True)
class ChangelogEntry:
    date: str
    kind: str
    summary: str
    action: str


@dataclass(frozen=True)
class ScanFinding:
    pattern: str
    reason: str
    line: int


@dataclass(frozen=True)
class SmokeCall:
    name: str
    cost_usd: float


@dataclass(frozen=True)
class SmokeReport:
    ran: tuple[str, ...]
    skipped: tuple[str, ...]
    spent_usd: float
    cap_usd: float

    @property
    def within_budget(self) -> bool:
        return self.spent_usd <= self.cap_usd + 1e-12


def load_changelog(path: Path | None = None) -> list[ChangelogEntry]:
    json_path = path if path is not None else repo_root() / CHANGELOG_PATH
    raw = json.loads(json_path.read_text(encoding="utf-8"))
    entries = raw.get("entries") if isinstance(raw, dict) else None
    if not isinstance(entries, list):
        raise ValueError("changelog must have an entries array")
    out: list[ChangelogEntry] = []
    for row in entries:
        if not isinstance(row, dict):
            raise ValueError("changelog entry must be an object")
        out.append(
            ChangelogEntry(
                date=str(row["date"]),
                kind=str(row["kind"]),
                summary=str(row["summary"]),
                action=str(row["action"]),
            )
        )
    return out


def pin_ok(declared: str, locked: str) -> bool:
    """True when the lockfile pin equals the declared exact version."""
    if not declared or not locked:
        raise ValueError("versions must be non-empty")
    return declared == locked


def requires_responses(entry: ChangelogEntry) -> bool:
    return "responses" in entry.action.lower() or entry.kind == "sunset"


def scan_source(source: str) -> list[ScanFinding]:
    """Find sunset / removed API strings. Line numbers are 1-based."""
    findings: list[ScanFinding] = []
    for index, line in enumerate(source.splitlines(), start=1):
        for pattern, reason in SUNSET_PATTERNS:
            if pattern in line:
                findings.append(ScanFinding(pattern=pattern, reason=reason, line=index))
    return findings


def sunset_free(source: str) -> bool:
    return scan_source(source) == []


def run_smoke(calls: list[SmokeCall], cap_usd: float) -> SmokeReport:
    """Run prefix of calls until the next one would exceed the cap."""
    if cap_usd < 0:
        raise ValueError("cap_usd must be >= 0")
    ran: list[str] = []
    skipped: list[str] = []
    spent = 0.0
    over = False
    for call in calls:
        if call.cost_usd < 0:
            raise ValueError("call cost must be >= 0")
        if over or spent + call.cost_usd > cap_usd + 1e-12:
            skipped.append(call.name)
            over = True
            continue
        ran.append(call.name)
        spent += call.cost_usd
    return SmokeReport(
        ran=tuple(ran),
        skipped=tuple(skipped),
        spent_usd=round(spent, 8),
        cap_usd=cap_usd,
    )


def sanitize_record(payload: dict[str, Any]) -> dict[str, Any]:
    """Redact known secret shapes from a recorded fixture dict (recursive)."""

    def _clean(value: Any) -> Any:
        if isinstance(value, str):
            text = value
            for pattern in SECRET_PATTERNS:
                text = pattern.sub("***", text)
            return text
        if isinstance(value, list):
            return [_clean(item) for item in value]
        if isinstance(value, dict):
            return {str(key): _clean(item) for key, item in value.items()}
        return value

    cleaned = _clean(payload)
    if not isinstance(cleaned, dict):
        raise TypeError("payload must be a JSON object")
    return cleaned
