import typer
from rich import print
from wuneed.utils.alias_manager import alias_manager

app = typer.Typer()

@app.command()
def add(alias: str, command: str):
    """Add a new alias."""
    alias_manager.add_alias(alias, command)
    print(f"[bold]Alias added:[/bold] {alias} -> {command}")

@app.command()
def remove(alias: str):
    """Remove an existing alias."""
    alias_manager.remove_alias(alias)
    print(f"[bold]Alias removed:[/bold] {alias}")

@app.command()
def list():
    """List all aliases."""
    aliases = alias_manager.list_aliases()
    for alias, command in aliases.items():
        print(f"[bold]{alias}:[/bold] {command}")