# Importing all agent classes into the package namespace
from .orchestrator import OrchestratorAgent
from .ticket_classifier import TicketClassifierAgent
from .ticket_fetcher import TicketFetcherAgent
from .reservation_fetcher import ReservationFetcherAgent
from .articles_fetcher import ArticlesFetcherAgent
from .resolver import ResolutionAgent
from .escalator import EscalationAgent
from .memory_updater import MemoryUpdaterAgent

# Define __all__ to control what is exported when someone uses "from agentic.agents import *"
__all__ = [
    "OrchestratorAgent",
    "TicketClassifierAgent",
    "TicketFetcherAgent",
    "ReservationFetcherAgent",
    "ArticlesFetcherAgent",
    "ResolutionAgent",
    "EscalationAgent",
    "MemoryUpdaterAgent",
]
