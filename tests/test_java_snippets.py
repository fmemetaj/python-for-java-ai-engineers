"""Java snippets compile when JDK 21+ is on PATH (CI installs Temurin 21)."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "compile_java_snippets.py"
MIN_JAVAC_MAJOR = 21


def _javac_major() -> int | None:
    javac = shutil.which("javac")
    if javac is None:
        return None
    result = subprocess.run(
        [javac, "-version"],
        check=False,
        capture_output=True,
        text=True,
    )
    text = f"{result.stdout} {result.stderr}"
    for token in text.replace("\n", " ").split():
        if token[:1].isdigit() and "." in token:
            try:
                return int(token.split(".", 1)[0])
            except ValueError:
                return None
        if token.isdigit():
            return int(token)
    return None


_JAVAC_MAJOR = _javac_major()


@pytest.mark.skipif(shutil.which("javac") is None, reason="JDK not installed")
@pytest.mark.skipif(
    shutil.which("javac") is not None and (_JAVAC_MAJOR is None or _JAVAC_MAJOR < MIN_JAVAC_MAJOR),
    reason=f"javac {_JAVAC_MAJOR} cannot compile -source {MIN_JAVAC_MAJOR}",
)
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
    assert len(files) >= 17
