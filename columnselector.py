import tkinter as tk

class ColumnSelector(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Ensure controller has tables_data
        if not hasattr(controller, "tables_data"):
            controller.tables_data = {}

        # Make this frame stretch when parent grids it
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Title
        label = tk.Label(self, text="This is the column selector screen.", font=("Arial", 14))
        label.grid(row=0, column=0, sticky="n", pady=12)

        # Button bar
        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=0, sticky="ew", padx=10)
        button_frame.grid_columnconfigure(0, weight=1)

        tk.Button(button_frame, text="Go Back",
                  command=lambda: controller.show_frame("WelcomeScreen")).pack(side="left", padx=5)
        tk.Button(button_frame, text="Add Table",
                  command=self.add_table).pack(side="left", padx=5)
        tk.Button(button_frame, text="Remove Newest Table",
                  command=self.remove_table).pack(side="left", padx=5)
        tk.Button(button_frame, text="Next",
                  command=self.go_next).pack(side="left", padx=5)

        # ------------------ Canvas + Scrollbar ------------------
        canvas_frame = tk.Frame(self)
        canvas_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=12)
        self.grid_rowconfigure(2, weight=1)

        # Canvas for tables
        self.tables_canvas = tk.Canvas(canvas_frame, highlightthickness=0)
        self.tables_canvas.pack(side="left", fill="both", expand=True)

        # Vertical scrollbar
        v_scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.tables_canvas.yview)
        v_scrollbar.pack(side="right", fill="y")
        self.tables_canvas.configure(yscrollcommand=v_scrollbar.set)

        # Inner frame inside canvas
        self.inner_frame = tk.Frame(self.tables_canvas)
        self._inner_window = self.tables_canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Bind resize to reflow tables
        self.tables_canvas.bind("<Configure>", self._on_canvas_configure)

        # Make inner_frame resize its scrollregion
        self.inner_frame.bind("<Configure>", lambda e: self.tables_canvas.configure(scrollregion=self.tables_canvas.bbox("all")))

        # Optional: mouse wheel scrolling
        self.tables_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Store table frames
        self.table_frames = []

        # Validation
        def validate_letters(value):
            return value.isalpha() or value == ""

        def validate_digits(value):
            return value.isdigit() or value == ""

        self.letters_vcmd = (self.register(validate_letters), "%P")
        self.digits_vcmd = (self.register(validate_digits), "%P")

        # Create first table after a small delay to let geometry settle
        self.after(50, self.add_table)

    # ------------------------ Canvas helper ------------------------
    def _on_canvas_configure(self, event):
        # Set inner_frame width to canvas width so grid can use it
        canvas_width = event.width
        # update the inner window width so inner_frame.winfo_width() matches canvas width
        self.tables_canvas.itemconfig(self._inner_window, width=canvas_width)
        # reposition tables based on new width
        self.reposition_tables()

    # ---------------- Table Unit -----------------
    def create_table_unit(self, table_number):
        frame = tk.LabelFrame(self.inner_frame,
                              text=f"Table {table_number}",
                              padx=10, pady=10)

        tk.Label(frame, text="Insert table name").pack(anchor="w")
        table_name_entry = tk.Entry(frame, width=30)
        table_name_entry.pack(pady=5)

        tk.Label(frame, text="Insert column name coordinates").pack(anchor="w", pady=(10, 0))

        coord_frame = tk.Frame(frame)
        coord_frame.pack(pady=5)

        entry1 = tk.Entry(coord_frame, width=5,
                          validate="key", validatecommand=self.letters_vcmd)
        entry1.pack(side="left", padx=2)

        entry2 = tk.Entry(coord_frame, width=5,
                          validate="key", validatecommand=self.digits_vcmd)
        entry2.pack(side="left", padx=2)

        tk.Label(coord_frame, text="-").pack(side="left", padx=5)

        entry3 = tk.Entry(coord_frame, width=5,
                          validate="key", validatecommand=self.letters_vcmd)
        entry3.pack(side="left", padx=2)

        entry4 = tk.Entry(coord_frame, width=5,
                          validate="key", validatecommand=self.digits_vcmd)
        entry4.pack(side="left", padx=2)

        frame.entries = {
            "table_name": table_name_entry,
            "entry1": entry1,
            "entry2": entry2,
            "entry3": entry3,
            "entry4": entry4
        }

        # Ensure geometry info is available
        frame.update_idletasks()

        return frame

    # ---------------- Add / Remove ----------------
    def add_table(self):
        table_number = len(self.table_frames) + 1
        new_table = self.create_table_unit(table_number)
        self.table_frames.append(new_table)
        # We grid into inner_frame inside reposition_tables
        self.reposition_tables()

    def remove_table(self):
        if not self.table_frames:
            return

        frame = self.table_frames.pop()
        frame.destroy()

        self.renumber_tables()
        self.reposition_tables()

    def renumber_tables(self):
        for i, frame in enumerate(self.table_frames, start=1):
            frame.config(text=f"Table {i}")

    # ---------------- Dynamic Wrapping (grid inside inner_frame) ----------------
    def reposition_tables(self):
        if not self.table_frames:
            return

        # ensure geometry up-to-date
        self.update_idletasks()
        self.inner_frame.update_idletasks()
        canvas_width = self.tables_canvas.winfo_width()

        if canvas_width <= 1:
            # canvas not ready yet, try again soon
            self.after(50, self.reposition_tables)
            return

        # measure a sample table width (requested width) + padding
        sample = self.table_frames[0]
        sample.update_idletasks()
        table_width = sample.winfo_reqwidth() + 20  # buffer for padding

        max_columns = max(canvas_width // table_width, 1)

        # clear previous grid placements
        for f in self.table_frames:
            f.grid_forget()

        # grid tables into inner_frame
        for index, frame in enumerate(self.table_frames):
            row = index // max_columns
            col = index % max_columns
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="n")

        # configure column weights so frames spread nicely
        for c in range(max_columns):
            self.inner_frame.grid_columnconfigure(c, weight=1)

        # update canvas scrollregion if needed
        self.tables_canvas.configure(scrollregion=self.tables_canvas.bbox("all"))

    # ---------------- Data Collection ----------------
    def update_tables_data(self):
        self.controller.tables_data.clear()

        for idx, frame in enumerate(self.table_frames, start=1):
            e = frame.entries
            table_name = e["table_name"].get()
            start_coord = e["entry1"].get() + e["entry2"].get()
            end_coord = e["entry3"].get() + e["entry4"].get()
            self.controller.tables_data[f"Table {idx}"] = [
                table_name,
                start_coord,
                end_coord
            ]

    def _on_mousewheel(self, event):
        # For Windows / Mac / Linux compatibility
        if self.tables_canvas.winfo_height() < self.inner_frame.winfo_height():
            self.tables_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def go_next(self):
        self.update_tables_data()
        self.controller.show_frame("TableEditor")