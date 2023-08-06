#!/usr/bin/env python
from setuptools import setup
import os
from codecs import open
import sys


here = os.path.abspath(os.path.dirname(__file__))

def readme():
    with open('README.rst') as f:
        return f.read()

about = {}
with open(os.path.join(here, 'apikeystore', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description='',
    long_description=readme(),
    url=about['__homepage__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    license=about['__license__'],
    packages=['apikeystore'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 2 - Pre-Alpha'
        ],
    include_package_data=True,
    zip_safe=False    
)
