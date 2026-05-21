from app.graph.state import TravelState
from app.services.vector_store import retrieve_city_info

def route_to_retrieval_or_search(state: TravelState) -> str:
    
    city = state.get("city", "")
    info = retrieve_city_info(city)
    
    if info:
        return "retrieval_node"
    else:
        return "web_search_node"
