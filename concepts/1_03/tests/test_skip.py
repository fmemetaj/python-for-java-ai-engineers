from course_kit.loader import load_concept_module

skip = load_concept_module("1_03", "skip")


def test_per_project() -> None:
    assert skip.venv_is_per_project() is True


def test_not_global() -> None:
    assert skip.one_global_site_packages_is_enough() is False
