"""2–3 minute skip check for 7.3. Still recommended — this concept is NEW."""


def write_tools_need_an_approval_gate() -> bool:
    """Must propose_page wait for an explicit human approval flag?"""
    return True


def rag_answers_may_omit_citations_in_v1() -> bool:
    """May a v1.0 ask() return prose with no citations?"""
    return False
