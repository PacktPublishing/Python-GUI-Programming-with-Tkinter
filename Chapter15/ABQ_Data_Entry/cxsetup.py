import cx_Freeze as cx
import platform
import os

base = None
include_files = [('abq_data_entry/images', 'images')]
target_name = 'abq'
if platform.system() == "Windows":
    base = "Win32GUI"
    target_name = 'abq.exe'
    PYTHON_DIR = os.path.dirname(os.path.dirname(os.__file__))
    os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_DIR, 'tcl', 'tcl8.6')
    os.environ['TK_LIBRARY'] = os.path.join(PYTHON_DIR, 'tcl', 'tk8.6')
    include_files += [
        (os.path.join(PYTHON_DIR, 'DLLs', 'tcl86t.dll'), ''),
        (os.path.join(PYTHON_DIR, 'DLLs', 'tk86t.dll'), '')
    ]


shortcut_data = [
    # (Type, Folder, Name, ?, Target exe, arguments, description, hotkey, icon, icon index, show cmd, Working dir)
    ('DesktopShortcut', 'DesktopFolder', 'ABQ Data Entry', 'TARGETDIR',
     '[TARGETDIR]' + target_name, None,
     'Data Entry application for ABQ Agrilabs', None,
     None, None, None, 'TARGETDIR'),
    ('MenuShortcut', 'ProgramMenuFolder', 'ABQ Data Entry', 'TARGETDIR',
     '[TARGETDIR]' + target_name, None,
     'Data Entry application for ABQ Agrilabs', None,
     None, None, None, 'TARGETDIR'),
]

cx.setup(
    name='ABQ_Data_Entry',
    version='1.0',
    author='Alan D Moore',
    author_email='alandmoore@example.com',
    description='Data entry application for ABQ Agrilabs',
    url="http://abq.example.com",
    packages=['abq_data_entry'],
    executables=[
        cx.Executable('abq_data_entry.py', base=base,
                      targetName=target_name, icon='abq.ico')],
    options={
        'build_exe': {
            'packages': ['psycopg2', 'requests', 'matplotlib', 'numpy'],
            'includes': ['idna.idnadata', 'zlib'],
            'excludes': ['PyQt4', 'PyQt5', 'PySide', 'IPython',
                         'jupyter_client', 'jupyter_core', 'ipykernel',
                         'ipython_genutils'],
            'include_files': include_files
        },
        'bdist_msi': {
            # can be generated in powershell: "{"+[System.Guid]::NewGuid().ToString().ToUpper()+"}"
            'upgrade_code': '{12345678-90AB-CDEF-1234-567890ABCDEF}',
            'data': {'Shortcut': shortcut_data}
        },
        'bdist_mac': {
            # Sets the application name
            'bundle_name': 'ABQ-Data-Entry',
            'iconfile': 'abq.icns'
        }
    }
)
