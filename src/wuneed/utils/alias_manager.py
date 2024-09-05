from wuneed.config.user_config import user_config
from typing import Dict

class AliasManager:
    def __init__(self):
        self.aliases: Dict[str, str] = user_config.get('aliases', {})

    def add_alias(self, alias: str, command: str):
        self.aliases[alias] = command
        user_config.set('aliases', self.aliases)

    def remove_alias(self, alias: str):
        if alias in self.aliases:
            del self.aliases[alias]
            user_config.set('aliases', self.aliases)

    def get_command(self, alias: str) -> str:
        return self.aliases.get(alias)

    def list_aliases(self) -> Dict[str, str]:
        return self.aliases

alias_manager = AliasManager()