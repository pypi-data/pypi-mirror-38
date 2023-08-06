#!/usr/bin/env python

from setuptools import setup, find_packages

description = "Python SDK for Bhex REST API (https://www.bhex.com)"

setup(
    name="bhex",
    version="0.0.1",
    author="Bhex",
    author_email="support@bhex.com",
    description=description,
    url="https://github.com/bhexopen/BHEX-OpenApi/tree/master/sdk/python",
    packages=find_packages(),
    install_requires=['requests', 'six'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)