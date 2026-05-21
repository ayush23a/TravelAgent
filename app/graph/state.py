from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage

class TravelState(TypedDict):
    user_query: str
    city: Optional[str]
    source: Optional[str]  # 'vector_db' or 'web_search'
    city_summary: Optional[str]
    weather_forecast: Optional[List[dict]]
    image_urls: Optional[List[str]]
    messages: Optional[List[BaseMessage]] 
