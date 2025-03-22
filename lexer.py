import re

def lexer(self, code):
        tokens = re.findall(r'[a-zA-Z_][a-zA-Z_0-9]*|[=+\-*/()]|\d+', code)
        return tokens