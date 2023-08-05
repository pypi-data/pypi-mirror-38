#!/usr/bin/env python

from setuptools import setup

with open('README.md') as f:
	long_description = f.read()

with open('requirements.txt', 'r') as f:
	required = f.read().splitlines()

setup(name='pycopula',
      version='0.1.2',
      description='Python copulas library for dependency modeling',
      author='Maxime Jumelle',
      author_email='maxime@aipcloud.io',
      license="Apache 2",
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/MaximeJumelle/pycopula/',
      install_requires=required
     )
