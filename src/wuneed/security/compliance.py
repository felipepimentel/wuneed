import re
from typing import List, Dict
import ast

class ComplianceChecker:
    def __init__(self):
        self.rules = {
            'password_strength': r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
            'pii_detection': r'\b\d{3}-\d{2}-\d{4}\b'  # Simple SSN detection
        }
        self.coding_standards = {
            'max_line_length': 100,
            'use_snake_case': r'^[a-z_][a-z0-9_]*$',
            'docstring_required': True
        }

    def check_compliance(self, text: str) -> Dict[str, List[str]]:
        violations = {}
        for rule_name, pattern in self.rules.items():
            matches = re.findall(pattern, text)
            if matches:
                violations[rule_name] = matches
        return violations

    def check_coding_standards(self, code: str) -> Dict[str, List[str]]:
        violations = {}
        lines = code.split('\n')

        # Check line length
        for i, line in enumerate(lines):
            if len(line) > self.coding_standards['max_line_length']:
                if 'max_line_length' not in violations:
                    violations['max_line_length'] = []
                violations['max_line_length'].append(f"Line {i+1} exceeds {self.coding_standards['max_line_length']} characters")

        # Parse the code
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {'syntax_error': [str(e)]}

        # Check function and variable names
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if not re.match(self.coding_standards['use_snake_case'], node.name):
                    if 'use_snake_case' not in violations:
                        violations['use_snake_case'] = []
                    violations['use_snake_case'].append(f"{node.__class__.__name__} name '{node.name}' does not follow snake_case")

                # Check for docstrings
                if self.coding_standards['docstring_required'] and not ast.get_docstring(node):
                    if 'docstring_required' not in violations:
                        violations['docstring_required'] = []
                    violations['docstring_required'].append(f"{node.__class__.__name__} '{node.name}' is missing a docstring")

        return violations

compliance_checker = ComplianceChecker()