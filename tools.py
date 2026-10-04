"""
Trip Planner Tools for Google ADK
=================================

In Google ADK, any standard Python function can be a tool!
Key concepts for Google ADK tools:
1. Type hints (e.g. `city: str`, `days: int`): ADK inspects these to tell the LLM
   what data types to provide when calling the function.
2. Docstring: The docstring is the prompt for the tool! The LLM reads the docstring
   to understand *when* to invoke the tool and what each parameter means.
3. Return value: Typically a string, dictionary, or list containing the tool's result,
   which is fed back to the LLM to formulate its response.
"""

from typing import Dict, Any


def get_destination_weather(city: str) -> str:
    """
    Get current weather information, average temperature, and packing tips for a travel destination.

    Args:
        city: Name of the destination city (e.g., 'Tokyo', 'Paris', 'New York').

    Returns:
        A formatted summary of current weather conditions and clothing advice.
    """
    city_normalized = city.strip().lower()

    # Pre-defined weather data for common destinations; realistic fallback for any other city
    weather_database = {
        "tokyo": {
            "condition": "Mild and pleasant",
            "temperature": "18°C (64°F)",
            "season": "Spring / Autumn transition",
            "packing_advice": "Light layers, a comfortable walking jacket, and an umbrella."
        },
        "paris": {
            "condition": "Partly cloudy with gentle breeze",
            "temperature": "16°C (61°F)",
            "season": "Spring",
            "packing_advice": "Trench coat, scarf, comfortable walking shoes for cobblestones."
        },
        "new york": {
            "condition": "Sunny and crisp",
            "temperature": "15°C (59°F)",
            "season": "Autumn",
            "packing_advice": "Medium jacket, versatile layers, flat walking shoes."
        },
        "london": {
            "condition": "Overcast with occasional light drizzle",
            "temperature": "13°C (55°F)",
            "season": "Spring",
            "packing_advice": "Waterproof jacket or umbrella, sweater, waterproof boots."
        },
        "rome": {
            "condition": "Warm and sunny",
            "temperature": "23°C (73°F)",
            "season": "Late Spring",
            "packing_advice": "Breathable cotton clothing, sunglasses, sun hat, sunscreen."
        },
        "dubai": {
            "condition": "Hot and sunny",
            "temperature": "32°C (90°F)",
            "season": "Summer",
            "packing_advice": "Light linen fabrics, sunglasses, sunscreen, light cardigan for air-conditioned indoors."
        }
    }

    if city_normalized in weather_database:
        data = weather_database[city_normalized]
    else:
        # Generous default fallback for any unlisted city
        data = {
            "condition": "Partly cloudy and moderate",
            "temperature": "20°C (68°F)",
            "season": "Temperate",
            "packing_advice": "Standard travel attire, light jacket for evenings, and comfortable walking shoes."
        }

    return (
        f"Weather for {city.title()}:\n"
        f"- Conditions: {data['condition']}\n"
        f"- Temperature: {data['temperature']}\n"
        f"- Season: {data['season']}\n"
        f"- Packing Recommendation: {data['packing_advice']}"
    )


def get_attractions(city: str, category: str = "all") -> str:
    """
    Discover top points of interest and attractions for a destination.

    Args:
        city: Name of the destination city.
        category: Filter by attraction type: 'culture', 'nature', 'food', or 'all'.

    Returns:
        A list of recommended spots and highlights.
    """
    city_normalized = city.strip().lower()

    attractions_db: Dict[str, Dict[str, list[str]]] = {
        "tokyo": {
            "culture": ["Senso-ji Temple (Asakusa)", "Meiji Shrine (Shibuya)", "Tokyo National Museum"],
            "nature": ["Shinjuku Gyoen National Garden", "Ueno Park", "Mount Takao (day trip)"],
            "food": ["Tsukiji Outer Market (fresh seafood)", "Omoide Yokocho (yakitori)", "Ramen Street in Tokyo Station"]
        },
        "paris": {
            "culture": ["Louvre Museum", "Musée d'Orsay", "Notre-Dame Cathedral"],
            "nature": ["Jardin du Luxembourg", "Tuileries Garden", "Seine River Bank stroll"],
            "food": ["Le Marais bakeries (croissants)", "Rue Cler market street", "Traditional bistros in Saint-Germain"]
        },
        "rome": {
            "culture": ["Colosseum & Roman Forum", "Vatican Museums & Sistine Chapel", "Pantheon"],
            "nature": ["Villa Borghese Gardens", "Appian Way Regional Park"],
            "food": ["Trastevere trattorias (cacio e pepe)", "Campo de' Fiori market", "Artisanal Gelaterias"]
        },
        "new york": {
            "culture": ["The Metropolitan Museum of Art (Met)", "Broadway Theater District", "Statue of Liberty"],
            "nature": ["Central Park", "High Line elevated park", "Brooklyn Bridge walk"],
            "food": ["Chelsea Market", "Chinatown dumpling spots", "Little Italy pizzerias"]
        }
    }

    city_data = attractions_db.get(
        city_normalized,
        {
            "culture": [f"{city.title()} Historic Old Town", f"{city.title()} Museum of Art", "Local Heritage Center"],
            "nature": [f"{city.title()} City Botanical Park", "Riverside Promenade", "Scenic Hill Lookout"],
            "food": ["Central Food Market", "Traditional Local Restaurants", "Street Food Alley"]
        }
    )

    category_clean = category.strip().lower()
    results = []

    if category_clean in ("all", "culture"):
        results.append(f"[Culture & Heritage]:\n  * " + "\n  * ".join(city_data["culture"]))
    if category_clean in ("all", "nature"):
        results.append(f"[Nature & Outdoors]:\n  * " + "\n  * ".join(city_data["nature"]))
    if category_clean in ("all", "food"):
        results.append(f"[Food & Culinary]:\n  * " + "\n  * ".join(city_data["food"]))

    return f"Attractions in {city.title()}:\n\n" + "\n\n".join(results)


def estimate_budget(destination: str, days: int, travel_style: str = "moderate") -> str:
    """
    Estimate the travel budget based on destination, number of days, and travel style.

    Args:
        destination: City or country of travel.
        days: Number of days of the trip (must be an integer, e.g. 3, 5, 7).
        travel_style: One of 'budget', 'moderate', or 'luxury'. Defaults to 'moderate'.

    Returns:
        Estimated daily and total costs breakdown in USD.
    """
    if days <= 0:
        days = 1

    style_clean = travel_style.strip().lower()

    # Base daily rates [lodging, food, activities/transport] in USD
    rates = {
        "budget": {"lodging": 45, "food": 25, "transport_activities": 15},
        "moderate": {"lodging": 120, "food": 60, "transport_activities": 40},
        "luxury": {"lodging": 350, "food": 160, "transport_activities": 120}
    }

    tier = rates.get(style_clean, rates["moderate"])
    daily_total = tier["lodging"] + tier["food"] + tier["transport_activities"]
    grand_total = daily_total * days

    return (
        f"Estimated Budget for {days} days in {destination.title()} ({style_clean.title()} Style):\n"
        f"- Lodging: ${tier['lodging']} / night (Total: ${tier['lodging'] * days})\n"
        f"- Food & Dining: ${tier['food']} / day (Total: ${tier['food'] * days})\n"
        f"- Local Transport & Sightseeing: ${tier['transport_activities']} / day (Total: ${tier['transport_activities'] * days})\n"
        f"-----------------------------------------\n"
        f"* Estimated Daily Cost: ${daily_total} USD\n"
        f"* Estimated Total Cost: ${grand_total} USD (excluding international flights)\n"
        f"Tip: Add 10-15% as a buffer for souvenirs and unexpected expenses."
    )
