from tkinter import Frame, Label, Entry

form = Frame()
label = Label(form, text='Name')
name_input = Entry(form)
label.grid(row=0, column=0)
name_input.grid(row=1, column=0)

form.pack()
form.mainloop()
