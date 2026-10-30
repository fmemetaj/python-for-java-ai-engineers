import pytest
from course_kit.loader import load_concept_module

tokens = load_concept_module("a_03", "tokens")


def test_low_detail_flat() -> None:
    assert tokens.image_tokens("low", 1024, 768) == 85
    assert tokens.image_tokens("low", 64, 64) == 85


def test_high_detail_tiles() -> None:
    # 1024x768 → 2x2 tiles of 512 → 85 + 170*4 = 765
    assert tokens.image_tokens("high", 1024, 768) == 765


def test_cost_uses_input_rate() -> None:
    amount = tokens.vision_cost_usd(
        image_tokens=85,
        text_input_tokens=15,
        output_tokens=20,
        input_per_million=0.40,
        output_per_million=1.60,
    )
    expected = (85 + 15) * 0.40 / 1_000_000 + 20 * 1.60 / 1_000_000
    assert abs(amount - expected) < 1e-12


def test_rejects_bad_detail() -> None:
    with pytest.raises(ValueError):
        tokens.image_tokens("medium", 100, 100)
