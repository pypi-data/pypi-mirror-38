#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the tangoctl project
#
# Copyright (c) 2018 Tiago Coutinho
# Distributed under the MIT license. See LICENSE for more info.

"""The setup script."""

from setuptools import setup, find_packages

def get_rst(name='README.rst'):
    """Get readme file contents without the badges."""
    with open(name) as f:
        return '\n'.join(
            line for line in f.read().splitlines()
            if not line.startswith('|') or not line.endswith('|'))

readme = get_rst()
history = get_rst(name='HISTORY.rst')

requirements = ['pytango', 'click', 'treelib', 'gevent', 'tabulate', 'six']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', 'pytest-cov']

setup(
    author="Jose Tiago Macara Coutinho",
    author_email='coutinhotiago@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 3',
    ],
    description="tango system cli manager",
    entry_points={
        'console_scripts': [
            'tangoctl = tangoctl.cli:cli',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='tangoctl',
    name='tangoctl',
    packages=find_packages(include=['tangoctl']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/tiagocoutinho/tangoctl',
    version='0.2.1',
    zip_safe=False,
)
