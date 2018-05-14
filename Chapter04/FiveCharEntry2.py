import tkinter as tk
from tkinter import ttk

class FiveCharEntry2(ttk.Entry):
    """An Entry that truncates to five characters on exit."""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(
            validate='focusout',
            validatecommand=(self.register(self._validate), '%P'),
            invalidcommand=(self.register(self._on_invalid),)
        )

    def _validate(self, proposed_value):
        return len(proposed_value) <= 5

    def _on_invalid(self):
        self.delete(5, tk.END)


if __name__ == '__main__':
    root = tk.Tk()
    entry = FiveCharEntry2(root)
    entry.pack()
    tk.Entry(root).pack()
    root.mainloop()
