import typer
from rich import print
from wuneed.config.manager import config_manager
from wuneed.config.user_config import user_config

app = typer.Typer()

@app.command()
def set_profile(profile_name: str):
    """Set the active profile."""
    config_manager.set_active_profile(profile_name)
    print(f"[green]Active profile set to: {profile_name}[/green]")

@app.command()
def get_profile():
    """Get the current active profile."""
    profile = config_manager.get_active_profile()
    print(f"[bold]Active profile:[/bold] {config_manager.config.active_profile}")
    print("[bold]Settings:[/bold]")
    for key, value in profile.items():
        print(f"  {key}: {value}")

@app.command()
def update_profile(key: str, value: str):
    """Update a setting in the current profile."""
    profile_name = config_manager.config.active_profile
    config_manager.update_profile(profile_name, {key: value})
    print(f"[green]Updated {key} to {value} in profile {profile_name}[/green]")

@app.command()
def get(key: str):
    """Get a configuration value."""
    value = user_config.get(key)
    print(f"[bold]{key}:[/bold] {value}")

@app.command()
def set(key: str, value: str):
    """Set a configuration value."""
    user_config.set(key, value)
    print(f"[bold]Configuration updated:[/bold] {key} = {value}")

@app.command()
def list():
    """List all configuration values."""
    for key, value in user_config.config.items():
        print(f"[bold]{key}:[/bold] {value}")