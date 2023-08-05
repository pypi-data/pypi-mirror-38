#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Install the "polevault" package and CLI command.'''


from __future__ import print_function, division

from setuptools import setup, find_packages


VERSION = '0.1.4'

setup(
    name='polevault',
    version=VERSION,
    author='Paulo Lopes',
    author_email='palopes@cisco.com',
    url='https://paulopes.github.io/polevault/',
    description='Encrypts and decrypts credentials',
    long_description='''\
Encrypts and decrypts credentials, stores them
in a .ini, .conf, .json, .yml, or .yaml file,
and can decrypt them into Hashicorp's Vault.
''',
    packages=find_packages(exclude=[
        "*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        'click',
        # It can use pyyaml if installed, but it does not require it, but it
        # needs either cryptography or pycryptodome, whichever is available.
        # It also will need hvac if decrypting into Hashicorp's Vault.
    ],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'polevault = polevault:cli',
        ]
    },
)
