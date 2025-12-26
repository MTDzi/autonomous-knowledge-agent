from typing import Literal

from langgraph.types import Command

from agentic.agents.states import AgentState
from agentic.agents.agent_names import ORCHESTRATOR_AGENT_NAME


class TicketFetcherAgent:
    def __init__(self):
        self.path_to_tickets_db = "path/to/tickets_db.json"

    def __call__(self, state: AgentState) -> Command[Literal[ORCHESTRATOR_AGENT_NAME]]:
        # Logic to fetch tickets based on the ticket information
        state["previous_tickets"] = [
            {"ticket_id": "123", "issue": "Unable to login to my account."},
            {"ticket_id": "456", "issue": "How to change my subscription plan?"}
        ]

        return Command(goto=ORCHESTRATOR_AGENT_NAME)
