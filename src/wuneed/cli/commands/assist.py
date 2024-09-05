import typer
from rich import print
from wuneed.ai.copilot import ai_copilot
from wuneed.ai.rag.plugin_manager import plugin_manager
from typing import List
from wuneed.utils.logger import wuneed_logger
from wuneed.utils.command_history import command_history
from wuneed.utils.hook_manager import hook_manager
from wuneed.ai.context_recommender import context_recommender

app = typer.Typer()

@app.command()
def suggest(query: str, plugins: List[str] = typer.Option([], "--plugin", "-p")):
    """Get an AI-suggested command with optional RAG plugins."""
    hook_manager.run_hook("pre_command", "suggest", query=query, plugins=plugins)
    wuneed_logger.log_command("suggest", {"query": query, "plugins": plugins})
    suggestion = ai_copilot.suggest_command(query, plugins)
    print(f"[bold]Suggested command:[/bold] {suggestion}")
    command_history.add_command(f"suggest: {query}")
    hook_manager.run_hook("post_command", "suggest", query=query, plugins=plugins, suggestion=suggestion)

@app.command()
def explain(command: str, plugins: List[str] = typer.Option([], "--plugin", "-p")):
    """Get an explanation for a command with optional RAG plugins."""
    explanation = ai_copilot.explain_command(command, plugins)
    print(f"[bold]Explanation:[/bold] {explanation}")

@app.command()
def list_plugins():
    """List available RAG plugins."""
    plugins = plugin_manager.list_plugins()
    print("[bold]Available RAG plugins:[/bold]")
    for name in plugins:
        print(f"- {name}")

@app.command()
def feedback(query: str, suggestion: str, helpful: bool = typer.Option(..., prompt=True), comment: str = typer.Option("", prompt=True)):
    """Provide feedback on a suggestion."""
    ai_copilot.provide_feedback(query, suggestion, helpful, comment)
    print("[bold]Thank you for your feedback![/bold]")

@app.command()
def analyze_security(code: str, plugins: List[str] = typer.Option(["security_analyzer"], "--plugin", "-p")):
    """Analyze code for potential security issues."""
    analysis = ai_copilot.analyze_security(code, plugins)
    print("[bold]Security Analysis:[/bold]")
    for issue in analysis:
        print(f"- {issue['type']}: {issue['description']}")

@app.command()
def history():
    """Show command history."""
    history = command_history.get_history()
    for i, cmd in enumerate(history, 1):
        print(f"{i}. {cmd}")

@app.command()
def clear_history():
    """Clear command history."""
    command_history.clear_history()
    print("[bold]Command history cleared.[/bold]")

@app.command()
def recommend():
    """Get a command recommendation based on the current project context."""
    recommendation = context_recommender.recommend_command()
    print(f"[bold]Recommended command:[/bold] {recommendation}")