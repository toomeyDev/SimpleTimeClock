import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

class Frontend(tk.Tk):
    def __init__(self, backend):
        super().__init__()

        self.row_count = 0 # keep track of number of rows
        self.row_entries = [] # hold all current row-entries in the program
        self.total_values = [0, 0, 0] # keep track of running total values for h/m/s

        self.backend = backend # hold reference to backend module

        self.title("SimpleTimeClock")
        self.rowconfigure(0, minsize= 400)
        self.columnconfigure(1, minsize=800)

        # widgets to handle function buttons area
        self.frm_buttons = tk.Frame(self, borderwidth=1, relief=tk.RIDGE)
        self.btn_clear = tk.Button(self.frm_buttons, text="Clear", command=self.clear_rows)
        self.btn_save = tk.Button(self.frm_buttons, text="Save", command=self.save_total)
        self.btn_load = tk.Button(self.frm_buttons, text="Load", command=self.load_total)
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
        self.btn_calculate = tk.Button(self.frm_entry_controls, text="Calculate", command=self.assign_totals)
        
        # hold labels and output for total calculations
        self.frm_total = tk.Frame(self.frm_entry_controls)
        
        self.lbl_total_hrs = tk.Label(self.frm_total, text="0 Hours,")
        self.lbl_total_min = tk.Label(self.frm_total, text="0 Minutes,")
        self.lbl_total_sec = tk.Label(self.frm_total, text="0 Seconds,")

        # add total output labels to frm_total grid
        self.lbl_total_hrs.grid(row=0, column=0)
        self.lbl_total_min.grid(row=0, column=1)
        self.lbl_total_sec.grid(row=0, column=2)

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

    def clear_rows(self):
        """Destroy all widgets in the rows section."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            # reset related values
            global row_entries, row_count
            row_entries = []
            row_count = 0

        self.add_row() # add a single blank row
        # assign_totals() # assign the new empty total
        self.title("SimpleTimeClock")

    def assign_totals(self):
        """
        Assign calculated total values for hours, minutes, and seconds
        to the corresponding labels in frm_total.
        """
        self.total_values = self.backend.calculate_total(self.row_entries)
        self.lbl_total_hrs['text'] = f"{self.total_values[0]} Hours,"
        self.lbl_total_min['text'] = f"{self.total_values[1]} Minutes,"
        self.lbl_total_sec['text'] = f"{self.total_values[2]} Seconds"

    def save_total(self):
        """
        Save the calculated total for hours, minutes, and seconds
        to a text file for future viewing/loading.
        """
        total = self.total_values
        savepath = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not savepath:
            return
        with open(savepath, "w") as output:
            output.write("Total Time:\n")
            output.write(f"{str(total[0])} hours, {str(total[1])} minutes, {str(total[2])} seconds")
            
        self.title(f"SimpleTimeClock - {savepath}")

    def add_total_row(self, total):
        # create empty frame to hold the row content
        frm_entry_indiv = tk.Frame(self.scrollable_frame)
        
        """Add a new row of entries to the frame."""
        self.row_count += 1
        
        # add individual entry widgets to the frame
        lbl_hrs = tk.Label(frm_entry_indiv, text="Hours:")
        ent_hrs = tk.Entry(frm_entry_indiv, width=5)
        ent_hrs.insert(0, total[0])
        
        lbl_min = tk.Label(frm_entry_indiv, text="Minutes:")
        ent_min = tk.Entry(frm_entry_indiv, width=5)
        ent_min.insert(0, total[1])
        
        lbl_sec = tk.Label(frm_entry_indiv, text="Seconds:")
        ent_sec = tk.Entry(frm_entry_indiv, width=5)
        ent_sec.insert(0, total[2])

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

        # add the entries to the frm_rows grid as a new row
        frm_entry_indiv.grid(row=self.row_count,column=0, sticky="ns", padx=5)

    def load_total(self):
        """
        Load a pre-existing timesheet into the program
        keeping track of the prior total in the first row.
        """
        timesheet_path = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not timesheet_path:
            return

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            # reset related values
            self.row_entries = []
            self.row_count = 0

        self.totals = []
        with open(timesheet_path, "r") as input:
            input.readline()
            read_total = input.readline().split()
        for word in read_total:
            if word.isnumeric():
                self.totals.append(int(word))
            else:
                # remove any non-numeric content
                continue
        self.add_total_row(self.totals) # add the prior total to the top of an empty sheet
        self.assign_totals()

        self.title(f"SimpleTimeClock - {timesheet_path}")
