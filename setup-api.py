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
from os import name as os_name
#from distutils.core import setup
from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from platform import system as platform_system
import glob
import os
import sys

if sys.hexversion >= 0x3000000:
    dispatch_package = 'pydispatcher >= 2.0.5'
else:
    dispatch_package = 'Louie >= 1.1'

DEBIAN_PACKAGE = False
filtered_args = []

for arg in sys.argv:
    if arg == "--debian-package":
        DEBIAN_PACKAGE = True
    else:
        filtered_args.append(arg)
sys.argv = filtered_args

def _getDirs(base):
    return [x for x in glob.iglob(os.path.join( base, '*')) if os.path.isdir(x) ]

def data_files_config(target, source, pattern):
    ret = list()
    tup = list()
    tup.append(target)
    tup.append(glob.glob(os.path.join(source,pattern)))
    #print tup
    ret.append(tup)
    dirs = _getDirs(source)
    if len(dirs):
        for d in dirs:
            #print os.path.abspath(d)
            rd = d.replace(source+os.sep, "", 1)
            #print target,rd
            #print os.path.join(target,rd)
            ret.extend(data_files_config(os.path.join(target,rd), \
                os.path.join(source,rd), pattern))
    return ret

data_files = data_files_config('share/doc/python-openzwave','docs/_build/html','*.html')
data_files.extend(data_files_config('share/doc/python-openzwave','docs/_build/html','*.js'))
data_files.extend(data_files_config('share/doc/python-openzwave','docs/_build/html','inv'))
data_files.extend(data_files_config('share/doc/python-openzwave','docs/_build/html','*.txt'))
data_files.extend(data_files_config('share/doc/python-openzwave','docs/_build/html','*.png'))
data_files.extend(data_files_config('share/doc/python-openzwave','docs/_build/html','*.css'))
data_files.extend(data_files_config('share/doc/python-openzwave','docs/_build/html','*.gif'))

setup(
  name = 'python-openzwave-api',
  author='Sébastien GALLET aka bibi2100 <bibi21000@gmail.com>',
  author_email='bibi21000@gmail.com',
  url='https://github.com/bibi21000/python-openzwave',
  #Need to update libopenzwave.pyx too
  version = '0.2.6',
  package_dir = {'openzwave' : 'api', 'pyozwman' : 'manager' },
  #The following line install config drectory in share/python-openzwave
  data_files = data_files,
  packages = ['openzwave', 'pyozwman' ],
  install_requires=[ 'nose >= 0.8.3', dispatch_package ]
)
