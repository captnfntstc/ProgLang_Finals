import ast

def semantic_analyzer(tree):
    errors = []
    variables = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if isinstance(node.targets[0], ast.Name):
                variables.add(node.targets[0].id)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if node.id not in variables:
                errors.append(f"Undefined variable: {node.id}")
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                errors.append("Division by zero detected.")
    
    return errors
