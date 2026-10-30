"""Solutions for the skip check for 2.2."""


def tokens_are_the_billing_unit() -> bool:
    """Are tokens the unit OpenAI uses to bill LLM calls?"""
    return True


def tokens_equal_whitespace_words() -> bool:
    """Is splitting on whitespace a correct tokenizer for bills?"""
    return False
