import tkinter as tk

window = tk.Tk()
window.rowconfigure([0, 1, 2], minsize=50)
window.columnconfigure([0,1,2], minsize= 150)

frm_header = tk.Frame(master=window, borderwidth=2)
frm_header.grid(row=0, column=1)

lbl_title = tk.Label(master=frm_header, text="SimpleTimeClock")
lbl_title.pack()

# Run the event loop
window.mainloop()
