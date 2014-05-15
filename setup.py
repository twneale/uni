#!/usr/bin/env python
from setuptools import setup, find_packages


long_description = 'Unit tests for data!'

setup(name='uni',
      version='0.0',
      packages=find_packages(),
      author='Thom Neale',
      author_email='twneale@gmail.com',
      url='http://github.com/twneale/uni',
      description='Execute mongo-style queries on dictionaries.',
      long_description=long_description,
      platforms=['any'],
      install_requires=[
          'nmmd',
      ],
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3.4"]
)
