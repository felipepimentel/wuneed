from typing import Dict, Any
import time

class MetricsManager:
    def __init__(self):
        self.metrics: Dict[str, Any] = {}

    def start_timer(self, name: str):
        self.metrics[f"{name}_start_time"] = time.time()

    def end_timer(self, name: str):
        start_time = self.metrics.get(f"{name}_start_time")
        if start_time:
            self.metrics[f"{name}_duration"] = time.time() - start_time
            del self.metrics[f"{name}_start_time"]

    def add_metric(self, name: str, value: Any):
        self.metrics[name] = value

    def get_metrics(self) -> Dict[str, Any]:
        return self.metrics

    def clear_metrics(self):
        self.metrics.clear()

metrics_manager = MetricsManager()