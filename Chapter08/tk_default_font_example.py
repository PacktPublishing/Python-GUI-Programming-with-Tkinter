import tkinter as tk
from tkinter.font import nametofont

root = tk.Tk()

# Get and adjust default font
default_font = nametofont('TkDefaultFont')
default_font.config(family='Helvetica', size=32)

# Display a label
tk.Label(text='Feeling Groovy').pack()

root.mainloop()
