from course_kit.loader import load_concept_module
import pytest

uv_commands = load_concept_module("1_01", "uv_commands")


def test_install_python() -> None:
    assert uv_commands.command_for("install-python") == "uv python install"


def test_sync_locked() -> None:
    assert uv_commands.command_for("sync-locked") == "uv sync --locked"


def test_run_tests() -> None:
    assert uv_commands.command_for("run-tests") == "uv run pytest"


def test_run_script() -> None:
    assert uv_commands.command_for("run-script") == "uv run python"


def test_unknown_task() -> None:
    with pytest.raises(ValueError, match="unknown task"):
        uv_commands.command_for("mvn package")


def test_prefers_uv_run() -> None:
    assert uv_commands.prefers_uv_run() is True
