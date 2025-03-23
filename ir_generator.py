import ast

def generate_ir(tree):
    ir_code = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if isinstance(node.targets[0], ast.Name):
                ir_code.append(f"STORE {node.targets[0].id}")
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op).__name__
            ir_code.append(f"BINARY_OP {op_type}")
        elif isinstance(node, ast.Constant):
            ir_code.append(f"LOAD_CONST {node.value}")
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            ir_code.append(f"LOAD_VAR {node.id}")
        elif isinstance(node, ast.Call):
            ir_code.append(f"CALL {node.func.id}")
        elif isinstance(node, ast.If):
            ir_code.append("IF_START")
        elif isinstance(node, ast.Return):
            ir_code.append("RETURN")
    
    return "\n".join(ir_code)
