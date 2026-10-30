from course_kit.loader import load_concept_module

binding = load_concept_module("0_03", "binding")


def test_rebind_leaves_alias_on_old_list() -> None:
    source = [1, 2]
    alias, rebound = binding.after_rebind(source)
    assert alias == [1, 2]
    assert alias is source
    assert rebound == [0]
    assert rebound is not source


def test_mutate_is_visible_on_both_names() -> None:
    source = [1, 2]
    alias, mutated = binding.after_mutate(source)
    assert alias == [1, 2, 99]
    assert mutated is alias
    assert mutated is source
