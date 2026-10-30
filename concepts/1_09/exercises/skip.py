"""2–3 minute skip check for 1.9."""


def patch_where_looked_up() -> bool:
    """Should you patch the name in the module that *looks it up*, not where it was defined?"""
    raise NotImplementedError


def patch_the_stdlib_always() -> bool:
    """Is patching `httpx.get` globally always the right target?"""
    raise NotImplementedError
