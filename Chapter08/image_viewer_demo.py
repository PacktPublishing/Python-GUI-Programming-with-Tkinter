import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk  # this is pillow


class PictureViewer(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.image_display = tk.Label(self)
        self.image_display.pack(expand=1, fill='both')
        self.photoimage = None
        button = tk.Button(self, text='Select image',
                           command=self.choose_file)
        button.pack()

    def choose_file(self):
        filename = filedialog.askopenfilename(
            filetypes=(
                ('PNG files', '*.png *.PNG'),
                ('JPEG files', '*.jpg *.jpeg *.JPG *.JPEG'),
                ('GIF files', '*.gif *.GIF')
            ))
        image = Image.open(filename)
        self.photoimage = ImageTk.PhotoImage(image)
        self.image_display.config(image=self.photoimage)


app = PictureViewer()
app.mainloop()
