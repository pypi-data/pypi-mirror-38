#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="mxgames",
    version="1.0.2",
    author="Memory&Xinxin",
    author_email="memory_d@foxmail.com",
    description="free python games written by pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/MemoryD/mxgames",
    packages=find_packages(),
    install_requires=[
        "pygame <= 1.9.5",
        ],
    classifiers=[
        "Topic :: Games/Entertainment ",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)