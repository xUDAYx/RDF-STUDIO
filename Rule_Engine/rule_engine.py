import json
import re

class HtmlRuleEngine:
    def __init__(self, rules_file):
        self.rules = self.load_rules(rules_file)

    def load_rules(self, filename):
        with open(filename, 'r') as file:
            rules = json.load(file)["rules"]
        return rules

    def apply_rules(self, html_content):
        errors = []
        lines = html_content.splitlines()

        if not re.search(r'<table.*?>', html_content, re.IGNORECASE | re.DOTALL):
            errors.append("Global: Table tag should compulsorily be present.")

        for i, line in enumerate(lines, 1):
            for rule in self.rules:
                pattern = rule["pattern"]
                matches = re.finditer(pattern, line, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    highlighted_code = line.replace(match.group(0), f'<span style="color:red;">{match.group(0)}</span>')
                    errors.append(f"Line {i}: {rule['description']}. Offending code: {highlighted_code}")
        return errors
