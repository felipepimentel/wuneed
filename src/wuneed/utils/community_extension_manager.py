import requests
import json
import os
from typing import List, Dict, Any
from wuneed.config.user_config import user_config

class CommunityExtensionManager:
    def __init__(self):
        self.extension_registry_url = "https://api.github.com/repos/wuneed/extension-registry/contents/registry.json"
        self.installed_extensions = user_config.get('installed_extensions', {})

    def fetch_extension_registry(self) -> List[Dict[str, Any]]:
        response = requests.get(self.extension_registry_url)
        if response.status_code == 200:
            content = json.loads(response.json()['content'])
            return content['extensions']
        else:
            print(f"Failed to fetch extension registry: {response.status_code}")
            return []

    def install_extension(self, extension_name: str):
        registry = self.fetch_extension_registry()
        extension = next((ext for ext in registry if ext['name'] == extension_name), None)
        if extension:
            response = requests.get(extension['url'])
            if response.status_code == 200:
                extension_dir = os.path.join(os.path.dirname(__file__), "..", "community_extensions")
                os.makedirs(extension_dir, exist_ok=True)
                with open(os.path.join(extension_dir, f"{extension_name}.py"), "w") as f:
                    f.write(response.text)
                self.installed_extensions[extension_name] = extension['version']
                user_config.set('installed_extensions', self.installed_extensions)
                print(f"Extension {extension_name} installed successfully.")
            else:
                print(f"Failed to download extension: {response.status_code}")
        else:
            print(f"Extension {extension_name} not found in registry.")

    def uninstall_extension(self, extension_name: str):
        if extension_name in self.installed_extensions:
            extension_file = os.path.join(os.path.dirname(__file__), "..", "community_extensions", f"{extension_name}.py")
            if os.path.exists(extension_file):
                os.remove(extension_file)
            del self.installed_extensions[extension_name]
            user_config.set('installed_extensions', self.installed_extensions)
            print(f"Extension {extension_name} uninstalled successfully.")
        else:
            print(f"Extension {extension_name} is not installed.")

    def list_available_extensions(self) -> List[Dict[str, Any]]:
        return self.fetch_extension_registry()

    def list_installed_extensions(self) -> Dict[str, str]:
        return self.installed_extensions

community_extension_manager = CommunityExtensionManager()