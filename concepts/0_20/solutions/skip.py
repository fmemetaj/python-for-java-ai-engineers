"""Solutions for the 0.20 skip check."""


def python_allows_multiple_inheritance() -> bool:
    """Can a Python class list more than one base class?"""
    return True


def mro_is_linear() -> bool:
    """Does Python linearize bases into an MRO that super() follows?"""
    return True
