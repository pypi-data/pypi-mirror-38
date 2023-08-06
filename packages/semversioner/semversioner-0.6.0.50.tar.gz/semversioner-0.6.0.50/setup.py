#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:copyright: (c) 2018 by Raul GOmis
:license: MIT, see LICENSE for more details.
"""
import io
import os

from setuptools import setup, find_packages


VERSION = "0.6.0." + os.getenv('BITBUCKET_BUILD_NUMBER', 0)

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name='semversioner',
    version=VERSION,
    description='Manager properly semver in your repository',
    long_description=readme,
    tests_require=['nose'],
    url='https://bitbucket.org/rgomish/versioner',
    author='Raul Gomis',
    author_email='rgomis@atlassian.com',
    license='MIT',
    packages=find_packages(exclude=['tests*']),

    entry_points={
        'console_scripts': [
            'semversioner = semversioner.__main__:main'
        ]
    },

    install_requires=[
        'click'
    ],
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Environment :: Console',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',

        'Topic :: Software Development :: Libraries :: Python Modules',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',

        'Operating System :: OS Independent',

    ]
)