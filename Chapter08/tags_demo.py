import tkinter as tk

text = tk.Text(width=50, height=20, bg='black', fg='lightgreen')
text.pack()
text.tag_configure('prompt', foreground='magenta')
text.tag_configure('output', foreground='yellow')
text.insert('end', '>>> ', ('prompt',))

def on_return(*args):
    cmd = text.get('prompt.last', 'end').strip()
    if cmd:
        try:
            output = str(eval(cmd))
        except Exception as e:
            output = str(e)
        text.insert('end', '\n' + output, ('output',))
    text.insert('end', '\n>>> ', ('prompt',))
    return 'break'


text.bind('<Return>', on_return)
text.mainloop()
