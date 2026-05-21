from pydantic import BaseModel
from typing import TypedDict, Annotated, List, Dict
from langchain_core.messages import BaseMessage

class FinalResponse(BaseModel):
    city_summary: str
    weather_forecast: List[dict]
    image_urls: List[str]

    




