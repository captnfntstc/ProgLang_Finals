import ast

def parser(code):
    tree = ast.parse(code)
    return tree