# -*- coding: utf-8 -*-

# A simple setup script to create an executable using PyQt4. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt4app.py is a very simple type of PyQt4 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

packages = ['ssq_ui',
            'ssq_ui.ssq_main',
            'ssq_ui.result',
            'ssq_ui.ssq_rc'
]

includes = ['atexit'
]

options = {
    'build_exe': {
    #    'includes': 'atexit',
    #   'packages': packages
        'includes': includes
    }
}

executables = [
    Executable('ssq.py', base=base)
]

setup(name='ssq',
      version='0.1',
      description='ssq exe',
      options=options,
      executables=executables
      )
