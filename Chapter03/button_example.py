import tkinter as tk
from tkinter import ttk

parent = tk.Tk()

tvar = tk.StringVar()
def swaptext():
    tvar.set('There' if tvar.get() == 'Hi' else 'Hi')

my_button = ttk.Button(parent, textvariable=tvar, command=swaptext)
my_button.pack()


parent.mainloop()
