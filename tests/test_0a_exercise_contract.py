"""Starters fail the concept tests; solutions pass them.

Java analogy: a red/green contract like a failing JUnit test checked in
alongside the implementation that makes it green.
"""

from __future__ import annotations

import os
import subprocess
import sys

import pytest
from course_kit.catalog import CONCEPTS_0A
from course_kit.loader import repo_root


def _pytest(paths: list[str], *, impl: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["COURSE_IMPL"] = impl
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--tb=line", *paths],
        cwd=repo_root(),
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )


@pytest.mark.parametrize("folder", [concept["folder"] for concept in CONCEPTS_0A])
def test_solutions_pass_concept_tests(folder: str) -> None:
    result = _pytest([f"concepts/{folder}/tests"], impl="solutions")
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("folder", [concept["folder"] for concept in CONCEPTS_0A])
def test_starters_fail_concept_tests(folder: str) -> None:
    result = _pytest([f"concepts/{folder}/tests"], impl="exercises")
    assert result.returncode != 0, f"{folder} starters unexpectedly passed"


def test_log_stats_solution_passes() -> None:
    result = _pytest(["fundamentals/test_log_stats.py"], impl="solutions")
    assert result.returncode == 0, result.stdout + result.stderr


def test_log_stats_starter_fails() -> None:
    result = _pytest(["fundamentals/test_log_stats.py"], impl="exercises")
    assert result.returncode != 0


def test_placement_solution_passes() -> None:
    result = _pytest(["placement/test_self_check.py"], impl="solutions")
    assert result.returncode == 0, result.stdout + result.stderr


def test_placement_starter_fails() -> None:
    result = _pytest(["placement/test_self_check.py"], impl="exercises")
    assert result.returncode != 0
