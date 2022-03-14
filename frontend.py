import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

class Frontend(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SimpleTimeClock")
        self.geometry("600x400")

        self.canvas_container = tk.Frame(self)
        self.canvas = tk.Canvas(self.canvas_container)
        self.scrollbar = tk.Scrollbar(self.canvas_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: 
                self.canvas.configure(
                scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        for i in range(50):
            tk.Entry(self.scrollable_frame).pack()

        self.canvas_container.pack()
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")