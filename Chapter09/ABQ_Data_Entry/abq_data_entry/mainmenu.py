import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from functools import partial


class GenericMainMenu(tk.Menu):
    """The Application's main menu"""

    def __init__(self, parent, settings, callbacks, **kwargs):
        """Constructor for MainMenu

        arguments:
          parent - The parent widget
          settings - a dict containing Tkinter variables
          callbacks - a dict containing Python callables
        """
        super().__init__(parent, **kwargs)
        self.settings = settings
        self.callbacks = callbacks
        self._build_menu()
        self._bind_accelerators()

    def _build_menu(self):
        # The file menu
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(
            label="Select file…",
            command=self.callbacks['file->select'],
            accelerator='Ctrl+O'
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Quit",
            command=self.callbacks['file->quit'],
            accelerator='Ctrl+Q'
        )
        self.add_cascade(label='File', menu=file_menu)

        # The options menu
        options_menu = tk.Menu(self, tearoff=False)
        options_menu.add_checkbutton(
            label='Autofill Date',
            variable=self.settings['autofill date']
        )
        options_menu.add_checkbutton(
            label='Autofill Sheet data',
            variable=self.settings['autofill sheet data']
        )
        # font size submenu
        font_size_menu = tk.Menu(self, tearoff=False)
        for size in range(6, 17, 1):
            font_size_menu.add_radiobutton(
                label=size, value=size,
                variable=self.settings['font size']
            )
        options_menu.add_cascade(label='Font size', menu=font_size_menu)

        # themes menu
        style = ttk.Style()
        themes_menu = tk.Menu(self, tearoff=False)
        for theme in style.theme_names():
            themes_menu.add_radiobutton(
                label=theme, value=theme,
                variable=self.settings['theme']
            )
        options_menu.add_cascade(label='Theme', menu=themes_menu)
        self.settings['theme'].trace('w', self.on_theme_change)
        self.add_cascade(label='Options', menu=options_menu)

        # switch from recordlist to recordform
        go_menu = tk.Menu(self, tearoff=False)
        go_menu.add_command(
            label="Record List",
            command=self.callbacks['show_recordlist'],
            accelerator='Ctrl+L'
        )
        go_menu.add_command(
            label="New Record",
            command=self.callbacks['new_record'],
            accelerator='Ctrl+N'
        )
        self.add_cascade(label='Go', menu=go_menu)

        # The help menu
        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(label='About…', command=self.show_about)
        self.add_cascade(label='Help', menu=help_menu)

    def get_keybinds(self):
        return {
            '<Control-o>': self.callbacks['file->select'],
            '<Control-q>': self.callbacks['file->quit'],
            '<Control-n>': self.callbacks['new_record'],
            '<Control-l>': self.callbacks['show_recordlist']
        }

    @staticmethod
    def _argstrip(function, *args):
        return function()

    def _bind_accelerators(self):
        keybinds = self.get_keybinds()
        for key, command in keybinds.items():
            self.bind_all(
                key,
                partial(self._argstrip, command)
            )

    def on_theme_change(self, *args):
        """Popup a message about theme changes"""
        message = "Change requires restart"
        detail = (
            "Theme changes do not take effect"
            " until application restart")
        messagebox.showwarning(
            title='Warning',
            message=message,
            detail=detail)

    def show_about(self):
        """Show the about dialog"""

        about_message = 'ABQ Data Entry'
        about_detail = (
            'by Alan D Moore\n'
            'For assistance please contact the author.'
        )
        messagebox.showinfo(
            title='About',
            message=about_message,
            detail=about_detail
        )


class WindowsMainMenu(GenericMainMenu):
    """
    Changes:
     - Windows uses file->exit instead of file->quit,
       and no accelerator is used.
     - Windows can handle commands on the menubar, so
       put 'Record List' / 'New Record' on the bar
     - Put 'options' under 'Tools' with separator
    """

    def _build_menu(self):
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(
            label="Select file…",
            command=self.callbacks['file->select'],
            accelerator='Ctrl+O'
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit",
            command=self.callbacks['file->quit']
        )
        self.add_cascade(label='File', menu=file_menu)

        self.add_command(
            label="Record List",
            command=self.callbacks['show_recordlist'],
            accelerator='Ctrl+L'
        )
        self.add_command(
            label="New Record",
            command=self.callbacks['new_record'],
            accelerator='Ctrl+N'
        )

        # The Tools menu
        tools_menu = tk.Menu(self, tearoff=False)

        # The options menu
        options_menu = tk.Menu(tools_menu, tearoff=False)
        options_menu.add_checkbutton(
            label='Autofill Date',
            variable=self.settings['autofill date']
        )
        options_menu.add_checkbutton(
            label='Autofill Sheet data',
            variable=self.settings['autofill sheet data']
        )
        # font size submenu
        font_size_menu = tk.Menu(self, tearoff=False)
        for size in range(6, 17, 1):
            font_size_menu.add_radiobutton(
                label=size, value=size,
                variable=self.settings['font size']
            )
        options_menu.add_cascade(label='Font size', menu=font_size_menu)

        # themes menu
        style = ttk.Style()
        themes_menu = tk.Menu(self, tearoff=False)
        for theme in style.theme_names():
            themes_menu.add_radiobutton(
                label=theme, value=theme,
                variable=self.settings['theme']
            )
        options_menu.add_cascade(label='Theme', menu=themes_menu)
        self.settings['theme'].trace('w', self.on_theme_change)
        tools_menu.add_separator()
        tools_menu.add_cascade(label='Options', menu=options_menu)
        self.add_cascade(label='Tools', menu=tools_menu)

        # The help menu
        help_menu = tk.Menu(self, tearoff=False)

        self.add_cascade(label='Help', menu=help_menu)

    def get_keybinds(self):
        return {
            '<Control-o>': self.callbacks['file->select'],
            '<Control-n>': self.callbacks['new_record'],
            '<Control-l>': self.callbacks['show_recordlist']
        }


class LinuxMainMenu(GenericMainMenu):
    """Differences for Linux:

      - Edit menu for autofill options
      - View menu for font & theme options
    """
    def _build_menu(self):
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(
            label="Select file…",
            command=self.callbacks['file->select'],
            accelerator='Ctrl+O'
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Quit",
            command=self.callbacks['file->quit'],
            accelerator='Ctrl+Q'
        )
        self.add_cascade(label='File', menu=file_menu)

        # The edit menu
        edit_menu = tk.Menu(self, tearoff=False)
        edit_menu.add_checkbutton(
            label='Autofill Date',
            variable=self.settings['autofill date']
        )
        edit_menu.add_checkbutton(
            label='Autofill Sheet data',
            variable=self.settings['autofill sheet data']
        )
        self.add_cascade(label='Edit', menu=edit_menu)

        # The View menu
        view_menu = tk.Menu(self, tearoff=False)
        # font size submenu
        font_size_menu = tk.Menu(view_menu, tearoff=False)
        for size in range(6, 17, 1):
            font_size_menu.add_radiobutton(
                label=size, value=size,
                variable=self.settings['font size']
            )
        view_menu.add_cascade(label='Font size', menu=font_size_menu)

        # themes menu
        style = ttk.Style()
        themes_menu = tk.Menu(view_menu, tearoff=False)
        for theme in style.theme_names():
            themes_menu.add_radiobutton(
                label=theme, value=theme,
                variable=self.settings['theme']
            )
        view_menu.add_cascade(label='Theme', menu=themes_menu)
        self.settings['theme'].trace('w', self.on_theme_change)
        self.add_cascade(label='View', menu=view_menu)

        # switch from recordlist to recordform
        go_menu = tk.Menu(self, tearoff=False)
        go_menu.add_command(
            label="Record List",
            command=self.callbacks['show_recordlist'],
            accelerator='Ctrl+L'
        )
        go_menu.add_command(
            label="New Record",
            command=self.callbacks['new_record'],
            accelerator='Ctrl+N'
        )
        self.add_cascade(label='Go', menu=go_menu)

        # The help menu
        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(label='About…', command=self.show_about)
        self.add_cascade(label='Help', menu=help_menu)


class MacOsMainMenu(GenericMainMenu):
    """
    Differences for MacOS:

      - Create App Menu
      - Move about to app menu, remove 'help'
      - Remove redundant quit command
      - Change accelerators to Command-[]
      - Add View menu for font & theme options
      - Add Edit menu for autofill options
      - Add Window menu for navigation commands
    """

    def _build_menu(self):
        app_menu = tk.Menu(self, tearoff=False, name='apple')
        app_menu.add_command(
            label='About ABQ Data Entry',
            command=self.show_about
        )
        self.add_cascade(label='ABQ Data Entry', menu=app_menu)
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(
            label="Select file…",
            command=self.callbacks['file->select'],
            accelerator="Cmd-O"
        )
        self.add_cascade(label='File', menu=file_menu)

        edit_menu = tk.Menu(self, tearoff=False)
        edit_menu.add_checkbutton(
            label='Autofill Date',
            variable=self.settings['autofill date']
        )
        edit_menu.add_checkbutton(
            label='Autofill Sheet data',
            variable=self.settings['autofill sheet data']
        )
        self.add_cascade(label='Edit', menu=edit_menu)

        # View menu
        view_menu = tk.Menu(self, tearoff=False)
        # font size submenu
        font_size_menu = tk.Menu(view_menu, tearoff=False)
        for size in range(6, 17, 1):
            font_size_menu.add_radiobutton(
                label=size, value=size,
                variable=self.settings['font size']
            )
        view_menu.add_cascade(label='Font size', menu=font_size_menu)
        # themes menu
        style = ttk.Style()
        themes_menu = tk.Menu(view_menu, tearoff=False)
        for theme in style.theme_names():
            themes_menu.add_radiobutton(
                label=theme, value=theme,
                variable=self.settings['theme']
            )
        view_menu.add_cascade(label='Theme', menu=themes_menu)
        self.settings['theme'].trace('w', self.on_theme_change)
        self.add_cascade(label='View', menu=view_menu)

        # Window Menu
        window_menu = tk.Menu(self, name='window', tearoff=False)
        window_menu.add_command(
            label="Record List",
            command=self.callbacks['show_recordlist'],
            accelerator="Cmd-L"
        )
        window_menu.add_command(
            label="New Record",
            command=self.callbacks['new_record'],
            accelerator="Cmd-N"
        )
        self.add_cascade(label='Window', menu=window_menu)

    def get_keybinds(self):
        return {
            '<Command-o>': self.callbacks['file->select'],
            '<Command-n>': self.callbacks['new_record'],
            '<Command-l>': self.callbacks['show_recordlist']
        }


def get_main_menu_for_os(os_name):
    menus = {
        'Linux': LinuxMainMenu,
        'Darwin': MacOsMainMenu,
        'freebsd7': LinuxMainMenu,
        'Windows': WindowsMainMenu
    }

    return menus.get(os_name, GenericMainMenu)
