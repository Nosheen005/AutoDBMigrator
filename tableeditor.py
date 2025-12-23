import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from excel_reader import read_excel_for_controller, ExcelReadError
import copy



class TableEditor(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Internal storage:
        self.tables_data: dict[str, list[str]] = {}
        self.table_frames = {}       
        self.table_listboxes = {}    
        self.move_dropdowns = {}     

        # Title
        label = tk.Label(self, text="Table Editor", font=("Arial", 14))
        label.grid(row=0, column=0, sticky="n", pady=12)

        # Button bar
        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        button_frame.grid_columnconfigure(0, weight=1)

        tk.Button(
            button_frame,
            text="Go Back",
            command=lambda: controller.show_frame("ColumnSelector")
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Add Table",
            command=self.add_table
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Refresh Page",
            command=self.refresh
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Next",
            command=self.go_next
        ).pack(side="left", padx=5)

        # Canvas for tables
        canvas_frame = tk.Frame(self)
        canvas_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.grid_rowconfigure(2, weight=1)

        self.tables_canvas = tk.Canvas(canvas_frame, highlightthickness=0)
        self.tables_canvas.pack(side="left", fill="both", expand=True)

        v_scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.tables_canvas.yview)
        v_scrollbar.pack(side="right", fill="y")
        self.tables_canvas.configure(yscrollcommand=v_scrollbar.set)

        self.inner_frame = tk.Frame(self.tables_canvas)
        self._inner_window = self.tables_canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Bind resize
        self.tables_canvas.bind("<Configure>", self._on_canvas_configure)
        self.inner_frame.bind(
            "<Configure>",
            lambda e: self.tables_canvas.configure(scrollregion=self.tables_canvas.bbox("all"))
        )

        # Bind mouse wheel scrolling anywhere over the canvas
        self.tables_canvas.bind("<Enter>", lambda e: self.tables_canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.tables_canvas.bind("<Leave>", lambda e: self.tables_canvas.unbind_all("<MouseWheel>"))

    # ------------- Refreshing window with new data -------------
    def refresh(self):
        self.load_from_excel()
        self.clear_tables()
        self.populate_tables()

    # ---------------- Load tables from Excel via excel_reader ----------------
    def load_from_excel(self):
        """
        Use read_excel_for_controller(self.controller) to get table->columns
        from the Excel file, then rebuild the UI.
        """
        try:
            self.tables_data = read_excel_for_controller(self.controller)
        except ExcelReadError as exc:
            messagebox.showerror("Excel Read Error", str(exc))
            return

    # ---------------- Clear all existing table widgets ----------------
    def clear_tables(self):
        for frame in self.table_frames.values():
            frame.destroy()
        self.table_frames.clear()
        self.table_listboxes.clear()
        self.move_dropdowns.clear()

    # ---------------- Mouse wheel handler ----------------
    def _on_mousewheel(self, event):
        self.tables_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ---------------- Canvas configure ----------------
    def _on_canvas_configure(self, event):
        self.tables_canvas.itemconfig(self._inner_window, width=event.width)
        self.reposition_tables()

    # ---------------- Populate tables (from self.tables_data) ----------------
    def populate_tables(self):
        for table_name, columns in self.tables_data.items():
            self.create_table_frame(table_name, columns)

        # Update all dropdowns once all tables exist
        for table_name in self.table_frames.keys():
            self.update_dropdown_options(table_name)

        self.reposition_tables()

    # ---------------- Create single table frame ----------------
    def create_table_frame(self, table_name, columns):
        frame = tk.LabelFrame(self.inner_frame, text=table_name, padx=10, pady=10)
        frame.pack_propagate(True)  # Allow frame to resize based on content

        listbox = tk.Listbox(frame, selectmode="extended", height=min(10, len(columns) or 1))
        listbox.pack(fill="both", expand=True)

        for col in columns:
            listbox.insert("end", col)

        # Control frame for Move/Delete
        control_frame = tk.Frame(frame)
        control_frame.pack(pady=5)

        frame.listbox = listbox
        frame.control_frame = control_frame

        self.table_frames[table_name] = frame
        self.table_listboxes[table_name] = listbox

        self.refresh_table_controls(table_name)

    # ---------------- Refresh controls ----------------
    def refresh_table_controls(self, table_name):
        frame = self.table_frames[table_name]
        listbox = frame.listbox

        # Clear existing controls
        for widget in frame.control_frame.winfo_children():
            widget.destroy()

        if listbox.size() == 0:
            # Show delete button if empty
            tk.Button(
                frame.control_frame,
                text="Delete Table",
                command=lambda t=table_name: self.delete_table(t)
            ).pack(side="left", padx=2)
            if table_name in self.move_dropdowns:
                del self.move_dropdowns[table_name]
        else:
            # Show move dropdown + button
            dropdown = ttk.Combobox(frame.control_frame, state="readonly")
            dropdown.pack(side="left", padx=2)
            self.move_dropdowns[table_name] = dropdown
            self.update_dropdown_options(table_name)

            tk.Button(
                frame.control_frame,
                text="Move",
                command=lambda t=table_name: self.move_columns(t)
            ).pack(side="left", padx=2)

    # ---------------- Update dropdown options ----------------
    def update_dropdown_options(self, source_table):
        if source_table not in self.move_dropdowns:
            return

        options = [t for t in self.table_frames.keys() if t != source_table]
        self.move_dropdowns[source_table]["values"] = options
        if options:
            self.move_dropdowns[source_table].current(0)

    # ---------------- Dynamic wrapping ----------------
    def reposition_tables(self):
        if not self.table_frames:
            return

        self.update_idletasks()
        canvas_width = self.tables_canvas.winfo_width()
        if canvas_width <= 1:
            self.after(50, self.reposition_tables)
            return

        frames = list(self.table_frames.values())
        sample_width = frames[0].winfo_reqwidth() + 20
        max_columns = max(canvas_width // sample_width, 1)

        for f in frames:
            f.grid_forget()

        for idx, frame in enumerate(frames):
            row = idx // max_columns
            col = idx % max_columns
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="n")

        for c in range(max_columns):
            self.inner_frame.grid_columnconfigure(c, weight=1)

    # ---------------- Move Columns ----------------
    def move_columns(self, table_name):
        listbox = self.table_listboxes[table_name]
        selected = listbox.curselection()
        if not selected:
            messagebox.showinfo("Move Columns", "No column selected.")
            return

        dest_table = self.move_dropdowns[table_name].get()
        if not dest_table or dest_table == table_name:
            return

        columns = [listbox.get(i) for i in selected]

        # Remove from source
        for i in reversed(selected):
            col = listbox.get(i)
            listbox.delete(i)
            self.tables_data[table_name].remove(col)

        # Add to destination
        dest_listbox = self.table_listboxes[dest_table]
        for col in columns:
            dest_listbox.insert("end", col)
            self.tables_data[dest_table].append(col)

        # Adjust Listbox heights
        listbox.config(height=max(1, listbox.size()))
        dest_listbox.config(height=max(1, dest_listbox.size()))

        # Refresh controls on both tables (Delete/Move)
        self.refresh_table_controls(table_name)
        self.refresh_table_controls(dest_table)

        # Force LabelFrames to resize
        self.table_frames[table_name].update_idletasks()
        self.table_frames[dest_table].update_idletasks()

        # Refresh dropdowns only for tables that still have them
        for t in self.table_frames.keys():
            if t in self.move_dropdowns:
                self.update_dropdown_options(t)

        self.reposition_tables()

    # ---------------- Add Table ----------------
    def add_table(self):
        while True:
            table_name = simpledialog.askstring("New Table", "Enter table name:")
            if table_name is None:
                return
            table_name = table_name.strip()
            if not table_name:
                messagebox.showwarning("Invalid Name", "Table name cannot be empty.")
                continue
            if table_name in self.tables_data:
                messagebox.showwarning("Duplicate Name", "This table name already exists.")
                continue
            break

        self.tables_data[table_name] = []
        self.create_table_frame(table_name, [])

        for t in self.table_frames.keys():
            if t in self.move_dropdowns:
                self.update_dropdown_options(t)
        self.reposition_tables()

    # ---------------- Delete Table ----------------
    def delete_table(self, table_name):
        if self.tables_data[table_name]:  # Safety check
            return

        self.table_frames[table_name].destroy()

        del self.tables_data[table_name]
        del self.table_frames[table_name]
        del self.table_listboxes[table_name]
        if table_name in self.move_dropdowns:
            del self.move_dropdowns[table_name]

        for t in self.table_frames.keys():
            self.refresh_table_controls(t)
        self.reposition_tables()

    def go_next(self):
        self.controller.detailsdata = copy.deepcopy(self.tables_data)
        self.controller.show_frame("ColumnDetails")
