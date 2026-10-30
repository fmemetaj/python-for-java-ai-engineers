"""Solutions for the 1.12 skip check."""


def backoff_grows_between_attempts() -> bool:
    """Does exponential backoff make each wait longer than the last?"""
    return True


def retry_all_4xx() -> bool:
    """Should DocsDesk retry every HTTP 4xx (including 400 and 404)?"""
    return False
