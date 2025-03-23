import re, sys, ast, io, subprocess
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from semantic import semantic_analyzer
from ir_generator import generate_ir
from execution import run_code


class CompilerFeatures:
    def __init__(self):
        self.unsaved_changes = False
        self.current_file = None

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

    def run_code(self):
        code = self.text_area.get("1.0", tk.END)  # Get code from text editor
        if not code.strip():
            messagebox.showerror("Error", "No code to run.")
            return
        
        try:
            # Run the code using subprocess and capture output
            process = subprocess.run(["python", "-c", code], capture_output=True, text=True)
            output = process.stdout if process.stdout else process.stderr
            
            # Display output in the output area
            self.output_area.config(state=tk.NORMAL)
            self.output_area.delete("1.0", tk.END)
            self.output_area.insert(tk.END, output)
            self.output_area.config(state=tk.DISABLED)
        
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))
    
    def display_output(self, text):
        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete(1.0, tk.END)

        # Define color mappings for different IR instructions
        color_tags = {
            "STORE": "red",
            "BINARY_OP": "yellow",
            "LOAD_CONST": "blue",
            "LOAD_VAR": "cyan",
            "CALL": "green",
            "IF_START": "magenta",
            "RETURN": "gray"
        }

        # Configure tag colors in Tkinter text widget (MUST be done before inserting)
        for tag, color in color_tags.items():
            self.output_area.tag_config(tag, foreground=color)

        # Apply color tags to the text
        for line in text.split("\n"):
            words = line.split()
            if words:
                instr = words[0]  # First word (IR instruction)
                tag = color_tags.get(instr, None)  # Get corresponding color

                if tag:
                    self.output_area.insert(tk.END, line + "\n", tag)  # Insert with tag
                    self.output_area.tag_add(tag, "end-2l linestart", "end-2l lineend")
                else:
                    self.output_area.insert(tk.END, line + "\n")  # Insert normally

        self.output_area.config(state=tk.DISABLED)

        
    def run_lexer(self):
        try:
            code = self.text_area.get(1.0, tk.END)
            tokens = self.lexer(code)
            self.display_output(f"Tokens:\n{tokens}")
        except Exception as e:
            self.display_output(f"Lexical Analysis Error: {str(e)}")
    
    def run_parser(self):
        try:
            code = self.text_area.get(1.0, tk.END)
            tree = self.parser(code)  
            self.display_output("Syntax Analysis: Valid")
        except Exception as e:
            self.display_output(f"Syntax Analysis Error: {str(e)}")
    
    def run_semantic(self):
        try:
            code = self.text_area.get("1.0", tk.END).strip()  # Get code from text area
            tree = ast.parse(code)  # Convert code to AST
            errors = semantic_analyzer(tree)  # Call function (no 'self')

            output = "Semantic Analysis: " + ("No issues found" if not errors else "\n".join(errors))
            self.display_output(output)  # Show results
        except Exception as e:
            self.display_output(f"Semantic Analysis Error: {str(e)}")

    def run_ir(self):
        try:
            code = self.text_area.get(1.0, tk.END).strip()  # Get code
            tree = ast.parse(code)  # Parse code to AST
            ir_code = generate_ir(tree)  # Call generate_ir (no 'self')

            self.display_output(f"Intermediate Code:\n{ir_code}")  # Show output
        except Exception as e:
            self.display_output(f"Intermediate Code Generation Error: {str(e)}")
    
    def run_all(self):
        try:
            code = self.text_area.get(1.0, tk.END).strip()  # Get user code
            tokens = self.lexer(code)  # Tokenize code
            tree = self.parser(code)  # Parse to AST
            syntax_output = "Syntax Analysis: Valid"

            # Run Semantic Analysis
            errors = semantic_analyzer(tree)
            semantic_output = "Semantic Analysis: " + ("No issues found" if not errors else "\n".join(errors))

            # Generate Intermediate Representation (IR)
            ir_code = generate_ir(tree)

            # Execute Code and Capture Output
            execution_output = run_code(code)

            # Display Final Output
            final_output = (f"Tokens:\n{tokens}\n\n" +
                            f"{syntax_output}\n\n" +
                            f"{semantic_output}\n\n" + "\n"
                            f"Intermediate Code:\n{ir_code}\n\n" + "\n"
                            f"Execution Output:\n{execution_output}")
            
            self.display_output(final_output)

        except Exception as e:
            self.display_output(f"Error during compilation: {str(e)}")
    
    def lexer(self, code):
        tokens = re.findall(r'[a-zA-Z_][a-zA-Z_0-9]*|[=+\-*/()]|\d+', code)
        return tokens
    
    def parser(self, tree):
        return ast.parse(tree)
    
    def show_readme(self):
        messagebox.showinfo("README", "Python Mini Compiler\n\nThis tool provides basic file operations and text editing capabilities.")