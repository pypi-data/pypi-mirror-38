#!/usr/bin/env python

from setuptools import setup

# This needs to have the following format - see Makefile 'upload' target.
VERSION = '1.0.2'

setup(name='phylo-color',
      version=VERSION,
      include_package_data=False,
      url='https://github.com/acorg/phylo-color',
      download_url='https://github.com/acorg/phylo-color',
      author='Terry Jones',
      author_email='tcj25@cam.ac.uk',
      keywords=['phylogenetic tree color nexml nexus newick'],
      classifiers=[
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      license='MIT',
      scripts=['phylo-color.py'],
      description=('Color the nodes of a phylogenetic tree using regular '
                   'expressions to match taxa names.'),
      install_requires=[
          'dendropy',
      ],
      extras_require={
        'dev': [
            'flake8',
            'pytest',
        ]
      })
