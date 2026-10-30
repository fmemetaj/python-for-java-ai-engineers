"""2–3 minute skip check for 4.1."""


def embeddings_are_dense_vectors() -> bool:
    """Is an embedding a dense vector of floats, not a readable paragraph?"""
    raise NotImplementedError


def assistants_api_is_used_for_embeddings() -> bool:
    """Must you call the sunset Assistants API to embed text?"""
    raise NotImplementedError
