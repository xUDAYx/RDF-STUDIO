import json
import re

class JsRuleEngine:
    def __init__(self, rules_file):
        self.rules = self.load_rules(rules_file)

    def load_rules(self, filename):
        with open(filename, 'r') as file:
            rules = json.load(file)["rules"]
        return rules

    def apply_rules(self, js_content):
        errors = []
        lines = js_content.splitlines()

        for i, line in enumerate(lines, 1):
            for rule in self.rules:
                pattern = rule["pattern"]
                matches = re.finditer(pattern, line, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    highlighted_code = line.replace(match.group(0), f'<span style="color:red;">{match.group(0)}</span>')
                    errors.append(f"Line {i}: {rule['description']}. Offending code: {highlighted_code}")
        return errors
