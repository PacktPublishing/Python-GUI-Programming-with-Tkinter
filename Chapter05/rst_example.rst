==================
 This is the title
==================

--------------------
 This is a subtitle.
--------------------


Heading 1
=========

This is the first paragraph of the RST file.  The great thing about RST is that it can be read as a plain text document, or interpretted by software into more attractive formats like HTML or PDF.

The second paragraph starts here.  The docutils project provides a set of scripts to convert rst into other formats, including:

* HTML
* PDF
* ODT
* XML


Heading 2
---------

This is a paragraph under heading 2.  Let's add a block of code::

  from tkinter import Tk, Label
  r = Tk()
  Label(r, 'Hi!').pack()
  r.mainloop()

Here's a simple table:

================= ===============================
Node              Description
================= ===============================
docs              folder for documentation
abq_data_entry    folder for application module
abq_data_entry.py main executable for application
README.rst        The basic documentation
================  ===============================

Here's a more complex table:

+-----------------+-------------------------------+
|Node             |Description                    |
+=================+===============================+
|docs             |folder for documentation       |
+-----------------+-------------------------------+
|abq_data_entry   |folder for application module  |
+-----------------+-------------------------------+
|abq_data_entry.py|main executable for application|
+-----------------+-------------------------------+
|README.rst       |The basic documentation        |
+-----------------+-------------------------------+
