# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="word-embedder",
    version="1.0.0",
    description="Word Embedder",
    license="MIT",
    author="Solumilken",
    packages=find_packages(),
    install_requires=[
        "mkdir-p>=0.1.1",
        "numpy>=1.15.1",
        "python-dotenv==0.9.1",
    ],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
)
