"""Solutions for the 1.1 skip check."""


def uv_manages_interpreter_and_deps() -> bool:
    """Does uv install the Python interpreter *and* project dependencies?"""
    return True


def prefer_system_python_over_uv_run() -> bool:
    """Should you prefer a global `python` on PATH over `uv run python`?"""
    return False
