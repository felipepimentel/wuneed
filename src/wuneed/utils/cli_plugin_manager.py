import importlib
import os
from typing import Dict, Any
import typer

class CLIPluginManager:
    def __init__(self):
        self.plugins: Dict[str, typer.Typer] = {}

    def load_plugins(self):
        plugin_dir = os.path.join(os.path.dirname(__file__), "..", "cli", "plugins")
        for filename in os.listdir(plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                module = importlib.import_module(f"wuneed.cli.plugins.{module_name}")
                if hasattr(module, "plugin"):
                    self.plugins[module_name] = module.plugin

    def get_plugin(self, name: str) -> typer.Typer:
        return self.plugins.get(name)

    def list_plugins(self) -> Dict[str, typer.Typer]:
        return self.plugins

cli_plugin_manager = CLIPluginManager()
cli_plugin_manager.load_plugins()