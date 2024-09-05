import typer
from rich import print
from wuneed.utils.workflow_manager import workflow_manager
import json

app = typer.Typer()

@app.command()
def add(name: str, steps: str):
    """Add a new workflow."""
    steps_list = json.loads(steps)
    workflow_manager.add_workflow(name, steps_list)
    print(f"[bold]Workflow added:[/bold] {name}")

@app.command()
def remove(name: str):
    """Remove an existing workflow."""
    workflow_manager.remove_workflow(name)
    print(f"[bold]Workflow removed:[/bold] {name}")

@app.command()
def list():
    """List all workflows."""
    workflows = workflow_manager.list_workflows()
    for name, steps in workflows.items():
        print(f"[bold]{name}:[/bold]")
        for i, step in enumerate(steps, 1):
            print(f"  {i}. {step['command']} - Args: {step.get('args', {})}")

@app.command()
def execute(name: str, context: str = "{}"):
    """Execute a workflow."""
    context_dict = json.loads(context)
    results = workflow_manager.execute_workflow(name, context_dict)
    print(f"[bold]Workflow '{name}' executed:[/bold]")
    for i, result in enumerate(results, 1):
        print(f"  Step {i} result: {result}")