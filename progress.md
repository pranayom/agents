# Progress

This file tracks what has been completed and what should happen next.

## Project 1: Raw Tool-Calling CLI Agent

### Completed

- Created the Project 1 design note in `projects/projects_01_raw_cli_agent/DESIGN_NOTE.md`.
- Defined the first usable version of the CLI agent: a raw tool-calling loop without an agent framework.
- Documented Project 1 user stories, non-goals, tool contracts, run state, stopping conditions, error policy, logging policy, test plan, and open questions.
- Defined intended tool contracts for:
  - `calculator`
  - `get_current_time`
  - `search_local_notes`
  - `finish`
- Decided that tools should be local Python functions with explicit validation before execution.
- Decided that model-proposed tool calls should be treated as untrusted requests.
- Decided that tool and retrieval outputs should be treated as untrusted observations.
- Added Project 1 learning notes to `learnings.md`, including design-note best practices and raw agent loop structure.
- Created the initial Project 1 implementation files manually:
  - `models.py`
  - `tools.py`
  - `agent_loop.py`
  - `cli.py`
- Started the first rough implementation using:
  - typed run state models
  - a tool registry
  - `calculator`
  - `finish`
  - a fake model client
  - a max-step agent loop
- Identified and corrected the import issue where `Protocol` should come from `typing`, not `collections.abc`.
- Added and ran a fake-model smoke test for the rough loop.
- Confirmed the smoke test passes and the loop reaches `completed`.
- Added focused pytest coverage for the current Project 1 slice:
  - `calculator` happy path
  - `calculator` malformed arguments
  - `calculator` division by zero
  - `finish` happy path
  - `finish` invalid arguments
  - unknown tool handling
  - max-step handling
- Confirmed the focused current-slice tests pass.

### Current Checkpoint

Project 1 has passed the first fake-model rough-loop smoke test and focused tests for the current implemented slice.

The application-owned loop has now been proven for the basic happy path:

1. The model client proposes a tool call.
2. The application validates the tool name.
3. The application executes only approved tools.
4. The loop records observations.
5. The loop stops on `finish` or max steps.

The immediate learning goal is now to add the next approved tool, `get_current_time`, while preserving deterministic tests.

### Next Steps

- Add `get_current_time` to `tools.py`.
- Register `get_current_time` in `TOOL_REGISTRY`.
- Add deterministic tests for `get_current_time` using an injected clock.
- Decide the default local notes directory for Project 1.
- Add `search_local_notes` to `tools.py`.
- Register `search_local_notes` in `TOOL_REGISTRY`.
- Add tests for local notes search using a temporary notes directory.
- Add basic CLI wiring after the loop and tools work through tests.
- Only after the fake model path is stable, add a real model client behind the same `ModelClient` interface.

### Open Decisions

- What should the default max-step count be?
- Should validation failures always be sent back as observations, or should some stop the run immediately?
- Should the CLI show debug logs by default, behind a flag, or only write logs to a file?
- Should `search_local_notes` use simple case-insensitive substring matching in v1, or a small scoring algorithm?
