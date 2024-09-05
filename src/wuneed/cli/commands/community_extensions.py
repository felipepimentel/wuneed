import typer
from rich import print
from wuneed.utils.community_extension_manager import community_extension_manager

app = typer.Typer()

@app.command()
def list_available():
    """List available community extensions."""
    extensions = community_extension_manager.list_available_extensions()
    print("[bold]Available community extensions:[/bold]")
    for ext in extensions:
        print(f"- {ext['name']} (v{ext['version']}): {ext['description']}")

@app.command()
def list_installed():
    """List installed community extensions."""
    extensions = community_extension_manager.list_installed_extensions()
    print("[bold]Installed community extensions:[/bold]")
    for name, version in extensions.items():
        print(f"- {name} (v{version})")

@app.command()
def install(extension_name: str):
    """Install a community extension."""
    community_extension_manager.install_extension(extension_name)

@app.command()
def uninstall(extension_name: str):
    """Uninstall a community extension."""
    community_extension_manager.uninstall_extension(extension_name)