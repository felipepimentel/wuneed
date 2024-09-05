import os
from typing import List, Dict
from wuneed.telemetry.collector import telemetry_collector

class AutoDocumentation:
    def __init__(self, output_dir: str = "auto_docs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_usage_patterns(self) -> Dict[str, int]:
        command_usage = {}
        for event in telemetry_collector.data:
            if event['type'] == 'command_executed':
                command = event['data']['command']
                command_usage[command] = command_usage.get(command, 0) + 1
        return command_usage

    def generate_documentation(self):
        usage_patterns = self.generate_usage_patterns()
        
        with open(os.path.join(self.output_dir, "usage_patterns.md"), "w") as f:
            f.write("# Wuneed Usage Patterns\n\n")
            for command, count in sorted(usage_patterns.items(), key=lambda x: x[1], reverse=True):
                f.write(f"- `{command}`: Used {count} times\n")

        # Here you would add more documentation generation logic
        # For example, generating documentation for frequently used workflows,
        # or documenting common error patterns and their solutions

auto_documentation = AutoDocumentation()