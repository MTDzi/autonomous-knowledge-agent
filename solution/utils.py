# reset_udahub.py
import os
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import declarative_base, sessionmaker
from contextlib import contextmanager
from langchain_core.messages import (
    SystemMessage,
    HumanMessage, 
)
from langgraph.graph.state import CompiledStateGraph

from data.models import udahub

Base = declarative_base()


def reset_db(db_path: str, echo: bool = True):
    """Drops the existing udahub.db file and recreates all tables."""

    # Remove the file if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✅ Removed existing {db_path}")

    # Create a new engine and recreate tables
    engine = create_engine(f"sqlite:///{db_path}", echo=echo)
    Base.metadata.create_all(engine)
    print(f"✅ Recreated {db_path} with fresh schema")


@contextmanager
def get_session(engine: Engine):
    """
    Creates a context menager using a generator function and the contextmanager decorator.
    Noice.
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def model_to_dict(instance):
    """Convert a SQLAlchemy model instance to a dictionary."""
    return {
        column.name: getattr(instance, column.name)
        for column in instance.__table__.columns
    }

def chat_interface(agent:CompiledStateGraph, ticket_id:str):
    is_first_iteration = False
    messages = [SystemMessage(content = f"ThreadId: {ticket_id}")]
    while True:
        user_input = input("User: ")
        print("User:", user_input)
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Assistant: Goodbye!")
            break
        messages = [HumanMessage(content=user_input)]
        if is_first_iteration:
            messages.append(HumanMessage(content=user_input))
        trigger = {
            "messages": messages
        }
        config = {
            "configurable": {
                "thread_id": ticket_id,
            }
        }
        
        result = agent.invoke(input=trigger, config=config)
        print("Assistant:", result["messages"][-1].content)
        is_first_iteration = False
        
        
def get_available_tags(account_id: str) -> list[str]:
    """
    Connects to the Knowledge Base and retrieves available tags for the given account.
    """
    engine = create_engine(f"sqlite:///{udahub.UDAHUB_DB}", echo=False)
    all_tags = set()
    
    with get_session(engine) as session:
        account = session.query(udahub.Account).filter_by(
            account_id=account_id
        ).first()
        for article in account.knowledge_articles:
            tags = article.tags.replace(', ', ',').split(',')
            all_tags.update(tags)

    return sorted(list(all_tags))
