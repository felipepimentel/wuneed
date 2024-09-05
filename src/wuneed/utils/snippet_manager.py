from wuneed.config.user_config import user_config
from typing import Dict

class SnippetManager:
    def __init__(self):
        self.snippets: Dict[str, str] = user_config.get('snippets', {})

    def add_snippet(self, name: str, code: str):
        self.snippets[name] = code
        user_config.set('snippets', self.snippets)

    def remove_snippet(self, name: str):
        if name in self.snippets:
            del self.snippets[name]
            user_config.set('snippets', self.snippets)

    def get_snippet(self, name: str) -> str:
        return self.snippets.get(name)

    def list_snippets(self) -> Dict[str, str]:
        return self.snippets

snippet_manager = SnippetManager()