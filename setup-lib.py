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

"""
from os import name as os_name
import os, sys
import re
from setuptools import setup, find_packages
from distutils.extension import Extension
if os.path.isdir(os.path.join(os.getcwd(), '.git')):
    #Install from git
    from Cython.Distutils import build_ext
else:
    #Install from archive
    from distutils.command.build_ext import build_ext
from platform import system as platform_system
import glob
import subprocess

from pyozw_version import pyozw_version

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

def pkg_config_cflags_ozw():
    p = subprocess.Popen('pkg-config --cflags libopenzwave', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        try:
            #python 2
            return line.replace('\n', '')
        except TypeError:
            #python 3
            return line.decode("utf-8").replace('\n', '')
            #~ return re.sub('\n', '', str(line))

def pkg_config_libs_ozw():
    p = subprocess.Popen('pkg-config --libs libopenzwave', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        try:
            #python 2
            return line.replace('\n', '')
            #~ return re.sub(r'\n', '', line)
        except TypeError:
            #python 3
            return line.decode("utf-8").replace('\n', '')
            #~ return re.sub('\n', '', str(line))

def pkg_config_ozw():
    flags = pkg_config_cflags_ozw()
    libs = pkg_config_libs_ozw()
    return [ libs, flags] + [ flags.replace('//', '/%s/' % ndir) for ndir in ['aes', 'command_classes', 'platform', 'value_classes'] ]
    #~ return [ libs, flags] + [ re.sub(r'//', '/%s/' % ndir, flags) for ndir in ['aes', 'command_classes', 'platform', 'value_classes'] ]
    

def data_files_config(target, source, pattern):
    ret = list()
    tup = list()
    tup.append(target)
    tup.append(glob.glob(os.path.join(source,pattern)))
    ret.append(tup)
    dirs = _getDirs(source)
    if len(dirs):
        for d in dirs:
            rd = d.replace(source+os.sep, "", 1)
            ret.extend(data_files_config(os.path.join(target,rd), \
                os.path.join(source,rd), pattern))
    return ret

data_files = data_files_config('config','openzwave/config','*.xml')
data_files.extend(data_files_config('config','openzwave/config','*.xsd'))

cmdclass = { }
ext_modules = [ ]

if platform_system() == 'Windows':
    ext_modules = [Extension("libopenzwave",
                             sources=["src-lib/libopenzwave/libopenzwave.pyx"],
                             libraries=['setupapi', 'msvcrt', 'ws2_32', 'dnsapi'],
                             language="c++",
                             extra_objects=['openzwave/cpp/build/windows/vs2010/Release/openzwave.lib'],
                             include_dirs=['openzwave/cpp/src', 'openzwave/cpp/src/value_classes', 'openzwave/cpp/src/platform', 'openzwave/cpp/build/windows', "src-lib/libopenzwave"]
    )]
elif platform_system() == 'Darwin':
    ext_modules = [Extension("libopenzwave",
                             sources=["src-lib/libopenzwave/libopenzwave.pyx"],
                             libraries=['stdc++'],
                             language="c++",
                             extra_link_args=['-framework', 'CoreFoundation', '-framework', 'IOKit'],
                             extra_objects=['openzwave/libopenzwave.a'],
                             include_dirs=['openzwave/cpp/src', 'openzwave/cpp/src/value_classes', 'openzwave/cpp/src/platform', 'openzwave/cpp/build/mac', "src-lib/libopenzwave"]
    )]
elif platform_system() == 'FreeBSD':
    ext_modules = [Extension("libopenzwave",
                             sources=["src-lib/libopenzwave/libopenzwave.pyx"],
                             libraries=['usb', 'stdc++'],
                             language="c++",
                             define_macros=[
                                 ('PY_SSIZE_T_CLEAN',1),
                             ],
                             extra_objects=['openzwave/libopenzwave.a'],
                             include_dirs=['openzwave/cpp/src/', 'openzwave/cpp/src/value_classes/', 'openzwave/cpp/src/platform/', 'openzwave/cpp/build/linux/']
    )]
elif DEBIAN_PACKAGE == True:
    #For linux dynamic
    ext_modules = [Extension("libopenzwave",
                             sources=["src-lib/libopenzwave/libopenzwave.pyx"],
                             libraries=['udev', 'stdc++'],
                             language="c++",
                             define_macros=[
                                 ('PY_SSIZE_T_CLEAN',1),
                             ],
                             #extra_objects=['/usr/libopenzwave.a'],
                             extra_compile_args=pkg_config_ozw(),
                             #~ include_dirs=['/usr/include/openzwave', '/usr/include/openzwave/value_classes', '/usr/include/openzwave/platform', "src-lib/libopenzwave"],
    )]
else:
    #For linux static
    ext_modules = [Extension("libopenzwave",
                             sources=["src-lib/libopenzwave/libopenzwave.pyx"],
                             libraries=['udev', 'stdc++'],
                             language="c++",
                             define_macros=[
                                 ('PY_SSIZE_T_CLEAN',1),
                             ],
                             extra_objects=['openzwave/libopenzwave.a'],
                             include_dirs=['openzwave/cpp/src/', 'openzwave/cpp/src/value_classes/', 'openzwave/cpp/src/platform/', 'openzwave/cpp/build/linux/']
    )]

setup(
  name = 'libopenzwave',
  author='Sébastien GALLET aka bibi2100 <bibi21000@gmail.com>',
  author_email='bibi21000@gmail.com',
  version = pyozw_version,
  zip_safe = False,
  url='https://github.com/OpenZWave/python-openzwave',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules,
  #ext_modules = cythonize(ext_modules),
  package_dir = {'' : 'src-lib'},
  #The following line install config drectory in share/python-openzwave
  data_files = data_files,
  packages = find_packages('src-lib', exclude=["scripts"]),
  install_requires=[
                     'six',
                    ]
)
