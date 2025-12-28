from typing import Literal

from langgraph.types import Command
from langchain_core.prompts import ChatPromptTemplate

from agentic.agents.states import AgentState, EscalationResult
from agentic.agents.agent_names import ORCHESTRATOR_AGENT_NAME


class EscalationAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are an expert handling tickets for which no proper resolution was found by upstream agents / experts."

                "Using all the information gathered so far, including the ticket and metadata, as well as the insufficient resolution"
                " escalate the ticket appropriately."

                "Make sure to clearly state why the ticket is being escalated and what additional information or action is required."
                "For that, you will also have access to the relevant knowledge (FAQ) articles related to the ticket."

                "You will also have access to user preferences -- make sure to consider them when escalating the ticket."
            )),
            ("user", (
                "Find an escalation message for this ticket:\n\n{ticket_text}\n\nwith the following metadata:\n\n{ticket_metadata}"

                "Also, consider any relevant articles that might assist in resolving the issue:\n\n{relevant_articles}."

                "User preference (if any):\n{user_preference}\n\n"
            )),        
        ])


    def __call__(self, state: AgentState) -> Command[Literal[ORCHESTRATOR_AGENT_NAME]]:
        # Logic to escalate the ticket based on the gathered information
        chain = self.prompt | self.llm.with_structured_output(EscalationResult)

        result = chain.invoke({
            "ticket_text": state["ticket_text"],
            "ticket_metadata": state["ticket_metadata"],
            "relevant_articles": state["relevant_articles"],
            "user_preference": state["user_preference"]
        })

        return Command(
            goto=ORCHESTRATOR_AGENT_NAME,
            update={
                "escalation_reason": result.escalation_reason,
                "urgency_level": result.urgency_level,
            })
