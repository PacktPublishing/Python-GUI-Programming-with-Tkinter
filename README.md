


# Python GUI programming with Tkinter
This is the code repository for [Python GUI programming with Tkinter](https://www.packtpub.com/application-development/python-gui-programming-tkinter?utm_source=github&utm_medium=repository&utm_campaign=9781788835886), published by [Packt](https://www.packtpub.com/?utm_source=github). It contains all the supporting project files necessary to work through the book from start to finish.
## About the Book
Tkinter is a lightweight, portable, and easy-to-use graphical toolkit available in the Python Standard Library, widely used to build Python GUIs due to its simplicity and availability. This book teaches you to design and build graphical user interfaces that are functional, appealing, and user-friendly using the powerful combination of Python and Tkinter.

After being introduced to Tkinter, you will be guided step-by-step through the application development process. Over the course of the book, your application will evolve from a simple data-entry form to a complex data management and visualization tool while maintaining a clean and robust design. In addition to building the GUI, you'll learn how to connect to external databases and network resources, test your code to avoid errors, and maximize performance using asynchronous programming. You'll make the most of Tkinter's cross-platform availability by learning how to maintain compatibility, mimic platform-native look and feel, and build executables for deployment across popular computing platforms.
## Instructions and Navigation
All of the code is organized into folders. Each folder starts with a number followed by the application name. For example, Chapter02.

All code files are placed in their respective folders. The _init_ file would be empty in all the code files which is to be filled by the user as per instructions given in the book.

The code will look like the following:
```
def has_five_or_less_chars(string):
      return len(string) <= 5
      wrapped_function = root.register(has_five_or_less_chars)
      vcmd = (wrapped_function, '%P')
      five_char_input = ttk.Entry(root, validate='key',       validatecommand=vcmd)
```

This book expects that you know the basics of Python 3. You should know how to write
and run simple scripts using built-in types and functions, how to define your own
functions and classes, and how to import modules from the standard library.
You can follow this book if you run Windows, macOS, Linux, or even BSD. Ensure that you
have Python 3 and Tcl/Tk installed (Chapter 1, Introduction to Tkinter, contains instructions
for Windows, macOS, and Linux) and that you have an editing environment with which
you are comfortable (we suggest IDLE since it comes with Python and uses Tkinter). In the
later chapters, you'll need access to the internet so that you can install Python packages and
the PostgreSQL database.

## Errata
**Errata Type: Typo**
* Page number 07 PDF: \
 _It is:_ The Tk widget library originates from the Tool Command Language (Tcl) programming language. Tcl and Tk were created by John **Ousterman** \
 _Should be:_ The Tk widget library originates from the Tool Command Language (Tcl) programming language. Tcl and Tk were created by John **Ousterhout**

## Related Products
* [Tkinter GUI Application Development Cookbook](https://www.packtpub.com/web-development/tkinter-gui-application-development-cookbook?utm_source=github&utm_medium=repository&utm_campaign=9781788622301)

* [Tkinter GUI Application Development Blueprints - Second Edition](https://www.packtpub.com/application-development/tkinter-gui-application-development-blueprints-second-edition?utm_source=github&utm_medium=repository&utm_campaign=9781788837460)

* [Tkinter GUI Application Development Blueprints](https://www.packtpub.com/application-development/tkinter-gui-application-development-blueprints?utm_source=github&utm_medium=repository&utm_campaign=9781785889738)


### Download a free PDF

 <i>If you have already purchased a print or Kindle version of this book, you can get a DRM-free PDF version at no cost.<br>Simply click on the link to claim your free PDF.</i>
<p align="center"> <a href="https://packt.link/free-ebook/9781788835886">https://packt.link/free-ebook/9781788835886 </a> </p>