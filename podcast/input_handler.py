import sys
import os

def get_input_text(file_path=None):
    if file_path:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, 'r') as f:
            return f.read()
    
    if not sys.stdin.isatty():
        return sys.stdin.read()
    
    raise ValueError("No input provided. Provide a file path or pipe text via stdin.")
