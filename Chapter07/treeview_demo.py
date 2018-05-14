import tkinter as tk
from tkinter import ttk
from pathlib import Path

# Set up root window
root = tk.Tk()

# Create list of paths
paths = Path('.').glob('**/*')


def sort(tv, col):
    itemlist = list(tv.get_children(''))
    itemlist.sort(key=lambda x: tv.set(x, col))
    for index, iid in enumerate(itemlist):
        tv.move(iid, tv.parent(iid), index)

# Create and configure treeview
tv = ttk.Treeview(root, columns=['size', 'modified'], selectmode='none')
tv.heading('#0', text='Name', command=lambda: sort(tv, '#0'))
tv.heading('size', text='Size', anchor='center',
           command=lambda: sort(tv, 'size'))
tv.heading('modified', text='Modified', anchor='e',
           command=lambda: sort(tv, 'modified'))
tv.column('#0', stretch=True)
tv.column('size', width=200)

tv.pack(expand=True, fill='both')

# Populate Treeview
for path in paths:
    meta = path.stat()
    parent = str(path.parent)
    if parent == '.':
        parent = ''
    tv.insert(
        parent,
        'end',
        iid=str(path),
        text=str(path.name),
        values=[meta.st_size, meta.st_mtime]
    )

root.mainloop()
