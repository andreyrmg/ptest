from distutils.core import setup, Extension
import os

ext_modules = []
if os.name == 'nt':
    ext_modules.append(Extension('ptest.process_nt',
                                 sources=['ptest/process-nt.c']))

setup(name='ptest',
      packages=['ptest',
                'ptest.tools',
                'ptest.web'],
      ext_modules=ext_modules)
