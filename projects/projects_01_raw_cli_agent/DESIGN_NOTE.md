# Project 1 Design Note

Fill this in before implementation. Keep answers short and concrete.

## Problem Statement

What should this CLI agent do in its first usable version?

## User Stories

- As a user, I can ...
- As a user, I can ...
- As a user, I can ...

## Non-Goals

What will this project intentionally not do yet?

- No framework-based orchestration.
- No real web search.
- No persistent memory beyond local notes.

## Tool Contracts

Define each tool before implementation.

### `calculator`

- Purpose:
- Input schema:
- Output schema:
- Validation rules:
- Failure behavior:

### `get_current_time`

- Purpose:
- Input schema:
- Output schema:
- Validation rules:
- Failure behavior:

### `search_local_notes`

- Purpose:
- Input schema:
- Output schema:
- Validation rules:
- Failure behavior:

### `finish`

- Purpose:
- Input schema:
- Output schema:
- Validation rules:
- Failure behavior:

## Agent Loop Design

Describe the loop in plain language.

1. Receive user input.
2. ...
3. ...

## Run State

What fields should `AgentRunState` contain?

- `run_id`:
- `user_input`:
- `steps`:
- `observations`:
- `final_answer`:
- `status`:

## Stopping Conditions

When should the loop stop?

- successful `finish`
- max steps reached
- validation failure policy:
- model/client failure policy:

## Error Policy

What should happen for each case?

- unknown tool:
- malformed arguments:
- tool runtime error:
- empty local notes result:
- max steps reached:

## Logging Policy

What fields should be logged?

- `run_id`
- timestamp
- step number
- proposed tool name
- validation status
- execution status
- error type, if any

What must not be logged?

- secrets
- credentials
- sensitive personal data

## Test Plan

Define expected tests before code.

- tool validation happy path:
- unknown tool:
- malformed arguments:
- max steps:
- successful final answer:
- local notes search:

## Open Questions

List decisions you still need to make before coding.

- 
