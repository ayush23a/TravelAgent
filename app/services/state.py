from pydantic import BaseModel
from typing import TypedDict, Annotated, List, Dict
from langchain_core.messages import BaseMessage

class TravelState(TypedDict):
    user_query: str
    city: str
    source: str
    city_summary: str
    weather_forecast: List
    image_url: List

