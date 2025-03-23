import ast
import subprocess

def run_code(code):
    try:
        result = subprocess.run(
            ["python", "-c", code],  
            capture_output=True,
            text=True,
            timeout=5  
        )
        output = result.stdout if result.stdout else result.stderr
    except Exception as e:
        output = f"Execution Error: {str(e)}"
    
    return output.strip()
