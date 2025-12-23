# Introduction
This README contains the design of the Multi-Agent System (MAS) for the Autonomous Knowledge Agent.

# Requirements

1. [Project specification](#project_specification)
    * [High-level description](#high_level_description)
    * [Key capabilities](#key_capabilities)
    * [Inputs & Deliverables](#inputs_and_deliverables)

2. [Take-aways](#take_aways)
    * [Primary goal](#primary_goal)
    * [Functional Requirements](#functional_requirements)
    * [Non-Functional Requirements](#non_functional_requirements)

3. [Design](#design)
    * [Roles & Resonsibilities](#roles_and_responsibilities)
    * [Architecture pattern]($architecture_pattern)
    * [Communication & Data Flow](#communication_and_data_flow)

## Project specification <a name="project_specification"></a>
This is a quote from the project description:

### High-level description <a name="high_level_description"></a>
```
(...) UDA-Hub, a Universal Decision Agent designed to plug into existing customer support systems (Zendesk, Intercom, Freshdesk, internal CRMs) and intelligently resolve tickets. But this isn’t just another FAQ bot.

The goal? Build an agentic system that reads, reasons, routes, and resolves, acting as the operational brain behind support teams.

You’ll need to design an agent system that can:

* Understand customer tickets across channels
* Decide which agent or tool should handle each case
* Retrieve or infer answers when possible
* Escalate or summarize issues when necessary
* Learn from interactions by updating long-term memory

Your agent should not only automate, it should decide how to automate!
```

### Key capabilities: <a name="key_capabilities"></a>

Multi-Agent Architecture with LangGraph Design and orchestrate specialized agents (e.g., Supervisor, Classifier, Resolver, Escalation…).

Input Handling Accept incoming support tickets in natural language with metadata (e.g., platform, urgency, history).

Decision Routing and Resolution

Route tickets to the right agent based on classification
Retrieve relevant knowledge via RAG if needed
Resolve or escalate based on confidence and context
Memory Integration

Maintain state during steps of the execution
Short-term memory is used as context to keep conversation running during the same session
Store and recall long-term memory for preferences, as an example

### Inputs & Deliverables <a name="inputs_and_deliverables"></a>
**Inputs:**
* Incoming support ticket (text + metadata)
* Internal knowledge base (FAQ, previous tickets)
* Optional internal tool (e.g., refund)
* Memory store (for prior conversations and resolutions)

**Deliverables:**
A LangGraph-powered multi-agent system that:
* Understands tickets
* Routes to correct agent with tools
* Resolves or escalates based on decision logic
* Uses memory appropriately


## Take-aways <a name="take_aways"></a>

### Primary goal <a name="primary_goal"></a>
The Autonomous Knowledge Agent needs to accept tickets raised by users of the CultPass system, understand them, make decisions about what informations is needed (FAQ and / or previously resolved tickets, BUT also potentially info about the user like: What reservations he might have?), and then provide an answer to that ticket OR make a decision that it cannot be resolved and escalate the ticket to a human.

### Functional Requirements <a name="functional_requirements"></a>
* The MAS system can be asked questions in the form of a ticket alongside with metadata about the date, the user, etc.

### Non-Functional Requirements <a name="non_functional_requirements"></a>


# Design <a name="design"></a>

## Roles & Responsibilities <a name="roles_and_responsibilities"></a>
For each agent, list inputs, outputs, success/failure behavior, and retries.

#### Agent 1: Coordinator
* **Inputs:**
* **Outputs:**
* **Success:**
* **Failure:**
* **Retries:**

#### Agent 2: Slave

## Architecture pattern <a name="architecture_pattern"></a>
Compare patterns against scenario requirements:
* Use orchestrator when strict order, centralized state, or rollback is needed.
* For critical flows, prefer orchestrator to manage compensating transactions.
* Use peer-to-peer when flexibility, parallelism, or modular chaining is preferred.
* For highly parallel tasks (e.g., content enrichment), prefer peer-to-peer pipelines.
* Use retries with exponential backoff and a dead-letter mechanism for persistent failures.

Fill these fields:
* Pattern: ORCHESTRATOR or PEER-TO-PEER
* Reasoning: map requirements to pattern benefits
* Data Flow: describe message format and path (JSON payload with metadata, events, or commands)

## Communication & Data Flow <a name="communication_and_data_flow"></a>
* Choose communication protocol: direct method calls (in-proc), message queues (RabbitMQ/Kafka), or HTTP callbacks.
* Define message schema: minimal fields such as {id, type, payload, status, trace}.
* Decide on error handling: retries, dead-letter routing, and supervisor escalation.


OTHER NOTES:
**Implement agents and graph**
Use the starter code functions as templates.
For orchestrator:
Implement a supervisor function that reads state and returns the next agent name or END
Implement each agent to process state and return to supervisor or END
For peer-to-peer:
Implement agents that directly return the next agent name
Create a StateGraph(MessagesState), add nodes, and connect edges to reflect the chosen pattern.
Compile and visualize the graph with graph.get_graph().draw_mermaid_png() and display(Image(...)).

**Test the prototype**
Create sample messages that exercise normal and edge cases (failures, timeouts).
Run the workflow and validate transitions and outputs.
Log state transitions and use random or deterministic stubs for external calls to simulate responses.

**Produce the architecture diagram**
Export the visual produced by LangGraph or draw a simple diagram showing agents, flows, and protocols.
Annotate the diagram with data formats and failure paths.


### Reflection questions

* Why was the chosen pattern selected?
* What advantages does this pattern bring for the scenario?
* What challenges might arise in production (scaling, consistency, observability)?
* How would the design change if requirements evolve (e.g., add parallel processing, add audit logs)?