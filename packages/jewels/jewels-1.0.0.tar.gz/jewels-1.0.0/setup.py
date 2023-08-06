#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.md','r') as f:
    long_description = f.read()

setup(
      name='jewels',
      version='1.0.0',
      description='Secure file encryption and data access',
      author='andrea capitanelli',
      author_email='andrea.capitanelli@gmail.com',
      maintainer='andrea capitanelli',
      maintainer_email='andrea.capitanelli@gmail.com',
      url='https://github.com/vegaviz/jewels',
      packages=['jewels'],
      install_requires=[
          'pycryptodome >=3.7, <4',
      ],
      package_dir={'jewels': 'jewels'},
      long_description=long_description,
      keywords='file encryption cli key aes256 eax',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Topic :: Security :: Cryptography'
     ],
     scripts=['bin/jewels-cli'],
)
