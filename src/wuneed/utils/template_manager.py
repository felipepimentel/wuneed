from wuneed.config.user_config import user_config
from typing import Dict, Any
import re

class TemplateManager:
    def __init__(self):
        self.templates: Dict[str, str] = user_config.get('templates', {})

    def add_template(self, name: str, template: str):
        self.templates[name] = template
        user_config.set('templates', self.templates)

    def remove_template(self, name: str):
        if name in self.templates:
            del self.templates[name]
            user_config.set('templates', self.templates)

    def get_template(self, name: str) -> str:
        return self.templates.get(name)

    def list_templates(self) -> Dict[str, str]:
        return self.templates

    def apply_template(self, name: str, params: Dict[str, Any]) -> str:
        template = self.get_template(name)
        if not template:
            raise ValueError(f"Template '{name}' not found")
        
        def replace(match):
            param_name = match.group(1)
            return str(params.get(param_name, match.group(0)))

        return re.sub(r'\{(\w+)\}', replace, template)

template_manager = TemplateManager()