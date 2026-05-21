import asyncio


CITY_IMAGES = {
    "Tokyo": [
        "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf",
        "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?q=80&w=1200&auto=format&fit=crop"
    ],

    "Paris": [
        "https://images.unsplash.com/photo-1502602898657-3e91760cbb34",
        "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?q=80&w=1200&auto=format&fit=crop"
    ],

    "New York":[
        "https://images.unsplash.com/photo-1496588152823-86ff7695e68f?q=80&w=1600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1522083165195-3424ed129620?q=80&w=1600&auto=format&fit=crop"
    ],

    "Kyoto": [
        "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e",
        "https://images.unsplash.com/photo-1528164344705-47542687000d"
    ],

    "London": [
        "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad",
        "https://images.unsplash.com/photo-1526129318478-62ed807ebdf9"
    ],

    "Berlin": [
        "https://images.unsplash.com/photo-1560969184-10fe8719e047",
        "https://images.unsplash.com/photo-1587330979470-3595ac045ab0"
    ],

    "Sydney": [
        "https://images.unsplash.com/photo-1506973035872-a4ec16b8d4a5",
        "https://images.unsplash.com/photo-1523428461295-92770e70d7ae"
    ]
}


async def get_images(city: str):

    await asyncio.sleep(1)

    return CITY_IMAGES.get(
        city,
        [
            "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1600&auto=format&fit=crop"
        ]
    )

