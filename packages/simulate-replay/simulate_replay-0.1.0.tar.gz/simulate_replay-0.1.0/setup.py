#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

INSTALL_REQUIRES = ['numpy >= 1.14', 'scipy', 'pandas', 'matplotlib']
TESTS_REQUIRE = ['pytest >= 2.7.1']

setup(
        name='simulate_replay',
        version='0.1.0',
        license='MIT',
        description=('Simulate replay dataset'),
        author='Eric Denovellis',
        author_email='edeno@bu.edu',
        packages=find_packages(),
        install_requires=INSTALL_REQUIRES,
        tests_require=TESTS_REQUIRE,
        url='https://github.com/Eden-Kramer-Lab/simulate_replay',
      )
