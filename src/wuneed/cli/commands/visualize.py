import typer
from rich import print
from wuneed.utils.data_visualizer import data_visualizer
from wuneed.utils.metrics_manager import metrics_manager
from wuneed.utils.command_history import command_history
from wuneed.ai.continuous_learning import continuous_learning

app = typer.Typer()

@app.command()
def metrics():
    """Visualize current metrics."""
    metrics = metrics_manager.get_metrics()
    data_visualizer.plot_metrics(metrics)
    print("[bold]Metrics visualization saved as 'wuneed_metrics.png'[/bold]")

@app.command()
def usage():
    """Visualize command usage."""
    history = command_history.get_history()
    usage = {}
    for cmd in history:
        cmd_name = cmd.split(":")[0]
        usage[cmd_name] = usage.get(cmd_name, 0) + 1
    data_visualizer.plot_command_usage(usage)
    print("[bold]Command usage visualization saved as 'command_usage.png'[/bold]")

@app.command()
def feedback():
    """Visualize feedback distribution."""
    feedback_data = continuous_learning.feedback_data
    data_visualizer.plot_feedback_distribution(feedback_data)
    print("[bold]Feedback distribution visualization saved as 'feedback_distribution.png'[/bold]")