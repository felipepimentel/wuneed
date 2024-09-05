from typing import List, Dict, Any
import importlib
import os
import yaml

class RAGPlugin:
    def __init__(self, name: str):
        self.name = name
        self.config = {}

    def process(self, query: str, context: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def load_config(self, config: Dict[str, Any]):
        self.config = config

class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, RAGPlugin] = {}

    def load_plugins(self):
        plugin_dir = os.path.join(os.path.dirname(__file__), "plugins")
        config_file = os.path.join(plugin_dir, "plugin_config.yaml")
        
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        for filename in os.listdir(plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                module = importlib.import_module(f"wuneed.ai.rag.plugins.{module_name}")
                if hasattr(module, "plugin"):
                    plugin = getattr(module, "plugin")
                    plugin.load_config(config.get(plugin.name, {}))
                    self.plugins[plugin.name] = plugin

    def get_plugin(self, name: str) -> RAGPlugin:
        return self.plugins.get(name)

    def list_plugins(self) -> List[str]:
        return list(self.plugins.keys())

plugin_manager = PluginManager()
plugin_manager.load_plugins()