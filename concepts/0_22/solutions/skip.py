"""Solutions for the 0.22 skip check."""


def protocol_is_structural() -> bool:
    """Does a class satisfy a Protocol by matching methods, without inheriting it?"""
    return True


def abc_is_nominal() -> bool:
    """Does an ABC typically require inheritance (nominal typing)?"""
    return True
