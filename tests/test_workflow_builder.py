import pytest
from unittest.mock import patch, MagicMock
from wuneed.workflows.builder import WorkflowBuilder

@pytest.fixture
def mock_workflow_manager():
    with patch('wuneed.workflows.builder.workflow_manager') as mock:
        yield mock

@pytest.mark.asyncio
async def test_workflow_builder_add_step():
    builder = WorkflowBuilder()
    builder.command_input = MagicMock()
    builder.command_input.value = "test command"
    builder.step_list = MagicMock()

    event = MagicMock()
    event.button.label = "Add Step"

    await builder.on_button_pressed(event)

    assert len(builder.steps) == 1
    assert builder.steps[0]["command"] == "test command"
    builder.step_list.append.assert_called_once()

@pytest.mark.asyncio
async def test_workflow_builder_save_workflow(mock_workflow_manager):
    builder = WorkflowBuilder()
    builder.name_input = MagicMock()
    builder.name_input.value = "test workflow"
    builder.steps = [{"command": "test command"}]

    event = MagicMock()
    event.button.label = "Save Workflow"

    with patch.object(builder, 'quit') as mock_quit:
        await builder.on_button_pressed(event)

    mock_workflow_manager.create_workflow.assert_called_once_with("test workflow", [{"command": "test command"}])
    mock_quit.assert_called_once()