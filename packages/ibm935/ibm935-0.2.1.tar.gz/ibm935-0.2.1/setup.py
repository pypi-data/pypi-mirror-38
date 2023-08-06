#!/usr/bin/env python
# encoding: utf-8

import sys
from setuptools import setup
from ibm935 import version

description = (
    "Supports encoding conversion between `unicode` and `ibm935` in Python"
)

if sys.version_info > (3, ):
    kw = {"encoding": "utf-8"}
else:
    kw = {}

with open("README.md", **kw) as f:
    long_description = f.read()

package_data = {
    "ibm935": ["data"],
}

classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

setup(
    name="ibm935",
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Eric Wong",
    author_email="ericwong@zju.edu.cn",
    url="https://github.com/littlefisher/ibm935",
    packages=["ibm935"],
    package_data=package_data,
    classifiers=classifiers,
)
