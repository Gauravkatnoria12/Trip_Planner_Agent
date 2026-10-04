"""
Trip Planner Agent Package for Google ADK
=========================================
Google ADK CLI (`adk run`, `adk web`, etc.) looks for `root_agent` in this package.
"""

from . import agent
from .agent import root_agent

__all__ = ["agent", "root_agent"]
