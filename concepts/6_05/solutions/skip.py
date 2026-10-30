"""Solutions for the skip check for 6.5."""


def retrieved_docs_can_carry_injected_instructions() -> bool:
    """Can a document you retrieved contain instructions that override your prompt?"""
    return True


def prompt_injection_is_the_same_as_sql_injection() -> bool:
    """Is prompt injection the same bug class as SQL injection, with the same fix?"""
    return False
