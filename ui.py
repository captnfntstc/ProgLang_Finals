import tkinter as tk
from tkinter import scrolledtext, messagebox, Menu, filedialog, simpledialog, ttk
from features import CompilerFeatures
import subprocess
import os

class PythonCompiler(CompilerFeatures):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Python Mini Compiler")
        self.root.geometry("1000x600")
        self.root.iconphoto(False, tk.PhotoImage(file="icon.png"))
        
        self.font_family = "Courier New"
        self.font_size = 12
        self.theme = "light"
        
        # Menu Bar
        self.menu_bar = Menu(root)
        root.config(menu=self.menu_bar)
        
        # File Menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open File", command=self.open_file)
        self.file_menu.add_command(label="Open a Folder", command=self.open_folder)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        
        # Edit Menu
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Find", command=self.find_text)
        self.edit_menu.add_command(label="Replace", command=self.replace_text)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        
        # Settings Menu
        self.settings_menu = Menu(self.menu_bar, tearoff=0)
        self.settings_menu.add_command(label="Environment Options", command=self.open_environment_settings)
        self.settings_menu.add_command(label="Toggle Dark Mode", command=self.toggle_theme)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        
        # Layout Frames
        self.main_frame = tk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Folder Explorer
        self.folder_frame = tk.Frame(self.main_frame, width=200, bg="lightgray")
        self.folder_list = tk.Listbox(self.folder_frame)
        self.folder_list.pack(fill=tk.BOTH, expand=True)
        self.main_frame.add(self.folder_frame)
        
        # Text Editor Frame
        self.editor_frame = tk.PanedWindow(self.main_frame, orient=tk.VERTICAL)
        self.main_frame.add(self.editor_frame, stretch="always")

        # Button Frame
        self.button_frame = tk.Frame(self.editor_frame)
        self.editor_frame.add(self.button_frame, stretch="never")
        self.create_buttons()

        # Text Area
        self.text_area = scrolledtext.ScrolledText(self.editor_frame, wrap=tk.WORD, font=(self.font_family, self.font_size))
        self.text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.editor_frame.add(self.text_area, stretch="always")

        # Output Area
        self.output_area = scrolledtext.ScrolledText(self.editor_frame, wrap=tk.WORD, height=10, state=tk.DISABLED)
        self.editor_frame.add(self.output_area, stretch="never")
        
    def open_file_from_folder(self, event):
        # Get the selected file from the folder list
        file_name = self.folder_list.get(self.folder_list.curselection())
        if file_name:
            self.open_file(file_name)  # Use the existing open_file method to open the file
    
    def open_file(self, file_name=None):
        # Check if there are unsaved changes
        if self.text_area.get("1.0", tk.END) != "\n":
            response = messagebox.askyesnocancel("Unsaved Changes", "You have unsaved changes. Do you want to save them?")
            if response is None:  # Cancel was clicked
                return
            elif response:  # Yes was clicked
                self.save_file()  # Save the file before opening the new one
        
        # If file_name is provided, open that file, otherwise open the existing file
        if not file_name:
            file_name = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)  # Clear existing content
                    self.text_area.insert(tk.END, content)  # Insert file content
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")

    def create_buttons(self):
        self.lex_button = tk.Button(self.button_frame, text="Lexical Analysis", command=self.run_lexer, bg='purple', fg='white')
        self.lex_button.pack(side=tk.LEFT, padx=5)

        self.syntax_button = tk.Button(self.button_frame, text="Syntax Analysis", command=self.run_parser, bg='blue', fg='white')
        self.syntax_button.pack(side=tk.LEFT, padx=5)

        self.semantic_button = tk.Button(self.button_frame, text="Semantic Analysis", command=self.run_semantic, bg='orange', fg='white')
        self.semantic_button.pack(side=tk.LEFT, padx=5)

        self.ir_button = tk.Button(self.button_frame, text="Intermediate Code", command=self.run_ir, bg='brown', fg='white')
        self.ir_button.pack(side=tk.LEFT, padx=5)

        self.run_code_button = tk.Button(self.button_frame, text="Run Code", command=self.run_code, bg='pink', fg='white')
        self.run_code_button.pack(side=tk.LEFT, padx=5)

        self.run_button = tk.Button(self.button_frame, text="Run All", command=self.run_all, bg='green', fg='white')
        self.run_button.pack(side=tk.LEFT, padx=5)
    
    def open_environment_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Environment Settings")
        
        tk.Label(settings_window, text="Font:").pack()
        font_dropdown = ttk.Combobox(settings_window, values=["Courier New", "Arial", "Times New Roman"], state="readonly")
        font_dropdown.set(self.font_family)
        font_dropdown.pack()
        
        tk.Label(settings_window, text="Size:").pack()
        size_dropdown = ttk.Combobox(settings_window, values=["10", "12", "14", "16"], state="readonly")
        size_dropdown.set(str(self.font_size))
        size_dropdown.pack()
        
        def apply_settings():
            self.font_family = font_dropdown.get()
            self.font_size = int(size_dropdown.get())
            self.text_area.config(font=(self.font_family, self.font_size))
            settings_window.destroy()
        
        tk.Button(settings_window, text="Save", command=apply_settings).pack()
        tk.Button(settings_window, text="Cancel", command=settings_window.destroy).pack()
    
    def open_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_list.delete(0, tk.END)
            for file in os.listdir(folder_selected):
                if file.endswith(".py"):
                    self.folder_list.insert(tk.END, file)
            self.folder_list.bind("<Double-1>", self.open_file_from_folder)

    
    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
            self.text_area.config(bg="black", fg="white", insertbackground="white")
            self.output_area.config(bg="black", fg="white")
            self.folder_frame.config(bg="gray20")
            for button in self.button_frame.winfo_children():
                button.config(bg="gray30", fg="white")
        else:
            self.theme = "light"
            self.text_area.config(bg="white", fg="black", insertbackground="black")
            self.output_area.config(bg="white", fg="black")
            self.folder_frame.config(bg="lightgray")
            for button in self.button_frame.winfo_children():
                button.config(bg="SystemButtonFace", fg="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = PythonCompiler(root)
    root.mainloop()
