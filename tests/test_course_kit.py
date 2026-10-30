"""Smoke tests for the course_kit catalog, loader, and CLI."""

from __future__ import annotations

import subprocess
import sys

import pytest
from course_kit.catalog import (
    CONCEPTS_0A,
    CONCEPTS_0B,
    CONCEPTS_1,
    CONCEPTS_2,
    CONCEPTS_3,
    CONCEPTS_4,
    CONCEPTS_5,
    CONCEPTS_6,
    CONCEPTS_7,
    CONCEPTS_A,
)
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


def test_catalog_covers_1() -> None:
    folders = [concept["folder"] for concept in CONCEPTS_1]
    assert folders == [f"1_{index:02d}" for index in range(1, 13)]
    assert sum(1 for concept in CONCEPTS_1 if concept["kind"] == "new") == 1
    assert sum(1 for concept in CONCEPTS_1 if concept["kind"] == "analog") == 11


def test_catalog_covers_2() -> None:
    folders = [concept["folder"] for concept in CONCEPTS_2]
    assert folders == [f"2_{index:02d}" for index in range(1, 12)]
    assert sum(1 for concept in CONCEPTS_2 if concept["kind"] == "new") == 6
    assert sum(1 for concept in CONCEPTS_2 if concept["kind"] == "analog") == 5


def test_catalog_covers_3() -> None:
    folders = [concept["folder"] for concept in CONCEPTS_3]
    assert folders == [f"3_{index:02d}" for index in range(1, 6)]
    assert sum(1 for concept in CONCEPTS_3 if concept["kind"] == "new") == 2
    assert sum(1 for concept in CONCEPTS_3 if concept["kind"] == "analog") == 3


def test_catalog_covers_4() -> None:
    folders = [concept["folder"] for concept in CONCEPTS_4]
    assert folders == [f"4_{index:02d}" for index in range(1, 8)]
    assert sum(1 for concept in CONCEPTS_4 if concept["kind"] == "new") == 5
    assert sum(1 for concept in CONCEPTS_4 if concept["kind"] == "analog") == 2


def test_catalog_covers_5() -> None:
    folders = [concept["folder"] for concept in CONCEPTS_5]
    assert folders == [f"5_{index:02d}" for index in range(1, 7)]
    assert sum(1 for concept in CONCEPTS_5 if concept["kind"] == "new") == 3
    assert sum(1 for concept in CONCEPTS_5 if concept["kind"] == "analog") == 3


def test_catalog_covers_6() -> None:
    folders = [concept["folder"] for concept in CONCEPTS_6]
    assert folders == [f"6_{index:02d}" for index in range(1, 7)]
    assert sum(1 for concept in CONCEPTS_6 if concept["kind"] == "new") == 3
    assert sum(1 for concept in CONCEPTS_6 if concept["kind"] == "analog") == 3


def test_catalog_covers_7() -> None:
    folders = [concept["folder"] for concept in CONCEPTS_7]
    assert folders == [f"7_{index:02d}" for index in range(1, 8)]
    assert sum(1 for concept in CONCEPTS_7 if concept["kind"] == "new") == 5
    assert sum(1 for concept in CONCEPTS_7 if concept["kind"] == "analog") == 2


def test_catalog_covers_a() -> None:
    folders = [concept["folder"] for concept in CONCEPTS_A]
    assert folders == [f"a_{index:02d}" for index in range(1, 10)]
    assert sum(1 for concept in CONCEPTS_A if concept["kind"] == "new") == 6
    assert sum(1 for concept in CONCEPTS_A if concept["kind"] == "analog") == 3


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
    assert "m1" in result.stdout
    assert "m2" in result.stdout
    assert "m3" in result.stdout
    assert "m4" in result.stdout
    assert "m5" in result.stdout
    assert "m6" in result.stdout
    assert "m7" in result.stdout
    assert "ma" in result.stdout


def test_cli_module_is_callable() -> None:
    assert callable(main)


def test_safe_part_rejects_traversal() -> None:
    with pytest.raises(ValueError):
        _safe_part("../secrets")
    with pytest.raises(ValueError):
        _safe_part("foo/bar")
    assert _safe_part("0_01") == "0_01"
