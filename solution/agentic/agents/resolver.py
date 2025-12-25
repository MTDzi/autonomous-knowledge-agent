from langgraph.types import Command

from agentic.agents.states import AgentState
from agentic.agents.orchestrator import ORCHESTRATOR_AGENT_NAME

RESOLUTION_AGENT_NAME = "resolution_agent"


class ResolutionAgent:
    def __init__(self, llm):
        self.llm = llm

    def __call__(self, state: AgentState):
        # Logic to provide the final resolution based on the gathered information
        state["response"] = "Based on your previous tickets and reservations, here is the resolution to your issue."

        return Command(goto=ORCHESTRATOR_AGENT_NAME)
