from agentic.agents.states import AgentState

ARTICLE_FETCHER_AGENT_NAME = "articles_fetcher_agent"


class ArticlesFetcherAgent:
    def __init__(self):
        self.path_to_articles_db = "path/to/articles_db.json"

    def __call__(self, state: AgentState):
        # Logic to fetch articles based on the ticket information
        pass