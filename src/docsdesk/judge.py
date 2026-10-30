"""LLM-as-judge with calibration. Offline FakeLLM only for graded work.

An LLM-as-judge is a *second* model call that scores an answer against a
rubric. It is not JUnit of a pure function: the judge can be wrong, so you
calibrate it against frozen human (or fixture) labels before it is a CI gate.

Official: https://platform.openai.com/docs/guides/evaluation
Graded work uses ``LLM_PROVIDER=fake``. Live judges are optional and never a
threshold we claim.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from course_kit.llm import FakeLLM


@dataclass(frozen=True)
class JudgeVerdict:
    score: int
    passed: bool
    rationale: str


def verdict_passes(score: int, threshold: int) -> bool:
    """True when the integer score meets the pass bar (inclusive)."""
    if threshold < 1:
        raise ValueError("threshold must be >= 1")
    return score >= threshold


def agreement_rate(predicted: Sequence[bool], labeled: Sequence[bool]) -> float:
    """Fraction of matching pass/fail labels. Both sequences must be same length."""
    if len(predicted) != len(labeled) or not predicted:
        raise ValueError("predicted and labeled must be the same non-empty length")
    hits = sum(pred is label for pred, label in zip(predicted, labeled, strict=True))
    return hits / len(predicted)


def parse_verdict(payload: dict[str, Any], *, threshold: int = 4) -> JudgeVerdict:
    score = int(payload["score"])
    rationale = str(payload.get("rationale", ""))
    flagged = payload.get("pass")
    passed = bool(flagged) if flagged is not None else verdict_passes(score, threshold)
    return JudgeVerdict(score=score, passed=passed, rationale=rationale)


def scripted_judge() -> FakeLLM:
    """Deterministic judge for DocsDesk fixtures. Not a live model."""
    bearer = {
        "score": 5,
        "pass": True,
        "rationale": "cites Bearer and does not invent a secret",
    }
    weak = {"score": 1, "pass": False, "rationale": "empty or off-topic"}
    return FakeLLM(
        structured={
            "Clients send a Bearer token. DocsDesk never logs the token.": bearer,
            "GET /tickets/{id} returns a ticket. Timeouts are five seconds.": {
                "score": 4,
                "pass": True,
                "rationale": "matches the tickets fixture",
            },
            "I don't know": weak,
            "asdf": weak,
        }
    )


def judge_answer(
    answer: str,
    *,
    client: FakeLLM | None = None,
    threshold: int = 4,
) -> JudgeVerdict:
    """Score one answer. FakeLLM returns a structured verdict."""
    llm = client if client is not None else scripted_judge()
    response = llm.complete(answer)
    if response.output_parsed is None:
        return JudgeVerdict(score=1, passed=False, rationale="judge returned no JSON")
    return parse_verdict(response.output_parsed, threshold=threshold)


__all__ = [
    "JudgeVerdict",
    "agreement_rate",
    "judge_answer",
    "parse_verdict",
    "scripted_judge",
    "verdict_passes",
]
