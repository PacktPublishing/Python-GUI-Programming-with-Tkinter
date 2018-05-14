import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog
from datetime import datetime
from . import widgets as w

#matplotlib
import matplotlib
# needs to be set before we load any other libraries
# in order to avoid a warning
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2TkAgg)


class DataRecordForm(tk.Frame):
    """The input form for our widgets"""

    def __init__(self, parent, fields, settings, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.settings = settings
        self.callbacks = callbacks

        self.current_record = None

        # style configuration
        style = ttk.Style()

        # Label styles
        style.configure('RecordInfo.TLabel', background='khaki')
        style.configure('EnvironmentInfo.TLabel', background='lightblue')
        style.configure(
            'EnvironmentInfo.TCheckbutton',
            background='lightblue'
        )
        style.configure('PlantInfo.TLabel', background='lightgreen')

        # A dict to keep track of input widgets
        self.inputs = {}

        # Build the form
        self.record_label = ttk.Label(self)
        self.record_label.grid(row=0, column=0)

        # recordinfo section
        recordinfo = tk.LabelFrame(
            self,
            text="Record Information",
            bg="khaki",
            padx=10,
            pady=10
        )

        # line 1
        self.inputs['Date'] = w.LabelInput(
            recordinfo, "Date",
            field_spec=fields['Date'],
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['Date'].grid(row=0, column=0)
        self.inputs['Time'] = w.LabelInput(
            recordinfo, "Time",
            field_spec=fields['Time'],
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['Time'].grid(row=0, column=1)
        self.inputs['Lab'] = w.LabelInput(
            recordinfo, "Lab",
            field_spec=fields['Lab'],
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['Lab'].grid(row=0, column=2)
        # line 2
        self.inputs['Plot'] = w.LabelInput(
            recordinfo, "Plot",
            field_spec=fields['Plot'],
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['Plot'].grid(row=1, column=0)
        self.inputs['Technician'] = w.LabelInput(
            recordinfo, "Technician",
            field_spec=fields['Technician'],
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['Technician'].grid(row=1, column=1)
        self.inputs['Seed sample'] = w.LabelInput(
            recordinfo, "Seed sample",
            field_spec=fields['Seed sample'],
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['Seed sample'].grid(row=1, column=2)

        recordinfo.grid(row=1, column=0, sticky="we")

        # Environment Data
        environmentinfo = tk.LabelFrame(
            self,
            text="Environment Data",
            bg='lightblue',
            padx=10,
            pady=10
        )
        self.inputs['Humidity'] = w.LabelInput(
            environmentinfo, "Humidity (g/m³)",
            field_spec=fields['Humidity'],
            label_args={'style': 'EnvironmentInfo.TLabel'}
        )
        self.inputs['Humidity'].grid(row=0, column=0)
        self.inputs['Light'] = w.LabelInput(
            environmentinfo, "Light (klx)",
            field_spec=fields['Light'],
            label_args={'style': 'EnvironmentInfo.TLabel'}
        )
        self.inputs['Light'].grid(row=0, column=1)
        self.inputs['Temperature'] = w.LabelInput(
            environmentinfo, "Temperature (°C)",
            field_spec=fields['Temperature'],
            label_args={'style': 'EnvironmentInfo.TLabel'}
        )
        self.inputs['Temperature'].grid(row=0, column=2)
        self.inputs['Equipment Fault'] = w.LabelInput(
            environmentinfo, "Equipment Fault",
            field_spec=fields['Equipment Fault'],
            label_args={'style': 'EnvironmentInfo.TLabel'},
            input_args={'style': 'EnvironmentInfo.TCheckbutton'}
        )
        self.inputs['Equipment Fault'].grid(row=1, column=0, columnspan=3)
        environmentinfo.grid(row=2, column=0, sticky="we")

        # Plant Data section
        plantinfo = tk.LabelFrame(
            self,
            text="Plant Data",
            bg="lightgreen",
            padx=10,
            pady=10
        )

        self.inputs['Plants'] = w.LabelInput(
            plantinfo, "Plants",
            field_spec=fields['Plants'],
            label_args={'style': 'PlantInfo.TLabel'}
        )
        self.inputs['Plants'].grid(row=0, column=0)
        self.inputs['Blossoms'] = w.LabelInput(
            plantinfo, "Blossoms",
            field_spec=fields['Blossoms'],
            label_args={'style': 'PlantInfo.TLabel'}
        )
        self.inputs['Blossoms'].grid(row=0, column=1)
        self.inputs['Fruit'] = w.LabelInput(
            plantinfo, "Fruit",
            field_spec=fields['Fruit'],
            label_args={'style': 'PlantInfo.TLabel'}
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
                        "focus_update_var": min_height_var},
            label_args={'style': 'PlantInfo.TLabel'}
        )
        self.inputs['Min Height'].grid(row=1, column=0)
        self.inputs['Max Height'] = w.LabelInput(
            plantinfo, "Max Height (cm)",
            field_spec=fields['Max Height'],
            input_args={"min_var": min_height_var,
                        "focus_update_var": max_height_var},
            label_args={'style': 'PlantInfo.TLabel'}
        )
        self.inputs['Max Height'].grid(row=1, column=1)
        self.inputs['Median Height'] = w.LabelInput(
            plantinfo, "Median Height (cm)",
            field_spec=fields['Median Height'],
            input_args={"min_var": min_height_var,
                        "max_var": max_height_var},
            label_args={'style': 'PlantInfo.TLabel'}
        )
        self.inputs['Median Height'].grid(row=1, column=2)

        plantinfo.grid(row=3, column=0, sticky="we")

        # Notes section
        self.inputs['Notes'] = w.LabelInput(
            self, "Notes",
            field_spec=fields['Notes'],
            input_args={"width": 85, "height": 10}
        )
        self.inputs['Notes'].grid(sticky="w", row=4, column=0, padx=10, pady=10)

        # The save button
        self.savebutton = ttk.Button(
            self,
            text="Save",
            command=self.callbacks["on_save"])
        self.savebutton.grid(sticky="e", row=5, padx=10)

        # Triggers
        for field in ('Lab', 'Plot'):
            self.inputs[field].variable.trace(
                'w', self.callbacks['get_seed_sample'])

        for field in ('Date', 'Time', 'Lab'):
            self.inputs[field].variable.trace(
                'w', self.callbacks['get_check_tech'])


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

    def focus_next_empty(self):
        for labelwidget in self.inputs.values():
            if (labelwidget.get() == ''):
                labelwidget.input.focus()
                break

    def reset(self):
        """Resets the form entries"""

        # clear the current record id
        self.current_record = None

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

        self.focus_next_empty()

    def get_errors(self):
        """Get a list of field errors in the form"""

        errors = {}
        for key, widget in self.inputs.items():
            if hasattr(widget.input, 'trigger_focusout_validation'):
                widget.input.trigger_focusout_validation()
            if widget.error.get():
                errors[key] = widget.error.get()

        return errors

    def load_record(self, rowkey, data=None):
        self.current_record = rowkey
        if rowkey is None:
            self.reset()
            self.record_label.config(text='New Record')
        else:
            self.record_label.config(
                text='Record for Lab {2}, Plot {3} at {0} {1}'
                .format(*rowkey))
            for key, widget in self.inputs.items():
                self.inputs[key].set(data.get(key, ''))
                try:
                    widget.input.trigger_focusout_validation()
                except AttributeError:
                    pass


class RecordList(tk.Frame):
    """Display for CSV file contents"""

    column_defs = {
        '#0': {'label': 'Row', 'anchor': tk.W},
        'Date': {'label': 'Date', 'width': 150, 'stretch': True},
        'Time': {'label': 'Time'},
        'Lab': {'label': 'Lab', 'width': 40},
        'Plot': {'label': 'Plot', 'width': 80}
    }
    default_width = 100
    default_minwidth = 10
    default_anchor = tk.CENTER

    def __init__(self, parent, callbacks,
                 inserted, updated,
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        self.inserted = inserted
        self.updated = updated
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # create treeview
        self.treeview = ttk.Treeview(
            self,
            columns=list(self.column_defs.keys())[1:],
            selectmode='browse'
        )
        # hide first column
        self.treeview.config(show='headings')

        # configure scrollbar for the treeview
        self.scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.treeview.yview
        )
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        self.treeview.grid(row=0, column=0, sticky='NSEW')
        self.scrollbar.grid(row=0, column=1, sticky='NSW')

        # Configure treeview columns
        for name, definition in self.column_defs.items():
            label = definition.get('label', '')
            anchor = definition.get('anchor', self.default_anchor)
            minwidth = definition.get('minwidth', self.default_minwidth)
            width = definition.get('width', self.default_width)
            stretch = definition.get('stretch', False)
            self.treeview.heading(name, text=label, anchor=anchor)
            self.treeview.column(name, anchor=anchor, minwidth=minwidth,
                                 width=width, stretch=stretch)

        # configure row tags
        self.treeview.tag_configure('inserted', background='lightgreen')
        self.treeview.tag_configure('updated', background='lightblue')

        # Bind double-clicks
        self.treeview.bind('<<TreeviewOpen>>', self.on_open_record)

    def populate(self, rows):
        """Clear the treeview and write the supplied data rows to it."""

        for row in self.treeview.get_children():
            self.treeview.delete(row)

        valuekeys = list(self.column_defs.keys())[1:]
        for rowdata in rows:
            rowkey = (str(rowdata['Date']), rowdata['Time'],
                      rowdata['Lab'], str(rowdata['Plot']))
            values = [rowdata[key] for key in valuekeys]
            if self.inserted and rowkey in self.inserted:
                tag = 'inserted'
            elif self.updated and rowkey in self.updated:
                tag = 'updated'
            else:
                tag = ''
            stringkey = '{}|{}|{}|{}'.format(*rowkey)
            self.treeview.insert(
                '', 'end', iid=stringkey,
                text=stringkey, values=values,
                tag=tag)

        if len(rows) > 0:
            firstrow = self.treeview.identify_row(0)
            self.treeview.focus_set()
            self.treeview.selection_set(firstrow)
            self.treeview.focus(firstrow)

    def on_open_record(self, *args):

        selected_id = self.treeview.selection()[0]
        self.callbacks['on_open_record'](selected_id.split('|'))

class LoginDialog(Dialog):

    def __init__(self, parent, title, error=''):

        self.pw = tk.StringVar()
        self.user = tk.StringVar()
        self.error = tk.StringVar(value=error)
        super().__init__(parent, title=title)

    def body(self, parent):
        lf = tk.Frame(self)
        ttk.Label(lf, text='Login to ABQ',
                  font='TkHeadingFont').grid(row=0)

        ttk.Style().configure('err.TLabel',
                background='darkred', foreground='white')
        if self.error.get():
            ttk.Label(lf, textvariable=self.error,
                      style='err.TLabel').grid(row=1)
        ttk.Label(lf, text='User name:').grid(row=2)
        self.username_inp = ttk.Entry(lf, textvariable=self.user)
        self.username_inp.grid(row=3)
        ttk.Label(lf, text='Password:').grid(row=4)
        self.password_inp = ttk.Entry(lf, show='*', textvariable=self.pw)
        self.password_inp.grid(row=5)
        lf.pack()
        return self.username_inp

    def apply(self):

        self.result = (self.user.get(), self.pw.get())


class LineChartView(tk.Canvas):

    margin = 20

    def __init__(self, parent, chart_width, chart_height,
                 x_axis, y_axis, max_x, max_y):
        view_width = chart_width + 2 * self.margin
        view_height = chart_height + 2 * self.margin
        super().__init__(
            parent, width=view_width,
            height=view_height, background='lightgrey')
        self.max_x = max_x
        self.max_y = max_y
        self.chart_width = chart_width
        self.chart_height = chart_height

        # draw axes and labels
        self.origin = (self.margin, view_height - self.margin)
        self.create_line(
            self.origin, (self.margin, self.margin), width=2)
        self.create_line(
            self.origin,
            (view_width - self.margin,
             view_height - self.margin))
        self.create_text(
            (view_width // 2, view_height - self.margin),
            text=x_axis, anchor='n')
        # angle requires tkinter 8.6
        self.create_text(
            (self.margin, view_height // 2),
            text=y_axis, angle=90, anchor='s')

        # create chart
        self.chart = tk.Canvas(
            self, width=chart_width, height=chart_height,
            background='white')
        self.create_window(
            self.origin, window=self.chart, anchor='sw')

    def plot_line(self, data, color):
        x_scale = self.chart_width / self.max_x
        y_scale = self.chart_height / self.max_y

        # calculate coordinates
        coords = [(round(x * x_scale),
            self.chart_height - round(y * y_scale))
            for x, y in data]

        # create the line
        self.chart.create_line(*coords, width=2, fill=color)

    def draw_legend(self, mapping):
        y = self.margin
        x = round(self.margin * 1.5) + self.chart_width
        for label, color in mapping.items():
            self.create_text((x, y), text=label, fill=color, anchor='w')
            y += 20


class YieldChartView(tk.Frame):

    def __init__(self, parent, x_axis, y_axis, title):
        super().__init__(parent)
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self)

        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        self.axes = self.figure.add_subplot(1, 1, 1)
        self.axes.set_xlabel(x_axis)
        self.axes.set_ylabel(y_axis)
        self.axes.set_title(title)

        self.scatters = []
        self.scatter_labels = []

    def draw_scatter(self, data, color, label):
        """Draw data values on the scatter plot

        Should be a list of items in the format (x, y, s)"""
        x, y, s = zip(*data)
        # make differences in s more visible
        s = [(x ** 2)//2 for x in s]
        scatter = self.axes.scatter(x, y, s, c=color, label=label, alpha=.5)
        self.scatters.append(scatter)
        self.scatter_labels.append(label)
        self.axes.legend(self.scatters, self.scatter_labels)
