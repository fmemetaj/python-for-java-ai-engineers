"""Locate the venv interpreter and diagnose a missed `.venv`."""

from __future__ import annotations

from pathlib import Path


def venv_python(root: Path, system: str) -> Path:
    """Return root/.venv/Scripts/python.exe on Windows, root/.venv/bin/python otherwise."""
    raise NotImplementedError


def in_virtualenv(prefix: str, base_prefix: str) -> bool:
    """True when this interpreter is inside a venv (prefix differs from base_prefix)."""
    raise NotImplementedError


def diagnose_import_error(*, using_venv: bool) -> str:
    """Hint for ModuleNotFoundError: httpx — select `.venv` or run via `uv run`."""
    raise NotImplementedError
