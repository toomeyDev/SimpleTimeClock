import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

class Frontend(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SimpleTimeClock")
        self.geometry("600x400")
