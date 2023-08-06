#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import sys

version = sys.argv[-1]
sys.argv = sys.argv[:-1]

with open('poker_stats/ver.py', 'w') as f_h:
    f_h.write('ver = \'{}\'\n'.format(version))

setuptools.setup(name='poker_stats',
      version=version,
      author='Michal Nowak and Damian Szuberski for Polish Poker Community in Manila',
      author_email='dev@null.com',
      url='https://github.com/yarpenzigrin/pokerstats',
      description='Statistics generator for poker hands played online',
      long_description='Statistics generator for poker hands played online',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7'],
      keywords='poker holdem stats statistics',
      license='MIT',
      packages=setuptools.find_packages(exclude=['test', 'test.ut']),
      entry_points={'console_scripts':['poker_stats = poker_stats:main']},
      python_requires='>=3.7',
      install_requires=['pyparsing>=2.3.0']
)
