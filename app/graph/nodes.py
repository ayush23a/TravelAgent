import asyncio
from typing import Dict, Any
from app.graph.state import TravelState
from app.services.llm_services import get_groq, get_gemini
from app.services.vector_store import retrieve_city_info
from app.services.search_service import search_city_info
from app.services.weather_services import get_weather
from app.services.image_service import get_images
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser

def extract_city_node(state: TravelState) -> Dict[str, Any]:
    query = state.get("user_query", "")
    previous_city = state.get("city", "")
    
    llm = get_groq()
    if not llm:
        llm = get_gemini() 
        
    class CityExtract(BaseModel):
        city: str = Field(description="The name of the destination city")
    
    parser = JsonOutputParser(pydantic_object=CityExtract)
    prompt = PromptTemplate(
        template="""You are a travel routing agent.
                    Extract the destination city from the user query.
                    The user's previous city context was: '{previous_city}'.
                    If the query does NOT mention a new city (e.g., 'what about next week?', 'more info'), you MUST return '{previous_city}'.
                    If a NEW city is explicitly mentioned, return the NEW city.
                    {format_instructions}
                    Query: {query}
                    """,
        input_variables=["query", "previous_city"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | llm | parser
    
    try:
        result = chain.invoke({"query": query, "previous_city": previous_city})
        extracted_city = result.get("city", "").strip()
        
        if not extracted_city or extracted_city.lower() in ["none", "null", "unknown"]:
            return {"city": previous_city}
            
        return {"city": extracted_city}
    except Exception as e:
        print(f"Extraction failed: {e}")
        return {"city": previous_city if previous_city else query.split()[-1]}

def retrieval_node(state: TravelState) -> Dict[str, Any]:
    city = state.get("city", "")
    info = retrieve_city_info(city)
    return {"city_summary": info, "source": "vector_db"}

async def web_search_node(state: TravelState) -> Dict[str, Any]:
    city = state.get("city", "")
    info = await search_city_info(city)
    return {"city_summary": info, "source": "web_search"}

def summary_node(state: TravelState) -> Dict[str, Any]:
    city = state.get("city", "")
    context = state.get("city_summary", "")
    source = state.get("source", "")
    
    prompt = f"""
        You are a professional travel guide.
        Write a concise and engaging travel overview for {city}.

        Context:
        {context}

        Instructions:
        - Keep it under 2 paragraphs
        - Mention culture, attractions, food, and travel experience
        - Avoid generic AI-style marketing language
        - Sound informative and natural
        """
    
    llm = get_gemini()
    fallback_llm = get_groq()
    
    try:
        if llm:
            res = llm.invoke(prompt)
            summary = res.content
        else:
            res = fallback_llm.invoke(prompt)
            summary = res.content
    except Exception as e:
        print(f"Gemini failed, falling back to Groq: {e}")
        if fallback_llm:
            res = fallback_llm.invoke(prompt)
            summary = res.content
        else:
            summary = f"Could not generate summary for {city}."
            
    return {"city_summary": summary}

async def parallel_fetch_node(state: TravelState) -> Dict[str, Any]:
    """Fetches weather and images in parallel."""
    city = state.get("city", "")
    
    weather_task = get_weather(city)
    image_task = get_images(city)
    
    weather_forecast, image_urls = await asyncio.gather(weather_task, image_task)
    
    return {
        "weather_forecast": weather_forecast,
        "image_urls": image_urls
    }

def aggregation_node(state: TravelState) -> Dict[str, Any]:

    return state
