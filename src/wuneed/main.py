import typer
from wuneed.cli.commands import assist, config, alias, template, snippet, docs, workflow, metrics, visualize, update, community_extensions, extension_ci_cd
from wuneed.utils.cli_plugin_manager import cli_plugin_manager

app = typer.Typer()

app.add_typer(assist.app, name="assist")
app.add_typer(config.app, name="config")
app.add_typer(alias.app, name="alias")
app.add_typer(template.app, name="template")
app.add_typer(snippet.app, name="snippet")
app.add_typer(docs.app, name="docs")
app.add_typer(workflow.app, name="workflow")
app.add_typer(metrics.app, name="metrics")
app.add_typer(visualize.app, name="visualize")
app.add_typer(update.app, name="update")
app.add_typer(community_extensions.app, name="extensions")
app.add_typer(extension_ci_cd.app, name="extension-ci-cd")

# Add CLI plugins
for name, plugin in cli_plugin_manager.list_plugins().items():
    app.add_typer(plugin, name=name)

if __name__ == "__main__":
    app()