from sqlalchemy import create_engine, or_

from langchain_core.tools import tool

import data.models.udahub as udahub
from utils import get_session


UDAHUB_ENGINE =  create_engine(f"sqlite:///{udahub.UDAHUB_DB}", echo=False)


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


if __name__ == "__main__":
    articles = fetch_articles.func(
        account_id="cultpass",
        # tags=["events"],
        # tags=["subscription", "location"]
        tags=['location', 'account', 'settings', 'travel'],
    )
    for article in articles:
        print(article)
