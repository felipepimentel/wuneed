import yaml
from typing import List, Dict
from wuneed.config.manager import config_manager

class WorkflowManager:
    def __init__(self):
        self.workflows = config_manager.get_active_profile().get('workflows', {})

    def create_workflow(self, name: str, steps: List[Dict[str, str]]):
        self.workflows[name] = steps
        self._save_workflows()

    def run_workflow(self, name: str):
        if name not in self.workflows:
            raise ValueError(f"Workflow '{name}' not found")
        for step in self.workflows[name]:
            command = step['command']
            # Here you would actually execute the command
            print(f"Executing: {command}")

    def list_workflows(self):
        return list(self.workflows.keys())

    def _save_workflows(self):
        profile = config_manager.get_active_profile()
        profile['workflows'] = self.workflows
        config_manager.update_profile(config_manager.config.active_profile, profile)

workflow_manager = WorkflowManager()