from typing import Literal

from langgraph.types import Command
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent

from agentic.agents.states import AgentState, TicketFetcherResult
from agentic.agents.agent_names import ORCHESTRATOR_AGENT_NAME
from agentic.tools.tools import fetch_tickets


class TicketFetcherAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are an agent for Account: account_id={account_id} that needs to extract previous tickets from the database."

                "Based on the user_id and ticket_text, fetch the most relevant previous tickets from the database that can help resolve the user's issue."
            )),
            ("user", "Ticket text:\n\n{ticket_text}\n\nuser_id:\n\n{user_id}\n\naccount_id:\n\n{account_id}"),
        ])
        self.agent = create_react_agent(
            model=self.llm,
            tools=[fetch_tickets],
            response_format=TicketFetcherResult,
        )

    def __call__(self, state: AgentState) -> Command[Literal[ORCHESTRATOR_AGENT_NAME]]:
        # Logic to fetch tickets based on the user_id
        result = self.agent.invoke({
            "messages": self.prompt.invoke({
                "user_id": state['user_id'],
                "ticket_text": state["ticket_text"],
                "account_id": state['account_id'],
            }).messages,
        })
        structured_response = result["structured_response"]

        return Command(
            goto=ORCHESTRATOR_AGENT_NAME,
            update={
                "previous_tickets": [
                    {
                        'content': ticket.ticket_content,
                        'tags': ticket.ticket_tags,
                        'other': ticket.ticket_other,
                    }
                    for ticket in structured_response.previous_tickets
                ]
            }
        )
