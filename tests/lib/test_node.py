#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
.. module:: tests

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
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

import sys, os, shutil, stat
import time
import unittest
from pprint import pprint
import datetime
import random
import socket
from common import TestLib
import re
from tests.common import pyozw_version
from six import string_types
import libopenzwave

import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        """NullHandler logger for python 2.6"""
        def emit(self, record):
            pass

class TestNode(TestLib):


    def test_100_controller_name(self):
        self.start_lib()
        self.wait_for_ready()
        oldname = self.manager.getNodeName(self.homeid, 1)
        self.assertTrue(isinstance(oldname, string_types))
        self.manager.setNodeName(self.homeid, 1, "test lib name")
        newname = self.manager.getNodeName(self.homeid, 1)
        self.assertTrue(isinstance(newname, string_types))

    def test_101_controller_name_accent(self):
        self.start_lib()
        self.wait_for_ready()
        oldname = self.manager.getNodeName(self.homeid, 1)
        self.assertTrue(isinstance(oldname, string_types))
        self.manager.setNodeName(self.homeid, 1, "test lib name éé")
        newname = self.manager.getNodeName(self.homeid, 1)
        self.assertTrue(isinstance(newname, string_types))


if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
