from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI

from agentic.agents.states import AgentState
from agentic.agents.orchestrator import OrchestratorAgent, ORCHESTRATOR_AGENT_NAME
from agentic.agents.ticket_classifier import TicketClassifierAgent, TICKET_CLASSIFIER_AGENT_NAME
from agentic.agents.ticket_fetcher import TicketFetcherAgent, TICKET_FETCHER_AGENT_NAME
from agentic.agents.reservation_fetcher import ReservationFetcherAgent, RESERVATION_FETCHER_AGENT_NAME
from agentic.agents.articles_fetcher import ArticlesFetcherAgent, ARTICLE_FETCHER_AGENT_NAME
from agentic.agents.resolver import ResolutionAgent, RESOLUTION_AGENT_NAME


if __name__ == "__main__":
    # Start off by creating the state graph, and then populating it with agents 
    workflow = StateGraph(AgentState)

    # The orchestrator agent
    orchestrator_agent = OrchestratorAgent()
    workflow.add_node(ORCHESTRATOR_AGENT_NAME, orchestrator_agent)
    workflow.set_entry_point(ORCHESTRATOR_AGENT_NAME)

    # The LLM will be used in the following agents
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.0,
    )

    # The ticket classifier agent
    ticket_classifier_agent = TicketClassifierAgent(llm)
    workflow.add_node(TICKET_CLASSIFIER_AGENT_NAME, ticket_classifier_agent)

    # The previous tickets fetcher agent
    ticket_fetcher_agent = TicketFetcherAgent()
    workflow.add_node(TICKET_FETCHER_AGENT_NAME, ticket_fetcher_agent)

    # The reservations fetcher agent
    reservation_fetcher_agent = ReservationFetcherAgent()
    workflow.add_node(RESERVATION_FETCHER_AGENT_NAME, reservation_fetcher_agent)

    # The articles fetcher agent
    articles_fetcher_agent = ArticlesFetcherAgent()
    workflow.add_node(ARTICLE_FETCHER_AGENT_NAME, articles_fetcher_agent)

    # The final decision agent
    final_resolution_agent = ResolutionAgent(llm)
    workflow.add_node(RESOLUTION_AGENT_NAME, final_resolution_agent)

    # Compile and run the graph with an example input
    graph = workflow.compile()

    example_input = {
        "ticket_text": (
            "I need to change the location of my subscription as I will be traveling "
            "to a different country next month. How can I update my account settings to reflect this change?"
        ),
        "ticket_metadata": {
            "submission_date": "2024-10-01",
            "priority": "high",
            "channel": "email",
        },
        "account_id": "cultpass",
    }

    graph.invoke(example_input)
