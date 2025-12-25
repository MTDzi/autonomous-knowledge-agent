from langgraph.types import Command

from agentic.agents.states import AgentState
from agentic.agents.orchestrator import ORCHESTRATOR_AGENT_NAME

TICKET_FETCHER_AGENT_NAME = "ticket_fetcher_agent"


class TicketFetcherAgent:
    def __init__(self):
        self.path_to_tickets_db = "path/to/tickets_db.json"

    def __call__(self, state: AgentState):
        # Logic to fetch tickets based on the ticket information
        state["previous_tickets"] = [
            {"ticket_id": "123", "issue": "Unable to login to my account."},
            {"ticket_id": "456", "issue": "How to change my subscription plan?"}
        ]

        return Command(goto=ORCHESTRATOR_AGENT_NAME)
