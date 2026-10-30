"""Solutions for the skip check for A.7."""


def lockfile_pin_must_match_the_declared_version() -> bool:
    """Must uv.lock match the version you think you declared?"""
    return True


def a_maven_range_in_python_is_as_reproducible_as_uv_lock() -> bool:
    """Is a loose version range as reproducible as a committed lockfile?"""
    return False
