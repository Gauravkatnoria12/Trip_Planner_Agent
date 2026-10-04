"""
Trip Planner Agent - Powered by Google ADK (Agent Development Kit)
==================================================================

This module defines the central AI Agent: `root_agent`.

HOW GOOGLE ADK AGENTS WORK:
1. `name`: A unique internal identifier for the agent.
2. `model`: The Gemini model backing the agent (e.g. 'gemini-2.5-flash').
3. `description`: High-level explanation of what the agent does (used when multi-agent routing is involved).
4. `instruction`: The system prompt. Guides the personality, goals, and rules for how the agent uses its tools.
5. `tools`: A list of Python functions the agent can invoke when formulating an answer.

ABOUT API KEYS:
- You do NOT need different API keys for different agents.
- A single GOOGLE_API_KEY covers this agent, all its tools, and any sub-agents.
"""

import os
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent

# Load environment variables from .env file (if present)
load_dotenv()

# Import our custom tools (supporting both package and standalone execution)
try:
    from .tools import get_destination_weather, get_attractions, estimate_budget
except (ImportError, ValueError):
    from tools import get_destination_weather, get_attractions, estimate_budget


# The core system instruction guiding our trip planner
INSTRUCTION = """
You are an enthusiastic, well-organized, and practical AI Trip Planner assistant.
Your goal is to help travelers design memorable, realistic, and budget-conscious itineraries.

Follow these operational guidelines:
1. Destination Weather: When a user specifies or asks about a destination, call `get_destination_weather`
   to check weather conditions and give smart packing suggestions.
2. Attractions & Activities: Call `get_attractions` to discover recommended cultural, natural, and culinary spots.
3. Budget Breakdown: When the user asks about costs or mentions duration/style, call `estimate_budget`
   to provide clear cost estimates.
4. Structured Itinerary: Structure multi-day itineraries logically by day:
   - Morning activity
   - Afternoon exploration
   - Evening dining / leisure
5. Tone: Helpful, concise, organized, and encouraging.
"""

# Define the root agent that Google ADK expects
root_agent = Agent(
    name="trip_planner",
    model=os.getenv("ADK_MODEL", "gemini-3.5-flash-lite"),
    description="A smart travel planner that organizes itineraries, checks weather, suggests attractions, and calculates travel budgets.",
    instruction=INSTRUCTION,
    tools=[
        get_destination_weather,
        get_attractions,
        estimate_budget,
    ],
)
