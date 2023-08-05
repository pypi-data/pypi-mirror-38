# !/usr/bin/env python
# encoding: utf-8

import os

from setuptools import find_packages, setup

NAME = 'ernest'
DESCRIPTION = 'A CLI-based tool for making bulk changes to file text.'
URL = 'https://github.com/alycejenni/ernest'
EMAIL = 'alycejenni@gmail.com'
AUTHOR = 'Alice Butcher'
VERSION = '0.1.4'

REQUIRED = ['click', 'redbaron']

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'),
          encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    package_data={
        'ernest': ['data/ernest.json']
        },
    include_package_data=True,
    entry_points='''
        [console_scripts]
        ernest=ernest.cli:cli
    ''',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities'
        ]
    )
