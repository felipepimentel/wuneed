from wuneed.ai.rag.plugin_manager import RAGPlugin
import re
from typing import List, Dict, Any

class SecurityAnalyzerPlugin(RAGPlugin):
    def __init__(self):
        super().__init__("security_analyzer")

    def process(self, query: str, context: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for item in context:
            if "text" in item:
                item["security_issues"] = self.analyze_security(item["text"])
        return context

    def analyze_security(self, text: str) -> List[Dict[str, str]]:
        issues = []
        patterns = {
            "hardcoded_password": r'password\s*=\s*["\'][^"\']+["\']',
            "sql_injection": r'execute\s*\(\s*["\'][^"\']*\{.+\}[^"\']*["\']',
            "xss_vulnerability": r'innerHTML\s*=',
        }
        
        for issue_type, pattern in patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                issues.append({
                    "type": issue_type,
                    "description": f"Potential {issue_type.replace('_', ' ')} detected"
                })
        
        return issues

plugin = SecurityAnalyzerPlugin()