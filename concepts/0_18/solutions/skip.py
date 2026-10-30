"""Solutions for the 0.18 skip check."""


def eq_defaults_to_identity() -> bool:
    """Without __eq__, does == compare object identity?"""
    return True


def repr_is_for_developers() -> bool:
    """Is __repr__ the debug representation (like a better toString for logs)?"""
    return True
