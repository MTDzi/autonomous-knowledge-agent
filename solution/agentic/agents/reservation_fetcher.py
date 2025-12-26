from typing import Literal

from langgraph.types import Command

from agentic.agents.states import AgentState
from agentic.agents.agent_names import ORCHESTRATOR_AGENT_NAME


class ReservationFetcherAgent:
    def __init__(self, ):
        self.path_to_reservations_db = "path/to/reservations_db.json"

    def __call__(self, state: AgentState) -> Command[Literal[ORCHESTRATOR_AGENT_NAME]]:
        # Logic to fetch reservations based on the ticket information
        state["reservations"] = [
            {"reservation_id": "789", "event": "Annual Conference", "date": "2023-09-15"},
            {"reservation_id": "101", "event": "Monthly Meetup", "date": "2023-10-05"}
        ]

        return Command(goto=ORCHESTRATOR_AGENT_NAME)
