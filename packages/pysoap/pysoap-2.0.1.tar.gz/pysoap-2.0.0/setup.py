#!/usr/bin/env python

from distutils.core import setup
import os
import subprocess
import sys
import warnings
from os import path

try:
    import py2exe
    from nsis import build_installer
except:
    build_installer = None

from pysimplesoap import __version__, __author__, __author_email__, __license__

# convert the README and format in restructured text (only when registering)
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='pysoap',
    version=__version__,
    description='Python simple and lightweight SOAP Library',
    long_description=LONG_DESCRIPTION,
    author=__author__,
    author_email=__author_email__,
    url='https://github.com/vcancy/pysimplesoap',
    packages=['pysimplesoap'],
    license=__license__,
    # console=['client.py'],
    cmdclass={"py2exe": build_installer},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Communications",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
