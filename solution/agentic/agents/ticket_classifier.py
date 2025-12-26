from typing import Literal

from langgraph.types import Command
from langchain_core.prompts import ChatPromptTemplate

from agentic.agents.states import AgentState, create_dynamic_classifier_state
from agentic.agents.agent_names import ORCHESTRATOR_AGENT_NAME


class TicketClassifierAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are a support classifier for Account: {account_id}."
                "Assign tags to the user's support ticket into appropriate categories based on the provided tags in the output schema."
                "The ticket might require multiple tags, here's a couple of examples:\n"

                "How to Reserve a Spot for an Event --> Tags: reservation, events, booking, attendance\n"
                "Changing your Registered Email Address --> Tags: security, account, email, login\n"
                "Equipment and Rentals --> Tags: equipment, rentals, preparation, liability\n"
                "Changing the Location of your Subscription --> Tags: location, account, settings, travel\n\n"

                "Some of the tickets might be ambiguous, so use your best judgement to assign the most relevant tags.\n\n"

                "Once you assigned the tags, please, assess whether the ticket might require for the downstream agent to fetch the user's previous tickets to fully address the issue.\n\n"

                "Also, assess whether the ticket is related to reservations or event bookings -- this will determine whether a downstream agent should fetch that data.\n\n"

                "Once all that is done, make a self-assessment on whether you managed to classify the ticket clearly."

            )),
            ("user", "Classify this ticket:\n\n{ticket_text}\n\nwith the following metadata:\n\n{ticket_metadata}")
        ])

    def __call__(self, state: AgentState) -> Command[Literal[ORCHESTRATOR_AGENT_NAME]]:
        """
        TODO
        """
        account_id = state["account_id"]
        
        DynamicClassifierState = create_dynamic_classifier_state(account_id)

        chain = self.prompt | self.llm.with_structured_output(DynamicClassifierState)
        
        result = chain.invoke({
            "ticket_text": state["ticket_text"],
            "ticket_metadata": state["ticket_metadata"],
            "account_id": account_id
        })
        state["is_ticket_classified_score"] = result.is_ticket_classified_score
        state["needs_info_about_previous_user_tickets_score"] = result.needs_info_about_previous_user_tickets_score
        state["needs_info_about_reservations_score"] = result.needs_info_about_reservations_score
        state["tags"] = result.tags
        
        return Command(goto=ORCHESTRATOR_AGENT_NAME)
