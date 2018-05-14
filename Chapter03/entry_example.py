import tkinter as tk
from tkinter import ttk

parent = tk.Tk()
my_text_var = tk.StringVar()

my_entry = ttk.Entry(
    parent,
    textvariable=my_text_var
)
my_entry.pack()

parent.mainloop()
