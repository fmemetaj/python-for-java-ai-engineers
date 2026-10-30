from course_kit.loader import load_concept_module

fields = load_concept_module("7_05", "fields")


def test_fields() -> None:
    names = fields.cost_report_fields()
    for key in (
        "requests",
        "model",
        "usd_per_request",
        "usd_per_100",
        "pricing_source",
        "pricing_retrieved",
        "assumptions",
        "provider",
    ):
        assert key in names
