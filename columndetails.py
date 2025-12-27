import tkinter as tk
from tkinter import ttk

dropdown_config = {
    "type": {
        "label": "Type",
        "values": [
            "BOOLEAN",
            "TINYINT", "SMALLINT", "INTEGER", "BIGINT",
            "FLOAT", "DOUBLE",
            "DATE", "TIMESTAMP",
            "VARCHAR", "BLOB"
        ],
        "default": "VARCHAR"
    },
    "length": {
        "label": "Length",
        "values": [],
        "default": "",
        "depends_on": "type",
        "depend_value": "VARCHAR"
    },
    "nullable": {
        "label": "Nullable",
        "values": ["True", "False"],
        "default": "False"
    },
    "default": {
        "label": "Default Value",
        "values": [],
        "default": ""
    },
    "key": {
        "label": "Key Type",
        "values": ["None", "Primary Key", "Foreign Key"],
        "default": "None"
    },
       "auto_increment": {
        "label": "Auto Increment",
        "values": ["True", "False"],
        "default": "False",
        "depends_on": "key",
        "depend_value": "PRIMARY KEY"
    },
    "references_table": {
        "label": "References Table",
        "values": [],
        "default": "",
        "depends_on": "key",
        "depend_value": "Foreign Key"
    },
    "references_column": {
        "label": "References Column",
        "values": [],
        "default": "",
        "depends_on": "references_table"
    },
    "unique": {
        "label": "Unique",
        "values": ["True", "False"],
        "default": "False"
    },
    "comment": {
        "label": "Comment",
        "values": [],
        "default": ""
    },
    "check": {
        "label": "Check constraint",
        "values": [],
        "default": ""
    },
    "checkvalue": {
        "label": "Custom Check Function",
        "value": [],
        "default": ""
    }
}


class ColumnDetails(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.working_data = {}          #Compiled data
        self.dropdown_details = {}      #Dropdown objects
        self.text_vars = {}             #Dropdown information

        self.selected_table = None      #Current table
        self.selected_column = None     #Current column

        # =====================
        # Layout configuration
        # =====================

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # =====================
        # Top button bar
        # =====================
        top_frame = tk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        tk.Button(
            top_frame,
            text="Go Back",
            command=lambda: controller.show_frame("TableEditor")
        ).pack(side="left", padx=5)

        tk.Button(
            top_frame,
            text="Finish",
            command=lambda: self.finish(self)
        ).pack(side="left", padx=5)

        # =====================
        # Main content frame
        # =====================

        main_frame = tk.Frame(self)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        main_frame.grid_columnconfigure(0, weight=2)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_columnconfigure(2, weight=3)
        main_frame.grid_rowconfigure(0, weight=1)

        # =====================
        # TABLE SELECT
        # =====================

        table_frame = tk.LabelFrame(main_frame, text="Tables", padx=5, pady=5)
        table_frame.grid(row=0, column=0, sticky="nsew", padx=5)

        self.table_listbox = tk.Listbox(table_frame, exportselection=False)
        self.table_listbox.pack(fill="both", expand=True)
        self.table_listbox.bind("<<ListboxSelect>>", self.on_table_select)

        # =====================
        # COLUMN SELECT
        # =====================

        column_frame = tk.LabelFrame(main_frame, text="Columns", padx=5, pady=5)
        column_frame.grid(row=0, column=1, sticky="nsew", padx=5)

        self.column_listbox = tk.Listbox(column_frame, exportselection=False)
        self.column_listbox.pack(fill="both", expand=True)
        self.column_listbox.bind("<<ListboxSelect>>", self.on_column_select)

        # =====================
        # COLUMN DETAILS
        # =====================

        # Create a container for details
        details_container = tk.Frame(main_frame)
        details_container.grid(row=0, column=2, sticky="nsew", padx=5, pady =5)
        details_container.grid_propagate(False)
        
        # Create a canvas inside the container
        self.details_canvas = tk.Canvas(details_container, borderwidth=0)
        self.details_canvas.pack(side="left", fill="both", expand=True)

        # Add a vertical scrollbar linked to the canvas
        v_scroll = tk.Scrollbar(details_container, orient="vertical", command=self.details_canvas.yview)
        v_scroll.pack(side="right", fill="y")
        self.details_canvas.configure(yscrollcommand=v_scroll.set)

        # Create the frame that will hold the column settings
        self.details_panel = tk.Frame(self.details_canvas, padx=10, pady=10)
        self.details_window = self.details_canvas.create_window((0, 0), window=self.details_panel, anchor="nw")

        self.details_panel.bind("<Configure>", self.on_frame_configure)
        self.details_canvas.bind("<Configure>", self.on_canvas_configure)
        self.details_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    # =====================
    # Refresh the page
    # =====================

    def refresh(self):
        self.working_data.clear()
        self.table_listbox.delete(0, "end")
        self.column_listbox.delete(0, "end")

        for table, columns in self.controller.detailsdata.items():
            self.working_data[table] = {
                col: {
                    "type": "VARCHAR",
                    "nullable": "False",
                    "key": "None",
                    "reference_table": "",
                    "reference_column": ""
                }
                for col in columns
            }
            self.table_listbox.insert("end", table)

        self.selected_table = None
        self.selected_column = None
        self.set_details_panel_state("disabled")

    # =====================
    # Scrollbar Handlers
    # =====================

    # Make the canvas scrollable when content changes
    def on_frame_configure(self, event):
        self.details_canvas.configure(scrollregion=self.details_canvas.bbox("all"))

    # Make the frame expand to match the canvas width
    def on_canvas_configure(self, event):
        canvas_width = event.width
        self.details_canvas.itemconfig(self.details_window, width=canvas_width)

    # Optional: allow scrolling with mouse wheel
    def on_mousewheel(self, event):
        self.details_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    

    # =====================
    # Selection Handlers
    # =====================

    def on_table_select(self, event):
        if not self.table_listbox.curselection():
            return

        self.selected_table = self.table_listbox.get(
            self.table_listbox.curselection()[0]
        )

        self.selected_column = None
        self.column_listbox.delete(0, "end")

        for col in self.working_data[self.selected_table]:
            self.column_listbox.insert("end", col)

        for child in self.details_panel.winfo_children():
            child.destroy()

        self.text_vars.clear()
        self.dropdown_details.clear()

        self.set_details_panel_state("disabled")

    def on_column_select(self, event):
        if not self.column_listbox.curselection():
            return

        self.selected_column = self.column_listbox.get(
            self.column_listbox.curselection()[0]
        )

        self.detailscreation(self.details_panel, dropdown_config)

        meta = self.working_data[self.selected_table][self.selected_column]

        for key, var in self.text_vars.items():
            value = meta.get(key, "")
            var.set(value)

        self.set_details_panel_state("normal")
        self.on_key_type_change()

    # =====================
    # Foreign Key Logic
    # =====================

    def on_key_type_change(self, event=None):
        if not self.selected_table or not self.selected_column:
            return

        key_var = self.text_vars.get("key")
        if not key_var:
            return
        
        key_type = key_var.get()
        meta = self.working_data[self.selected_table][self.selected_column]

        meta["key"] = key_type

        if key_type != "Foreign Key":
            meta["reference_table"] = ""
            meta["reference_column"] = ""

        self.save_metadata()

    def update_ref_columns(self, event=None):

        if not self.selected_table or not self.selected_column:
            return
        
        ref_table_var = self.text_vars.get("references_table")
        if not ref_table_var:
            return

        ref_table = ref_table_var.get()
        meta = self.working_data[self.selected_table][self.selected_column]

        meta["reference_table"] = ref_table
        meta["reference_column"] = ""

        self.save_metadata()


    def remove_invalid_foreign_keys(self):
        for table, cols in self.working_data.items(): #Fetch list of columns from each table
            for col, meta in cols.items():            #Fetch metadata of each column
                ref_table = meta.get("reference_table")
                ref_column = meta.get("reference_column")

                if not ref_table or not ref_column:
                    continue

                if (
                    ref_table not in self.working_data or
                    ref_column not in self.working_data[ref_table] or
                    self.working_data[ref_table][ref_column].get("key") != "Primary Key"
                ):
                    meta["reference_table"] = ""
                    meta["reference_column"] = ""
                    meta["key"] = "None"

    # =====================
    # Persistence
    # =====================

    def save_metadata(self, event=None):
        if not self.selected_table or not self.selected_column:
            return

        metadata = self.working_data[self.selected_table][self.selected_column]

        for key, var in self.text_vars.items():
            metadata[key] = var.get()

        self.remove_invalid_foreign_keys()
        self.detailscreation(self.details_panel, dropdown_config)


    # =====================
    # UI Helpers
    # =====================

    def set_details_panel_state(self, state):
        for child in self.details_panel.winfo_children():
            if isinstance(child, ttk.Combobox):
                child.configure(state="disabled" if state == "disabled" else "readonly")

    def detailscreation(self, frame, config):
        """
        Dynamically creates labeled readonly dropdowns.
        config format: {"Name": {"label": String, "values": List}}
        """

        # Clear existing widgets
        for child in frame.winfo_children():
            child.destroy()

        self.text_vars.clear()
        self.dropdown_details.clear()
    
        if not self.selected_table or not self.selected_column:
            return
        
        meta_state = self.working_data[self.selected_table][self.selected_column]

        for key, meta in config.items():
            label = meta["label"]
            values = meta["values"]
            depends_on = meta.get("depends_on", False)
            depends_value = meta.get("depends_value", False)
            active = True

            if depends_on:
                parent_value = meta_state.get(depends_on, "")
                if depends_value:
                    active = (parent_value == depends_value)
                else:
                    active = bool(parent_value and parent_value != "None")

            if active:
                if key == "references_table":
                    values = [t for t in self.working_data if t != self.selected_table]

                elif key == "references_column":
                    ref_table = meta_state.get("reference_table")
                    if ref_table:
                        values = [
                            col for col, col_meta in self.working_data[ref_table].items()
                            if col_meta.get("key") == "Primary Key"
                        ]

                tk.Label(frame, text=label).pack(anchor="w")

                var = tk.StringVar()
                combo = ttk.Combobox(
                    frame,
                    textvariable=var,
                    state="readonly",
                    values=values
                )
                var.set(meta_state.get(key, meta.get("default", "")))

                combo.pack(fill="x", pady=2)
                combo.bind("<<ComboboxSelected>>", self.save_metadata)

                if key == "key":
                    combo.bind("<<ComboboxSelected>>", self.on_key_type_change)

                if key == "references_table":
                    combo.bind("<<ComboboxSelected>>", self.update_ref_columns)


                self.text_vars[key] = var
                self.dropdown_details[key] = combo

    def finish(self):
        self.sqlgeneration(self.working_data)


    #---Placeholder for sql generation---
    def sqlgeneration(self, data):
        print(data)
