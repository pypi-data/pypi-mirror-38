#! usr/bin/env python3

from setuptools import setup

setup(name='POSST',
      version='0.1.0',
      description='Module for the POSST project',
      url='https://github.com/tognotommy/POSST',
      author='Matteo Caruso, Tommaso Tognozzi',
      author_email='matteo1.caruso@mail.polimi.it, tommaso.tognozzi@mail.polimi.it',
      license='LICENSE.txt',
      packages=['POSST'],
      long_description=open('README.rst').read(),
      install_requires=[
      		'astropy',
      		'numpy',
      		'astride',
      		'spiceypy',
      		'sgp4'],
      zip_safe=False)