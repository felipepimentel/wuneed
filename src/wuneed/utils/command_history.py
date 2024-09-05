from wuneed.config.user_config import user_config
from typing import List

class CommandHistory:
    def __init__(self):
        self.history: List[str] = user_config.get('command_history', [])
        self.max_history = user_config.get('max_history_size', 100)

    def add_command(self, command: str):
        self.history.append(command)
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        user_config.set('command_history', self.history)

    def get_history(self) -> List[str]:
        return self.history

    def clear_history(self):
        self.history = []
        user_config.set('command_history', self.history)

command_history = CommandHistory()