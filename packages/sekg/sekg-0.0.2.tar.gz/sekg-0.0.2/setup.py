#!/usr/bin/env python
# -*- coding:utf-8 -*-

from os.path import dirname, join as path_join

from setuptools import setup, find_packages

from sekg.meta import __author__, __email__, __license__, __package__, __version__

packages = find_packages(exclude=("docs", "test"))

with open(path_join(dirname(__file__), "README.md")) as f:
    README = f.read()

setup(
    name=__package__,
    version=__version__,
    keywords=("pip", "kg", "se"),
    description="knowledge graph util for software engineering",
    long_description=README,
    license=__license__,

    url="https://github.com/FudanSELab/sekg",
    author=__author__,
    author_email=__email__,

    packages=packages,
    include_package_data=True,
    platforms="any",
    install_requires=[
        "py2neo>=4.1.0"
    ]
)
