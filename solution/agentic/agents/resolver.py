from typing import Literal

from langgraph.types import Command
from langchain_core.prompts import ChatPromptTemplate

from agentic.agents.states import AgentState, ResolutionResult
from agentic.agents.agent_names import ORCHESTRATOR_AGENT_NAME


class ResolutionAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are an expert formulting a final resolution to a ticket raised by a user."
                
                "Using all the information gathered so far, including previous tickets and reservations, provide a comprehensive resolution to the user's issue."
                "Make sure the resolution is clear, concise, and directly addresses the user's concerns."

                "You will also be given the original ticket text and metadata to ensure your resolution is relevant."
                "Also, consider any relevant articles that might assist in resolving the issue."

                "You will also be given a user preference, if available, to tailor your response accordingly."
                "\n\nBased on all this information, provide a final resolution."
                "However, if the ticket has nothing to do with the user's previous tickets, or reservations, or knowledge articles, make that clear by"
                " returning a score that is low."
            )),
            ("user", (
                "Resolve this ticket:\n\n{ticket_text}\n\nwith the following metadata:\n\n{ticket_metadata}"

                "Also, consider any relevant articles that might assist in resolving the issue:\n\n{relevant_articles}."

                "Assigned tags: {tags}\n\n"
                "User preference (if any):\n{user_preference}\n\n"
                "User reservations (if any):\n{reservations}\n\n"
                "User previous tickets (if any):\n{previous_tickets}\n\n"
            )),
        ])


    def __call__(self, state: AgentState) -> Command[Literal[ORCHESTRATOR_AGENT_NAME]]:
        # Logic to provide the final resolution based on the gathered information
        chain = self.prompt | self.llm.with_structured_output(ResolutionResult)
        result = chain.invoke({
            "ticket_text": state["ticket_text"],
            "ticket_metadata": state["ticket_metadata"],
            "relevant_articles": state["relevant_articles"],
            "tags": state["tags"],
            "user_preference": state["user_preference"],
            "reservations": state.get("reservations", "No reservations found."),
            "previous_tickets": state.get("previous_tickets", "No previous tickets found."),
        })

        return Command(
            goto=ORCHESTRATOR_AGENT_NAME,
            update={
                "resolution_text": result.resolution_text,
                "is_resolved_score": result.is_resolved_score,
            }
        )
