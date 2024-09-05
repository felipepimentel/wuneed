from wuneed.config.user_config import user_config
from typing import List, Dict, Any
import json

class WorkflowManager:
    def __init__(self):
        self.workflows: Dict[str, List[Dict[str, Any]]] = user_config.get('workflows', {})

    def add_workflow(self, name: str, steps: List[Dict[str, Any]]):
        self.workflows[name] = steps
        user_config.set('workflows', self.workflows)

    def remove_workflow(self, name: str):
        if name in self.workflows:
            del self.workflows[name]
            user_config.set('workflows', self.workflows)

    def get_workflow(self, name: str) -> List[Dict[str, Any]]:
        return self.workflows.get(name, [])

    def list_workflows(self) -> Dict[str, List[Dict[str, Any]]]:
        return self.workflows

    def execute_workflow(self, name: str, context: Dict[str, Any] = None) -> List[Any]:
        workflow = self.get_workflow(name)
        results = []
        context = context or {}

        for step in workflow:
            command = step['command']
            args = step.get('args', {})
            
            # Replace placeholders in args with context values
            for key, value in args.items():
                if isinstance(value, str) and value.startswith('$'):
                    args[key] = context.get(value[1:], value)

            # Execute the command (you'll need to implement this part)
            result = self.execute_command(command, args)
            results.append(result)

            # Update context with the result
            context[step.get('output_key', f'step_{len(results)}')] = result

        return results

    def execute_command(self, command: str, args: Dict[str, Any]) -> Any:
        # This is a placeholder. You'll need to implement the actual command execution logic.
        # It should integrate with your existing CLI commands.
        print(f"Executing command: {command} with args: {json.dumps(args)}")
        return f"Result of {command}"

workflow_manager = WorkflowManager()