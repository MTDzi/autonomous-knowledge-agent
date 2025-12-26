from typing import Literal

from langgraph.types import Command

from agentic.agents.states import AgentState
from agentic.agents.agent_names import ORCHESTRATOR_AGENT_NAME


class ArticlesFetcherAgent:
    def __init__(self):
        self.path_to_articles_db = "path/to/articles_db.json"

    def __call__(self, state: AgentState) -> Command[Literal[ORCHESTRATOR_AGENT_NAME]]:
        # Logic to fetch articles based on the ticket information
        state["relevant_articles"] = [
            {"article_id": "001", "title": "How to reset your password", "content": "To reset your password, follow these steps..."},
            {"article_id": "002", "title": "Managing your subscription", "content": "To manage your subscription, go to..."}
        ]

        return Command(goto=ORCHESTRATOR_AGENT_NAME)
