"""Solutions for the 0.26 skip check."""


def decorator_runs_code() -> bool:
    """Does applying @decorator call a function at definition time?"""
    return True


def annotation_is_the_same() -> bool:
    """Is a Python decorator the same as a Java annotation (metadata only)?"""
    return False
