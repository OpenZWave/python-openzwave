#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
.. module:: tests

This file is part of **python-openzwave** project https://github.com/bibi21000/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave Library

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

import sys, os
import time
import unittest
from pprint import pprint
import datetime
import random
import socket
import libopenzwave
from tests.lib.common import TestLib
import re
from tests.common import pyozw_version

class TestInit(TestLib):

    def test_000_init(self):
        self._manager = libopenzwave.PyManager()
        self.assertEqual(self._manager.getPythonLibraryVersionNumber(), pyozw_version)
        vers=re.findall(r'\d+', self._manager.getOzwLibraryVersionNumber())
        self.assertEqual(len(vers),3)

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
