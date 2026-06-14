from projects.projects_01_raw_cli_agent.agent_loop import FakeModelClient, run_agent
from projects.projects_01_raw_cli_agent.models import ToolCall


def test_fake_model_loop_reaches_completed() -> None:
    model = FakeModelClient(
        tool_calls=[
            ToolCall(
                name="calculator",
                arguments={"numbers": [2, 3, 4], "operators": ["+", "*"]},
            ),
            ToolCall(
                name="finish",
                arguments={"answer": "The calculation completed successfully."},
            ),
        ]
    )

    state = run_agent(
        user_input="What is 2 + 3 * 4?",
        model_client=model,
        max_steps=5,
    )

    assert state.status == "completed"
    assert state.final_answer == "The calculation completed successfully."
    assert len(state.steps) == 2
    assert state.steps[0].proposed_tool_name == "calculator"
    assert state.steps[0].execution_status == "succeeded"
    assert state.observations[0] == {"answer": 14, "error": None}
    assert state.steps[1].proposed_tool_name == "finish"
    assert state.steps[1].execution_status == "succeeded"