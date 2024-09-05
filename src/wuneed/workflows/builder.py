from textual.app import App
from textual.widgets import Button, Input, ListView, Static, Label
from textual.containers import Container, Horizontal, Vertical
from wuneed.workflows.manager import workflow_manager

class WorkflowBuilder(App):
    def __init__(self):
        super().__init__()
        self.steps = []
        self.workflow_name = ""

    async def on_mount(self) -> None:
        await self.view.dock(Static("Workflow Builder", id="title"), edge="top")
        
        self.step_list = ListView()
        self.command_input = Input(placeholder="Enter command")
        self.name_input = Input(placeholder="Enter workflow name")
        add_button = Button("Add Step", variant="primary")
        save_button = Button("Save Workflow", variant="success")
        cancel_button = Button("Cancel", variant="error")

        await self.view.dock(
            Vertical(
                Label("Workflow Name:"),
                self.name_input,
                Label("Steps:"),
                self.step_list,
                Horizontal(self.command_input, add_button),
                Horizontal(save_button, cancel_button)
            ),
            edge="left"
        )

        await self.name_input.focus()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.label == "Add Step":
            command = self.command_input.value
            if command:
                self.steps.append({"command": command})
                await self.step_list.append(f"Step {len(self.steps)}: {command}")
                self.command_input.value = ""
        elif event.button.label == "Save Workflow":
            self.workflow_name = self.name_input.value
            if self.workflow_name and self.steps:
                workflow_manager.create_workflow(self.workflow_name, self.steps)
                print(f"Workflow '{self.workflow_name}' saved with {len(self.steps)} steps")
                await self.quit()
            else:
                await self.view.dock(Static("[red]Please provide a workflow name and at least one step[/red]"), edge="bottom")
        elif event.button.label == "Cancel":
            await self.quit()

workflow_builder = WorkflowBuilder()