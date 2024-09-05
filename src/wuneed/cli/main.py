import typer
from rich import print
from wuneed.cli.commands import transcribe, config, plugin, workflow, assist
from wuneed.ui.tui import tui
from wuneed.telemetry.collector import telemetry_collector
from wuneed.security.compliance import compliance_checker
from wuneed.workflows.builder import workflow_builder
from wuneed.utils.language import language_manager
from wuneed.utils.auto_doc import auto_documentation
from wuneed.utils.logger import main_logger
from wuneed import __version__

app = typer.Typer()

app.add_typer(transcribe.app, name="transcribe")
app.add_typer(config.app, name="config")
app.add_typer(plugin.app, name="plugin")
app.add_typer(workflow.app, name="workflow")
app.add_typer(assist.app, name="assist")

@app.command()
def version():
    """Display the current version of wuneed."""
    print(f"wuneed version: [bold]{__version__}[/bold]")

@app.command()
def tui_mode():
    """Launch the Text User Interface mode."""
    try:
        tui.run()
    except Exception as e:
        main_logger.exception("Error in TUI mode")
        print(f"[red]Error in TUI mode: {str(e)}[/red]")

@app.command()
def check_compliance(text: str):
    """Check text for compliance violations."""
    try:
        violations = compliance_checker.check_compliance(text)
        if violations:
            print("[red]Compliance violations found:[/red]")
            for rule, matches in violations.items():
                print(f"  [bold]{rule}:[/bold] {', '.join(matches)}")
        else:
            print("[green]No compliance violations found.[/green]")
    except Exception as e:
        main_logger.exception("Error in compliance check")
        print(f"[red]Error in compliance check: {str(e)}[/red]")

@app.command()
def build_workflow():
    """Launch the visual workflow builder."""
    try:
        workflow_builder.run()
    except Exception as e:
        main_logger.exception("Error in workflow builder")
        print(f"[red]Error in workflow builder: {str(e)}[/red]")

@app.command()
def set_language(lang_code: str):
    """Set the application language."""
    try:
        language_manager.set_language(lang_code)
        print(f"[green]Language set to: {lang_code}[/green]")
    except ValueError as e:
        main_logger.error(f"Error setting language: {str(e)}")
        print(f"[red]Error: {str(e)}[/red]")

@app.command()
def generate_docs():
    """Generate auto-documentation based on usage patterns."""
    try:
        auto_documentation.generate_documentation()
        print("[green]Auto-documentation generated successfully.[/green]")
    except Exception as e:
        main_logger.exception("Error generating auto-documentation")
        print(f"[red]Error generating auto-documentation: {str(e)}[/red]")

if __name__ == "__main__":
    try:
        telemetry_collector.log_event("cli_start", {})
        app()
    except Exception as e:
        main_logger.exception("Unhandled exception in main CLI")
        print(f"[red]An unexpected error occurred: {str(e)}[/red]")
    finally:
        telemetry_collector.save_data()