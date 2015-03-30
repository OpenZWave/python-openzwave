#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of **python-openzwave** project https://github.com/bibi21000/python-openzwave.
    :platform: Unix, Windows, MacOS X

.. moduleauthor:: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>

License : GPL(v3)

**python-openzwave** is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

**python-openzwave** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with python-openzwave. If not, see http://www.gnu.org/licenses.

"""
from setuptools import setup, find_packages
import glob
import os
import sys
from pyozw_version import pyozw_version

DEBIAN_PACKAGE = False
filtered_args = []

for arg in sys.argv:
    if arg == "--debian-package":
        DEBIAN_PACKAGE = True
    else:
        filtered_args.append(arg)
sys.argv = filtered_args

setup(
  name = 'pyozwman',
  author='Sébastien GALLET aka bibi2100 <bibi21000@gmail.com>',
  author_email='bibi21000@gmail.com',
  url='https://github.com/bibi21000/python-openzwave',
  #Need to update libopenzwave.pyx too
  version = pyozw_version,
  zip_safe = False,
  package_dir = {'' : 'src-manager' },
  packages = find_packages('src-manager', exclude=["scripts"]),
#The following line install config drectory in share/python-openzwave
  install_requires=[ "urwid >= 1.1.1", 'openzwave == %s' % pyozw_version ]
)
