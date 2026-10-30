"""Solutions for the 1.3 skip check."""


def venv_is_per_project() -> bool:
    """Is `.venv` a per-project interpreter + site-packages tree?"""
    return True


def one_global_site_packages_is_enough() -> bool:
    """Is one global site-packages directory enough for every course project?"""
    return False
