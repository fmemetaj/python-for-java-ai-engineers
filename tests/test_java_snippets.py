"""Java snippets compile when a JDK is on PATH (CI installs Temurin 21)."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "compile_java_snippets.py"


@pytest.mark.skipif(shutil.which("javac") is None, reason="JDK not installed")
def test_java_snippets_compile() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_compile_script_exists_and_finds_files() -> None:
    assert SCRIPT.is_file()
    files = list((ROOT / "concepts").glob("*/java/*.java"))
    assert len(files) >= 8
