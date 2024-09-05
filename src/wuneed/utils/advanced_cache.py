import redis
import json
from typing import Any, Optional

class AdvancedCache:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def set(self, key: str, value: Any, expiration: int = 3600):
        self.redis.setex(key, expiration, json.dumps(value))

    def get(self, key: str) -> Optional[Any]:
        value = self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    def delete(self, key: str):
        self.redis.delete(key)

advanced_cache = AdvancedCache()