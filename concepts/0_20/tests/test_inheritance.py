from course_kit.loader import load_concept_module

inh = load_concept_module("0_20", "inheritance")


def test_search_uses_super() -> None:
    assert inh.Search().tag() == "search:tool"


def test_mro_left_to_right() -> None:
    names = inh.mro_names(inh.SearchWithMixin)
    assert names[0] == "SearchWithMixin"
    assert names[1] == "Mixin"
    assert names[2] == "Search"
    assert names[-1] == "object"


def test_mixin_wins_tag() -> None:
    assert inh.SearchWithMixin().tag() == "mixin"
