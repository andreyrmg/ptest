from distutils.core import setup, Extension

process = Extension('ptest.process',
                    sources=['ptest/process.c'])

setup(name='ptest',
      packages=['ptest',
                'ptest.tools',
                'ptest.web'],
      ext_modules=[process])