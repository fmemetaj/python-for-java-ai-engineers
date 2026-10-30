from course_kit.loader import load_concept_module

usage = load_concept_module("2_02", "usage")


def test_parse_flat() -> None:
    parsed = usage.parse_usage(
        {"input_tokens": 100, "output_tokens": 20, "total_tokens": 120, "cached_tokens": 40}
    )
    assert parsed["cached_tokens"] == 40
    assert parsed["input_tokens"] == 100


def test_parse_nested_cached() -> None:
    parsed = usage.parse_usage(
        {
            "input_tokens": 100,
            "output_tokens": 5,
            "input_tokens_details": {"cached_tokens": 80},
        }
    )
    assert parsed["cached_tokens"] == 80
    assert parsed["total_tokens"] == 105


def test_uncached() -> None:
    assert (
        usage.uncached_input({"input_tokens": 100, "output_tokens": 0, "cached_tokens": 25}) == 75
    )
