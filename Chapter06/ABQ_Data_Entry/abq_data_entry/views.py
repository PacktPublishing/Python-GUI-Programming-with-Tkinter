import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from . import widgets as w


class DataRecordForm(tk.Frame):
    """The input form for our widgets"""

    def __init__(self, parent, fields, settings, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.settings = settings

        # A dict to keep track of input widgets
        self.inputs = {}

        # Build the form
        # recordinfo section
        recordinfo = tk.LabelFrame(self, text="Record Information")

        # line 1
        self.inputs['Date'] = w.LabelInput(
            recordinfo, "Date",
            field_spec=fields['Date']
        )
        self.inputs['Date'].grid(row=0, column=0)
        self.inputs['Time'] = w.LabelInput(
            recordinfo, "Time",
            field_spec=fields['Time']
        )
        self.inputs['Time'].grid(row=0, column=1)
        self.inputs['Technician'] = w.LabelInput(
            recordinfo, "Technician",
            field_spec=fields['Technician']
        )
        self.inputs['Technician'].grid(row=0, column=2)

        # line 2
        self.inputs['Lab'] = w.LabelInput(
            recordinfo, "Lab",
            field_spec=fields['Lab']
        )
        self.inputs['Lab'].grid(row=1, column=0)
        self.inputs['Plot'] = w.LabelInput(
            recordinfo, "Plot",
            field_spec=fields['Plot']
        )
        self.inputs['Plot'].grid(row=1, column=1)
        self.inputs['Seed sample'] = w.LabelInput(
            recordinfo, "Seed sample",
            field_spec=fields['Seed sample']
        )
        self.inputs['Seed sample'].grid(row=1, column=2)

        recordinfo.grid(row=0, column=0, sticky="we")

        # Environment Data
        environmentinfo = tk.LabelFrame(self, text="Environment Data")
        self.inputs['Humidity'] = w.LabelInput(
            environmentinfo, "Humidity (g/m³)",
            field_spec=fields['Humidity']
        )
        self.inputs['Humidity'].grid(row=0, column=0)
        self.inputs['Light'] = w.LabelInput(
            environmentinfo, "Light (klx)",
            field_spec=fields['Light']
        )
        self.inputs['Light'].grid(row=0, column=1)
        self.inputs['Temperature'] = w.LabelInput(
            environmentinfo, "Temperature (°C)",
            field_spec=fields['Temperature']
        )
        self.inputs['Temperature'].grid(row=0, column=2)
        self.inputs['Equipment Fault'] = w.LabelInput(
            environmentinfo, "Equipment Fault",
            field_spec=fields['Equipment Fault']
        )
        self.inputs['Equipment Fault'].grid(row=1, column=0, columnspan=3)
        environmentinfo.grid(row=1, column=0, sticky="we")

        # Plant Data section
        plantinfo = tk.LabelFrame(self, text="Plant Data")

        self.inputs['Plants'] = w.LabelInput(
            plantinfo, "Plants",
            field_spec=fields['Plants']
        )
        self.inputs['Plants'].grid(row=0, column=0)
        self.inputs['Blossoms'] = w.LabelInput(
            plantinfo, "Blossoms",
            field_spec=fields['Blossoms']
        )
        self.inputs['Blossoms'].grid(row=0, column=1)
        self.inputs['Fruit'] = w.LabelInput(
            plantinfo, "Fruit",
            field_spec=fields['Fruit']
        )
        self.inputs['Fruit'].grid(row=0, column=2)
        # Height data
        # create variables to be updated for min/max height
        # they can be referenced for min/max variables
        min_height_var = tk.DoubleVar(value='-infinity')
        max_height_var = tk.DoubleVar(value='infinity')

        self.inputs['Min Height'] = w.LabelInput(
            plantinfo, "Min Height (cm)",
            field_spec=fields['Min Height'],
            input_args={"max_var": max_height_var,
                        "focus_update_var": min_height_var}
        )
        self.inputs['Min Height'].grid(row=1, column=0)
        self.inputs['Max Height'] = w.LabelInput(
            plantinfo, "Max Height (cm)",
            field_spec=fields['Max Height'],
            input_args={"min_var": min_height_var,
                        "focus_update_var": max_height_var}
        )
        self.inputs['Max Height'].grid(row=1, column=1)
        self.inputs['Median Height'] = w.LabelInput(
            plantinfo, "Median Height (cm)",
            field_spec=fields['Median Height'],
            input_args={"min_var": min_height_var,
                        "max_var": max_height_var}
        )
        self.inputs['Median Height'].grid(row=1, column=2)

        plantinfo.grid(row=2, column=0, sticky="we")

        # Notes section
        self.inputs['Notes'] = w.LabelInput(
            self, "Notes",
            field_spec=fields['Notes'],
            input_args={"width": 75, "height": 10}
        )
        self.inputs['Notes'].grid(sticky="w", row=3, column=0)

        # default the form
        self.reset()

    def get(self):
        """Retrieve data from form as a dict"""

        # We need to retrieve the data from Tkinter variables
        # and place it in regular Python objects

        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        return data

    def reset(self):
        """Resets the form entries"""

        # gather the values to keep for each lab
        lab = self.inputs['Lab'].get()
        time = self.inputs['Time'].get()
        technician = self.inputs['Technician'].get()
        plot = self.inputs['Plot'].get()
        plot_values = self.inputs['Plot'].input.cget('values')

        # clear all values
        for widget in self.inputs.values():
            widget.set('')

        # new for ch6
        if self.settings['autofill date'].get():
            current_date = datetime.today().strftime('%Y-%m-%d')
            self.inputs['Date'].set(current_date)
            self.inputs['Time'].input.focus()

        # check if we need to put our values back, then do it.
        if (
            self.settings['autofill sheet data'].get() and
            plot not in ('', plot_values[-1])
        ):
            self.inputs['Lab'].set(lab)
            self.inputs['Time'].set(time)
            self.inputs['Technician'].set(technician)
            next_plot_index = plot_values.index(plot) + 1
            self.inputs['Plot'].set(plot_values[next_plot_index])
            self.inputs['Seed sample'].input.focus()

    def get_errors(self):
        """Get a list of field errors in the form"""

        errors = {}
        for key, widget in self.inputs.items():
            if hasattr(widget.input, 'trigger_focusout_validation'):
                widget.input.trigger_focusout_validation()
            if widget.error.get():
                errors[key] = widget.error.get()

        return errors


class MainMenu(tk.Menu):
    """The Application's main menu"""

    def __init__(self, parent, settings, callbacks, **kwargs):
        """Constructor for MainMenu

        arguments:
          parent - The parent widget
          settings - a dict containing Tkinter variables
          callbacks - a dict containing Python callables
        """
        super().__init__(parent, **kwargs)

        # The file menu
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(label="Select file…", command=callbacks['file->select'])
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=callbacks['file->quit'])
        self.add_cascade(label='File', menu=file_menu)

        # The options menu
        options_menu = tk.Menu(self, tearoff=False)
        options_menu.add_checkbutton(
            label='Autofill Date',
            variable=settings['autofill date']
        )
        options_menu.add_checkbutton(
            label='Autofill Sheet data',
            variable=settings['autofill sheet data']
        )
        self.add_cascade(label='Options', menu=options_menu)

        # The help menu

        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(label='About…', command=self.show_about)
        self.add_cascade(label='Help', menu=help_menu)


    def show_about(self):
        """Show the about dialog"""

        about_message = 'ABQ Data Entry'
        about_detail = (
            'by Alan D Moore\n'
            'For assistance please contact the author.'
        )

        messagebox.showinfo(title='About', message=about_message, detail=about_detail)
