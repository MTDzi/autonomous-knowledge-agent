from typing import Literal
from pathlib import Path

from diskcache import Cache

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
    MEMORY_UPDATER_AGENT_NAME,
)


class OrchestratorAgent:
    def __init__(
            self,
            is_ticket_classified_score_threshold: float = 70.0,
            needs_info_about_previous_user_tickets_threshold: float = 70.0,
            needs_info_about_reservations_threshold: float = 70.0,
            is_resolved_score_threshold: float = 70.0,
            cache_directory: Path = Path("cache_directory"),
    ):
        self.is_ticket_classified_score_threshold = is_ticket_classified_score_threshold
        self.needs_info_about_previous_user_tickets_threshold = needs_info_about_previous_user_tickets_threshold
        self.needs_info_about_reservations_threshold = needs_info_about_reservations_threshold
        self.is_resolved_score_threshold = is_resolved_score_threshold
        self.cache = Cache(cache_directory)
        self.agent_list = [END, MEMORY_UPDATER_AGENT_NAME, RESOLUTION_AGENT_NAME, ARTICLE_FETCHER_AGENT_NAME, TICKET_CLASSIFIER_AGENT_NAME]


    def __call__(self, state: AgentState) -> Command[Literal[TICKET_CLASSIFIER_AGENT_NAME, TICKET_FETCHER_AGENT_NAME,
                                                             RESERVATION_FETCHER_AGENT_NAME, ARTICLE_FETCHER_AGENT_NAME,
                                                             RESOLUTION_AGENT_NAME, ESCALATION_AGENT_NAME,
                                                             MEMORY_UPDATER_AGENT_NAME, END]]:

        # Start off by extracting user preferences
        if user_id := state["user_id"]:     
            state["user_preference"] = self.cache.get(user_id)
        else:
            state["user_preference"] = None

        most_recent_agent = ORCHESTRATOR_AGENT_NAME
        while self.agent_list:
            next_step = self.agent_list.pop()
            print(f"Orchestrator delegating to: {next_step}")

            # Handle output from the ticket classifier agent
            if most_recent_agent == TICKET_CLASSIFIER_AGENT_NAME:
                if state['is_ticket_classified_score'] >= self.is_ticket_classified_score_threshold:
                    if state['needs_info_about_previous_user_tickets_score'] >= self.needs_info_about_previous_user_tickets_threshold:
                        self.agent_list.append(TICKET_FETCHER_AGENT_NAME)
                    elif state['needs_info_about_reservations_score'] >= self.needs_info_about_reservations_threshold:
                        self.agent_list.append(RESERVATION_FETCHER_AGENT_NAME)

            # Handle output from the resolution agent
            if most_recent_agent == RESOLUTION_AGENT_NAME:
                if state['is_resolved_score'] < self.is_resolved_score_threshold:
                    print("\t! Orchestrator deciding to escalate the ticket !")
                    self.agent_list.append(ESCALATION_AGENT_NAME)

            # Handle output from the memory updater agent
            if most_recent_agent == MEMORY_UPDATER_AGENT_NAME:
                if state["should_update_preference"]:
                    if user_id := state["user_id"]:
                        self.cache.set(user_id, state["new_preference"])

            # Remember which node we just came from
            most_recent_agent = next_step

            return Command(goto=next_step)

        raise ValueError("Orchestrator has no more agents to delegate to, the final one should have been END.")

    def reset(self):
        self.agent_list = [END, MEMORY_UPDATER_AGENT_NAME, RESOLUTION_AGENT_NAME, ARTICLE_FETCHER_AGENT_NAME, TICKET_CLASSIFIER_AGENT_NAME]
