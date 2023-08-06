#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ansible-tests',
    version='0.0.1',
    author="Tanguy Patte",
    url="https://github.com/TanguyPatte/ansible-tests.git",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["*_tests"]),
    install_requires=[
        'click',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'ansible_tests = ansible_tests.__main__:run',
        ],
    },
)
