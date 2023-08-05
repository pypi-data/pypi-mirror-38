#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from glob import glob

from os.path import (
    basename,
    splitext
)

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup(
    name='py-stac',
    version='0.2.6',
    description=(
        "Python command line and library utilities for interacting"
        "with and creating STAC compliant files."
    ),
    long_description=readme + '\n\n' + history,
    author="Geobeyond",
    author_email='info@geobeyond.it',
    url='https://github.com/geobeyond/py-stac',
    packages=find_packages(),
    py_modules=[splitext(basename(path))[0] for path in glob('stac/*.py')],
    entry_points={
        'console_scripts': [
            'stac=stac.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=[
        'python-dateutil==2.6.1',
        'rasterio==1.0a12',
        'Click>=6.0',
        'geojson==2.3.0',
        'requests>=2.18.0',
        'marshmallow>=3.0.0b12',
        'typing==3.6.2;python_version<="3.6"'
    ],
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords=[
        'pystac',
        'py-stac',
        'imagery',
        'raster',
        'catalog',
        'STAC'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests'
)
