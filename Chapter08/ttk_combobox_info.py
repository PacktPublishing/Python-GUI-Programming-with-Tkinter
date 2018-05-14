import tkinter as tk
from tkinter import ttk
from pprint import pprint

root = tk.Tk()
style = ttk.Style()

print('TTK Combobox\n')

cb = ttk.Combobox(root)
cb_stylename = cb.winfo_class()
print("Style name: ", cb_stylename)
print("Starting state:", cb.state())
cb.state(['active', 'invalid'])
print("New state:", cb.state())
cb.state(['!invalid'])
print("Newer state: ", cb.state())

cb_layout = style.layout(cb_stylename)
print("\nLayout: ")
pprint(cb_layout)

def walk_layout(layout):
    for element, subelements in layout:
        print("\nOptions for {}:".format(element))
        pprint(style.element_options(element))
        if subelements.get("children"):
            walk_layout(subelements.get("children"))
walk_layout(cb_layout)

cb_map = style.map(cb_stylename)
print("\nDefault Map:")
pprint(cb_map)

style.map(cb_stylename,
          fieldbackground=[
              ('!invalid', 'blue'),
              ('invalid', 'red')
          ],
          font=[
              ('!invalid', 'Helvetica 20 normal'),
              ('invalid', 'Helvetica 20 bold')
          ])

cb_map = style.map(cb_stylename)
print("\nNew Map:")
pprint(cb_map)

print('\nAvailable Themes:')
pprint(style.theme_names())

print('\nCurrent Theme:', style.theme_use())

pprint(style.element_names())
