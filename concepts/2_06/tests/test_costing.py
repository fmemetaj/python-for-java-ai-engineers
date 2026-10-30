from course_kit.loader import load_concept_module

costing = load_concept_module("2_06", "costing")


def test_hand_computed_gpt41() -> None:
    amount = costing.cost_of(
        {"input_tokens": 1000, "output_tokens": 500, "cached_tokens": 0},
        "gpt-4.1-mini",
    )
    assert abs(amount - 0.0012) < 1e-12


def test_cached() -> None:
    amount = costing.cost_of(
        {"input_tokens": 1000, "output_tokens": 500, "cached_tokens": 800},
        "gpt-4.1-mini",
    )
    assert abs(amount - 0.00096) < 1e-12
