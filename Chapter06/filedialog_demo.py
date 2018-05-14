from tkinter import filedialog

source = filedialog.askopenfile(
    mode='r',
    title='Select a CSV file to copy',
    filetypes=[('CSV', '*.csv *.CSV')])

if not source:
    exit()

destination = filedialog.asksaveasfile(
    mode='w',
    title='Select a destination file',
    defaultextension='.csv',
    filetypes=[('CSV', '*.csv *.CSV')])

destination.write(source.read())
source.close()
destination.close()
