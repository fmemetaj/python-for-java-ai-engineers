"""2–3 minute skip check for 0.23."""


def hints_enforced_at_runtime() -> bool:
    """Does Python reject list[str] passed to a list[int] parameter at runtime?"""
    raise NotImplementedError


def pyright_is_static() -> bool:
    """Is pyright/mypy a static checker (editor/CI), not the interpreter?"""
    raise NotImplementedError
