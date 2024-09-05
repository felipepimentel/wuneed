import typer
from rich import print
from wuneed.utils.snippet_manager import snippet_manager

app = typer.Typer()

@app.command()
def add(name: str, code: str):
    """Add a new code snippet."""
    snippet_manager.add_snippet(name, code)
    print(f"[bold]Snippet added:[/bold] {name}")

@app.command()
def remove(name: str):
    """Remove an existing snippet."""
    snippet_manager.remove_snippet(name)
    print(f"[bold]Snippet removed:[/bold] {name}")

@app.command()
def list():
    """List all snippets."""
    snippets = snippet_manager.list_snippets()
    for name, code in snippets.items():
        print(f"[bold]{name}:[/bold]\n{code}\n")

@app.command()
def get(name: str):
    """Get a specific snippet."""
    snippet = snippet_manager.get_snippet(name)
    if snippet:
        print(f"[bold]{name}:[/bold]\n{snippet}")
    else:
        print(f"[bold red]Snippet '{name}' not found.[/bold red]")