# ast_builder.py

class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type
        self.left = left
        self.right = right
        self.value = value

    def __str__(self):
        # Simple string representation of the AST node for testing
        return f"Node(type: {self.type}, value: {self.value})"


def create_ast(rule_string):
    # Placeholder function to generate an AST from the rule string
    # For now, we're not parsing; this is just a simple dummy node
    return Node(type="rule", value=rule_string)


def evaluate_ast(rule_ast, data):
    # Placeholder function to evaluate the AST with provided data
    # For now, let's just assume the rule is always True
    return True
