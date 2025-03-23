import ast

def semantic_analyzer(tree):
    errors = []
    variables = set()

    # Manually define built-in functions
    predefined_functions = {"print", "len", "range", "int", "str", "float", "bool", "list", "dict", "set"}

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    variables.add(target.id)  # Store assigned variables

        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if node.id not in variables and node.id not in predefined_functions:
                errors.append(f"Undefined variable: {node.id}")

        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                errors.append("Division by zero detected.")

    return errors
