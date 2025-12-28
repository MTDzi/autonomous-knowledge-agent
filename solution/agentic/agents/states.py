from functools import cache
from typing import Literal, Type

from langgraph.graph.message import MessagesState
from pydantic import BaseModel, Field, create_model

from utils import get_available_tags


class AgentState(MessagesState):
    ticket_text: str
    ticket_metadata: dict[str, str]
    account_id: str
    user_id: str
    user_preference: str | None = None

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

    # Resolution attributes
    resolution_text: str | None = None
    is_resolved_score: float = -1.0

    # Escalation attributes
    escalation_reason: str | None = None
    urgency_level: str | None = None

    # Summary attributes
    should_update_preference: bool = False
    new_preference: str | None = None


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


class _Article(BaseModel):
    """Represents a single knowledge base article."""
    title: str = Field(description="The title of the article.")
    content: str = Field(description="The full body content or summary of the article.")
    tags: str = Field(description="Comma-separated tags or a single string describing the article category.")


class ArticleFetcherResult(BaseModel):
    """The structured response containing multiple fetched articles."""
    relevant_articles: list[_Article] = Field(
        description="A list of relevant knowledge articles extracted from the knowledge base."
    )


class _Reservation(BaseModel):
    """Represents a single reservation made by the user."""
    reservation_details: str = Field(description="Details about the reservation, such as event name, date, and location.")
    reservation_status: str = Field(description="The current status of the reservation (e.g., confirmed, canceled).")
    reservation_other: str = Field(description="Any other relevant metadata about the reservation.")


class ReservationFetcherResult(BaseModel):
    """The structured response containing multiple fetched reservations."""
    reservations: list[_Reservation] = Field(
        description="A list of reservations associated with the user."
    )


class ResolutionResult(BaseModel):
    """Schema for summarizing the resolution."""
    resolution_text: str = Field(description="A response resolving the issue.")
    is_resolved_score: float = Field(description="A score between 0 and 100 indicating how well the issue was resolved.")


class EscalationResult(BaseModel):
    """Schema for escalation results."""
    escalation_reason: str = Field(description="A brief explanation of why the ticket is being escalated.")
    urgency_level: str = Field(description="The urgency level of the escalation (e.g., 'high', 'medium', 'low').")


class MemoryUpdate(BaseModel):
    """Schema for extracting long-term memory."""
    new_preference: str | None = Field(description="A specific user preference found (e.g. 'Prefers short emails')")
    resolution_summary: str | None = Field(description="A 1-sentence summary of the resolved issue.")
    should_update_preference: bool = Field(description="Whether there is actually anything worth saving.")


class _Ticket(BaseModel):
    """Represents a single previous ticket raised by the user."""
    ticket_content: str = Field(description="The full text content of the ticket.")
    ticket_tags: str = Field(description="Tags associated with the ticket.")
    ticket_other: str = Field(description="Any other relevant metadata about the ticket.")


class TicketFetcherResult(BaseModel):
    """The structured response containing multiple fetched previous tickets."""
    previous_tickets: list[_Ticket] = Field(
        description="A list of previous tickets raised by the user."
    )
