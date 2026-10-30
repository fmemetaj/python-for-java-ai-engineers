"""Pick ruff vs pyright the way you pick Checkstyle vs javac (solution)."""

RUFF_ISSUES = {"unused-import", "line-too-long", "format"}
PYRIGHT_ISSUES = {"type-mismatch", "unknown-name", "missing-stub"}


def tool_for(issue: str) -> str:
    """Return 'ruff' or 'pyright' for unused-import, line-too-long, or type-mismatch."""
    if issue in RUFF_ISSUES:
        return "ruff"
    if issue in PYRIGHT_ISSUES:
        return "pyright"
    raise ValueError(f"unknown issue {issue!r}")


def pyright_is_runtime_enforcement() -> bool:
    """Do type hints plus pyright change what the interpreter accepts at runtime?"""
    return False
