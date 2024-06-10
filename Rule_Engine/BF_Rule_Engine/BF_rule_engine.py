import json

class BusinessFunction:
    def __init__(self, func):
        self.func = func

    def execute(self, *args, **kwargs):
        return self.func(*args, **kwargs)

class RuleEngine:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def apply_rules(self, business_func, *args, **kwargs):
        errors = []
        for rule in self.rules:
            try:
                rule(business_func, *args, **kwargs)
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
        def rule(business_func, *args, **kwargs):
            result = business_func.execute(*args, **kwargs)
            local_vars = {"result": result, "args": args, "kwargs": kwargs}
            if eval(condition, {}, local_vars):
                for action in actions:
                    exec(action, {}, local_vars)
        return rule
