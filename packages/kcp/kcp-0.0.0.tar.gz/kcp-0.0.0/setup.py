#!/usr/bin/env python

from setuptools import setup, find_packages

from kcp import __version__

setup(
    name='kcp',
    version=__version__,
    description='Python Implements of KCP Protocol',
    url='https://github.com/goawm/kcp-py',
    author='gozssky',
    author_email='xiayjchn@gmail.com',
    packages=find_packages(),
)
