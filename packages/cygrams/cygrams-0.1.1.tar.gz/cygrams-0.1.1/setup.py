#!/usr/bin/env python

from setuptools import setup
from setuptools.extension import Extension

from Cython.Build import cythonize


setup(
    setup_requires=['pbr'],
    pbr=True,
    ext_modules=cythonize([
        Extension("cygrams", ["cygrams.pyx"]),
    ]),
)
