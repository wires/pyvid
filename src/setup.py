"""
Minimal setup.py example, run with:
% python setup.py py2app

For the list of available commands, see:
% python setup.py py2app --help
"""

from distutils.core import setup
import py2app
setup(
	data_files = ['font.ttf'],
	app = ['pyvid.py'],
)
