from typing import Literal, Type

from langgraph.types import Command
from langgraph.graph import END

from agentic.agents.states import AgentState
from agentic.agents.agent_names import (
    ORCHESTRATOR_AGENT_NAME,
    TICKET_CLASSIFIER_AGENT_NAME,
    TICKET_FETCHER_AGENT_NAME,
    RESERVATION_FETCHER_AGENT_NAME,
    ARTICLE_FETCHER_AGENT_NAME,
    RESOLUTION_AGENT_NAME,
    ESCALATION_AGENT_NAME,
)


class OrchestratorAgent:
    def __init__(
            self,
            is_ticket_classified_score_threshold: float = 70.0,
            needs_info_about_previous_user_tickets_threshold: float = 70.0,
            needs_info_about_reservations_threshold: float = 70.0,
            is_resolved_score_threshold: float = 70.0,
    ):
        self.is_ticket_classified_score_threshold = is_ticket_classified_score_threshold
        self.needs_info_about_previous_user_tickets_threshold = needs_info_about_previous_user_tickets_threshold
        self.needs_info_about_reservations_threshold = needs_info_about_reservations_threshold
        self.is_resolved_score_threshold = is_resolved_score_threshold
        self.agent_list = [END, RESOLUTION_AGENT_NAME, ARTICLE_FETCHER_AGENT_NAME, TICKET_CLASSIFIER_AGENT_NAME]

    def __call__(self, state: AgentState) -> Command[Literal[TICKET_CLASSIFIER_AGENT_NAME, TICKET_FETCHER_AGENT_NAME,
                                                          RESERVATION_FETCHER_AGENT_NAME, ARTICLE_FETCHER_AGENT_NAME,
                                                          RESOLUTION_AGENT_NAME, ESCALATION_AGENT_NAME, END]]:
        most_recent_agent = ORCHESTRATOR_AGENT_NAME
        while self.agent_list:
            next_step = self.agent_list.pop()

            # Handle output from the ticket classifier agent
            if most_recent_agent == TICKET_CLASSIFIER_AGENT_NAME:
                if state['is_ticket_classified_score'] >= self.is_ticket_classified_score_threshold:
                    if state['needs_info_about_previous_user_tickets_score'] >= self.needs_info_about_previous_user_tickets_threshold:
                        self.agent_list.append(TICKET_FETCHER_AGENT_NAME)
                    elif state['needs_info_about_reservations_score'] >= self.needs_info_about_reservations_threshold:
                        self.agent_list.append(RESERVATION_FETCHER_AGENT_NAME)
                else:
                    self.agent_list.append(RESOLUTION_AGENT_NAME)

            # Handle output from the resolution agent
            if most_recent_agent == RESOLUTION_AGENT_NAME:
                if state['is_resolved_score'] < self.is_resolved_score_threshold:
                    self.agent_list.append(ESCALATION_AGENT_NAME)

            # Remember which node we just came from
            most_recent_agent = next_step

            return Command(goto=next_step)

        raise ValueError("Orchestrator has no more agents to delegate to, the final one should have been END.")
