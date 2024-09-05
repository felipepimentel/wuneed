import typer
from rich import print
from wuneed.utils.updater import updater

app = typer.Typer()

@app.command()
def check():
    """Check for updates."""
    if updater.check_for_updates():
        print("[bold green]A new version of Wuneed is available![/bold green]")
        print("Run 'wuneed update install' to upgrade.")
    else:
        print("[bold]Wuneed is up to date.[/bold]")

@app.command()
def install():
    """Install the latest update."""
    updater.update()