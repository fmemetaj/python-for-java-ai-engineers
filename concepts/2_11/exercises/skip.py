"""2–3 minute skip check for 2.11."""


def reasoning_tokens_bill_as_output() -> bool:
    """Are reasoning tokens billed as output tokens (not visible answer text)?"""
    raise NotImplementedError


def short_visible_answer_means_cheap() -> bool:
    """Does a short visible answer guarantee a cheap call on a reasoning model?"""
    raise NotImplementedError
