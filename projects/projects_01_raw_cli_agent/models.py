from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal
from uuid import uuid4


RunStatus = Literal["running", "completed", "failed", "max_steps_reached"]
ValidationStatus = Literal["not_validated", "valid", "invalid"]
ExecutionStatus = Literal["not_executed", "succeeded", "failed"]


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class ToolResult:
    output: dict[str, Any]
    error: str | None = None


@dataclass
class AgentStep:
    step_number: int
    proposed_tool_name: str
    proposed_arguments: dict[str, Any]
    validation_status: ValidationStatus = "not_validated"
    execution_status: ExecutionStatus = "not_executed"
    observation: dict[str, Any] | None = None
    error: str | None = None


@dataclass
class AgentRunState:
    user_input: str
    max_steps: int
    run_id: str = field(default_factory=lambda: str(uuid4()))
    steps: list[AgentStep] = field(default_factory=list)
    observations: list[dict[str, Any]] = field(default_factory=list)
    final_answer: str | None = None
    status: RunStatus = "running"