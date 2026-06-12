from __future__ import annotations

from collections.abc import Protocol

from .models import AgentRunState, AgentStep, ToolCall
from .tools import TOOL_REGISTRY


class ModelClient(Protocol):
    def next_tool_call(self, state: AgentRunState) -> ToolCall:
        """Return the next tool call proposed by the model."""


class FakeModelClient:
    def __init__(self, tool_calls: list[ToolCall]) -> None:
        self._tool_calls = tool_calls
        self._index = 0

    def next_tool_call(self, state: AgentRunState) -> ToolCall:
        if self._index >= len(self._tool_calls):
            return ToolCall(
                name="finish",
                arguments={"answer": "I could not complete the request."},
            )

        tool_call = self._tool_calls[self._index]
        self._index += 1
        return tool_call


def run_agent(user_input: str, model_client: ModelClient, max_steps: int = 5) -> AgentRunState:
    state = AgentRunState(user_input=user_input, max_steps=max_steps)

    for step_number in range(1, max_steps + 1):
        tool_call = model_client.next_tool_call(state)

        step = AgentStep(
            step_number=step_number,
            proposed_tool_name=tool_call.name,
            proposed_arguments=tool_call.arguments,
        )

        tool = TOOL_REGISTRY.get(tool_call.name)
        if tool is None:
            step.validation_status = "invalid"
            step.error = "unknown_tool"
            step.observation = {"error": "unknown_tool", "tool_name": tool_call.name}
            state.steps.append(step)
            state.observations.append(step.observation)
            continue

        step.validation_status = "valid"

        try:
            result = tool(tool_call.arguments)
        except Exception:
            step.execution_status = "failed"
            step.error = "tool_runtime_error"
            step.observation = {"error": "tool_runtime_error", "tool_name": tool_call.name}
            state.steps.append(step)
            state.observations.append(step.observation)
            continue

        if result.error is not None:
            step.execution_status = "failed"
            step.error = result.error
            step.observation = result.output
            state.steps.append(step)
            state.observations.append(result.output)
            continue

        step.execution_status = "succeeded"
        step.observation = result.output
        state.steps.append(step)
        state.observations.append(result.output)

        if tool_call.name == "finish":
            final_answer = result.output.get("final_answer")
            if isinstance(final_answer, str):
                state.final_answer = final_answer
                state.status = "completed"
                return state

    state.status = "max_steps_reached"
    state.final_answer = "I could not complete the request within the step limit."
    return state