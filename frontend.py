from sys import maxsize
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

class Frontend(tk.Tk):
    def __init__(self):
        super().__init__()

        self.row_count = 0 # keep track of number 
        self.row_entries = [] # hold all current row-entries in the program

        self.title("SimpleTimeClock")
        self.rowconfigure(0, minsize= 400)
        self.columnconfigure(1, minsize=800)

        # widgets to handle function buttons area
        self.frm_buttons = tk.Frame(self, borderwidth=1, relief=tk.RIDGE)
        self.btn_clear = tk.Button(self.frm_buttons, text="Clear")
        self.btn_save = tk.Button(self.frm_buttons, text="Save")
        self.btn_load = tk.Button(self.frm_buttons, text="Load")
        self.btn_settings = tk.Button(self.frm_buttons, text="Settings")
        self.btn_exit = tk.Button(master=self.frm_buttons, text="Exit", command=self.destroy)

        # add function buttons to buttons frame
        self.btn_clear.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.btn_save.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.btn_load.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.btn_settings.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.btn_exit.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

        self.frm_buttons.grid(row=0, column=0, sticky="ns")

        # widgets to handle scrollable entry area
        self.canvas_container = tk.Frame(self)
        self.canvas = tk.Canvas(self.canvas_container)
        self.scrollbar = tk.Scrollbar(self.canvas_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # recalculate canvas area when new widgets are added
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: 
                self.canvas.configure(
                scrollregion=self.canvas.bbox("all"))
        )

        # configure canvas for scrolling entries
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="center")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)  

        self.canvas_container.grid(row=0, column=1)
        self.canvas.grid(row=0, column=0, sticky="ns")
        self.scrollbar.grid(row=0, column=1)

        self.add_row() # add a single row by-default

        # widgets to handle entry-controls (add new, calculate, get total)
        self.frm_entry_controls = tk.Frame(self)
        self.btn_new_row = tk.Button(self.frm_entry_controls, text="New Row", command=self.add_row)
        self.btn_calculate = tk.Button(self.frm_entry_controls, text="Calculate")
        self.frm_total = tk.Frame(self.frm_entry_controls)

        # add entry control widgets to frame
        self.btn_new_row.grid(row=0, column=0)
        self.btn_calculate.grid(row=0, column=1)
        self.frm_total.grid(row=1, column=0)

        self.frm_entry_controls.grid(row=1, column=1)

    def add_row(self):
        # create empty frame to hold the row content
        frm_entry_indiv = tk.Frame(self.scrollable_frame, relief=tk.RIDGE, borderwidth=1)
            
        """Add a new row of entries to the frame."""
            
        self.row_count += 1
            
        # add individual entry widgets to the frame
        lbl_hrs = tk.Label(frm_entry_indiv, text="Hours:")
        ent_hrs = tk.Entry(frm_entry_indiv, width=5)
        ent_hrs.insert(0, "0")
            
        lbl_min = tk.Label(frm_entry_indiv, text="Minutes:")
        ent_min = tk.Entry(frm_entry_indiv, width=5)
        ent_min.insert(0, "0")
            
        lbl_sec = tk.Label(frm_entry_indiv, text="Seconds:")
        ent_sec = tk.Entry(frm_entry_indiv, width=5)
        ent_sec.insert(0, "0")

        # store all entry widgets in row_entries for use in calculations
        row_contents = [ent_hrs, ent_min, ent_sec]
        self.row_entries.append(row_contents)

        # layout individual entry widgets in the frame
        lbl_hrs.grid(row=self.row_count, column=0)
        ent_hrs.grid(row=self.row_count, column=1)
        lbl_min.grid(row=self.row_count, column=2)
        ent_min.grid(row=self.row_count, column=3)
        lbl_sec.grid(row=self.row_count, column=4)
        ent_sec.grid(row=self.row_count, column=5)

        # add the entries to the scrollable_frame grid as a new row
        frm_entry_indiv.grid(row=self.row_count,column=0, sticky="ns", padx=5)