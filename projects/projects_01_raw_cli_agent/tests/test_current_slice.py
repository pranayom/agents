from projects.projects_01_raw_cli_agent.agent_loop import FakeModelClient, run_agent
from projects.projects_01_raw_cli_agent.models import ToolCall
from projects.projects_01_raw_cli_agent.tools import calculator, finish


def test_calculator_happy_path() -> None:
    result = calculator(
        {
            "numbers": [2, 3, 4],
            "operators": ["+", "*"],
        }
    )

    assert result.error is None
    assert result.output == {"answer": 14, "error": None}


def test_calculator_rejects_malformed_arguments() -> None:
    result = calculator(
        {
            "numbers": "2, 3, 4",
            "operators": ["+", "*"],
        }
    )

    assert result.error == "invalid_arguments"
    assert result.output == {"answer": None, "error": "invalid_arguments"}


def test_calculator_rejects_division_by_zero() -> None:
    result = calculator(
        {
            "numbers": [10, 0],
            "operators": ["/"],
        }
    )

    assert result.error == "division_by_zero"
    assert result.output == {"answer": None, "error": "division_by_zero"}


def test_finish_happy_path() -> None:
    result = finish({"answer": "Done."})

    assert result.error is None
    assert result.output == {"final_answer": "Done.", "error": None}


def test_finish_rejects_invalid_arguments() -> None:
    result = finish({"answer": ""})

    assert result.error == "invalid_arguments"
    assert result.output == {"final_answer": None, "error": "invalid_arguments"}


def test_agent_records_unknown_tool_observation() -> None:
    model = FakeModelClient(
        tool_calls=[
            ToolCall(name="made_up_tool", arguments={}),
            ToolCall(name="finish", arguments={"answer": "Recovered."}),
        ]
    )

    state = run_agent(
        user_input="Use a tool that does not exist.",
        model_client=model,
        max_steps=5,
    )

    assert state.status == "completed"
    assert state.final_answer == "Recovered."
    assert len(state.steps) == 2

    first_step = state.steps[0]
    assert first_step.proposed_tool_name == "made_up_tool"
    assert first_step.validation_status == "invalid"
    assert first_step.execution_status == "not_executed"
    assert first_step.error == "unknown_tool"
    assert first_step.observation == {
        "error": "unknown_tool",
        "tool_name": "made_up_tool",
    }


def test_agent_stops_at_max_steps() -> None:
    model = FakeModelClient(
        tool_calls=[
            ToolCall(
                name="calculator",
                arguments={"numbers": [1, 1], "operators": ["+"]},
            ),
            ToolCall(
                name="calculator",
                arguments={"numbers": [2, 2], "operators": ["+"]},
            ),
        ]
    )

    state = run_agent(
        user_input="Keep calculating.",
        model_client=model,
        max_steps=2,
    )

    assert state.status == "max_steps_reached"
    assert state.final_answer == "I could not complete the request within the step limit."
    assert len(state.steps) == 2
    assert state.observations == [
        {"answer": 2, "error": None},
        {"answer": 4, "error": None},
    ]