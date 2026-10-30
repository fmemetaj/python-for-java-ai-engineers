"""Solutions for the skip check for 2.7."""


def responses_uses_input_not_messages() -> bool:
    """Does the Responses API take `input` (and optional instructions) instead of a messages array?"""
    return True


def assistants_api_is_current() -> bool:
    """Is the Assistants API still the API this course should teach?"""
    return False
