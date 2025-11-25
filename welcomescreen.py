import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox 

class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.filepath = None

        # Informational text
        info_label = tk.Label(
            self,
            text="Please select an Excel file below to continue.",
            wraplength=450,
            justify="center"
        )
        info_label.pack(pady=10)

        # Displays selected file info
        self.file_label = tk.Label(
            self,
            text="No file selected",
            wraplength=450,
            justify="center",
            fg="blue"
        )
        self.file_label.pack(pady=10)

        # Button for selecting file
        self.file_button = tk.Button(
            self,
            text="Select Excel File",
            command=self.select_file
        )
        self.file_button.pack(pady=10)

        # Button to go to next screen
        next_button = tk.Button(
            self,
            text="Go to Next Screen",
            command=self.go_to_next_screen
        )
        next_button.pack(pady=10)

    def select_file(self):
        selected = filedialog.askopenfilename(
            title="Select an Excel file",
            filetypes=[
                ("Excel Files", "*.xlsx *.xls"),
                ("All Files", "*.*")
            ]
        )

        if selected:
            self.controller.filepath = selected
            self.file_label.config(text=f"Selected file:\n{self.controller.filepath}")
            self.file_button.config(text="Select Another Excel File")

    def go_to_next_screen(self):
        if self.controller.filepath:
            self.controller.show_frame("ColumnSelector")
        else:
            tk.messagebox.showwarning("No File Selected", "Please select an Excel file first.")