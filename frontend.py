import tkinter as tk
from functools import partial
from tkinter.filedialog import askopenfilename, asksaveasfilename
from xml.dom.minidom import TypeInfo

# keep track of number of rows of entries
row_count = 0
row_entries = [] # hold individual row entries for calculations in backend

def run(backend_module):
    window = tk.Tk()
    window.title("SimpleTimeClock")

    window.rowconfigure(0, minsize= 200)
    window.columnconfigure(1, minsize=400)

    # frame to contain function buttons
    frm_buttons = tk.Frame(master=window, borderwidth=1, relief=tk.RIDGE)
    # frame to contain entries
    frm_entry = tk.Frame(master=window, borderwidth=1, relief=tk.RIDGE)
    
    # create function buttons and assign commands
    btn_clear = tk.Button(master=frm_buttons, text="Clear")
    btn_save = tk.Button(master=frm_buttons, text="Save")
    btn_load = tk.Button(master=frm_buttons, text="Load")
    btn_settings = tk.Button(master=frm_buttons, text="Settings")
    btn_exit = tk.Button(master=frm_buttons, text="Exit", command=window.destroy)

    # add function buttons to frm_buttons grid
    btn_clear.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_save.grid(row=1, column=0, sticky="ew", padx=5)
    btn_load.grid(row=2, column=0, sticky="ew", padx=5)
    btn_settings.grid(row=3, column=0, sticky="ew", padx=5)
    btn_exit.grid(row=4, column=0, sticky="ew", padx=5)
    
    # create a frame to hold row frames
    frm_rows = tk.Frame(master=frm_entry)

    def add_row():
        # create empty frame to hold the row content
        frm_entry_indiv = tk.Frame(master=frm_rows)
        
        """Add a new row of entries to the frame."""
        global row_count, row_entries
        row_count += 1
        
        # add individual entry widgets to the frame
        lbl_hrs = tk.Label(master=frm_entry_indiv, text="Hours:")
        ent_hrs = tk.Entry(master=frm_entry_indiv)
        ent_hrs.insert(0, "0")
        
        lbl_min = tk.Label(master=frm_entry_indiv, text="Minutes:")
        ent_min = tk.Entry(master=frm_entry_indiv)
        ent_min.insert(0, "0")
        
        lbl_sec = tk.Label(master=frm_entry_indiv, text="Seconds:")
        ent_sec = tk.Entry(master=frm_entry_indiv)
        ent_sec.insert(0, "0")

        # store all entry widgets in row_entries for use in calculations
        row_contents = [ent_hrs, ent_min, ent_sec]
        row_entries.append(row_contents)

        # layout individual entry widgets in the frame
        lbl_hrs.grid(row=row_count, column=0)
        ent_hrs.grid(row=row_count, column=1)
        lbl_min.grid(row=row_count, column=2)
        ent_min.grid(row=row_count, column=3)
        lbl_sec.grid(row=row_count, column=4)
        ent_sec.grid(row=row_count, column=5)

        # add the entries to the frm_rows grid as a new row
        frm_entry_indiv.grid(row=row_count,column=0, sticky="ns", padx=5)

    def add_total_row(total):
        # create empty frame to hold the row content
        frm_entry_indiv = tk.Frame(master=frm_rows)
        
        """Add a new row of entries to the frame."""
        global row_count, row_entries
        row_count += 1
        
        # add individual entry widgets to the frame
        lbl_hrs = tk.Label(master=frm_entry_indiv, text="Hours:")
        ent_hrs = tk.Entry(master=frm_entry_indiv)
        ent_hrs.insert(0, total[0])
        
        lbl_min = tk.Label(master=frm_entry_indiv, text="Minutes:")
        ent_min = tk.Entry(master=frm_entry_indiv)
        ent_min.insert(0, total[1])
        
        lbl_sec = tk.Label(master=frm_entry_indiv, text="Seconds:")
        ent_sec = tk.Entry(master=frm_entry_indiv)
        ent_sec.insert(0, total[2])

        # store all entry widgets in row_entries for use in calculations
        row_contents = [ent_hrs, ent_min, ent_sec]
        row_entries.append(row_contents)

        # layout individual entry widgets in the frame
        lbl_hrs.grid(row=row_count, column=0)
        ent_hrs.grid(row=row_count, column=1)
        lbl_min.grid(row=row_count, column=2)
        ent_min.grid(row=row_count, column=3)
        lbl_sec.grid(row=row_count, column=4)
        ent_sec.grid(row=row_count, column=5)

        # add the entries to the frm_rows grid as a new row
        frm_entry_indiv.grid(row=row_count,column=0, sticky="ns", padx=5)

    def clear_rows():
        """Destroy all widgets in the rows section."""
        for widget in frm_rows.winfo_children():
            widget.destroy()
            # reset related values
            global row_entries, row_count
            row_entries = []
            row_count = 0

        add_row() # add a single blank row
        assign_totals() # assign the new empty total
        window.title("SimpleTimeClock")

    btn_clear.config(command=clear_rows)

    add_row() # add at least one row of entries at start
    
    # create button to handle adding new row of entries
    btn_new_row = tk.Button(master=frm_entry, text="New Row", command=add_row)

    # create button to handle calculation of time
    btn_calculate = tk.Button(master=frm_entry, text="Calculate")

    # create frame to handle total time calculation
    frm_total = tk.Frame(master=frm_entry)
    # add individual total widgets to the frame
    lbl_total = tk.Label(master=frm_total, text="Total:")
    lbl_total_hrs = tk.Label(master=frm_total, text="Hours: 0")
    lbl_total_min = tk.Label(master=frm_total, text="Minutes: 0")
    lbl_total_sec = tk.Label(master=frm_total, text="Seconds: 0")

    # layout frm_total level widgets inside frm_total
    lbl_total.grid(row=0, column = 0)
    lbl_total_hrs.grid(row=0, column=1)
    lbl_total_min.grid(row=0, column=2)
    lbl_total_sec.grid(row=0, column=3)

    def assign_totals():
        """
        Assign calculated total values for hours, minutes, and seconds
        to the corresponding labels in frm_total.
        """
        total_values = backend_module.calculate_total(row_entries)
        lbl_total_hrs['text'] = f"Hours: {total_values[0]}"
        lbl_total_min['text'] = f"Minutes: {total_values[1]}"
        lbl_total_sec['text'] = f"Seconds: {total_values[2]}"

    def save_total():
        """
        Save the calculated total for hours, minutes, and seconds
        to a text file for future viewing/loading.
        """
        total = backend_module.calculate_total(row_entries)
        savepath = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not savepath:
            return
        with open(savepath, "w") as output:
            output.write("Total Time:\n")
            output.write(f"{str(total[0])} hours, {str(total[1])} minutes, {str(total[2])} seconds")
            
        window.title(f"SimpleTimeClock - {savepath}")

    def load_total():
        """
        Load a pre-existing timesheet into the program
        keeping track of the prior total in the first row.
        """
        timesheet_path = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not timesheet_path:
            return

        for widget in frm_rows.winfo_children():
            widget.destroy()
            # reset related values
            global row_entries, row_count
            row_entries = []
            row_count = 0

        row_total = ""
        with open(timesheet_path, "r") as input:
            input.readline()
            row_total = input.readline().split()
        for word in row_total:
            if word.isnumeric():
                continue
            else:
                # remove any non-numeric content
                row_total.remove(word)
        total = [row_total[0], row_total[1], row_total[2]]
        add_total_row(total) # add the prior total to the top of an empty sheet
        assign_totals()

        window.title(f"SimpleTimeClock - {timesheet_path}")


    btn_save.config(command=save_total)
    btn_calculate.config(command=assign_totals)
    btn_load.config(command=load_total)

    # layout frm_entry level widgets inside frm_entry
    frm_rows.grid(row=0, column=0)
    btn_new_row.grid(row=1, column=0, sticky="ew", padx=5)
    btn_calculate.grid(row=1, column=1, sticky="ew",padx=5)
    frm_total.grid(row=2, column=0)

    # add top-level widgets to main grid
    frm_buttons.grid(row=0, column=0, sticky="ns")
    frm_entry.grid(row=0, column=1, sticky="ns")    

    # Run the event loop
    window.mainloop()
