import tkinter as tk
from tkinter import ttk
from datetime import datetime

class DateEntry(ttk.Entry):
    """An Entry for ISO-style dates (Year-month-day)"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(
            validate='all',
            validatecommand=(self.register(self._validate),  '%S', '%i', '%V', '%d'),
            invalidcommand=(self.register(self._on_invalid), '%V')
        )
        self.error = tk.StringVar()

    def _toggle_error(self, error=''):
        self.error.set(error)
        if error:
            self.config(foreground='red')
        else:
            self.config(foreground='black')

    def _validate(self, char, index, event, action):

        # reset error state
        self._toggle_error()
        valid = True

        # ISO dates only need digits and hyphens
        if event == 'key':
            if action == '0':
                valid = True
            elif index in ('0', '1', '2', '3', '5', '6', '8', '9'):
                valid = char.isdigit()
            elif index in ('4', '7'):
                valid = char == '-'
            else:
                valid = False
        elif event == 'focusout':
            try:
                datetime.strptime(self.get(), '%Y-%m-%d')
            except ValueError:
                valid = False
        return valid

    def _on_invalid(self, event):
        if event != 'key':
            self._toggle_error('Not a valid date')

if __name__ == '__main__':
    root = tk.Tk()
    entry = DateEntry(root)
    entry.pack()
    tk.Label(textvariable=entry.error).pack()

    # add this so we can unfocus the DateEntry
    tk.Entry(root).pack()
    root.mainloop()
