import tkinter as tk
from unittest import TestCase

class TkTestCase(TestCase):
    """A test case designed for Tkinter widgets and views"""

    keysyms = {
        '-': 'minus',
        ' ': 'space',
        ':': 'colon',
        #  For more see http://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm
    }
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.root.wait_visibility()

    @classmethod
    def tearDownClass(cls):
        cls.root.update()
        cls.root.destroy()

    def type_in_widget(self, widget, string):
        widget.focus_force()
        for char in string:
            char = self.keysyms.get(char, char)
            widget.event_generate('<KeyPress-{}>'.format(char))
            widget.event_generate('<KeyRelease-{}>'.format(char))
            self.root.update()

    def click_on_widget(self, widget, x, y, button=1):
        widget.focus_force()
        self.root.update()
        widget.event_generate("<ButtonPress-{}>".format(button), x=x, y=y)
        widget.event_generate("<ButtonRelease-{}>".format(button), x=x, y=y)
        self.root.update()
