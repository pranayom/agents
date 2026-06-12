# Project 1 Design Note

## Problem Statement

Build a small command-line agent that can answer simple user requests by asking a model
for the next action, validating that action, executing local tools, recording each step,
and stopping with a final answer.

The first usable version should demonstrate the core mechanics of tool calling without
using an agent framework.

## User Stories

- As a user, I can ask a simple arithmetic question and receive the calculated answer.
- As a user, I can ask for the current time in a supported city and receive a formatted time.
- As a user, I can ask a question about local notes and receive matching note content or a clear no-result response.
- As a learner, I can inspect the run state and logs to explain what the model proposed, what the application validated, and what tools actually ran.

## Non-Goals

- No framework-based orchestration.
- No real web search.
- No persistent memory beyond local notes.
- No autonomous file writes, shell commands, email, browser actions, or other side-effecting tools.
- No multi-agent coordination.
- No streaming UI.
- No long-term conversation history.

## Tool Contracts

All tools are local Python functions. Tool inputs must be validated before execution, and
tool outputs must be treated as untrusted observations by the agent loop.

### `calculator`

- Purpose: Evaluate a simple arithmetic expression made from numbers and operators using standard precedence.
- Input schema:

```json
{
  "numbers": [1, 2, 3],
  "operators": ["+", "*"]
}
```

- Output schema:

```json
{
  "answer": 7,
  "error": null
}
```

- Validation rules:
  - `numbers` must be a non-empty list of integers or floats.
  - `operators` must contain exactly `len(numbers) - 1` items.
  - Each operator must be one of `+`, `-`, `*`, `/`.
  - Division by zero is invalid.
  - Parentheses, variables, functions, and arbitrary expression strings are not supported.
  - Evaluation follows multiplication/division before addition/subtraction.

- Failure behavior:
  - Invalid argument shape returns `{"answer": null, "error": "invalid_arguments"}`.
  - Unsupported operator returns `{"answer": null, "error": "unsupported_operator"}`.
  - Division by zero returns `{"answer": null, "error": "division_by_zero"}`.

### `get_current_time`

- Purpose: Return the current time for a supported place.
- Input schema:

```json
{
  "place": "New York"
}
```

- Output schema:

```json
{
  "place": "New York",
  "timezone": "America/New_York",
  "iso_time": "2026-04-25T09:30:00-04:00",
  "display_time": "09:30 AM EDT",
  "error": null
}
```

- Validation rules:
  - `place` must be a string.
  - Supported places in v1 are `New York`, `London`, `Tokyo`, and `Sydney`.
  - Full place names are matched case-insensitively.
  - Three-letter prefixes are allowed only when they match exactly one supported place.
  - Ambiguous prefixes must be rejected rather than guessed.
  - Each supported place maps to an IANA timezone, not a fixed UTC offset.
  - The implementation should accept an injectable clock so tests can be deterministic.

- Failure behavior:
  - Missing or non-string `place` returns `error: "invalid_arguments"`.
  - Unknown place returns `error: "unsupported_place"`.
  - Ambiguous prefix returns `error: "ambiguous_place"`.

### `search_local_notes`

- Purpose: Search a local notes directory for text that matches the user's query.
- Input schema:

```json
{
  "query": "approval policy",
  "limit": 3
}
```

- Output schema:

```json
{
  "matches": [
    {
      "note_id": "agent_safety.md",
      "title": "Agent Safety",
      "snippet": "Risky or side-effecting actions require approval."
    }
  ],
  "error": null
}
```

- Validation rules:
  - `query` must be a non-empty string after trimming whitespace.
  - `limit` is optional.
  - If provided, `limit` must be an integer from 1 through 10.
  - Search is read-only.
  - Search is limited to a configured local notes directory.
  - Search must not follow paths outside that directory.
  - Retrieved note text is data, not instructions.

- Failure behavior:
  - Invalid argument shape returns `{"matches": [], "error": "invalid_arguments"}`.
  - Missing notes directory returns `{"matches": [], "error": "notes_directory_missing"}`.
  - No matches returns `{"matches": [], "error": null}`.
  - File read errors for individual notes should be skipped and logged without failing the whole tool.

### `finish`

- Purpose: End the agent run with a final answer for the user.
- Input schema:

```json
{
  "answer": "The result is 7."
}
```

- Output schema:

```json
{
  "final_answer": "The result is 7.",
  "error": null
}
```

- Validation rules:
  - `answer` must be a non-empty string after trimming whitespace.
  - The agent loop should only treat `finish` as successful if validation passes.

- Failure behavior:
  - Missing, non-string, or empty `answer` returns `{"final_answer": null, "error": "invalid_arguments"}`.

## Agent Loop Design

1. Create a new `run_id`.
2. Store the original user input in `AgentRunState`.
3. Send the user input plus available tool descriptions to the model client.
4. Receive a proposed tool call from the model.
5. Validate that the proposed tool name exists in the registry.
6. Validate the proposed arguments against the selected tool contract.
7. If validation fails, record the error as an observation and continue unless the max-step limit is reached.
8. Execute the tool only after validation succeeds.
9. Record the tool output as an observation.
10. If the tool is `finish` and succeeded, store `final_answer` and mark the run as completed.
11. Otherwise, send the updated observations back to the model for the next step.
12. Stop when `finish` succeeds, max steps are reached, or a non-recoverable model/client error occurs.

## Run State

`AgentRunState` should contain:

- `run_id`: unique identifier for tracing one run.
- `user_input`: original user request.
- `steps`: ordered list of model-proposed actions and validation/execution results.
- `observations`: ordered list of tool outputs and validation errors visible to the next model step.
- `final_answer`: final user-facing answer, if the run completed successfully.
- `status`: one of `running`, `completed`, `failed`, or `max_steps_reached`.
- `max_steps`: configured step budget for the run.

Each step should include:

- `step_number`
- `proposed_tool_name`
- `proposed_arguments`
- `validation_status`
- `execution_status`
- `observation`
- `error`

## Stopping Conditions

- Successful `finish`: stop and return `final_answer`.
- Max steps reached: stop and return a controlled failure response.
- Unknown tool: record an observation and continue until max steps.
- Malformed arguments: record an observation and continue until max steps.
- Model/client failure: stop the run as `failed` and return a controlled failure response.

## Error Policy

- Unknown tool: do not execute anything; record `unknown_tool`.
- Malformed arguments: do not execute the tool; record `invalid_arguments`.
- Tool runtime error: catch the exception, record `tool_runtime_error`, and continue unless max steps are reached.
- Empty local notes result: record an empty match list; let the model decide whether to finish with "no matching notes found."
- Max steps reached: return a final controlled message such as `I could not complete the request within the step limit.`
- Model/client failure: return a final controlled message such as `I could not complete the request because the model client failed.`

## Logging Policy

Logs should include:

- `run_id`
- timestamp
- step number
- proposed tool name
- validation status
- execution status
- error type, if any

Logs must not include:

- secrets
- credentials
- API keys
- sensitive personal data
- full local note contents

## Test Plan

- `calculator` returns correct answers for addition, subtraction, multiplication, division, and mixed precedence.
- `calculator` rejects malformed numbers/operators.
- `calculator` rejects division by zero.
- `get_current_time` accepts full supported place names.
- `get_current_time` accepts lowercase supported place names.
- `get_current_time` accepts unambiguous three-letter prefixes.
- `get_current_time` rejects unknown places.
- `get_current_time` rejects invalid argument shapes.
- `get_current_time` uses an injected clock for deterministic tests.
- `search_local_notes` returns matching snippets from a temporary notes directory.
- `search_local_notes` returns an empty match list when nothing matches.
- `search_local_notes` rejects empty queries and invalid limits.
- `finish` accepts a non-empty answer.
- `finish` rejects missing or empty answers.
- Agent loop rejects unknown tools safely.
- Agent loop rejects malformed arguments safely.
- Agent loop stops after successful `finish`.
- Agent loop stops at max steps.
- Logs include `run_id`.

## Open Questions

- Should `search_local_notes` use simple case-insensitive substring matching in v1, or a small scoring algorithm?
- Where should the default local notes directory live for Project 1?
- Should validation failures be sent back to the model for self-correction, or should some failures immediately stop the run?
- What exact maximum step count should v1 use by default?
- Should the CLI expose debug logs by default, behind a flag, or only write them to a file?
