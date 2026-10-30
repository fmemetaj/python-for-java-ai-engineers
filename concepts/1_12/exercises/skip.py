"""2–3 minute skip check for 1.12."""


def backoff_grows_between_attempts() -> bool:
    """Does exponential backoff make each wait longer than the last?"""
    raise NotImplementedError


def retry_all_4xx() -> bool:
    """Should DocsDesk retry every HTTP 4xx (including 400 and 404)?"""
    raise NotImplementedError
