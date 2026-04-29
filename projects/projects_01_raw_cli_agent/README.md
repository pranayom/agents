# Project 1: Raw Tool-Calling CLI Agent

## Goal

Build a small CLI agent loop from first principles before using any agent framework.

The learning target is to understand that the model can propose tool calls, but the
application owns validation, execution, state updates, logging, and stopping.

## Scope

The first version should support these tools:

- `calculator`
- `get_current_time`
- `search_local_notes`
- `finish`

The agent runtime should include:

- an explicit agent loop
- typed tool call and run state models
- a tool registry
- validated tool inputs
- untrusted tool outputs
- max-step stopping
- unknown-tool handling
- malformed-argument handling
- logs that include a `run_id`

## Human Responsibilities

Before implementation, write the design note in `DESIGN_NOTE.md`.

You own these decisions:

- user stories and scope
- tool contracts and argument schemas
- agent loop control flow
- stopping conditions
- error policy
- logging fields
- safety boundaries
- eval and test expectations
- final review of meaningful changes

You should also write the first rough agent loop yourself, even if it is messy. That is
part of the learning objective for this project.

## Codex Responsibilities

After the design note and rough loop exist, Codex can help with bounded engineering work:

- refactor the rough loop into clearer modules
- add type hints
- add explicit error classes
- add pytest tests
- add CLI argument parsing
- review edge cases
- debug failing tests after identifying likely root causes

Codex should not replace the explicit loop with LangChain, LangGraph, the OpenAI Agents
SDK, or another framework in this project.

## Acceptance Criteria

- simple calculation questions work
- current-time questions work
- local note search works and returns summarized results
- unknown tools are rejected safely
- malformed arguments are rejected safely
- the loop stops at the configured max-step budget
- logs include a `run_id`
- pytest passes
- you can explain why tools are executed by the application, not by the model

## Suggested File Shape

Keep the implementation small and explicit:

- `models.py` for typed run state and tool call models
- `tools.py` for tool functions and registry
- `agent_loop.py` for loop control
- `cli.py` for command-line input/output
- tests under `tests/project_01/`

This file shape is a starting point, not an architecture mandate. If you choose a
different structure, document why in the design note.
