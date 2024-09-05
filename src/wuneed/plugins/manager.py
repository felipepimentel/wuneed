import importlib
import os
from typing import Dict, Any, List
from wuneed.config.manager import config_manager
from wuneed.plugins.sandbox import sandbox

class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, Any] = {}
        self.hooks: Dict[str, List[callable]] = {}
        self.load_activated_plugins()

    def load_activated_plugins(self):
        for plugin_name in config_manager.config.activated_plugins:
            self.load_plugin(plugin_name)

    def load_plugin(self, plugin_name: str):
        try:
            plugin_path = os.path.join("plugins", f"{plugin_name}.py")
            module = sandbox.load_plugin(plugin_path)
            self.plugins[plugin_name] = module
            self.register_hooks(module)
            print(f"Loaded plugin: {plugin_name}")
        except Exception as e:
            print(f"Failed to load plugin: {plugin_name}. Error: {str(e)}")

    def register_hooks(self, module):
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if callable(attr) and hasattr(attr, '_wuneed_hook'):
                hook_name = getattr(attr, '_wuneed_hook')
                if hook_name not in self.hooks:
                    self.hooks[hook_name] = []
                self.hooks[hook_name].append(attr)

    def activate_plugin(self, plugin_name: str):
        if plugin_name not in config_manager.config.activated_plugins:
            config_manager.config.activated_plugins.append(plugin_name)
            config_manager.save_config()
            self.load_plugin(plugin_name)

    def deactivate_plugin(self, plugin_name: str):
        if plugin_name in config_manager.config.activated_plugins:
            config_manager.config.activated_plugins.remove(plugin_name)
            config_manager.save_config()
            if plugin_name in self.plugins:
                del self.plugins[plugin_name]

    def get_plugin(self, plugin_name: str):
        return self.plugins.get(plugin_name)

    def run_hook(self, hook_name: str, *args, **kwargs):
        if hook_name in self.hooks:
            for hook in self.hooks[hook_name]:
                sandbox.run_plugin_function(self.plugins[hook.__module__], hook.__name__, *args, **kwargs)

def wuneed_hook(hook_name: str):
    def decorator(func):
        func._wuneed_hook = hook_name
        return func
    return decorator

plugin_manager = PluginManager()