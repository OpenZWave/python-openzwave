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
  name = 'pyozwweb',
  author='Sébastien GALLET aka bibi2100 <bibi21000@gmail.com>',
  author_email='bibi21000@gmail.com',
  url='https://github.com/bibi21000/python-openzwave',
  version = pyozw_version,
  zip_safe = False,
  package_dir = {'' : 'src-web' },
  packages = find_packages('src-web', exclude=["scripts"]),
  install_requires = [
                     'openzwave == %s' % pyozw_version,
                     'Flask == 0.10.1',
                     'Flask-WTF == 0.9.5',
                     'Babel >= 1.0',
                     'Flask-Babel == 0.9',
                     'Flask-Fanstatic == 0.2.0',
                     'fanstatic',
                     #'js.bootstrap >= 3.3.1',
                     'js.jquery >= 1.9.1',
                     #'js.jquery_timepicker_addon >= 1.3',
                     'js.jquery_datatables >= 1.10',
                     'Flask-Themes >= 0.1.3',
                     'WebOb >= 1.4',
                     'Jinja2 >= 2.5.5',
                     'gevent-socketio >= 0.3.6',
                     'Flask-SocketIO >= 0.6.0',
                     'js.socketio < 1.0.0',
                     'PyYAML>= 3.10',
                    ],
  #include_package_data=True,
  package_data={
    'pyozwweb': ['app/static/*/*', 'app/templates/*', 'app/templates/*/*'],
  },
)
