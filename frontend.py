import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

class Frontend(tk.Tk):
    def __init__(self):
        super().__init__()

        self.row_count = 0

        self.title("SimpleTimeClock")
        self.rowconfigure(0, minsize= 200)
        self.columnconfigure(1, minsize=400)

        # widgets to handle function buttons area
        frm_buttons = tk.Frame(self, borderwidth=1, relief=tk.RIDGE)
        btn_clear = tk.Button(frm_buttons, text="Clear")
        btn_save = tk.Button(frm_buttons, text="Save")
        btn_load = tk.Button(frm_buttons, text="Load")
        btn_settings = tk.Button(frm_buttons, text="Settings")
        btn_exit = tk.Button(master=frm_buttons, text="Exit", command=self.destroy)

        # add function buttons to buttons frame
        btn_clear.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        btn_save.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        btn_load.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        btn_settings.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        btn_exit.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

        frm_buttons.grid(row=0, column=0, sticky="ns")

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
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        for i in range(50):
            self.add_row()     

        self.add_row()

        self.canvas_container.grid(row=0, column=1)
        self.canvas.grid(row=0, column=0, sticky="ns")
        self.scrollbar.grid(row=0, column=1)

    def add_row(self):
        # create empty frame to hold the row content
        frm_entry_indiv = tk.Frame(self.scrollable_frame)
            
        """Add a new row of entries to the frame."""
            
        self.row_count += 1
            
        # add individual entry widgets to the frame
        lbl_hrs = tk.Label(frm_entry_indiv, text="Hours:")
        ent_hrs = tk.Entry(frm_entry_indiv)
        ent_hrs.insert(0, "0")
            
        lbl_min = tk.Label(frm_entry_indiv, text="Minutes:")
        ent_min = tk.Entry(frm_entry_indiv)
        ent_min.insert(0, "0")
            
        lbl_sec = tk.Label(frm_entry_indiv, text="Seconds:")
        ent_sec = tk.Entry(frm_entry_indiv)
        ent_sec.insert(0, "0")

        # store all entry widgets in row_entries for use in calculations
        row_contents = [ent_hrs, ent_min, ent_sec]
        #row_entries.append(row_contents)

        # layout individual entry widgets in the frame
        lbl_hrs.grid(row=self.row_count, column=0)
        ent_hrs.grid(row=self.row_count, column=1)
        lbl_min.grid(row=self.row_count, column=2)
        ent_min.grid(row=self.row_count, column=3)
        lbl_sec.grid(row=self.row_count, column=4)
        ent_sec.grid(row=self.row_count, column=5)

        # add the entries to the scrollable_frame grid as a new row
        frm_entry_indiv.grid(row=self.row_count,column=0, sticky="ns", padx=5)