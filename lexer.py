import re

def lexer(self, code):
    # Define valid token patterns
    token_pattern = r'[a-zA-Z_][a-zA-Z_0-9]*|[=+\-*/()]|\d+|".*?"|\'.*?\''
    valid_tokens = re.findall(token_pattern, code)

    # Find all individual words/characters (including invalid ones)
    all_tokens = re.findall(r'\S+|\n', code)  # Matches all non-whitespace sequences and newlines

    # Detect invalid tokens (anything not matching the valid pattern)
    invalid_tokens = [token for token in all_tokens if not re.fullmatch(token_pattern, token) and token.strip()]

    if invalid_tokens:
        raise ValueError(f"Lexical Analysis Error: Invalid token(s) detected: {', '.join(invalid_tokens)}")

    return valid_tokens