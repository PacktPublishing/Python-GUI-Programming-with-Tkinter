from os import path
import sys

if getattr(sys, 'frozen', False):
    # The application is frozen
    IMAGE_DIRECTORY = path.join(path.dirname(sys.executable), 'images')
else:
    # The application is not frozen
    # Change this bit to match where you store your data files:
    IMAGE_DIRECTORY = path.dirname(__file__)

ABQ_LOGO_16 = path.join(IMAGE_DIRECTORY, 'abq_logo-16x10.png')
ABQ_LOGO_32 = path.join(IMAGE_DIRECTORY, 'abq_logo-32x20.png')
ABQ_LOGO_64 = path.join(IMAGE_DIRECTORY, 'abq_logo-64x40.png')
