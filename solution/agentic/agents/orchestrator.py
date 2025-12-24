from agentic.agents.states import AgentState
from langgraph.types import Command


class OrchestratorAgent:
    def __init__(
            self,
            is_ticket_classified_score_threshold: float = 70.0,
            needs_info_about_previous_user_tickets_threshold: float = 70.0,
            needs_info_about_reservations_threshold: float = 70.0,
    ):
        self.is_ticket_classified_score_threshold = is_ticket_classified_score_threshold
        self.needs_info_about_previous_user_tickets_threshold = needs_info_about_previous_user_tickets_threshold
        self.needs_info_about_reservations_threshold = needs_info_about_reservations_threshold

    def __call__(self, state: AgentState): # -> Command[]:
        next_step = 'classifier_agent'

        if 'is_ticket_classified_score' in state:
            if state['is_ticket_classified_score'] >= self.is_ticket_classified_score_threshold:
                if state['needs_info_about_previous_user_tickets_score'] >= self.needs_info_about_previous_user_tickets_threshold:
                    next_step = 'fetch_previous_tickets_agent'
                elif state['needs_info_about_reservations_score'] >= self.needs_info_about_reservations_threshold:
                    next_step = 'fetch_reservations_agent'
                else:
                    next_step = 'final_resolution_agent'

        return Command(
            goto=next_step,
        )        
