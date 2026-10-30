"""2–3 minute skip check for 0.12."""


def slice_includes_the_stop_index() -> bool:
    """Does items[1:3] include index 3?"""
    raise NotImplementedError


def list_slice_copies() -> bool:
    """Does items[:] copy a list instead of aliasing it?"""
    raise NotImplementedError
