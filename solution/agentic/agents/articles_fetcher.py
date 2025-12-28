from typing import Literal

from langgraph.types import Command
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent

from agentic.agents.states import AgentState, ArticleFetcherResult
from agentic.agents.agent_names import ORCHESTRATOR_AGENT_NAME
from agentic.tools.tools import fetch_articles


class ArticlesFetcherAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are an agent for Account: account_id={account_id} that needs to extract articles from a knowledge base (FAQ)."

                "Based on the provided tags, fetch the most relevant articles from the knowledge base that can help resolve the user's issue."

                "However, if no articles were found OR if the tags are an empty list, go through all the articles and find exactly one that best matches the ticket raised by the user."

                "As output, provide a list of Python dictionaries with relevant articles with keys: \"title\", \"content\", and \"tags\". And that's it, nothing more."
            )),
            ("user", "Ticket text:\n\n{ticket_text}\n\nwith the following tags:\n\n{tags}")
        ])
        self.agent = create_react_agent(
            model=self.llm,
            tools=[fetch_articles],
            response_format=ArticleFetcherResult,
        )

    def __call__(self, state: AgentState) -> Command[Literal[ORCHESTRATOR_AGENT_NAME]]:
        result = self.agent.invoke({
            "messages": self.prompt.invoke({
                "account_id": state['account_id'],
                "tags": state['tags'],
                "ticket_text": state["ticket_text"],
            }).messages,
        })
        structured_response = result["structured_response"]

        return Command(
            goto=ORCHESTRATOR_AGENT_NAME,
            update={
                "relevant_articles": [
                    {
                        'title': article.title,
                        'content': article.content,
                        'tags': article.tags,
                    }
                    for article in structured_response.relevant_articles
                ]
            }
        )
