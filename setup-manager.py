#!env python
# -*- coding: utf-8 -*-
"""
This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
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
import pyozw_version 

setup(
  name = 'pyozwman',
  author='Sébastien GALLET aka bibi2100 <bibi21000@gmail.com>',
  author_email='bibi21000@gmail.com',
  url='https://github.com/OpenZWave/python-openzwave',
  version = pyozw_version.pyozw_version,
  zip_safe = False,
  scripts=['src-manager/scripts/pyozw_shell'],
  package_dir = {'' : 'src-manager' },
  packages = find_packages('src-manager', exclude=["scripts"]),
  install_requires=pyozw_version.install_requires() + [ "urwid>=1.1.1"],
)
