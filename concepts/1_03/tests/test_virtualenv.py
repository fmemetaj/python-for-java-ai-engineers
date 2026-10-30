from pathlib import Path

from course_kit.loader import load_concept_module

virtualenv = load_concept_module("1_03", "virtualenv")


def test_venv_python_windows() -> None:
    path = virtualenv.venv_python(Path("C:/course"), "Windows")
    assert path.as_posix().endswith(".venv/Scripts/python.exe")


def test_venv_python_posix() -> None:
    path = virtualenv.venv_python(Path("/opt/course"), "Linux")
    assert path.as_posix().endswith(".venv/bin/python")


def test_in_virtualenv() -> None:
    assert virtualenv.in_virtualenv("/proj/.venv", "/usr") is True
    assert virtualenv.in_virtualenv("/usr", "/usr") is False


def test_diagnose_not_in_venv() -> None:
    hint = virtualenv.diagnose_import_error(using_venv=False)
    assert "venv" in hint.lower()


def test_diagnose_missing_package() -> None:
    hint = virtualenv.diagnose_import_error(using_venv=True)
    assert "uv sync" in hint
