"""Solutions for the 0.13 skip check."""


def list_comprehension_is_lazy() -> bool:
    """Does a list comprehension wait to compute items until you iterate?"""
    return False


def set_comprehension_keeps_duplicates() -> bool:
    """Does {x for x in items} keep duplicate x values?"""
    return False
