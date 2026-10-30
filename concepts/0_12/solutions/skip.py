"""Solutions for the 0.12 skip check."""


def slice_includes_the_stop_index() -> bool:
    """Does items[1:3] include index 3?"""
    return False


def list_slice_copies() -> bool:
    """Does items[:] copy a list instead of aliasing it?"""
    return True
