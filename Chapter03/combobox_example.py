import tkinter as tk
from tkinter import ttk

parent = tk.Tk()
my_string_var = tk.StringVar()

combobox = ttk.Combobox(
    parent,
    textvariable=my_string_var,
    values=["Option 1", "Option 2", "Option 3"]
)
combobox.pack()
parent.mainloop()
