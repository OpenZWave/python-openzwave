# -*- coding: utf-8 -*-

"""
.. module:: tests

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

import sys, os
import time
import unittest
import threading
import logging
import json as mjson
import shutil
from nose.plugins.skip import SkipTest

from tests.common import SLEEP
from tests.common import TestPyZWave

class TestLib(TestPyZWave):
    """
    Parent test class for lib
    """
    @classmethod
    def setUpClass(self):
        super(TestPyZWave, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        super(TestPyZWave, self).tearDownClass()

