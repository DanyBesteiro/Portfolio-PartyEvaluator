from langgraph.graph import StateGraph
from langgraph.graph import START, END
from langgraph.types import RetryPolicy

from .state import PartyResolutionState
from .nodes import detect_safe_match_node, web_validation_node, compare_results_node

def web_validation_route(state):
    
    if state.get("safe_match_found") is False:
        return "web_validation"

    return "__end__"
    
builder = StateGraph(PartyResolutionState)

builder.add_node(
    "detect_safe_match",
    detect_safe_match_node.detect_safe_match,
)

builder.add_node(
    "web_validation",
    web_validation_node.web_validation,
    retry=RetryPolicy(max_attempts=3, backoff_factor=2) 
)

builder.add_node(
    "compare_results",
    compare_results_node.compare_results
)

builder.add_edge(
    START,
    "detect_safe_match"
)

builder.add_edge(
    "detect_safe_match",
    "web_validation"
)

builder.add_edge(
    "web_validation",
    "compare_results"
)

builder.add_edge(
    "compare_results",
    END
)

graph = builder.compile()