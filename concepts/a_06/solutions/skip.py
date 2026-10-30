"""Solutions for the skip check for A.6."""


def a_decision_record_belongs_in_the_portfolio() -> bool:
    """Should a hosted-vs-own choice be written down as a short decision record?"""
    return True


def vendor_chunking_is_ci_honest() -> bool:
    """Can you unit-test vendor-hosted chunking the way you test FakeEmbedder?"""
    return False
