from pathlib import Path
import os
import shutil

from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver

from agentic.agents.states import AgentState
from agentic.agents import (
    OrchestratorAgent,
    TicketClassifierAgent,
    TicketFetcherAgent,
    ReservationFetcherAgent,
    ArticlesFetcherAgent,
    ResolutionAgent,
    EscalationAgent,
    MemoryUpdaterAgent,
)
from agentic.agents.agent_names import (
    ORCHESTRATOR_AGENT_NAME,
    TICKET_CLASSIFIER_AGENT_NAME,
    TICKET_FETCHER_AGENT_NAME,
    RESERVATION_FETCHER_AGENT_NAME,
    ARTICLE_FETCHER_AGENT_NAME,
    RESOLUTION_AGENT_NAME,
    ESCALATION_AGENT_NAME,
    MEMORY_UPDATER_AGENT_NAME,
)


if __name__ == "__main__":
    # Start off by creating the state graph, and then populating it with agents 
    workflow = StateGraph(AgentState)

    # The orchestrator agent
    path_to_cache = Path(__file__).parent / "cache"
    if os.path.exists(path_to_cache):
        shutil.rmtree(path_to_cache)
        print(f"Re-created empty directory: {path_to_cache}")
    os.makedirs(path_to_cache)

    orchestrator_agent = OrchestratorAgent(path_to_cache)
    workflow.add_node(ORCHESTRATOR_AGENT_NAME, orchestrator_agent)
    workflow.set_entry_point(ORCHESTRATOR_AGENT_NAME)

    # The following LLM will be used in the following agents
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.0,
    )

    # The ticket classifier agent
    ticket_classifier_agent = TicketClassifierAgent(llm)
    workflow.add_node(TICKET_CLASSIFIER_AGENT_NAME, ticket_classifier_agent)

    # The previous tickets fetcher agent
    ticket_fetcher_agent = TicketFetcherAgent(llm)
    workflow.add_node(TICKET_FETCHER_AGENT_NAME, ticket_fetcher_agent)

    # The reservations fetcher agent
    reservation_fetcher_agent = ReservationFetcherAgent(llm)
    workflow.add_node(RESERVATION_FETCHER_AGENT_NAME, reservation_fetcher_agent)

    # The articles fetcher agent
    articles_fetcher_agent = ArticlesFetcherAgent(llm)
    workflow.add_node(ARTICLE_FETCHER_AGENT_NAME, articles_fetcher_agent)

    # The resolution agent
    resolution_agent = ResolutionAgent(llm)
    workflow.add_node(RESOLUTION_AGENT_NAME, resolution_agent)

    # The escalation agent
    escalation_agent = EscalationAgent(llm)
    workflow.add_node(ESCALATION_AGENT_NAME, escalation_agent)

    memory_updater_agent = MemoryUpdaterAgent(llm)
    workflow.add_node(MEMORY_UPDATER_AGENT_NAME, memory_updater_agent)

    # Compile and run the graph with an example input
    with SqliteSaver.from_conn_string((path_to_cache / "graph_checkpoints.db").resolve().as_posix()) as checkpointer:
        graph = workflow.compile(checkpointer=checkpointer)

        png_data = graph.get_graph().draw_mermaid_png()
        with open(Path(__file__).parent / "images" / "graph_outline.png", "wb") as f:
            f.write(png_data)
        print("Successfully saved graph_outline.png")

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
            "user_id": "888fb2",
            "user_preference": None,
        }

        response_for_example_input = graph.invoke(example_input, {'configurable': {'thread_id': example_input['user_id']}})
        print(f'Final response 1: {response_for_example_input}')
        orchestrator_agent.reset()

        example_input = {
            "ticket_text": (
                "Can you remind me what my last reservation details were? I think I booked something for next weekend but can't recall the specifics."
            ),
            "ticket_metadata": {
                "submission_date": "2024-10-01",
                "priority": "high",
                "channel": "email",
            },
            "account_id": "cultpass",
            "user_id": "888fb2",
            "user_preference": None,
        }

        response_for_example_input = graph.invoke(example_input, {'configurable': {'thread_id': example_input['user_id']}})
        print(f'Final response 2: {response_for_example_input}')
        orchestrator_agent.reset()

        example_input = {
            "ticket_text": (
                "Yo yo my man, what is the best cupcake recipe??"
            ),
            "ticket_metadata": {
                "submission_date": "2024-10-01",
                "priority": "high",
                "channel": "email",
            },
            "account_id": "cultpass",
            "user_id": "88382b",
            "user_preference": None,
        }

        response_for_example_input = graph.invoke(example_input, {'configurable': {'thread_id': example_input['user_id']}})
        print(f'Final response 3: {response_for_example_input}')
        orchestrator_agent.reset()

        example_input = {
            "ticket_text": (
                "Ah, shoot, what was my last reservation again? I think I booked something for next weekend but can't remember the details."
            ),
            "ticket_metadata": {
                "submission_date": "2024-10-01",
                "priority": "high",
                "channel": "email",
            },
            "account_id": "cultpass",
            "user_id": "888fb2",
            "user_preference": None,
        }

        response_for_example_input = graph.invoke(example_input, {'configurable': {'thread_id': example_input['user_id']}})
        print(f'Final response 4: {response_for_example_input}')
        orchestrator_agent.reset()
