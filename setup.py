#!/usr/bin/env python
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

Build process :
- ask user what to do (zmq way in pip) 
- or parametrizes it 
    --dev : use local sources and cythonize way (for python-openzwave devs, ...)
    --embed : use local sources and cpp file (for third parties packagers, ...)
    --git : download openzwave from git (for geeks)
    --shared : use pkgconfig and cython (for debian devs and common users)
    --pybind : use pybind alternative (not tested)
    --auto (default) : try static, shared and cython, fails if it can't
"""
from os import name as os_name
import os, sys
import re
import shutil
import setuptools
from setuptools import setup, find_packages
from distutils.extension import Extension
from distutils import log
from distutils.command.install import install as _install
from distutils.command.build import build as _build
from distutils.command.clean import clean as _clean
from setuptools.command.bdist_egg import bdist_egg as _bdist_egg
from setuptools.command.develop import develop as _develop
import time
from platform import system as platform_system
import glob

from pyozw_version import pyozw_version
from pyozw_setup import LOCAL_OPENZWAVE, SETUP_DIR
from pyozw_setup import get_default_exts, cython_context, cpp_context, pybind_context, system_context, cython_context
from pyozw_setup import current_template, parse_template, get_dirs, data_files_config
from pyozw_setup import Template, DevTemplate, GitTemplate, EmbedTemplate, SharedTemplate
from pyozw_setup import bdist_egg, build_openzwave, build, clean, develop, install

print(current_template)
print(current_template.ctx)


setup(
  name = 'python_openzwave',
  author='Sébastien GALLET aka bibi2100 <bibi21000@gmail.com>',
  author_email='bibi21000@gmail.com',
  version = pyozw_version,
  zip_safe = False,
  url='https://github.com/OpenZWave/python-openzwave',
  cmdclass = {
        'build_ext': current_template.build_ext,
        'bdist_egg': bdist_egg,
        'build': build,
        'build_openzwave': build_openzwave,
        'clean': clean,
        'develop': develop,
        'install': install
        },
  ext_modules = [
        Extension(**current_template.ctx)
    ],
  #ext_modules = cythonize(ext_modules),
  package_dir = {'libopenzwave' : 'src-lib', 'openzwave' : 'src-api/openzwave'},
  #The following line install config drectory in share/python-openzwave
  #~ data_files = data_files,
  packages = find_packages('src-lib', exclude=["scripts"]) + find_packages('src-api', exclude=["scripts"]),
  install_requires = [ 'six' ],
  description = 'python_openzwave is a python wrapper for the openzwave c++ library.',
  long_description = 'A fullAPI to map the ZWave network in Python objects. Look at examples at : https://github.com/OpenZWave/python-openzwave',
  download_url = 'https://github.com/OpenZWave/python-openzwave/archive/v{0}.zip'.format(pyozw_version),
  keywords = ['openzwave', 'zwave'],
  classifiers = [
    "Topic :: Home Automation",
    "Topic :: System :: Hardware",
    "Topic :: System :: Hardware :: Hardware Drivers",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    "Operating System :: POSIX :: BSD",
    "Programming Language :: C++",
    "Programming Language :: Cython",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],

)
