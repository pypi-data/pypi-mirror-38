
config = {
  "name": "bf",
  "version": "1.9.0",
  "description": "File interface library",
  "url": "https://github.com/BlackEarth/bf",
  "author": "Sean Harrison",
  "author_email": "sah@bookgenesis.com",
  "license": "MPL 2.0",
  "classifiers": [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
    "Programming Language :: Python :: 3"
  ],
  "entry_points": {},
  "install_requires": ["bl", "unum", "cssselect", "cssutils", "libsass"],
  "extras_require": {
    "dev": [],
    "test": []
  },
  "package_data": {
    "bf": []
    },
  "data_files": [],
  "scripts": []
}


import os
from setuptools import setup, find_packages
from codecs import open

path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(path, 'README.md'), encoding='utf-8') as f:
    read_me = f.read()

setup(
    long_description=read_me,
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    **config
)
