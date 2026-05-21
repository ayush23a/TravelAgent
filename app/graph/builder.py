from langgraph.graph import StateGraph, START, END
from app.graph.state import TravelState
from app.graph.nodes import (
    extract_city_node,
    retrieval_node,
    web_search_node,
    summary_node,
    parallel_fetch_node,
    aggregation_node
)
from app.graph.router import route_to_retrieval_or_search
from langgraph.checkpoint.memory import MemorySaver

def build_graph():
    workflow = StateGraph(TravelState)
    
    #nodes
    workflow.add_node("extract_city_node", extract_city_node)
    workflow.add_node("retrieval_node", retrieval_node)
    workflow.add_node("web_search_node", web_search_node)
    workflow.add_node("summary_node", summary_node)
    workflow.add_node("parallel_fetch_node", parallel_fetch_node)
    workflow.add_node("aggregation_node", aggregation_node)
    
    #edges
    workflow.add_edge(START, "extract_city_node")
    
    workflow.add_conditional_edges(
        "extract_city_node",
        route_to_retrieval_or_search,
        {
            "retrieval_node": "retrieval_node",
            "web_search_node": "web_search_node"
        }
    )
    

    workflow.add_edge("retrieval_node", "summary_node")
    workflow.add_edge("web_search_node", "summary_node")
    
    workflow.add_edge("summary_node", "parallel_fetch_node")
    
    workflow.add_edge("parallel_fetch_node", "aggregation_node")
    
    workflow.add_edge("aggregation_node", END)
    
    # memory checkpointer
    checkpointer = MemorySaver()
    
    app = workflow.compile(checkpointer=checkpointer)
    return app

_graph_instance = None

def get_graph():
    global _graph_instance
    if _graph_instance is None:
        _graph_instance = build_graph()
    return _graph_instance
