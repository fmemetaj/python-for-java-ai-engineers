"""2–3 minute skip check for 1.1."""


def uv_manages_interpreter_and_deps() -> bool:
    """Does uv install the Python interpreter *and* project dependencies?"""
    raise NotImplementedError


def prefer_system_python_over_uv_run() -> bool:
    """Should you prefer a global `python` on PATH over `uv run python`?"""
    raise NotImplementedError
