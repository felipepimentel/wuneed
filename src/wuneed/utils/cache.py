import json
import os
from typing import Any, Dict
from datetime import datetime, timedelta

class SmartCache:
    def __init__(self, cache_dir: str = ".wuneed_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_file(self, key: str) -> str:
        return os.path.join(self.cache_dir, f"{key}.json")

    def set(self, key: str, value: Any, ttl: int = 3600):
        cache_data = {
            "value": value,
            "expires_at": (datetime.now() + timedelta(seconds=ttl)).isoformat()
        }
        with open(self._get_cache_file(key), "w") as f:
            json.dump(cache_data, f)

    def get(self, key: str) -> Any:
        cache_file = self._get_cache_file(key)
        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                cache_data = json.load(f)
            if datetime.now() < datetime.fromisoformat(cache_data["expires_at"]):
                return cache_data["value"]
        return None

    def clear(self):
        for file in os.listdir(self.cache_dir):
            os.remove(os.path.join(self.cache_dir, file))

smart_cache = SmartCache()