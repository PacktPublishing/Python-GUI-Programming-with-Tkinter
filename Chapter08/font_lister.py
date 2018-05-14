from tkinter import Tk
from tkinter.font import names, nametofont

r = Tk()
for fontname in names():
    font = nametofont(fontname)
    print('{}:\t {} {} {} {}'.format(
        fontname,
        font['family'],
        font['size'],
        font['weight'],
        font['slant']
    ))
