from course_kit.loader import load_concept_module

tokens = load_concept_module("2_02", "tokens")


def test_empty_is_zero() -> None:
    assert tokens.estimate_tokens("") == 0


def test_four_chars() -> None:
    assert tokens.estimate_tokens("abcd") == 1
    assert tokens.estimate_tokens("abcdefgh") == 2


def test_whitespace_count() -> None:
    assert tokens.whitespace_token_count("one two  three") == 3
