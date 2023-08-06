#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys


setup(
    name="life_game",
    version="1.2.0",
    author="Memory",
    author_email="memory_d@foxmail.com",
    description="life game",
    long_description="life game written by pygame",
    license="MIT",
    url="https://github.com/MemoryD/life_game",
    packages=['life_game'],
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