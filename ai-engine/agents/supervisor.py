"""
Supervisor Agent — Routes user intent to specialized sub-agents.
Uses LangGraph for stateful multi-agent orchestration.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    input: str
    output: str
    agent: str
    messages: list


def supervisor_router(state: AgentState) -> Literal["researcher", "writer", "coder", "analyst", "finance", "__end__"]:
    routing_keywords = {
        "researcher": ["search", "research", "find", "look up", "what is", "who is"],
        "writer": ["write", "draft", "compose", "rewrite", "summarize", "translate"],
        "coder": ["code", "program", "debug", "function", "algorithm", "python", "javascript"],
        "analyst": ["analyze", "chart", "graph", "data", "statistics", "trend"],
        "finance": ["stock", "trade", "portfolio", "market", "finance", "investment"],
    }

    input_lower = state["input"].lower()
    for agent, keywords in routing_keywords.items():
        if any(kw in input_lower for kw in keywords):
            return agent
    return "researcher"


def build_supervisor_graph():
    workflow = StateGraph(AgentState)
    workflow.set_conditional_edge_source(supervisor_router)
    return workflow.compile()
