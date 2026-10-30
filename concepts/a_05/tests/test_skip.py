from course_kit.loader import load_concept_module

skip = load_concept_module("a_05", "skip")


def test_true_fact() -> None:
    assert skip.hosted_file_search_is_a_model_tool_not_your_lucene_query() is True


def test_false_fact() -> None:
    assert skip.the_fake_loop_is_allowed_to_run_forever() is False
