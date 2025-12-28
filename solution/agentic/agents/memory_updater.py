from typing import Literal

from langgraph.types import Command
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent

from agentic.agents.states import AgentState, MemoryUpdate
from agentic.agents.agent_names import ORCHESTRATOR_AGENT_NAME


class MemoryUpdaterAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are a Long-Term Memory Manager. Your job is to analyze a support interaction"
                " and decide if there is information worth saving for future visits."
                
                "Focus on:"
                "1. User preferences (e.g., tone, technical level)."
                "2. Recurring issues."
                "3. Successful resolutions for complex problems."
            )),
            ("user", "Ticket text:\n\n{ticket_text}\n\nResolution:\n\n{resolution_text}\n\nEscalation message (if any):\n\n{escalation_reason}")
        ])

    def __call__(self, state: AgentState) -> Command[Literal[ORCHESTRATOR_AGENT_NAME]]:
        chain = self.prompt | self.llm.with_structured_output(MemoryUpdate)

        result = chain.invoke({
            "ticket_text": state["ticket_text"],
            "resolution_text": state["resolution_text"],
            "escalation_reason": state.get("escalation_reason", "")
        })

        return Command(
            goto=ORCHESTRATOR_AGENT_NAME,
            update={
                "should_update_preference": result.should_update_preference,
                "new_preference": result.new_preference,
            }
        )
