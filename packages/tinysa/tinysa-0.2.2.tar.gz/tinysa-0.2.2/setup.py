#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    author="Jun Harashima",
    author_email='j.harashima@gmail.com',
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
        'Programming Language :: Python :: 3.7',
    ],
    description="Minimal implementation for constructing a suffix array",
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='tiny suffix array',
    name='tinysa',
    packages=find_packages(include=['tinysa']),
    test_suite='tests',
    url='https://github.com/jun-harashima/tinysa',
    version='0.2.2',
    zip_safe=False,
)
