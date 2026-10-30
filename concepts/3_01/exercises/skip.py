"""2–3 minute skip check for 3.1."""


def structured_outputs_use_json_schema() -> bool:
    """Do Structured Outputs take a JSON Schema (often from a Pydantic model)?"""
    raise NotImplementedError


def assistants_api_is_required_for_json() -> bool:
    """Must you use the sunset Assistants API to get JSON from a model?"""
    raise NotImplementedError
