# ADR-001: ResearchForge AI Project Architecture

* **Status:** Accepted
* **Date:** 2026-07-24
* **Decision Makers:** Project Team

---

# Context

ResearchForge AI is a multi-agent AI research platform designed to retrieve information, verify evidence, generate citations, and produce trustworthy answers using an orchestrated workflow.

The architecture must:

* Support multiple AI providers.
* Support multiple retrieval backends.
* Scale to additional agents without refactoring existing components.
* Keep business logic independent of infrastructure.
* Remain maintainable as the codebase grows.

---

# Decision

The project will adopt a **Hybrid Clean Architecture** with **Bounded Contexts**.

Top-level backend domains:

```text
backend/app/

api/
core/
ai/
knowledge/
research/
```

Each domain has a single responsibility and clear dependency boundaries.

---

# Bounded Contexts

## api

Responsible for:

* HTTP routing
* Request validation
* Response serialization
* Dependency resolution

Does **not** contain business logic.

---

## core

Shared framework components.

Includes:

* Configuration
* Dependency Injection
* Logging
* Exceptions
* Middleware
* Telemetry
* Utilities

No business-domain knowledge.

---

## ai

Responsible for AI capabilities.

Includes:

* LLM abstraction
* Embeddings
* Rerankers
* Prompt cache
* Provider implementations

This domain does **not** know about documents or workflows.

---

## knowledge

Responsible for knowledge management.

Includes:

* Document ingestion
* Chunking
* Vector storage
* Retrieval
* Metadata

This domain does **not** know about LangGraph or agents.

---

## research

Business domain.

Responsible for:

* Workflows
* Agents
* Conversation management
* Research state
* Application services
* Citation generation

Coordinates AI and Knowledge domains.

---

# Architecture Principles

## 1. Thin Frontend

Frontend responsibilities:

* Display UI
* Accept input
* Upload files
* Render streamed responses

The frontend does not contain business logic.

---

## 2. Backend Owns State

The backend owns:

* Conversations
* Memory
* Workflow execution
* Agent execution
* Retrieval
* Verification
* Citations

Clients communicate using identifiers (e.g. `conversation_id`) rather than complete conversation history.

---

## 3. LangGraph Owns Orchestration

Workflow orchestration is performed exclusively by LangGraph.

Agents never invoke other agents.

```
Graph
    ↓
Planner
    ↓
Retriever
    ↓
Verifier
    ↓
Citation
    ↓
Synthesizer
```

Workflow changes are made by modifying the graph, not agent implementations.

---

## 4. Single Responsibility Agents

Each agent:

* Reads `ResearchState`
* Performs one responsibility
* Updates `ResearchState`
* Returns it

Agents do not:

* Route execution
* Select the next node
* Access infrastructure directly

---

## 5. Canonical Research State

A single `ResearchState` flows through the graph.

Specialized domain models are embedded within it, including:

* Conversation
* RetrievedChunk
* VerifiedSource
* Citation
* FinalAnswer
* Metrics

---

## 6. Service-Oriented Design

Agents communicate only with services.

```
Agent
    ↓
Service
    ↓
Provider
    ↓
SDK
```

Agents never directly instantiate or call:

* LLM SDKs
* Vector databases
* Cache clients
* External APIs

---

## 7. Dependency Injection

The DI container manages:

* Services
* Workflows
* Agents
* Providers
* Database clients
* Cache clients
* SDK wrappers

The DI container does not manage:

* DTOs
* Pydantic models
* Value objects
* State models
* Stateless helper functions

---

## 8. Provider Organization

Providers are colocated with the capability they implement.

Example:

```text
ai/

llms/
    providers/

embeddings/
    providers/

rerankers/
    providers/
```

A global `providers/` package will not be used.

---

## 9. Prompt Organization

Agent-specific prompts are colocated with their agents.

Example:

```text
research/
└── agents/
    └── retriever/
        ├── agent.py
        ├── prompt.py
        ├── models.py
        └── parser.py
```

Generic reusable prompts may reside under `ai/prompts/`.

---

## 10. Dependency Direction

Dependencies must always point inward.

```
API
    ↓
Research
    ↓
Knowledge
    ↓
AI
    ↓
Infrastructure
```

Reverse dependencies are not permitted.

---

## 11. Error Handling

Exceptions are caught only when the layer can:

* Retry
* Recover
* Translate
* Add meaningful context

Otherwise, exceptions propagate to the appropriate layer.

HTTP translation occurs only within the API layer.

---

## 12. Class-Based Components

The following are implemented as classes:

* Agents
* Services
* Workflows
* Providers

Reasons:

* Dependency Injection
* Testability
* Extensibility
* Lifecycle management

---

# Request Lifecycle

```
Client
    ↓
FastAPI
    ↓
ChatService
    ↓
Workflow
    ↓
ConversationService
    ↓
LangGraph
    ↓
Agents
    ↓
Services
    ↓
Providers
    ↓
External SDKs
```

---

# Initial Backend Structure

```text
backend/app/
├── api/
├── core/
├── ai/
├── knowledge/
├── research/
└── main.py
```

---

# Consequences

## Benefits

* Clear separation of concerns.
* Provider independence.
* Workflow flexibility.
* Scalable agent architecture.
* Improved testability.
* Reduced coupling.
* Easier maintenance.

## Trade-offs

* More initial structure than a simple application.
* Requires consistent adherence to dependency boundaries.
* Slightly higher upfront design complexity in exchange for long-term maintainability.

---

# Future Compatibility

The architecture is designed to support:

* LangGraph orchestration
* Multi-agent workflows
* RAG
* Multimodal inputs
* Streaming responses
* Prompt caching
* Conversation memory
* Checkpointing
* Human-in-the-loop
* Multiple AI providers
* Multiple embedding providers
* Multiple vector databases
* Evaluation and observability

No architectural changes should be required to introduce these capabilities.
