import ast

def semantic_analyzer(self, tree):
    errors = []
    variables = set()

    # Traverse the AST
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            # Handle variable assignments
            if isinstance(node.targets[0], ast.Name):
                variables.add(node.targets[0].id)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            # Check if the variable is defined
            if node.id not in variables:
                errors.append(f"Undefined variable: {node.id}")
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            # Check for division by zero
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                errors.append("Division by zero detected.")

    return errors