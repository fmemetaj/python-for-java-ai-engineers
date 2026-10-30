"""Solutions for the 0.23 skip check."""


def hints_enforced_at_runtime() -> bool:
    """Does Python reject list[str] passed to a list[int] parameter at runtime?"""
    return False


def pyright_is_static() -> bool:
    """Is pyright/mypy a static checker (editor/CI), not the interpreter?"""
    return True
