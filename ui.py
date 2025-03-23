import tkinter as tk
from tkinter import scrolledtext, messagebox, Menu, filedialog, simpledialog
from features import CompilerFeatures

class PythonCompiler(CompilerFeatures):  # Inherit from CompilerFeatures
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Python Mini Compiler")
        self.root.geometry("800x600")
        
        # Menu Bar
        self.menu_bar = Menu(root)
        root.config(menu=self.menu_bar)
        
        # File Menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Edit Menu
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Undo", command=lambda: self.text_area.event_generate("<Control-z>"))
        self.edit_menu.add_command(label="Redo", command=lambda: self.text_area.event_generate("<Control-y>"))
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<Control-c>"))
        self.edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<Control-v>"))
        self.edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<Control-x>"))
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find", command=self.find_text)
        self.edit_menu.add_command(label="Replace", command=self.replace_text)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        
        # About Menu
        self.about_menu = Menu(self.menu_bar, tearoff=0)
        self.about_menu.add_command(label="README", command=self.show_readme)
        self.menu_bar.add_cascade(label="About", menu=self.about_menu)

        # Text Area Frame
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Line Numbers
        self.line_numbers = tk.Text(self.frame, width=4, state=tk.DISABLED, bg="lightgray")
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Code Input Area
        self.text_area = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=76, height=20)
        self.text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.text_area.bind("<KeyRelease>", self.update_line_numbers)

        # Buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5)

        self.lex_button = tk.Button(self.button_frame, text="Lexical Analysis", command=self.run_lexer, bg='purple', fg='white')
        self.lex_button.pack(side=tk.LEFT, padx=5)

        self.syntax_button = tk.Button(self.button_frame, text="Syntax Analysis", command=self.run_parser, bg='blue', fg='white')
        self.syntax_button.pack(side=tk.LEFT, padx=5)

        self.semantic_button = tk.Button(self.button_frame, text="Semantic Analysis", command=self.run_semantic, bg='orange', fg='white')
        self.semantic_button.pack(side=tk.LEFT, padx=5)

        self.ir_button = tk.Button(self.button_frame, text="Intermediate Code", command=self.run_ir, bg='brown', fg='white')
        self.ir_button.pack(side=tk.LEFT, padx=5)

        self.run_button = tk.Button(self.button_frame, text="Run All", command=self.run_all, bg='green', fg='white')
        self.run_button.pack(side=tk.LEFT, padx=5)

        # Output Area
        self.output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=10, state=tk.DISABLED)
        self.output_area.pack(pady=10)

        # Initialize line numbers
        self.update_line_numbers()

    def update_line_numbers(self, event=None):
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)
        line_count = self.text_area.get(1.0, tk.END).count('\n') + 1
        self.line_numbers.insert(1.0, "\n".join(str(i) for i in range(1, line_count + 1)))
        self.line_numbers.config(state=tk.DISABLED)

    def show_readme(self):
        messagebox.showinfo("README", "Python Mini Compiler\n\nThis tool provides basic file operations and text editing capabilities.")