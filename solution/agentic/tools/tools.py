from sqlalchemy import create_engine, or_
from sqlalchemy.orm import joinedload, selectinload

from langchain_core.tools import tool

import data.models.udahub as udahub
import data.models.cultpass as cultpass
from utils import get_session


UDAHUB_ENGINE =  create_engine(f"sqlite:///{udahub.UDAHUB_DB}", echo=False)
CULTPASS_ENGINE = create_engine(f"sqlite:///{cultpass.CULTPASS_DB}", echo=False)


@tool
def fetch_articles(account_id: str, tags: list[str] | None = None) -> list[dict[str, str]]:
    """
    Fetch relevant knowledge articles based on tags.

    Args:
        account_id (str): The account identifier.
        tags (list[str] | None): List of tags to filter articles. If None, fetch all articles.
    
    Returns:
        list[dict[str, str]]: List of articles with title, content, and tags.
    """
    with get_session(UDAHUB_ENGINE) as session:
        # Start with the base query filtering by account_id
        query = session.query(udahub.Knowledge).filter_by(
            account_id=account_id
        )
        if tags:
            # Now, filter by each tag
            query = query.filter(
                or_(
                    udahub.Knowledge.tags.like(f"%{tag}%") for tag in tags
                )
            )
        
    return [
        {
            "title": article.title,
            "content": article.content,
            "tags": article.tags,
        }
        for article in query.all()
    ]


@tool
def fetch_reservations(user_id: str) -> list[dict[str, str]]:
    """
    Fetch reservations for this user.

    Args:
        user_id (str): The user identifier.
    
    Returns:
        list[dict[str, str]]: List of articles with title, content, and tags.
    """
    with get_session(CULTPASS_ENGINE) as session:
        # We use joinedload to fetch the Experience data in a single SQL JOIN
        # rather than querying the database again for every single reservation row.
        query = (
            session.query(cultpass.Reservation)
            .options(joinedload(cultpass.Reservation.experience))
            .filter(cultpass.Reservation.user_id == user_id)
        )
        
        results = query.all()
        
        reservation_list = []
        for res in results:
            exp = res.experience
            
            res_dict = {
                "reservation_id": res.reservation_id,
                "status": res.status,
                "created_at": res.created_at.isoformat() if res.created_at else None,
            }

            if exp is not None:
                res_dict.update({
                    "experience_title": exp.title,
                    "experience_description": exp.description,
                    "experience_location": exp.location,
                    "experience_when": exp.when.isoformat() if exp.when else None,
                    "experience_is_premium": exp.is_premium,
                    "experience_slots_available": exp.slots_available
                })
            reservation_list.append(res_dict)
            
    return reservation_list


@tool
def fetch_tickets(user_id: str) -> list[dict[str, str]]:
    """
    Fetch support tickets for this user.

    Args:
        user_id (str): The user identifier.
    """
    with get_session(UDAHUB_ENGINE) as session:
        query = (
            session.query(udahub.Ticket)
            .options(
                joinedload(udahub.Ticket.ticket_metadata),
                selectinload(udahub.Ticket.messages)
            )
            .filter(udahub.Ticket.user_id == user_id)
        .order_by(udahub.Ticket.created_at.desc())
    )

    tickets = query.all()
    
    results = []
    for ticket in tickets:
        results.append({
            "channel": ticket.channel,
            "created_at": ticket.created_at.isoformat(),
            "metadata": {
                "status": ticket.ticket_metadata.status,
                "issue_type": ticket.ticket_metadata.main_issue_type,
                "tags": ticket.ticket_metadata.tags,
            } if ticket.ticket_metadata else None,
            "messages": [
                {
                    "role": msg.role.value,  # Accessing the string value of the Enum
                    "content": msg.content,
                    "sent_at": msg.created_at.isoformat()
                } for msg in ticket.messages
            ]
        })
    
    return results


if __name__ == "__main__":
    articles = fetch_articles.func(
        account_id="cultpass",
        # tags=["events"],
        # tags=["subscription", "location"]
        tags=['location', 'account', 'settings', 'travel'],
    )
    for article in articles:
        print(article)


    reservations = fetch_reservations.func(
        user_id="888fb2",
    )
    for reservation in reservations:
        print(reservation)

    tickets = fetch_tickets.func(
        user_id="88382b",
    )
    for ticket in tickets:
        print(ticket)
    print(f"Total tickets fetched: {len(tickets)}")
