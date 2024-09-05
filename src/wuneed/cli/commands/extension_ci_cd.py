import typer
from rich import print
from wuneed.utils.extension_ci_cd import extension_ci_cd

app = typer.Typer()

@app.command()
def trigger(extension_name: str, repo_url: str, branch: str = "main"):
    """Trigger CI/CD pipeline for a community extension."""
    result = extension_ci_cd.trigger_ci_cd(extension_name, repo_url, branch)
    if result["status"] == "success":
        print(f"[bold green]{result['message']}[/bold green]")
    else:
        print(f"[bold red]{result['message']}[/bold red]")

@app.command()
def status(extension_name: str):
    """Check the status of a CI/CD pipeline for a community extension."""
    result = extension_ci_cd.get_ci_cd_status(extension_name)
    print(f"[bold]CI/CD Status for {extension_name}:[/bold] {result['status']}")
    print(f"Message: {result['message']}")