import tkinter as tk
from tkinter import ttk

root = tk.Tk()

def has_five_or_less_chars(string):
    return len(string) <= 5

wrapped_function = root.register(has_five_or_less_chars)
vcmd = (wrapped_function, '%P')
five_char_input = ttk.Entry(root, validate='key', validatecommand=vcmd)

five_char_input.pack()
root.mainloop()
