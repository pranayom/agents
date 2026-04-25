# ADR 0001: Learning Contract For This Repository

## Status

Accepted

## Date

2026-04-25

## Context

This repository is a hands-on workspace for learning production-grade Agentic AI through a staged project roadmap.

The goal is not only to build working demos, but to understand how real agentic systems are designed and operated. That includes explicit tool contracts, bounded autonomy, validation, retrieval, workflow control, approvals, guardrails, evaluation, observability, and deployment.

The repository will be developed incrementally, with each project focusing on one major concept and building toward a larger capstone system.

Because the purpose of this repo is learning, the process matters as much as the output. The implementation should stay understandable, explicit, and easy to explain in interviews.

## Decision

The repository will follow a learning-first engineering contract.

### 1. The human owns the design

The human user is responsible for:

- problem definition
- scope and user stories
- architecture decisions and tradeoffs
- tool contracts and schemas
- workflow boundaries and state transitions
- approval policies
- guardrail and safety decisions
- eval design and pass/fail expectations
- failure-mode analysis
- final review of all meaningful code changes

### 2. Codex is a bounded engineering partner

Codex may assist with:

- scaffolding the repository
- implementing small, clearly bounded modules
- writing tests against defined interfaces
- refactoring without changing intended behavior
- reviewing code for bugs, risks, and missing tests
- debugging after first identifying likely root causes
- generating boilerplate for tooling, CI, APIs, and infrastructure when requested

Codex should not replace architecture thinking or make broad product decisions without explicit direction.

### 3. The codebase should optimize for clarity

This repository prioritizes:

- typed Python
- small and explicit modules
- separation of I/O from business logic
- validation at tool and schema boundaries
- deterministic tests where possible
- readable code over clever abstractions
- learning value over premature framework usage

### 4. Frameworks are introduced progressively

The repo starts from first principles and lower-level mechanics before moving to higher-level frameworks.

Planned progression:

- Python workspace and tooling first
- raw tool-calling loop before orchestration frameworks
- local retrieval before more advanced workflows
- approvals, guardrails, evals, and observability before production deployment layers

Frameworks such as FastAPI, OpenAI Agents SDK, LangGraph, PostgreSQL with pgvector, Redis, and Docker Compose will be introduced only when justified by later projects.

### 5. Production habits begin in Project 0

Even in early learning projects, the repository will establish the following norms:

- tests for behavior changes
- linting and type checking
- explicit repository conventions
- documented decisions
- controlled scope
- traceable reasoning about failures and tradeoffs

## Consequences

### Positive consequences

- The repo stays aligned with the learning goal rather than drifting into copy-paste implementation.
- Design decisions remain explainable in interviews.
- Codex use remains disciplined and auditable.
- Later projects can build on a consistent engineering foundation.
- Safety, evals, and reliability are treated as core parts of agentic systems rather than afterthoughts.

### Negative consequences

- Development may feel slower than using a high-level framework immediately.
- Some boilerplate will be written earlier than in a demo-first approach.
- The human user must stay actively involved in architecture and review rather than delegating everything.

## Alternatives Considered

### 1. Framework-first learning

Use a high-level agent framework immediately and learn the abstractions first.

This was rejected because it can hide the underlying mechanics of tool calling, control flow, validation, and state management too early.

### 2. Codex-heavy autopilot workflow

Allow Codex to make most implementation and architecture decisions.

This was rejected because it reduces learning value and makes it harder to explain design choices, tradeoffs, and failure modes independently.

### 3. Demo-first repository

Optimize for shipping many quick prototypes without strong repo conventions.

This was rejected because the roadmap is intended to build production-grade habits, not only working demos.

## Initial Stack Decision

The initial stack for Project 0 is:

- Python
- pytest
- ruff
- mypy
- python-dotenv

Planned later additions include:

- FastAPI
- PostgreSQL + pgvector
- Redis
- OpenAI Agents SDK
- LangGraph
- Docker Compose

## Review Trigger

This ADR should be revisited if:

- the repo shifts away from learning-first goals
- a major framework is introduced earlier than planned
- the collaboration model between the human and Codex changes
- the project scope changes significantly
