import requests
import asyncio
import logging

logger = logging.getLogger(__name__)

async def get_weather(city: str) -> list:
    """Fetch weather forecast data for a city."""
    try:
        # Geocode the city
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        
        loop = asyncio.get_event_loop()
        geo_response = await loop.run_in_executor(None, requests.get, geocode_url)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data.get("results"):
            logger.warning(f"Could not find coordinates for city: {city}")
            return [{"day": "N/A", "temperature": 0, "condition": "Unavailable"}]
            
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&daily=temperature_2m_max,weathercode"
            f"&timezone=auto"
        )
        weather_response = await loop.run_in_executor(None, requests.get, weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        forecast = []
        daily = weather_data.get("daily", {})
        if not daily:
            return [{"day": "N/A", "temperature": 0, "condition": "Unavailable"}]
            
        times = daily.get("time", [])
        temps = daily.get("temperature_2m_max", [])
        weather_codes = daily.get("weathercode", [])
        
        def code_to_condition(code):
            if code == 0: return "🌤️ Clear sky"
            if code in [1, 2, 3]: return "🌥️ Partly cloudy"
            if code in [45, 48]: return "🌫️ Fog"
            if code in [51, 53, 55, 56, 57]: return "🌧️ Drizzle"
            if code in [61, 63, 65, 66, 67]: return "🌨️ Rain"
            if code in [71, 73, 75, 77]: return "🌨️ Snow"
            if code in [80, 81, 82]: return "🌨️ Rain showers"
            if code in [95, 96, 99]: return "⛈️ Thunderstorm"
            return "Unknown"

        for i in range(min(7, len(times))):
            forecast.append({
                "day": times[i],
                "temperature": temps[i],
                "condition": code_to_condition(weather_codes[i])
            })
            
        return forecast
        
    except Exception as e:
        logger.error(f"Error fetching weather for {city}: {e}")
        return [{"day": "N/A", "temperature": 0, "condition": "Error fetching data"}]