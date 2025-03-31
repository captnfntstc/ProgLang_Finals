import ast

def semantic_analyzer(tree):
    errors = []
    warnings = []
    variables = {}  # Tracks variables and their types
    functions = {}  # Tracks function definitions and argument counts
    used_variables = set()  # Tracks variables that are used

    predefined_functions = {"print", "len", "range", "int", "str", "float", "bool", "list", "dict", "set"}

    def get_type(node):
        """Determine the type of a node."""
        if isinstance(node, ast.Constant):
            return type(node.value).__name__
        elif isinstance(node, ast.Name):
            return variables.get(node.id, None)  # Return stored type if available
        return None

    for node in ast.walk(tree):
        # Track variable assignments
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id
                    value_type = get_type(node.value)

                    if var_name in variables:
                        warnings.append(f"Warning: Variable '{var_name}' is redefined.")

                    variables[var_name] = value_type  # Store type instead of just tracking existence
        
        # Detect usage of undefined variables
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if node.id not in variables and node.id not in predefined_functions:
                errors.append(f"Undefined variable: '{node.id}'")
            else:
                used_variables.add(node.id)  # Track that this variable is used

        # Division by zero check
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            right_type = get_type(node.right)
            if right_type == "int" and isinstance(node.right, ast.Constant) and node.right.value == 0:
                errors.append("Error: Division by zero detected.")

        # Type checking for binary operations
        elif isinstance(node, ast.BinOp):
            left_type = get_type(node.left)
            right_type = get_type(node.right)

            if left_type and right_type and left_type != right_type:
                errors.append(f"Type Error: Cannot perform operation between {left_type} and {right_type}.")

        # Function definitions
        elif isinstance(node, ast.FunctionDef):
            func_name = node.name
            arg_count = len(node.args.args)
            functions[func_name] = arg_count
        
        # Function call validation
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name not in functions and func_name not in predefined_functions:
                    errors.append(f"Error: Undefined function '{func_name}' called.")
                elif func_name in functions:
                    expected_args = functions[func_name]
                    given_args = len(node.args)
                    if expected_args != given_args:
                        errors.append(f"Error: Function '{func_name}' expects {expected_args} arguments, but {given_args} were given.")

    # Check for unused variables
    for var in variables.keys():
        if var not in used_variables:
            warnings.append(f"Warning: Variable '{var}' is assigned but never used.")

    return errors, warnings
