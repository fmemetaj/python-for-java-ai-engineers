"""Locate the venv interpreter and diagnose a missed `.venv` (solution)."""

from __future__ import annotations

from pathlib import Path


def venv_python(root: Path, system: str) -> Path:
    """Return root/.venv/Scripts/python.exe on Windows, root/.venv/bin/python otherwise."""
    if system.lower().startswith("win"):
        return root / ".venv" / "Scripts" / "python.exe"
    return root / ".venv" / "bin" / "python"


def in_virtualenv(prefix: str, base_prefix: str) -> bool:
    """True when this interpreter is inside a venv (prefix differs from base_prefix)."""
    return prefix != base_prefix


def diagnose_import_error(*, using_venv: bool) -> str:
    """Hint for ModuleNotFoundError: httpx — select `.venv` or run via `uv run`."""
    if using_venv:
        return "package missing from this venv; run uv sync --locked --group dev"
    return "interpreter is not the project venv; use uv run python or select .venv"
