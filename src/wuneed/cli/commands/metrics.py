import typer
from rich import print
from wuneed.utils.metrics_manager import metrics_manager

app = typer.Typer()

@app.command()
def show():
    """Show current metrics."""
    metrics = metrics_manager.get_metrics()
    print("[bold]Current Metrics:[/bold]")
    for name, value in metrics.items():
        print(f"{name}: {value}")

@app.command()
def clear():
    """Clear all metrics."""
    metrics_manager.clear_metrics()
    print("[bold]Metrics cleared.[/bold]")