from course_kit.loader import load_concept_module

skip = load_concept_module("a_08", "skip")


def test_true_fact() -> None:
    assert skip.assistants_api_is_sunset_and_out_of_scope() is True


def test_false_fact() -> None:
    assert skip.client_chat_completions_create_is_the_same_as_the_removed_0x_helper() is False
