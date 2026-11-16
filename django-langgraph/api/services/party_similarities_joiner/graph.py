from langgraph.graph import StateGraph
from langgraph.graph import START, END
from langgraph.types import RetryPolicy

from .state import PartySimilaritiesState
from .nodes import grammatical_comparation_node, web_validation_node

def web_validation_route(state):
    
    if state.get("safe_match_found") is False:
        return "web_validation"

    return "__end__"
    
builder = StateGraph(PartySimilaritiesState)

builder.add_node(
    "grammatical_comparation",
    grammatical_comparation_node.filter_similarities,
)

builder.add_node(
    "web_validation",
    web_validation_node.web_validation
)

builder.add_edge(
    START,
    "grammatical_comparation"
)

builder.add_edge(
    "grammatical_comparation",
    "web_validation"
)

builder.add_edge(
    "web_validation",
    END
)

graph = builder.compile()