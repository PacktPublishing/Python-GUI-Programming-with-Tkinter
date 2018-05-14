import cx_Freeze as cx

include_files = [('abq_data_entry/images', 'images')]

cx.setup(
    name='ABQ_Data_Entry',
    version='1.0',
    author='Alan D Moore',
    author_email='alandmoore@example.com',
    description='Data entry application for ABQ Agrilabs',
    url="http://abq.example.com",
    packages=['abq_data_entry'],
    executables=[
        cx.Executable('abq_data_entry.py',
                      targetName='abq', icon='abq.ico')],
    options={
        'build_exe': {
            'packages': ['psycopg2', 'requests', 'matplotlib', 'numpy'],
            'includes': ['idna.idnadata', 'zlib'],
            'include_files': include_files
        }
    }
)
