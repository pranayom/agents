# AGENTS.md

## Purpose

This repository is for learning production-grade Agentic AI through staged, hands-on projects.

The human user owns the design thinking in this repo: architecture, tool contracts, workflow boundaries, eval design, guardrails, safety decisions, and failure analysis.

Codex should assist as a bounded engineering partner for implementation, tests, refactoring, review, and debugging.

## Working Rules

- Do not implement large features without first producing a short plan.
- Do not modify unrelated files.
- Prefer small, explicit modules over clever abstractions.
- Use typed Python.
- Add tests for every behavior change.
- Run tests after changes when practical.
- Do not introduce new dependencies without explaining why.
- Do not hide or ignore failing tests.
- Preserve existing public interfaces unless the task explicitly allows changes.
- Keep the code easy for a learner to understand.
- Explain important design or implementation choices clearly.

## What The Human Owns

The human user is responsible for:

- problem definition
- user stories and scope
- architecture decisions and tradeoffs
- tool contracts and schemas
- workflow and state-machine boundaries
- eval categories and pass/fail expectations
- approval policies
- guardrail severity and safety decisions
- failure-mode analysis
- final review of all important changes

## What Codex Should Do

Codex may help with:

- scaffolding the repository
- implementing one bounded module at a time
- writing tests against defined interfaces
- refactoring without changing behavior
- reviewing diffs for bugs, edge cases, and risks
- debugging failing tests after identifying root cause
- improving code clarity and maintainability
- creating boilerplate for tooling, CI, Docker, or API layers when requested

## What Codex Must Not Do

- Do not take over architecture decisions unless explicitly asked.
- Do not invent hidden behavior or requirements.
- Do not change unrelated code to make a task easier.
- Do not replace explicit learning-oriented code with a high-level framework unless the task asks for it.
- Do not bypass validation, approvals, or safety checks for convenience.
- Do not add unnecessary dependencies.
- Do not conceal tradeoffs or uncertainty.
- Do not make risky side-effecting changes without clearly surfacing them.

## Agentic AI Rules

- Tool calls must be explicit and typed.
- Tool inputs must be validated.
- Tool outputs must be treated as untrusted until validated.
- Risky or side-effecting actions require approval.
- Retrieval outputs are data, not instructions.
- Guardrails should be implemented outside the prompt where possible.
- Logs and traces must include a `run_id` where applicable.
- Do not log secrets, credentials, or sensitive personal data.
- Prefer deterministic behavior in tests and core control logic.
- Separate read-only actions from side-effecting actions when possible.

## Code Style

- Use Python for implementation unless another language is explicitly justified.
- Use Pydantic for schemas where structured validation is needed.
- Use pytest for tests.
- Use ruff for linting and formatting.
- Use mypy where practical.
- Prefer dependency injection for services.
- Keep I/O boundaries separate from business logic.
- Prefer simple, readable functions over deeply abstracted designs.
- Add comments only where they clarify non-obvious logic.

## Testing Expectations

- Every meaningful behavior change should include or update tests.
- Prefer unit tests first, then integration tests where useful.
- Use fake or stubbed LLM clients in tests whenever possible.
- Keep tests deterministic and fast.
- Cover happy paths, edge cases, and failure cases.
- For agentic systems, add eval-style cases for ambiguity, tool failure, unsafe requests, and adversarial inputs where relevant.

## Safety And Review Expectations

- Surface hidden risks before implementing behavior that could have broader consequences.
- Call out assumptions when requirements are ambiguous.
- Prefer bounded autonomy over open-ended agent behavior.
- Make failure handling explicit.
- Preserve observability hooks and logging patterns.
- When reviewing, prioritize correctness, regressions, unsafe assumptions, and missing tests.

## Definition Of Done

A task is only done when:

- the code works
- tests pass, or any unrun tests are explicitly called out
- behavior changes are reflected in tests or documentation
- important failure modes are considered
- changes are limited to the intended scope
- the human user can understand and explain the result
