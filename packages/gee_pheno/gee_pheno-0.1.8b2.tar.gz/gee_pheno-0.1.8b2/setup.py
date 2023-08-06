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

requirements = [
    'earthengine-api',
    'daiquiri',
    'pandas'
]

setup_requirements = [
    'pytest-runner',
    'earthengine-api',
    'daiquiri',
    'pandas'
]

test_requirements = ['pytest', ]
setup(
    author="Francesco Bartoli",
    author_email='francesco.bartoli@geobeyond.it',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="GEE phenology",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='gee_pheno',
    name='gee_pheno',
    packages=find_packages(),
    py_modules=[splitext(basename(path))[0] for path in glob('gee_pheno/*.py')],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/francbartoli/gee_pheno',
    version='0.1.8b2',
    zip_safe=False,
)
