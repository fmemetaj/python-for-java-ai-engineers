"""Solutions for the 1.7 skip check."""


def env_example_is_safe_to_commit() -> bool:
    """Is `.env.example` (names only, empty values) safe to commit?"""
    return True


def env_file_with_keys_is_safe_to_commit() -> bool:
    """Is `.env` with real keys safe to commit if the repo is private?"""
    return False
