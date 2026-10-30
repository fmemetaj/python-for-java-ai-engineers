"""2–3 minute skip check for 0.22."""


def protocol_is_structural() -> bool:
    """Does a class satisfy a Protocol by matching methods, without inheriting it?"""
    raise NotImplementedError


def abc_is_nominal() -> bool:
    """Does an ABC typically require inheritance (nominal typing)?"""
    raise NotImplementedError
