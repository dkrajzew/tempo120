# ===================================================================
# tempo120 - A party car racing game.
#
# Setup module
#
# (c) Daniel Krajzewicz 2023
# daniel@krajzewicz.de
# - https://github.com/dkrajzew/tempo120
# - https://dkrajzew.itch.io/tempo120
# - http://www.krajzewicz.de
#
# Available under the GPLv3 license.
# ===================================================================



# --- imports -------------------------------------------------------
import setuptools


# --- definitions ---------------------------------------------------
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tempo120",
    version="1.0.2",
    author="dkrajzew",
    author_email="d.krajzewicz@gmail.com",
    description="A party car racing game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://dkrajzew.itch.io/tempo120',
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

