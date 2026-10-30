"""Starters fail the Electives (A) concept tests; solutions pass them."""

from __future__ import annotations

import os
import subprocess
import sys

import pytest
from course_kit.catalog import CONCEPTS_A
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


@pytest.mark.parametrize("folder", [concept["folder"] for concept in CONCEPTS_A])
def test_solutions_pass_concept_tests(folder: str) -> None:
    result = _pytest([f"concepts/{folder}/tests"], impl="solutions")
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("folder", [concept["folder"] for concept in CONCEPTS_A])
def test_starters_fail_concept_tests(folder: str) -> None:
    result = _pytest([f"concepts/{folder}/tests"], impl="exercises")
    assert result.returncode != 0, f"{folder} starters unexpectedly passed"
