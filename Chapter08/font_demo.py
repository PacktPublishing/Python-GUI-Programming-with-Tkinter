import tkinter as tk
from tkinter.font import Font

root = tk.Tk()

# Fonts can be specified directly as a string
# in the format "family size [style] [style] ..."
# where "style" can be any of normal, bold, italic, underline, overstrike

tk.Label(text="Direct font format", font="Times").pack()

# Fonts can be specified as a tuple in the same order
tk.Label(
    text="Tuple font format",
    font=('Droid sans', 15, 'overstrike')
).pack()

# Fonts can use named fonts created via the Font class
labelfont = Font(family='Courier', size=30,
                 weight='bold', slant='roman',
                 underline=False, overstrike=False)
tk.Label(text='Using the Font class', font=labelfont).pack()

def toggle_overstrike():
    labelfont['overstrike'] = not labelfont['overstrike']

tk.Button(text='Toggle Overstrike', command=toggle_overstrike).pack()

root.mainloop()
