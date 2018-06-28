from distutils.core import setup
from py2exe.build_exe import py2exe
from PyQt5 import *
from PyQt4 import *
import py2exe
#setup(console=['tkinter.py'])
setup(windows=['tkinter.py'], options={"py2exe":{"includes":["sip"]}})

#To execute this script run the following command in the CMD
#python deploywithoutpython.py   py2exe --bundle-files 1 --dll-excludes w9xpopen.exe --dist-dir deployment_build
