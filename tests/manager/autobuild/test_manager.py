#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Unittests for the pyozwwzb Server.

See http://werkzeug.pocoo.org/docs/0.9/test/
See http://werkzeug.pocoo.org/docs/0.9/wrappers/

"""

__license__ = """

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.

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
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'

import sys
import time
import logging
import unittest

from tests.manager.common import TestManager

class ManagerTest(TestManager):

    def test_000_import(self):
        from pyozwman.ozwsh_main import MainWindow
        from pyozwman.ozwsh_widgets import NodeTree

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
