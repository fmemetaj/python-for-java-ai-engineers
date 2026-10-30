"""2–3 minute skip check for 0.18."""


def eq_defaults_to_identity() -> bool:
    """Without __eq__, does == compare object identity?"""
    raise NotImplementedError


def repr_is_for_developers() -> bool:
    """Is __repr__ the debug representation (like a better toString for logs)?"""
    raise NotImplementedError
