from typing import Literal

from langgraph.types import Command

from agentic.agents.states import AgentState
from agentic.agents.agent_names import ORCHESTRATOR_AGENT_NAME


class EscalationAgent:
    def __init__(self, llm):
        self.llm = llm

    def __call__(self, state: AgentState) -> Command[Literal[ORCHESTRATOR_AGENT_NAME]]:
        # Logic to fetch articles based on the ticket information
        

        return Command(goto=ORCHESTRATOR_AGENT_NAME)
