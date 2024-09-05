import requests
import json
import os
from typing import Dict, Any
from wuneed.config.user_config import user_config

class ExtensionCICD:
    def __init__(self):
        self.ci_cd_api_url = "https://api.github.com/repos/wuneed/extension-ci-cd/dispatches"
        self.github_token = user_config.get('github_token', '')

    def trigger_ci_cd(self, extension_name: str, repo_url: str, branch: str = "main") -> Dict[str, Any]:
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        payload = {
            "event_type": "extension_update",
            "client_payload": {
                "extension_name": extension_name,
                "repo_url": repo_url,
                "branch": branch
            }
        }
        response = requests.post(self.ci_cd_api_url, headers=headers, data=json.dumps(payload))
        if response.status_code == 204:
            return {"status": "success", "message": f"CI/CD pipeline triggered for {extension_name}"}
        else:
            return {"status": "error", "message": f"Failed to trigger CI/CD pipeline: {response.text}"}

    def get_ci_cd_status(self, extension_name: str) -> Dict[str, Any]:
        # This is a placeholder. In a real implementation, you would query the CI/CD system for the status.
        return {"status": "running", "message": f"CI/CD pipeline for {extension_name} is in progress"}

extension_ci_cd = ExtensionCICD()