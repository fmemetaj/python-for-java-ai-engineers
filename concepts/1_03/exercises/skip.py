"""2–3 minute skip check for 1.3."""


def venv_is_per_project() -> bool:
    """Is `.venv` a per-project interpreter + site-packages tree?"""
    raise NotImplementedError


def one_global_site_packages_is_enough() -> bool:
    """Is one global site-packages directory enough for every course project?"""
    raise NotImplementedError
