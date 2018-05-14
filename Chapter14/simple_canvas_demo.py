import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=1024, height=768)
canvas.pack()
# configure canvas
canvas.config(background='black')

# draw a square
canvas.create_rectangle(100, 100, 200, 200, fill='orange')
canvas.create_rectangle((600, 100), (700, 200), fill='#FF8800')

# draw an oval
canvas.create_oval((350, 250), (450, 350), fill='blue')

# draw a line
canvas.create_line((100, 400), (400, 500), (700, 400), (100, 400), width=5, fill='red')

# draw a polygon
canvas.create_polygon((400, 150), (350,  300), (450, 300), fill='blue',  smooth=True)

# draw text
canvas.create_text((400, 600), text='Smile!', fill='cyan', font='TkDefaultFont 64')
# draw an image
smiley = tk.PhotoImage(file='smile.gif')
image_item = canvas.create_image((400, 300), image=smiley)
canvas.tag_bind(image_item, '<Button-1>', lambda e: canvas.delete(image_item))

root.mainloop()
