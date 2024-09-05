from typing import Dict, Callable, List
import importlib
import os

class HookManager:
    def __init__(self):
        self.hooks: Dict[str, List[Callable]] = {}

    def register_hook(self, hook_name: str, func: Callable):
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(func)

    def run_hook(self, hook_name: str, *args, **kwargs):
        if hook_name in self.hooks:
            for func in self.hooks[hook_name]:
                func(*args, **kwargs)

    def load_hooks(self):
        hook_dir = os.path.join(os.path.dirname(__file__), "..", "hooks")
        for filename in os.listdir(hook_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                module = importlib.import_module(f"wuneed.hooks.{module_name}")
                if hasattr(module, "register_hooks"):
                    module.register_hooks(self)

hook_manager = HookManager()
hook_manager.load_hooks()