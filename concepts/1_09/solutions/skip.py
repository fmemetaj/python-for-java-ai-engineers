"""Solutions for the 1.9 skip check."""


def patch_where_looked_up() -> bool:
    """Should you patch the name in the module that *looks it up*, not where it was defined?"""
    return True


def patch_the_stdlib_always() -> bool:
    """Is patching `httpx.get` globally always the right target?"""
    return False
