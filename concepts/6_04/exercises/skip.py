"""2–3 minute skip check for 6.4. Still recommended — this concept is NEW."""


def cached_input_tokens_are_cheaper_than_uncached() -> bool:
    """Are prompt-cached input tokens billed at a lower rate than uncached input?"""
    raise NotImplementedError


def over_budget_calls_should_still_run() -> bool:
    """If remaining USD cannot cover the next call, should you still call the model?"""
    raise NotImplementedError
