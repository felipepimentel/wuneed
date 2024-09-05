import typer
from rich import print
from wuneed.plugins.manager import plugin_manager

app = typer.Typer()

@app.command()
def install(plugin_name: str):
    """Install and activate a plugin."""
    plugin_manager.activate_plugin(plugin_name)
    print(f"[green]Installed and activated plugin: {plugin_name}[/green]")

@app.command()
def uninstall(plugin_name: str):
    """Deactivate and uninstall a plugin."""
    plugin_manager.deactivate_plugin(plugin_name)
    print(f"[green]Deactivated and uninstalled plugin: {plugin_name}[/green]")

@app.command()
def list():
    """List all activated plugins."""
    plugins = plugin_manager.plugins.keys()
    if plugins:
        print("[bold]Activated plugins:[/bold]")
        for plugin in plugins:
            print(f"  - {plugin}")
    else:
        print("[yellow]No plugins are currently activated.[/yellow]")