"""Solutions for the skip check for 2.3."""


def window_includes_output_tokens() -> bool:
    """Does a context window count output tokens as well as input tokens?"""
    return True


def context_window_is_unlimited() -> bool:
    """Can you send an entire git history in one call because modern windows are large?"""
    return False
