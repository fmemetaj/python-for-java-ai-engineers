from course_kit.loader import load_concept_module

skip = load_concept_module("0_03", "skip")


def test_assignment_does_not_copy() -> None:
    assert skip.assignment_copies_a_list() is False


def test_mutation_is_shared() -> None:
    assert skip.append_is_visible_through_aliases() is True
