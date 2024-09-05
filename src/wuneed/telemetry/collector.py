import json
from datetime import datetime
from wuneed.config.manager import config_manager

class TelemetryCollector:
    def __init__(self):
        self.data = []

    def log_event(self, event_type: str, event_data: dict):
        if config_manager.get_active_profile().get('telemetry_enabled', False):
            self.data.append({
                'timestamp': datetime.now().isoformat(),
                'type': event_type,
                'data': event_data
            })

    def save_data(self):
        if self.data:
            with open('telemetry.json', 'w') as f:
                json.dump(self.data, f)
            self.data = []

telemetry_collector = TelemetryCollector()