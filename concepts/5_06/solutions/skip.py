"""Solutions for the skip check for 5.6."""


def mcp_is_json_rpc() -> bool:
    """Is MCP a JSON-RPC 2.0 protocol for listing and calling tools?"""
    return True


def mcp_requires_the_assistants_api() -> bool:
    """Must you use the sunset Assistants API to speak MCP?"""
    return False
