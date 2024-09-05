import typer
from rich import print
from wuneed.utils.template_manager import template_manager

app = typer.Typer()

@app.command()
def add(name: str, template: str):
    """Add a new template."""
    template_manager.add_template(name, template)
    print(f"[bold]Template added:[/bold] {name}")

@app.command()
def remove(name: str):
    """Remove an existing template."""
    template_manager.remove_template(name)
    print(f"[bold]Template removed:[/bold] {name}")

@app.command()
def list():
    """List all templates."""
    templates = template_manager.list_templates()
    for name, template in templates.items():
        print(f"[bold]{name}:[/bold] {template}")

@app.command()
def apply(name: str, params: str):
    """Apply a template with given parameters."""
    param_dict = dict(param.split('=') for param in params.split(','))
    result = template_manager.apply_template(name, param_dict)
    print(f"[bold]Applied template:[/bold] {result}")