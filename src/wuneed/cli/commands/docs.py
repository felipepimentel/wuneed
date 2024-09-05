import typer
from rich import print
from wuneed.utils.auto_doc import auto_documentation

app = typer.Typer()

@app.command()
def generate():
    """Generate automatic documentation based on usage patterns."""
    docs = auto_documentation.generate_documentation()
    print("[bold]Documentation generated:[/bold]")
    print(docs)

@app.command()
def update():
    """Update the existing documentation with new usage patterns."""
    updated_docs = auto_documentation.update_documentation()
    print("[bold]Documentation updated:[/bold]")
    print(updated_docs)