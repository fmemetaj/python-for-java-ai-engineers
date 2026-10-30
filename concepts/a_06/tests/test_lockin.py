from course_kit.loader import load_concept_module

lockin = load_concept_module("a_06", "lockin")


def test_hosted_not_ci_honest() -> None:
    row = lockin.flags(vendor_chunking=True, exportable=False, billed_separately=True)
    assert row["ci_honest"] is False
    assert row["billed_separately"] is True


def test_own_is_ci_honest() -> None:
    row = lockin.flags(vendor_chunking=False, exportable=True, billed_separately=False)
    assert row["ci_honest"] is True
