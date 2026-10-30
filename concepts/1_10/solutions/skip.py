"""Solutions for the 1.10 skip check."""


def httpx_has_a_default_timeout() -> bool:
    """Does httpx apply a default timeout (unlike requests, which waits forever)?"""
    return True


def skipping_timeouts_is_fine_in_prod() -> bool:
    """Is it fine to omit timeouts on DocsDesk HTTP calls in production?"""
    return False
