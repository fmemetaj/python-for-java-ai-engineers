"""Every concept examples.py must run offline with a zero exit status."""

from __future__ import annotations

import subprocess
import sys

import pytest
from course_kit.catalog import CONCEPTS_0A
from course_kit.loader import repo_root


@pytest.mark.parametrize("folder", [concept["folder"] for concept in CONCEPTS_0A])
def test_examples_script(folder: str) -> None:
    path = repo_root() / "concepts" / folder / "examples.py"
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=repo_root(),
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ok" in result.stdout
