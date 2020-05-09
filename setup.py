# -*- encoding: utf-8 -*-
#
#    PyNomo - nomographs with Python
#    Copyright (C) 2007- 2020  Leif Roschier
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
""" PyNomo - nomographs or nomograms with Python

Pynomo is a program to create (pdf) nomographs (nomograms)
using Python interpreter. A nomograph (nomogram) is a graphical
solution to an equation.
"""
# example from: https://github.com/pypa/sampleproject/blob/master/setup.py
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='PyNomo',
      version='0.3.3',
      description='PyNomo - Python Nomograms',
      long_description=long_description,
      author='Leif Roschier',
      author_email='lefakkomies@users.sourceforge.net',
      url='http://pynomo.org/',
      download_url='https://github.com/lefakkomies/pynomo',
      packages=['pynomo'],
      license='GPL',
      platforms='OS Independent',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Topic :: Scientific/Engineering :: Visualization',
          'Topic :: Multimedia :: Graphics',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Programming Language :: Python',
      ],
      keywords='nomograph nomogram graphics calculator visualization',
      # install numpy, scipy, pyx and latex manually :(
      #install_requires=['numpy', 'scipy'],  # have to install pyx and tex/latex manually
      )
