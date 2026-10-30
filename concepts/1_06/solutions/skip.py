"""Solutions for the 1.6 skip check."""


def use_module_logger_not_print() -> bool:
    """Should library/service code use `logging.getLogger(__name__)` rather than print?"""
    return True


def log_the_api_key_at_debug() -> bool:
    """Is it acceptable to log OPENAI_API_KEY at DEBUG because DEBUG is off in prod?"""
    return False
