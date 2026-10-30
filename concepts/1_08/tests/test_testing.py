from course_kit.loader import load_concept_module
import pytest

testing = load_concept_module("1_08", "testing")


def test_test_annotation() -> None:
    assert testing.junit_to_pytest("@Test") == "def test_..."


def test_before_each() -> None:
    assert testing.junit_to_pytest("@BeforeEach") == "@pytest.fixture"


def test_parameterized() -> None:
    assert testing.junit_to_pytest("@ParameterizedTest") == "@pytest.mark.parametrize"


def test_assert_equals() -> None:
    assert testing.junit_to_pytest("assertEquals") == "assert"


def test_unknown() -> None:
    with pytest.raises(ValueError):
        testing.junit_to_pytest("@SpringBootTest")


def test_parametrize_cases() -> None:
    assert testing.parametrize_cases(["auth", "tickets"]) == [("auth",), ("tickets",)]
