"""Smoke tests for the course_kit catalog, loader, and CLI."""

from __future__ import annotations

import subprocess
import sys

import pytest
from course_kit.catalog import CONCEPTS_0A, CONCEPTS_0B
from course_kit.cli import main
from course_kit.loader import _safe_part, impl_name, load_concept_module, repo_root


def test_catalog_covers_0a() -> None:
    folders = [concept["folder"] for concept in CONCEPTS_0A]
    assert folders == [f"0_{index:02d}" for index in range(1, 16)]
    assert sum(1 for concept in CONCEPTS_0A if concept["kind"] == "new") == 7
    assert sum(1 for concept in CONCEPTS_0A if concept["kind"] == "analog") == 8


def test_catalog_covers_0b() -> None:
    folders = [concept["folder"] for concept in CONCEPTS_0B]
    assert folders == [f"0_{index:02d}" for index in range(16, 30)]
    assert sum(1 for concept in CONCEPTS_0B if concept["kind"] == "new") == 5
    assert sum(1 for concept in CONCEPTS_0B if concept["kind"] == "analog") == 9


def test_loader_reads_solutions() -> None:
    import os

    previous = os.environ.get("COURSE_IMPL")
    os.environ["COURSE_IMPL"] = "solutions"
    try:
        assert impl_name() == "solutions"
        skip = load_concept_module("0_01", "skip")
        assert skip.is_entry_point("__main__") is True
    finally:
        if previous is None:
            os.environ.pop("COURSE_IMPL", None)
        else:
            os.environ["COURSE_IMPL"] = previous


def test_cli_help() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "course_kit.cli", "check", "--help"],
        cwd=repo_root(),
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "m0a" in result.stdout
    assert "m0b" in result.stdout


def test_cli_module_is_callable() -> None:
    assert callable(main)


def test_safe_part_rejects_traversal() -> None:
    with pytest.raises(ValueError):
        _safe_part("../secrets")
    with pytest.raises(ValueError):
        _safe_part("foo/bar")
    assert _safe_part("0_01") == "0_01"
