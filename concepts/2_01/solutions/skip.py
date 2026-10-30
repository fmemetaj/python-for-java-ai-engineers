"""Solutions for the skip check for 2.1."""


def sdk_is_configured_from_env() -> bool:
    """Does the official OpenAI Python SDK read OPENAI_API_KEY from the environment by default?"""
    return True


def assistants_api_is_the_current_api() -> bool:
    """Is the Assistants API the current API this course should call?"""
    return False
