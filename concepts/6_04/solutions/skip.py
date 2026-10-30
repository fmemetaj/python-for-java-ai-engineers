"""Solutions for the skip check for 6.4."""


def cached_input_tokens_are_cheaper_than_uncached() -> bool:
    """Are prompt-cached input tokens billed at a lower rate than uncached input?"""
    return True


def over_budget_calls_should_still_run() -> bool:
    """If remaining USD cannot cover the next call, should you still call the model?"""
    return False
