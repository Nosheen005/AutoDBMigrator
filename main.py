import tkinter as tk
from welcomescreen import WelcomeScreen
from columnselector import ColumnSelector
from tableeditor import TableEditor
from columndetails import ColumnDetails
from excel_reader import read_excel_for_controller, ExcelReadError
from sql_preview import SQLPreview #added newly N




class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Multi-Screen Tkinter App")
        self.geometry("800x400")

        self.filepath = None
        self.tables_data = {}
        self.detailsdata = {}
        self.sql_text = ""  # added newly N


        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for Screen in (WelcomeScreen, ColumnSelector, TableEditor, ColumnDetails, SQLPreview): # added newly 
            screen_name = Screen.__name__
            frame = Screen(parent=container, controller=self)
            self.frames[screen_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomeScreen")

    def show_frame(self, screen_name):
        frame = self.frames[screen_name]
        frame.tkraise()
        if hasattr(frame, "refresh"):
            frame.refresh()


if __name__ == "__main__":
    app = App()
    app.mainloop()
