import platform
from os import environ
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.font import nametofont
from datetime import datetime
from . import views as v
from . import models as m
from .mainmenu import get_main_menu_for_os
from .images import ABQ_LOGO_32, ABQ_LOGO_64


class Application(tk.Tk):
    """Application root window"""
    config_dirs = {
        'Linux': environ.get('$XDG_CONFIG_HOME', '~/.config'),
        'freebsd7': environ.get('$XDG_CONFIG_HOME', '~/.config'),
        'Darwin': '~/Library/Application Support',
        'Windows': '~/AppData/Local'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("ABQ Data Entry Application")
        self.resizable(width=False, height=False)

        self.taskbar_icon = tk.PhotoImage(file=ABQ_LOGO_64)
        self.call('wm', 'iconphoto', self._w, self.taskbar_icon)

        self.logo = tk.PhotoImage(file=ABQ_LOGO_32)
        tk.Label(self, image=self.logo).grid(row=0)

        self.inserted_rows = []
        self.updated_rows = []

        # data model
        datestring = datetime.today().strftime("%Y-%m-%d")
        default_filename = "abq_data_record_{}.csv".format(datestring)
        self.filename = tk.StringVar(value=default_filename)
        self.data_model = m.CSVModel(filename=self.filename.get())

        # settings model & settings
        config_dir = self.config_dirs.get(platform.system(), '~')
        self.settings_model = m.SettingsModel(path=config_dir)
        self.load_settings()
        self.set_font()
        self.settings['font size'].trace('w', self.set_font)

        style = ttk.Style()
        theme = self.settings.get('theme').get()
        if theme in style.theme_names():
            style.theme_use(theme)

        self.callbacks = {
            'file->select': self.on_file_select,
            'file->quit': self.quit,
            'show_recordlist': self.show_recordlist,
            'new_record': self.open_record,
            'on_open_record': self.open_record,
            'on_save': self.on_save
        }
        menu_class = get_main_menu_for_os(platform.system())
        menu = menu_class(self, self.settings, self.callbacks)
        self.config(menu=menu)

        # The data record form
        self.recordform = v.DataRecordForm(
            self, m.CSVModel.fields, self.settings, self.callbacks)
        self.recordform.grid(row=1, padx=10, sticky='NSEW')

        # The data record list
        self.recordlist = v.RecordList(
            self,
            self.callbacks,
            inserted=self.inserted_rows,
            updated=self.updated_rows
        )
        self.recordlist.grid(row=1, padx=10, sticky='NSEW')
        self.populate_recordlist()

        # status bar
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky="we", row=3, padx=10)

        self.records_saved = 0

    def show_recordlist(self):
        """Show the recordform"""

        self.recordlist.tkraise()

    def populate_recordlist(self):
        try:
            rows = self.data_model.get_all_records()
        except Exception as e:
            messagebox.showerror(
                title='Error',
                message='Problem reading file',
                detail=str(e)
            )
        else:
            self.recordlist.populate(rows)

    def open_record(self, rownum=None):
        if rownum is None:
            record = None
        else:
            rownum = int(rownum)
            try:
                record = self.data_model.get_record(rownum)
            except Exception as e:
                messagebox.showerror(
                    title='Error',
                    message='Problem reading file',
                    detail=str(e)
                )
                return
        self.recordform.load_record(rownum, record)
        self.recordform.tkraise()

    def on_save(self):
        """Handles save button clicks"""

        # Check for errors first
        errors = self.recordform.get_errors()
        if errors:
            message = "Cannot save record"
            detail = "The following fields have errors: \n  * {}".format(
                '\n  * '.join(errors.keys())
            )
            self.status.set(
                "Cannot save, error in fields: {}"
                .format(', '.join(errors.keys()))
            )
            messagebox.showerror(title='Error', message=message, detail=detail)

            return False

        data = self.recordform.get()
        rownum = self.recordform.current_record
        try:
            self.data_model.save_record(data, rownum)
        except IndexError as e:
            messagebox.showerror(
                title='Error',
                message='Invalid row specified',
                detail=str(e)
            )
            self.status.set('Tried to update invalid row')

        except Exception as e:
            messagebox.showerror(
                title='Error',
                message='Problem saving record',
                detail=str(e)
            )
            self.status.set('Problem saving record')

        else:
            self.records_saved += 1
            self.status.set(
                "{} records saved this session".format(self.records_saved)
            )
            if rownum is not None:
                self.updated_rows.append(rownum)
            else:
                # we just inserted row number equal to one less than
                # the number of rows in the CSV
                rownum = len(self.data_model.get_all_records()) - 1
                self.inserted_rows.append(rownum)
            self.populate_recordlist()
            # Only reset the form when we're appending records
            if self.recordform.current_record is None:
                self.recordform.reset()


    def on_file_select(self):
        """Handle the file->select action from the menu"""

        filename = filedialog.asksaveasfilename(
            title='Select the target file for saving records',
            defaultextension='.csv',
            filetypes=[('CSV', '*.csv *.CSV')]
        )
        if filename:
            self.filename.set(filename)
            self.data_model = m.CSVModel(filename=self.filename.get())
            self.populate_recordlist()
            self.inserted_rows = []
            self.updated_rows = []


    def save_settings(self, *args):
        """Save the current settings to a preferences file"""

        for key, variable in self.settings.items():
            self.settings_model.set(key, variable.get())
        self.settings_model.save()

    def load_settings(self):
        """Load settings into our self.settings dict."""

        vartypes = {
            'bool': tk.BooleanVar,
            'str': tk.StringVar,
            'int': tk.IntVar,
            'float': tk.DoubleVar
        }

        # create our dict of settings variables from the model's settings.
        self.settings = {}
        for key, data in self.settings_model.variables.items():
            vartype = vartypes.get(data['type'], tk.StringVar)
            self.settings[key] = vartype(value=data['value'])

        # put a trace on the variables so they get stored when changed.
        for var in self.settings.values():
            var.trace('w', self.save_settings)

    def set_font(self, *args):
        font_size = self.settings['font size'].get()
        font_names = ('TkDefaultFont', 'TkMenuFont', 'TkTextFont')
        for font_name in font_names:
            tk_font = nametofont(font_name)
            tk_font.config(size=font_size)
