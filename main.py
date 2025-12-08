import tkinter as tk
from welcomescreen import WelcomeScreen
from columnselector import ColumnSelector
from tableeditor import TableEditor
from excel_reader import read_excel_for_controller, ExcelReadError



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Multi-Screen Tkinter App")
        self.geometry("800x400")

        self.filepath = None
        self.tables_data = {}

        # Use grid, NOT pack
        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")

        # Allow the root window to expand its content
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Allow container to expand its content
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for Screen in (WelcomeScreen, ColumnSelector, TableEditor):
            screen_name = Screen.__name__
            frame = Screen(parent=container, controller=self)
            self.frames[screen_name] = frame

            # Make every screen fill container fully
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomeScreen")

    def show_frame(self, screen_name):
        frame = self.frames[screen_name]
        frame.tkraise()
        # NEW / UPDATED PART STARTS HERE
        # If the frame defines an on_show() method, call it
        if hasattr(frame, "on_show"):
            frame.on_show()
        # NEW / UPDATED PART ENDS HERE 


if __name__ == "__main__":
    app = App()
    app.mainloop()
