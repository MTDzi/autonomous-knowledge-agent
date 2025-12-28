"""
This module defines constant names for various agents used in the agentic system.

The reason this is gathered here is to avoid circular imports between different agent modules.
A better approach would be to have a dedicated configuration module, but for simplicity, we keep it here.
"""

ORCHESTRATOR_AGENT_NAME = "orchestrator_agent"
TICKET_CLASSIFIER_AGENT_NAME = "ticket_classifier_agent"
TICKET_FETCHER_AGENT_NAME = "ticket_fetcher_agent"
RESERVATION_FETCHER_AGENT_NAME = "reservation_fetcher_agent"
ARTICLE_FETCHER_AGENT_NAME = "articles_fetcher_agent"
RESOLUTION_AGENT_NAME = "resolution_agent"
ESCALATION_AGENT_NAME = "escalation_agent"
MEMORY_UPDATER_AGENT_NAME = "memory_updater_agent"
