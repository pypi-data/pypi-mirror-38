#
# This file is part of the Fonolo Python Wrapper package.
#
# (c) Foncloud, Inc.
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='fonolo',
    version='1.0.1',
    description='A Python wrapper for the Fonolo Call-Back Service',
    author='Mike Pultz',
    author_email='mike@fonolo.com',
    url='https://fonolo.com/',
    license='MIT',
    install_requires=[
        'requests >= 2.1.0',
        'six >= 1.9.0'
    ],
    packages=[
        'fonolo',
        'fonolo.api',
        'fonolo.exception'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
