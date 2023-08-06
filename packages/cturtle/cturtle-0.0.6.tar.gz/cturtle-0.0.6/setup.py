#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages
import cturtle

setup(
    name = "cturtle",
    version = cturtle.__version__,
    packages = find_packages(),
    author = "Valentin Niess",
    author_email = "valentin.niess@gmail.com",
    description = "A ctypes interface to the TURTLE library",
    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",
    include_package_data = True,
    url = "https://github.com/niess/turtle-python",
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Physics",
    ]
)
