"""2–3 minute skip check for 2.5."""


def default_provider_is_fake() -> bool:
    """Is the default LLM_PROVIDER fake so CI stays offline?"""
    raise NotImplementedError


def assistants_is_a_valid_provider() -> bool:
    """Is 'assistants' a valid LLM_PROVIDER in this course?"""
    raise NotImplementedError
