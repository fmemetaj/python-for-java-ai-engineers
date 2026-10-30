"""Solutions for the 1.4 skip check."""


def src_layout_keeps_imports_clean() -> bool:
    """Does putting packages under src/ stop tests from importing the unfinished tree by accident?"""
    return True


def console_scripts_equal_public_static_void_main() -> bool:
    """Is a console script entry point the same thing as `public static void main` in the class file name?"""
    return False
