from distutils.core import setup, Extension

setup(name='pplp',
      version='0.1',
      packages=['pplp'],
      ext_modules=[Extension('pplp.libcall_glpk', ['pplp/call_glpk.c'], libraries=['glpk'])],
      )
