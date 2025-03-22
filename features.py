import re
import ast
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

class CompilerFeatures:
    def on_text_change(self, event=None):
        self.unsaved_changes = True

    def new_file(self):
        if self.unsaved_changes:
            response = messagebox.askyesnocancel("Unsaved Changes", "You have unsaved changes. Do you want to save?")
            if response:  # User clicked 'Yes'
                self.save_file()
            elif response is None:  # User clicked 'Cancel'
                return
        self.text_area.delete(1.0, tk.END)  
        self.unsaved_changes = False

    
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, file.read())
            self.current_file = file_path
            self.unsaved_changes = False
    
    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.text_area.get(1.0, tk.END).strip())
            self.unsaved_changes = False
        else:
            self.save_file_as()
    
    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            self.current_file = file_path
            self.save_file()
    
    def find_text(self):
        find_str = simpledialog.askstring("Find", "Enter text to find:")
        if find_str:
            self.text_area.tag_remove("highlight", "1.0", tk.END)
            start_pos = "1.0"
            while True:
                start_pos = self.text_area.search(find_str, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(find_str)}c"
                self.text_area.tag_add("highlight", start_pos, end_pos)
                start_pos = end_pos
            self.text_area.tag_config("highlight", background="yellow")
    
    def replace_text(self):
        find_str = simpledialog.askstring("Replace", "Enter text to find:")
        replace_str = simpledialog.askstring("Replace", "Enter replacement text:")
        if find_str and replace_str:
            content = self.text_area.get(1.0, tk.END)
            content = content.replace(find_str, replace_str)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, content)
    
    
    def update_line_numbers(self, event=None):
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)
        line_count = self.text_area.get(1.0, tk.END).count('\n')
        self.line_numbers.insert(1.0, "\n".join(str(i) for i in range(1, line_count + 1)))
        self.line_numbers.config(state=tk.DISABLED)
    
    def display_output(self, text):
        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, text)
        self.output_area.config(state=tk.DISABLED)
    
    def run_lexer(self):
        code = self.text_area.get(1.0, tk.END)
        tokens = self.lexer(code)
        self.display_output(f"Tokens:\n{tokens}")
    
    def run_parser(self):
        code = self.text_area.get(1.0, tk.END)
        tree = self.parser(code)  
        self.display_output("Syntax Analysis: Valid")
    
    def run_semantic(self):
        code = self.text_area.get(1.0, tk.END)
        tree = self.parser(code)
        errors = self.semantic_analyzer(tree)
        output = "Semantic Analysis: " + ("No issues found" if not errors else "\n".join(errors))
        self.display_output(output)

    def run_ir(self):
        code = self.text_area.get(1.0, tk.END)
        tree = self.parser(code)
        ir_code = self.generate_ir(tree)
        self.display_output(f"Intermediate Code:\n{ir_code}")
    
    
    def run_all(self):
        code = self.text_area.get(1.0, tk.END)
        tokens = self.lexer(code)
        tree = self.parser(code)
        syntax_output = "Syntax Analysis: Valid"
        
        errors = self.semantic_analyzer(tree)
        semantic_output = "Semantic Analysis: " + ("No issues found" if not errors else "\n".join(errors))
        
        ir_code = self.generate_ir(tree)
        
        final_output = (f"Tokens:\n{tokens}\n\n" +
                        f"{syntax_output}\n\n" +
                        f"{semantic_output}\n\n" +
                        f"Intermediate Code:\n{ir_code}")
        self.display_output(final_output)
    
    def lexer(self, code):
        tokens = re.findall(r'[a-zA-Z_][a-zA-Z_0-9]*|[=+\-*/()]|\d+', code)
        return tokens
    
    def parser(self, code):
        return ast.parse(code)
    
    def semantic_analyzer(self, tree):
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
    
    def generate_ir(self, tree):
        ir_code = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                ir_code.append(f"STORE {node.targets[0].id}")
            elif isinstance(node, ast.BinOp):
                ir_code.append("BINARY_OP")
            elif isinstance(node, ast.Constant):
                ir_code.append(f"LOAD_CONST {node.value}")
        return "\n".join(ir_code)
    
    def show_readme(self):
        messagebox.showinfo("README", "Python Mini Compiler\n\nThis tool provides basic file operations and text editing capabilities.")
