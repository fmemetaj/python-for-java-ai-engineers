"""Solutions for the skip check for 4.6."""


def recall_at_k_measures_retrieval() -> bool:
    """Is recall@k a retrieval metric (gold docs in the top-k), not a prose exact-match?"""
    return True


def junit_equals_on_live_prose_is_the_rag_gate() -> bool:
    """Should CI assert exact equality on live model wording to accept RAG?"""
    return False
