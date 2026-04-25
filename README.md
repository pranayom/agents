# Agentic AI Learning Roadmap

This repository is a hands-on workspace for learning production-grade Agentic AI project by project.

The goal is not just to build demos, but to understand how real agentic systems are designed: explicit tool contracts, bounded autonomy, validation, retrieval, approvals, guardrails, evals, observability, and deployment.

This repo follows a staged roadmap. Each project adds one major concept and builds toward a portfolio-grade capstone.

The aim is to help candidates clear the Claude Architect Certification exam (I have moved to Codex last month so the irony writes itself!)

## Learning Goals

- Build agentic systems from first principles before relying on high-level frameworks
- Practice production-minded engineering habits from the start
- Use Codex as a pair programmer, not an autopilot
- Develop interview-ready explanations for architecture, tradeoffs, safety, and evaluation

## Project Roadmap

- `Project 0`: Engineering workspace and repo conventions
- `Project 1`: Raw tool-calling CLI agent
- `Project 2`: Structured outputs and validation
- `Project 3`: Local RAG notes assistant
- `Project 4`: Hybrid retrieval
- `Project 5+`: Workflows, frameworks, durable execution, approvals, guardrails, evals, observability, API layer, and capstone

## Repository Structure

```text
.
├── AGENTS.md
├── README.md
├── Makefile
├── pyproject.toml
├── docs/
│   └── architecture_decisions/
├── evals/
├── logs/
├── projects/
│   ├── project_00_workspace/
│   └── project_01_raw_cli_agent/
├── shared/
│   ├── schemas/
│   └── utils/
├── scripts/
├── config/
└── tests/


## Tech Stack
Current and planned stack for the roadmap:

Python
pytest
ruff
mypy
python-dotenv
Planned for later projects:

FastAPI
PostgreSQL + pgvector
Redis
OpenAI Agents SDK
LangGraph
Docker Compose
Development Principles
Keep modules small and explicit
Prefer typed Python
Separate business logic from I/O boundaries
Validate tool inputs and outputs
Treat retrieval output as untrusted data
Add tests for behavior changes
Build learning-friendly code before framework-heavy abstractions