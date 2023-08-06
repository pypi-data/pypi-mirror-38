#!/usr/bin/env python
# encoding: utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys

version = "0.1.4"
description = (
    "Supports encoding conversion between `unicode` and `ibm935` in Python"
)

if sys.version_info > (3, ):
    kw = { "encoding": "utf-8" }
else:
    kw = {}

with open("README.md", **kw) as f:
    long_description = f.read()

classifiers = [
    "Development Status :: 3 - Alpha",
    "Programming Language :: Python",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

setup(
    name="ibm935",
    version=version,
    description=description,
    long_description=long_description,
    license="MIT",
    author="Eric Wong",
    author_email="ericwong@zju.edu.cn",
    url="https://github.com/littlefisher/ibm935",
    classifiers=classifiers,
    py_modules=['ibm935'],
)
