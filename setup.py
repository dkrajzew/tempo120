#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ===========================================================================
"""tempo120 - Setup module."""
# ===========================================================================
__author__     = "Daniel Krajzewicz"
__copyright__  = "Copyright 2023-2024, Daniel Krajzewicz"
__credits__    = ["Daniel Krajzewicz"]
__license__    = "GPL 3.0"
__version__    = "1.8.0"
__maintainer__ = "Daniel Krajzewicz"
__email__      = "daniel@krajzewicz.de"
__status__     = "Production"
# ===========================================================================
# - https://github.com/dkrajzew/tempo120
# - http://www.krajzewicz.de
# ===========================================================================



# --- imports ---------------------------------------------------------------
import setuptools


# --- definitions -----------------------------------------------------------
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
ib = long_description.find("imgs begin")
ie = long_description.find("imgs end")
if ib>=0 and ie>=0:
    long_description = long_description[:ib] + long_description[ie:]

setuptools.setup(
    name="tempo120",
    version="1.8.0",
    author="dkrajzew",
    author_email="d.krajzewicz@gmail.com",
    description="A party car racing game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/dkrajzew/tempo120',
    download_url='http://pypi.python.org/pypi/tempo120',
    project_urls={
        'Source': 'https://github.com/dkrajzew/tempo120',
        'Tracker': 'https://github.com/dkrajzew/tempo120/issues',
        'Discussions': 'https://github.com/dkrajzew/tempo120/discussions',
    },
    license='GPLv3',
    # add modules
    py_modules = ['tempo120'],
    packages = ['gfx','muzak','scores'],
    package_data = {
        'gfx': ['*'],
        'muzak': ['*'],
        'scores': ['*']
    },
    entry_points = {
        'console_scripts': [
            'tempo120 = tempo120:main'
        ]
    },
    install_requires = [ "pygame==2.6.0" ],
    # see https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment"
    ],
    python_requires='>=2.7, <4',
)

