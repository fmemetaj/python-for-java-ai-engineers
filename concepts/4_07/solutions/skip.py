"""Solutions for the skip check for 4.7."""


def hybrid_combines_bm25_and_vectors() -> bool:
    """Does hybrid search combine a lexical BM25 score with a vector score?"""
    return True


def hosted_file_search_is_required_in_ci() -> bool:
    """Must graded DocsDesk eval call OpenAI hosted file_search?"""
    return False
