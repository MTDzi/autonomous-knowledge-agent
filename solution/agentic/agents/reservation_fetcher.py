from typing import Literal

from langgraph.types import Command
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent

from agentic.agents.states import AgentState, ReservationFetcherResult
from agentic.agents.agent_names import ORCHESTRATOR_AGENT_NAME
from agentic.tools.tools import fetch_reservations


class ReservationFetcherAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are an agent for Account: account_id={account_id} that needs to extract reservations from the database."

                "Based on the user_id, fetch the most relevant reservations from the database."
            )),
            ("user", "user_id:\n\n{user_id}"),
        ])
        self.agent = create_react_agent(
            model=self.llm,
            tools=[fetch_reservations],
            response_format=ReservationFetcherResult,
        )

    def __call__(self, state: AgentState) -> Command[Literal[ORCHESTRATOR_AGENT_NAME]]:
        # Logic to fetch reservations based on the user_id
        result = self.agent.invoke({
            "messages": self.prompt.invoke({
                "user_id": state['user_id'],
            }).messages,
        })
        structured_response = result["structured_response"]

        return Command(
            goto=ORCHESTRATOR_AGENT_NAME,
            update={
                "reservations": [
                    {
                        'content': reservation.reservation_details,
                        'status': reservation.reservation_status,
                        'other': reservation.reservation_other,
                    }
                    for reservation in structured_response.reservations
                ]
            }
        )

