#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') as readme_file, \
    open('HISTORY.rst', encoding='utf-8') as history_file:
    long_description = (readme_file.read() + "\n\n" + history_file.read())

install_requires = [
    'click>=6.0',
    'PyYAML',
]

setup_requires = [
    'pytest-runner',
    # TODO(starofrainnight): put setup requirements (distutils extensions, etc.) here
]

tests_requires = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='shotatlogging',
    version='0.1.1',
    description="Provide simple way to initialize logging module with default environment",
    long_description=long_description,
    author="Hong-She Liang",
    author_email='starofrainnight@gmail.com',
    url='https://github.com/starofrainnight/shotatlogging',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    license="Apache Software License",
    zip_safe=False,
    keywords='shotatlogging',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=tests_requires,
    setup_requires=setup_requires,
)
