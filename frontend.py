import tkinter as tk

def run():
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

    # create entry widgets for time entry process
    frm_entry_indiv = tk.Frame(master=frm_entry)
    # add individual entry widgets to the frame
    lbl_hrs = tk.Label(master=frm_entry_indiv, text="Hours:")
    ent_hrs = tk.Entry(master=frm_entry_indiv)
    lbl_min = tk.Label(master=frm_entry_indiv, text="Minutes:")
    ent_min = tk.Entry(master=frm_entry_indiv)
    lbl_sec = tk.Label(master=frm_entry_indiv, text="Seconds:")
    ent_sec = tk.Entry(master=frm_entry_indiv)

    # layout individual entry widgets in the frame
    lbl_hrs.grid(row=0, column=0)
    ent_hrs.grid(row=0, column=1)
    lbl_min.grid(row=0, column=2)
    ent_min.grid(row=0, column=3)
    lbl_sec.grid(row=0, column=4)
    ent_sec.grid(row=0, column=5)
    
    # create button to handle adding new row of entries
    btn_new_row = tk.Button(master=frm_entry, text="New Row")

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

    # layout frm_entry level widgets inside frm_entry
    frm_entry_indiv.grid(row=0, column=0)
    btn_new_row.grid(row=1, column=0)
    frm_total.grid(row=2, column=0)

    # add top-level widgets to main grid
    frm_buttons.grid(row=0, column=0, sticky="ns")
    frm_entry.grid(row=0, column=1)

    # Run the event loop
    window.mainloop()
