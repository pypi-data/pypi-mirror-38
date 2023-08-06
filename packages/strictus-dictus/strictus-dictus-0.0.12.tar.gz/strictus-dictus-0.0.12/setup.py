#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="strictus-dictus",
    version="0.0.12",
    url="https://github.com/jbasko/strictus-dictus",
    license="MIT",
    author="Jazeps Basko",
    author_email="jazeps.basko@gmail.com",
    maintainer="Jazeps Basko",
    maintainer_email="jazeps.basko@gmail.com",
    description="Strictus Dictus",
    keywords="dictionary schema attribute attrdict type hinting typing annotations",
    long_description=read("README.rst"),
    py_modules=["strictus_dictus"],
    python_requires=">=3.6.0",
    install_requires=[
        "typing_inspect",
    ],
    extras_require={
        ':python_version=="3.6"': [
            "dataclasses",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
)
