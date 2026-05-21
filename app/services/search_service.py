import asyncio

async def search_city_info(city: str) -> str:

    await asyncio.sleep(1) # Simulate network latency
    
    mock_search_results = {
        "Berlin": "Berlin is the capital of Germany, known for its art scene, modern landmarks like the gold-colored, swoop-roofed Berliner Philharmonie, and historical sites like the Brandenburg Gate.",
        "London": "London, the capital of England and the United Kingdom, is a 21st-century city with history stretching back to Roman times. It features the iconic 'Big Ben' clock tower and Westminster Abbey.",
        "Kyoto": "Kyoto, once the capital of Japan, is a city on the island of Honshu. It's famous for its numerous classical Buddhist temples, as well as gardens, imperial palaces, Shinto shrines and traditional wooden houses.",
        "Sydney": "Sydney, capital of New South Wales and one of Australia's largest cities, is best known for its harbourfront Sydney Opera House, with a distinctive sail-like design."
    }
    
    return mock_search_results.get(
    city,
    f"""
    {city} is a globally recognized destination known for tourism, local culture, scenic attractions, food experiences, historical significance, and outdoor activities. Travelers often visit {city} for sightseeing,
    local cuisine, architecture, and cultural experiences.
    """
    )
