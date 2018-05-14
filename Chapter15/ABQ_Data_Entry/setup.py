from setuptools import setup
with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(
    name='ABQ_Data_Entry',
    version='1.0',
    author='Alan D Moore',
    author_email='alandmoore@example.com',
    description='Data entry application for ABQ Agrilabs',
    url="http://abq.example.com",
    license='ABQ corporate license',
    long_description=long_description,
    packages=['abq_data_entry'],
    install_requires=['psycopg2', 'requests', 'matplotlib'],
    python_requires='>=3.6',
    package_data={'abq_data_entry.images': ['*.png']},
    entry_points={
        'console_scripts': [
            'abq = abq_data_entry:main'
        ]
    }
)
