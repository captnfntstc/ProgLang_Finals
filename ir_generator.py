import ast

def generate_ir(tree):
    ir_code = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            ir_code.append(f"STORE {node.targets[0].id}")
        elif isinstance(node, ast.BinOp):
            ir_code.append("BINARY_OP")
        elif isinstance(node, ast.Constant):
            ir_code.append(f"LOAD_CONST {node.value}")
    
    return "\n".join(ir_code)
