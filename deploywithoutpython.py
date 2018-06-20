from distutils.core import setup
import py2exe
setup(console=['deploy_win_standalone.py'])

#To execute this script run the following command in the CMD
#python deploywithoutpython.py   py2exe --bundle-files 1 --dll-excludes w9xpopen.exe --dist-dir deployment_build
