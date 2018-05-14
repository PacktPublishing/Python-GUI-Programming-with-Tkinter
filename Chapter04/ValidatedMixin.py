import tkinter as tk
from tkinter import ttk


class ValidatedMixin:
    """Adds a validation functionality to an input widget"""

    def __init__(self, *args, error_var=None, **kwargs):
        self.error = error_var or tk.StringVar()
        super().__init__(*args, **kwargs)

        vcmd = self.register(self._validate)
        invcmd = self.register(self._invalid)

        self.config(
            validate='all',
            validatecommand=(vcmd, '%P', '%s', '%S', '%V', '%i', '%d'),
            invalidcommand=(invcmd, '%P', '%s', '%S', '%V', '%i', '%d')
        )

    def _toggle_error(self, on=False):
        self.config(foreground=('red' if on else 'black'))

    def _validate(self, proposed, current, char, event, index, action):
        """The validation method.

        Don't override this, override _key_validate, and _focus_validate
        """
        self._toggle_error(False)
        self.error.set('')
        valid = True
        if event == 'focusout':
            valid = self._focusout_validate(event=event)
        elif event == 'key':
            valid = self._key_validate(
                proposed=proposed,
                current=current,
                char=char,
                event=event,
                index=index,
                action=action
            )
        return valid

    def _focusout_validate(self, **kwargs):
        return True

    def _key_validate(self, **kwargs):
        return True

    def _invalid(self, proposed, current, char, event, index, action):
        if event == 'focusout':
            self._focusout_invalid(event=event)
        elif event == 'key':
            self._key_invalid(
                proposed=proposed,
                current=current,
                char=char,
                event=event,
                index=index,
                action=action
            )

    def _focusout_invalid(self, **kwargs):
        """Handle invalid data on a focus event"""
        self._toggle_error(True)

    def _key_invalid(self, **kwargs):
        """Handle invalid data on a key event.  By default we want to do nothing"""
        pass


class FiveCharEntry(ValidatedMixin, tk.Entry):

    def _key_validate(self, **kwargs):
        valid = len(kwargs['proposed']) <= 5
        if not valid:
            self.error.set('Too long!')
        return valid

    def _focusout_validate(self, **kwargs):
        value = self.get()

        if 'q' in value:
            self.error.set('Has a q.  I hate q')
            return False
        return True


class BetterCombobox(ValidatedMixin, ttk.Combobox):

    def _key_validate(self, **kwargs):

        proposed = kwargs['proposed']
        current = kwargs['current']
        action = kwargs['action']

        if action == '0': # deletion.  Delete it all
            self.set('')
            return True

        values = self.cget('values')
        matching = [
            x for x in values
            if x.lower().startswith(proposed.lower())
        ]

        if len(matching) == 0:
            self.set(current)
            return False
        elif len(matching) == 1:
            self.set(matching[0])
            self.icursor(tk.END)
            return False
        else:
            return True


if __name__ == '__main__':

    root = tk.Tk()
    ev = tk.StringVar()
    FiveCharEntry(root, error_var=ev).pack()
    sv = tk.StringVar()
    BetterCombobox(root, textvariable=sv, values=['Ken', 'Barb', 'Betty', 'Barry', 'Joe']).pack()
    root.mainloop()
