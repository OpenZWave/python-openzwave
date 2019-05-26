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

from setuptools import setup
from distutils.extension import Extension
from pyozw_version import pyozw_version
from pyozw_setup import LOCAL_OPENZWAVE, SETUP_DIR
from pyozw_setup import current_template, parse_template, get_dirs, data_files_config, install_requires
from pyozw_setup import Template, DevTemplate, GitTemplate, EmbedTemplate, SharedTemplate
from pyozw_setup import bdist_egg, build_openzwave, build, clean, develop, install

print(current_template)
print(current_template.ctx)
print(install_requires())

setup(
    name='libopenzwave',
    author='Sébastien GALLET aka bibi2100 <bibi21000@gmail.com>',
    author_email='bibi21000@gmail.com',
    version = pyozw_version,
    # ~ scripts=['src-lib/scripts/pyozw_check'],
    zip_safe=False,
    url='https://github.com/OpenZWave/python-openzwave',
    cmdclass=dict(
        build_ext=current_template.build_ext,
        bdist_egg=bdist_egg,
        build=build,
        build_openzwave=build_openzwave,
        clean=clean,
        develop=develop,
        install=install
    ),
    ext_modules=[Extension(**current_template.ctx)],
    # ext_modules = cythonize(ext_modules),
    package_dir=dict(
        libopenzwave='src-lib'
    ),
    # The following line install config drectory in share/python-openzwave
    # ~ data_files = data_files,
    packages=['libopenzwave'],
    install_requires=install_requires(),
)

