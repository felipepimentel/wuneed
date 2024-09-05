import importlib
import os
from typing import Dict, Any

class RAGExtension:
    def __init__(self, name: str):
        self.name = name

    def preprocess(self, query: str) -> str:
        return query

    def postprocess(self, results: Dict[str, Any]) -> Dict[str, Any]:
        return results

class ExtensionManager:
    def __init__(self):
        self.extensions: Dict[str, RAGExtension] = {}

    def load_extensions(self):
        extension_dir = os.path.join(os.path.dirname(__file__))
        for filename in os.listdir(extension_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                module = importlib.import_module(f"wuneed.ai.rag.extensions.{module_name}")
                if hasattr(module, "extension"):
                    self.extensions[module_name] = module.extension

    def get_extension(self, name: str) -> RAGExtension:
        return self.extensions.get(name)

    def list_extensions(self) -> Dict[str, RAGExtension]:
        return self.extensions

extension_manager = ExtensionManager()
extension_manager.load_extensions()