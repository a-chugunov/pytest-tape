#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-tape',
    version='0.1.0',
    author='Alexey Chugunov',
    author_email='alexey@chugunov.dev',
    maintainer='Alexey Chugunov',
    maintainer_email='alexey@chugunov.dev',
    license='MIT',
    url='https://github.com/a-chugunov/pytest-tape',
    description='easy assertion with expected results saved to yaml files',
    long_description=read('README.rst'),
    py_modules=['pytest_tape'],
    python_requires='>=3.5',
    install_requires=['pytest>=6.2.2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'tape = pytest_tape',
        ],
    },
)
