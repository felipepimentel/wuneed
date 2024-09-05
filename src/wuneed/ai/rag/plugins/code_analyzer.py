from wuneed.ai.rag.plugin_manager import RAGPlugin
import re
from typing import List, Dict, Any

class CodeAnalyzerPlugin(RAGPlugin):
    def __init__(self):
        super().__init__("code_analyzer")

    def process(self, query: str, context: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for item in context:
            if "text" in item:
                code_blocks = re.findall(r'```[\s\S]*?```', item["text"])
                if code_blocks:
                    item["code_blocks"] = code_blocks
                    item["code_languages"] = [self.detect_language(block) for block in code_blocks]
                    item["code_complexity"] = [self.analyze_complexity(block) for block in code_blocks]
                    item["code_metrics"] = [self.calculate_metrics(block) for block in code_blocks]
        return context

    def detect_language(self, code_block: str) -> str:
        languages = {
            "python": ["def ", "class ", "import ", "from "],
            "javascript": ["function ", "const ", "let ", "var "],
            "java": ["public ", "private ", "class ", "interface "],
            "c++": ["#include", "using namespace", "int main("],
        }
        for lang, keywords in languages.items():
            if any(keyword in code_block for keyword in keywords):
                return lang
        return "unknown"

    def analyze_complexity(self, code_block: str) -> str:
        lines = code_block.split("\n")
        if len(lines) < 10:
            return "Low"
        elif len(lines) < 50:
            return "Medium"
        else:
            return "High"

    def calculate_metrics(self, code_block: str) -> Dict[str, Any]:
        lines = code_block.split("\n")
        return {
            "line_count": len(lines),
            "character_count": len(code_block),
            "average_line_length": sum(len(line) for line in lines) / len(lines) if lines else 0,
        }

plugin = CodeAnalyzerPlugin()