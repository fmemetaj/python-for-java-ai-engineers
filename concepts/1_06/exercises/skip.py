"""2–3 minute skip check for 1.6."""


def use_module_logger_not_print() -> bool:
    """Should library/service code use `logging.getLogger(__name__)` rather than print?"""
    raise NotImplementedError


def log_the_api_key_at_debug() -> bool:
    """Is it acceptable to log OPENAI_API_KEY at DEBUG because DEBUG is off in prod?"""
    raise NotImplementedError
