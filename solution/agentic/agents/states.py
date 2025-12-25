from functools import cache
from typing import Literal, Type

from langgraph.graph.message import MessagesState
from pydantic import BaseModel, Field, create_model

from utils import get_available_tags


class AgentState(MessagesState):
    ticket_text: str
    ticket_metadata: dict[str, str]
    account_id: str
    user_id: str | None = None

    # Classification attributes
    tags: list[str]
    is_ticket_classified_score: float = -1.0
    needs_info_about_previous_user_tickets_score: float = -1.0
    needs_info_about_reservations_score: float = -1.0

    # Previous tickets attributes
    previous_tickets: list[dict[str, str]] = []
    
    # Reservations attributes
    reservations: list[dict[str, str]] = []

    # Articles attributes
    relevant_articles: list[dict[str, str]] = []


@cache
def create_dynamic_classifier_state(account_id: str) -> Type[BaseModel]:
    """
    Creates a Pydantic model on-the-fly using the available tags.
    """
    current_tags: list[str] = get_available_tags(account_id)
    
    # We create a Literal type from the list
    TagLiteral = Literal[tuple(current_tags)]
    
    # Define the fields for our dynamic model
    fields = {
        "is_ticket_classified_score": (
            float, 
            Field(description="A score between 0 and 100; 100 if the user's intent is clearly understood, 0 if not.")
        ),
        "needs_info_about_previous_user_tickets_score": (
            float, 
            Field(description="A score between 0 and 100; 100 if we need to look up historical support data for this user, 0 if not.")
        ),
        "needs_info_about_reservations_score": (
            float, 
            Field(description="A score between 0 and 100; 100 if the query relates to event bookings, 0 if not.")
        ),
        "tags": (
            list[TagLiteral], 
            Field(description=f"Select all applicable tags from: {', '.join(current_tags)}")
        )
    }
    
    # 'create_model' returns a brand new Pydantic class
    return create_model("DynamicClassifierState", **fields)
