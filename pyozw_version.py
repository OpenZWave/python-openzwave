# -*- coding: utf-8 -*-
"""
This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave API

.. moduleauthor: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>

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
pyozw_version = '0.4.9'
if "-" in pyozw_version:
    pyozw_version_short = pyozw_version.split("-")
else:
    pyozw_version_short = pyozw_version

def install_requires():
    try:
        import python_openzwave
        return ['python_openzwave==%s' % pyozw_version]
    except ImportError:
        pass
    try:
        import libopenzwave
        return ['openzwave==%s' % pyozw_version]
    except ImportError:
        pass
    return ['python_openzwave==%s' % pyozw_version]

if __name__ == '__main__':
    import sys
    if len(sys.argv)>1 and sys.argv[1]=="--major":
        print(pyozw_version_short)
    else:
        print(pyozw_version)

