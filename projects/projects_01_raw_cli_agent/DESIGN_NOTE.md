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

- Purpose: Evaluate a simple arithmetic expression made from numbers and operators using BODMAS precedence. Brackets are not supported.
- Input schema:
{
"numbers" : [number],
"operators": ["+","-"."*","/"]
}
- Output schema:
{answer: number | null,
error: string| null
}
- Validation rules:
 -'numbers' must contain at least 1 item.
 -'operators' must contain exactly 'len(numbers)-1' items.
 - Operators must be one of `+`, `-`, `*`, `/`.
 - Division by zero is not allowed
 - Brackets are not supported
 - Evaluation follows BODMAS precedence

- Failure behavior:
- if division by 0 detected, return:
{"answer": null}
- if arguments are malformed, return:

### `get_current_time`

- Purpose: Given a supported place name, return the current time of the place
- Input schema: 
{
    place : string

}
- Output schema:
{
    time: time
}
- Validation rules:
- Place name should match with first 3 letters
- Failure behavior:

Suggestions:

- Support a small explicit place list in v1, for example `New York`, `London`, `Tokyo`, and `Sydney`.
- Map each supported place to an IANA timezone such as `America/New_York`, not a fixed UTC offset.
- Accept case-insensitive full names.
- Accept 3-letter prefixes only when they match exactly one supported place.
- Reject ambiguous prefixes instead of guessing.
- Normalize the matched place to one canonical name before returning the result.
- Prefer this output shape:
{
    "place": string | null,
    "timezone": string | null,
    "iso_time": string | null,
    "display_time": string | null,
    "error": string | null
}
- Use an injectable clock in the implementation so tests do not depend on the real current time.
- Keep this tool read-only and local. It should not call a network API.

Suggested failure behavior:

- Unknown place: return `error: "unsupported_place"`.
- Ambiguous prefix: return `error: "ambiguous_place"`.
- Missing or non-string `place`: return `error: "invalid_arguments"`.

Suggested tests:

- full place name works
- lowercase place name works
- supported 3-letter prefix works
- unknown place returns `unsupported_place`
- ambiguous prefix returns `ambiguous_place`
- non-string `place` returns `invalid_arguments`
- injected clock produces deterministic output

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
