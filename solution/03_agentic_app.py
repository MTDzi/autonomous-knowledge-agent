from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from agentic.agents.states import AgentState, create_dynamic_classifier_state
from agentic.agents.orchestrator import OrchestratorAgent
from agentic.agents.classifier import TicketClassifier


if __name__ == "__main__":
    orchestrator = OrchestratorAgent()

    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.0,
    )
    ticket_classifier_agent = TicketClassifier(llm)

    workflow = StateGraph(AgentState)
    workflow.add_node("orchestrator_agent", orchestrator)
    workflow.add_node("classifier_agent", ticket_classifier_agent)

    workflow.set_entry_point("orchestrator_agent")
    # workflow.add_edge("orchestrator_agent", END)

    graph = workflow.compile()

    example_input = {
        "ticket_text": ("I need to change the location of my subscription as I will be traveling "
                        "to a different country next month. How can I update my account settings to reflect this change?"),
        "account_id": "cultpass",
        "ticket_metadata": {
            "submission_date": "2024-10-01",
            "priority": "high",
            "channel": "email",
        },
    }

    graph.invoke(example_input)
