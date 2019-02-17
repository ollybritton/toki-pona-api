#!/usr/bin/env python

from distutils.core import setup
from glob import glob

from setuptools import find_packages
from os.path import splitext, basename

setup(name='Toki Pona API',
      version='2.0',
      description='An API to get information of Toki Pona words.',
      author='Olly Britton',
      packages=find_packages('.'),
      package_dir={'': '.'},
      py_modules=[splitext(basename(path))[0] for path in glob('./*.py')],
)
