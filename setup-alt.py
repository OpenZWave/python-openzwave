#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import name as os_name
from distutils.core import setup
from Cython.Distutils import extension
from Cython.Distutils import build_ext

if os_name == 'nt':
    ext_modules = [extension.Extension("libopenzwave", ["lib/libopenzwave.pyx"],
                             libraries=['setupapi', 'stdc++'],
                             language="c++",
                             extra_objects=['openzwave/cpp/lib/windows-mingw32/libopenzwave.a'],
                             include_dirs=['openzwave/cpp/src', 'openzwave/cpp/src/value_classes', 'openzwave/cpp/src/platform']
    )]    
else:
    ext_modules = [extension.Extension("libopenzwave", ["lib/libopenzwave.pyx"],
                             libraries=['udev', 'stdc++'],
                             language="c++",
                             extra_objects=['openzwave/cpp/lib/linux/libopenzwave.a'], 
                             include_dirs=['openzwave/cpp/src', 'openzwave/cpp/src/value_classes', 'openzwave/cpp/src/platform']
    )]

setup(
  name = 'python-openzwave',
  author='Sébastien GALLET aka bibi2100 <bibi21000@gmail.com>',
  author_email='bibi21000@gmail.com',
  url='http://code.google.com/p/python-openzwave',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)
