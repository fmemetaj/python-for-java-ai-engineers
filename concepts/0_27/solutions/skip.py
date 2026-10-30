"""Solutions for the 0.27 skip check."""


def file_is_a_module() -> bool:
    """Is a .py file a module?"""
    return True


def init_marks_a_package() -> bool:
    """Does a directory with __init__.py (or a namespace package) act as a package?"""
    return True
