"""Pick ruff vs pyright the way you pick Checkstyle vs javac."""


def tool_for(issue: str) -> str:
    """Return 'ruff' or 'pyright' for unused-import, line-too-long, or type-mismatch."""
    raise NotImplementedError


def pyright_is_runtime_enforcement() -> bool:
    """Do type hints plus pyright change what the interpreter accepts at runtime?"""
    raise NotImplementedError
