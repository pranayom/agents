from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .models import ToolResult


ToolFunction = Callable[[dict[str, Any]], ToolResult]


def calculator(arguments: dict[str, Any]) -> ToolResult:
    numbers = arguments.get("numbers")
    operators = arguments.get("operators")

    if not isinstance(numbers, list) or not numbers:
        return ToolResult(output={"answer": None, "error": "invalid_arguments"}, error="invalid_arguments")

    if not all(isinstance(number, int | float) for number in numbers):
        return ToolResult(output={"answer": None, "error": "invalid_arguments"}, error="invalid_arguments")

    if not isinstance(operators, list):
        return ToolResult(output={"answer": None, "error": "invalid_arguments"}, error="invalid_arguments")

    if len(operators) != len(numbers) - 1:
        return ToolResult(output={"answer": None, "error": "invalid_arguments"}, error="invalid_arguments")

    allowed_operators = {"+", "-", "*", "/"}
    if not all(operator in allowed_operators for operator in operators):
        return ToolResult(
            output={"answer": None, "error": "unsupported_operator"},
            error="unsupported_operator",
        )

    if any(operator == "/" and numbers[index + 1] == 0 for index, operator in enumerate(operators)):
        return ToolResult(output={"answer": None, "error": "division_by_zero"}, error="division_by_zero")

    working_numbers = list(numbers)
    working_operators = list(operators)

    index = 0
    while index < len(working_operators):
        operator = working_operators[index]

        if operator == "*":
            working_numbers[index] = working_numbers[index] * working_numbers[index + 1]
        elif operator == "/":
            working_numbers[index] = working_numbers[index] / working_numbers[index + 1]
        else:
            index += 1
            continue

        del working_numbers[index + 1]
        del working_operators[index]

    answer = working_numbers[0]
    for index, operator in enumerate(working_operators):
        next_number = working_numbers[index + 1]
        if operator == "+":
            answer += next_number
        elif operator == "-":
            answer -= next_number

    return ToolResult(output={"answer": answer, "error": None})


def finish(arguments: dict[str, Any]) -> ToolResult:
    answer = arguments.get("answer")

    if not isinstance(answer, str) or not answer.strip():
        return ToolResult(
            output={"final_answer": None, "error": "invalid_arguments"},
            error="invalid_arguments",
        )

    return ToolResult(output={"final_answer": answer.strip(), "error": None})


TOOL_REGISTRY: dict[str, ToolFunction] = {
    "calculator": calculator,
    "finish": finish,
}