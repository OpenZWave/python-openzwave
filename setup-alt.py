#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of **python-openzwave** project http://code.google.com/p/python-openzwave.
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
from distutils.core import setup
from Cython.Distutils import extension
from Cython.Distutils import build_ext
from platform import system as platform_system
import glob
import os

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

data_files = data_files_config('share/python-openzwave/config','openzwave/config','*.xml')
data_files.extend(data_files_config('share/python-openzwave/config','openzwave/config','*.xsd'))
data_files.extend(data_files_config('share/doc/python-openzwave','docs/_build/html','*.html'))
data_files.extend(data_files_config('share/doc/python-openzwave','docs/_build/html','*.js'))
data_files.extend(data_files_config('share/doc/python-openzwave','docs/_build/html','inv'))
data_files.extend(data_files_config('share/doc/python-openzwave','docs/_build/html','*.txt'))
data_files.extend(data_files_config('share/doc/python-openzwave','docs/_build/html','*.png'))
data_files.extend(data_files_config('share/doc/python-openzwave','docs/_build/html','*.css'))
data_files.extend(data_files_config('share/doc/python-openzwave','docs/_build/html','*.gif'))

cmdclass = { }
ext_modules = [ ]

if os_name == 'nt':
    ext_modules = [extension.Extension("libopenzwave", ["lib/libopenzwave.pyx"],
                             libraries=['setupapi', 'stdc++'],
                             language="c++",
                             extra_objects=['openzwave/cpp/lib/windows-mingw32/libopenzwave.a'],
                             include_dirs=['openzwave/cpp/src', 'openzwave/cpp/src/value_classes', 'openzwave/cpp/src/platform', 'openzwave/cpp/build/linux']
    )]
elif platform_system() == 'Darwin':
    ext_modules += [Extension("libopenzwave", ["lib/libopenzwave.pyx"],
                             libraries=['stdc++'],
                             language="c++",
                             extra_link_args=['-framework', 'CoreFoundation', '-framework', 'IOKit'],
                             extra_objects=['openzwave/cpp/lib/mac/libopenzwave.a'],
                             include_dirs=['openzwave/cpp/src', 'openzwave/cpp/src/value_classes', 'openzwave/cpp/src/platform', 'openzwave/cpp/build/linux']
    )]
else:
    ext_modules = [extension.Extension("libopenzwave", ["lib/libopenzwave.pyx"],
                             libraries=['udev', 'stdc++'],
                             language="c++",
                             extra_objects=['openzwave/cpp/lib/linux/libopenzwave.a'], 
                             include_dirs=['openzwave/cpp/src', 'openzwave/cpp/src/value_classes', 'openzwave/cpp/src/platform', 'openzwave/cpp/build/linux']
    )]

setup(
  name = 'python-openzwave',
  author='Sébastien GALLET aka bibi2100 <bibi21000@gmail.com>',
  author_email='bibi21000@gmail.com',
  url='http://code.google.com/p/python-openzwave',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules,
  package_dir = {'libopenzwave' : 'lib', 'openzwave' : 'src'},
  #The following line install config drectory in share/python-openzwave
  data_files = data_files,
  packages = ['libopenzwave','openzwave']
)
