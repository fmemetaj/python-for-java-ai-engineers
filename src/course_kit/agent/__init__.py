"""From-scratch agent loop, memory, tracing, a thin framework facade, and fake MCP.

The loop is the production path. The facade exists only so Module 5.5 can
ask "what did a framework buy us?" without adding LangChain or the OpenAI
Agents SDK as a dependency. MCP is a fake JSON-RPC server for 5.6.
"""

from .decide import classify_orchestration, should_use_agent
from .facade import Agent, Runner
from .loop import AgentResult, AgentState, run_agent_loop
from .mcp import FakeMcpServer, mcp_tools_to_openai
from .memory import AgentMemory, MemoryItem
from .trace import AgentTrace, Span

__all__ = [
    "Agent",
    "AgentMemory",
    "AgentResult",
    "AgentState",
    "AgentTrace",
    "FakeMcpServer",
    "MemoryItem",
    "Runner",
    "Span",
    "classify_orchestration",
    "mcp_tools_to_openai",
    "run_agent_loop",
    "should_use_agent",
]
