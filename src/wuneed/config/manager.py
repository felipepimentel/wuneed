import os
import yaml
from typing import Dict, Any
from pydantic import BaseModel

class WuneedConfig(BaseModel):
    profiles: Dict[str, Dict[str, Any]] = {}
    active_profile: str = "default"
    activated_plugins: list[str] = []

class ConfigManager:
    def __init__(self):
        self.config_path = os.path.expanduser("~/.wuneed/config.yml")
        self.config = self.load_config()

    def load_config(self) -> WuneedConfig:
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config_data = yaml.safe_load(f)
            return WuneedConfig(**config_data)
        return WuneedConfig()

    def save_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config.dict(), f)

    def get_active_profile(self) -> Dict[str, Any]:
        return self.config.profiles.get(self.config.active_profile, {})

    def set_active_profile(self, profile_name: str):
        if profile_name not in self.config.profiles:
            self.config.profiles[profile_name] = {}
        self.config.active_profile = profile_name
        self.save_config()

    def update_profile(self, profile_name: str, settings: Dict[str, Any]):
        if profile_name not in self.config.profiles:
            self.config.profiles[profile_name] = {}
        self.config.profiles[profile_name].update(settings)
        self.save_config()

config_manager = ConfigManager()