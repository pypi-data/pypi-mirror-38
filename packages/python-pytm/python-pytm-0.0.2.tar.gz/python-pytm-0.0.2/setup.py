#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://PyTM.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='python-pytm',
    version='0.0.2',
    description='PyTM - an Open Source Python Time Management Tool for Mankind',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Wasi Mohammed Abdullah',
    author_email='wasi0013@gmail.com',
    url='https://github.com/wasi0013/PyTM',
    packages=[
        'PyTM',
    ],
    package_dir={'python-pytm': 'PyTM'},
    include_package_data=True,
    install_requires=[
        'click',

    ],
    license='MIT',
    zip_safe=False,
    keywords='PyTM',
    entry_points={
        'console_scripts': ['pytm=PyTM.cli:cli'],
    }
    ,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],


)
