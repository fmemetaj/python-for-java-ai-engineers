"""Solutions for the 1.5 skip check."""


def ruff_is_the_style_linter() -> bool:
    """Is ruff the Checkstyle/Spotless analog (lint + format)?"""
    return True


def pyright_enforces_types_at_runtime() -> bool:
    """Does pyright reject a wrong type at runtime the way javac does at compile time?"""
    return False
