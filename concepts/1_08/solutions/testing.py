"""Translate JUnit 5 annotations into pytest forms (solution)."""

MAPPING = {
    "@Test": "def test_...",
    "@BeforeEach": "@pytest.fixture",
    "@ParameterizedTest": "@pytest.mark.parametrize",
    "assertEquals": "assert",
}


def junit_to_pytest(kind: str) -> str:
    """Map @Test, @BeforeEach, @ParameterizedTest, assertEquals to pytest."""
    try:
        return MAPPING[kind]
    except KeyError as exc:
        raise ValueError(f"unknown JUnit construct {kind!r}") from exc


def parametrize_cases(slugs: list[str]) -> list[tuple[str]]:
    """Return a list of 1-tuples pytest can unpack as @parametrize args."""
    return [(slug,) for slug in slugs]
