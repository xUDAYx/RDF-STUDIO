import json

class BusinessValueObject:
    def __init__(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

class RuleEngine:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def apply_rules(self, bvo):
        errors = []
        for rule in self.rules:
            try:
                rule(bvo)
            except Exception as e:
                errors.append(str(e))
        return errors

    def load_rules_from_json(self, json_file_path):
        with open(json_file_path, 'r') as file:
            rules = json.load(file)['rules']
            for rule in rules:
                condition = rule['condition']
                actions = rule['actions']
                self.add_rule(self.create_rule(condition, actions))

    def create_rule(self, condition, actions):
        def rule(bvo):
            data = bvo.get_data()
            if eval(condition, {}, data):
                for action in actions:
                    exec(action, {}, data)
                bvo.set_data(data)
        return rule
