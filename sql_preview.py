# sqlpreview.py
import tkinter as tk
from tkinter import filedialog, messagebox


class SQLPreview(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        top = tk.Frame(self)
        top.pack(fill="x", padx=10, pady=8)

        tk.Button(top, text="Go Back",
                  command=lambda: controller.show_frame("ColumnDetails")
                  ).pack(side="left")

        tk.Button(top, text="Copy SQL",
                  command=self.copy_sql
                  ).pack(side="left", padx=6)

        tk.Button(top, text="Save SQL",
                  command=self.save_sql
                  ).pack(side="left", padx=6)

        # Text area
        self.text = tk.Text(self, wrap="none")
        self.text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Scrollbars (vertical + horizontal)
        y_scroll = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        y_scroll.pack(side="right", fill="y")
        self.text.configure(yscrollcommand=y_scroll.set)

        x_scroll = tk.Scrollbar(self, orient="horizontal", command=self.text.xview)
        x_scroll.pack(side="bottom", fill="x")
        self.text.configure(xscrollcommand=x_scroll.set)

    def refresh(self):
        sql = getattr(self.controller, "sql_text", "") or ""
        self.text.delete("1.0", "end")
        self.text.insert("1.0", sql)

    def copy_sql(self):
        sql = self.text.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(sql)
        messagebox.showinfo("Copied", "SQL copied to clipboard.")

    def save_sql(self):
        sql = self.text.get("1.0", "end-1c")

        file_path = filedialog.asksaveasfilename(
            title="Save SQL Script",
            defaultextension=".sql",
            filetypes=[("SQL files", "*.sql"), ("All files", "*.*")]
        )
        if not file_path:
            return

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(sql)

        messagebox.showinfo("Saved", f"Saved to:\n{file_path}")
