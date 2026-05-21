import asyncio
import os
import urllib.request
import urllib.parse
import json

# Fallback images
CITY_IMAGES = {
    "Tokyo": [
        "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?q=80&w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?q=80&w=800&auto=format&fit=crop"
    ],
    "Paris": [
        "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?q=80&w=800&auto=format&fit=crop"
    ],
    "New York":[
        "https://images.unsplash.com/photo-1496588152823-86ff7695e68f?q=80&w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1522083165195-3424ed129620?q=80&w=800&auto=format&fit=crop"
    ],
    "Kyoto": [
        "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?q=80&w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1528164344705-47542687000d?q=80&w=800&auto=format&fit=crop"
    ],
    "London": [
        "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?q=80&w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1526129318478-62ed807ebdf9?q=80&w=800&auto=format&fit=crop"
    ],
}

async def get_images(city: str):
    api_key = os.getenv("UNSPLASH_API_KEY")
    
    if api_key:
        try:
            loop = asyncio.get_event_loop()
            url = f"https://api.unsplash.com/search/photos?query={urllib.parse.quote(city)}&per_page=2&orientation=landscape"
            req = urllib.request.Request(url, headers={"Authorization": f"Client-ID {api_key}"})
            
            def fetch():
                with urllib.request.urlopen(req) as response:
                    return json.loads(response.read())
            
            data = await loop.run_in_executor(None, fetch)
            results = data.get("results", [])
            
            if len(results) >= 2:
                return [
                    results[0]["urls"]["regular"],
                    results[1]["urls"]["regular"]
                ]
        except Exception as e:
            print(f"Unsplash API error: {e}")
            pass

    await asyncio.sleep(1) 
    #fallback to default
    default = [
        "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?q=80&w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=800&auto=format&fit=crop"
    ]
    return CITY_IMAGES.get(city, default)

