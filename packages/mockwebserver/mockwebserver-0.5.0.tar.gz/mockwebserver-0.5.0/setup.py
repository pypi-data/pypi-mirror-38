#!/usr/bin/env python

import os

from setuptools import find_packages, setup

long_description = 'Please see our GitHub README'
if os.path.exists('README.md'):
    long_description = open('README.md').read()

setup(
    name='mockwebserver',
    version='0.5.0',
    description='A simple web server for unit testing purposes. Acts as context manager for teardown.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Virtualstock',
    author_email='dev.admin@virtualstock.com',
    url='https://github.com/Virtualstock/mockwebserver',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'attrs',
        'wsgi-intercept==1.5.1',
        'requests',
    ],
    test_suite='tests',
)
