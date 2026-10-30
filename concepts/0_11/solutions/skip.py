"""Solutions for the 0.11 skip check."""


def dict_preserves_insertion_order() -> bool:
    """Do modern Python dicts remember insertion order?"""
    return True


def missing_key_with_brackets_returns_none() -> bool:
    """Does d['missing'] return None?"""
    return False
