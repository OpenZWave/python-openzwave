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
import libopenzwave
from common import TestLib
import re
from tests.common import pyozw_version
from six import string_types

import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        """NullHandler logger for python 2.6"""
        def emit(self, record):
            pass

class TestDriver(TestLib):

    def setUp(self):
        self.options = libopenzwave.PyOptions(config_path="openzwave/config", \
            user_path=self.userpath, cmd_line="--logging false")
        self.options.lock()
        
    def tearDown(self):
        self.stop_lib()

    def test_100_start(self):
        time.sleep(1.0)
        self.manager = libopenzwave.PyManager()
        self.manager.create()
        self.manager.addWatcher(self.zwcallback)
        time.sleep(1.0)
        self.manager.addDriver(self.device)
        for i in range(0,600):
            if self.driver_ready:
                break
            else:
                time.sleep(0.1)
        self.assertTrue(self.driver_ready)
        #~ for i in range(0,600):
            #~ if self.network_awake:
                #~ break
            #~ else:
                #~ time.sleep(0.1)
        #~ self.assertTrue(self.network_awake)
        for i in range(0,1200):
            if self.network_ready:
                break
            else:
                time.sleep(0.1)
        self.assertTrue(self.network_ready)
        self.manager.removeDriver(self.device)
        for i in range(0,600):
            if self.driver_removed:
                break
            else:
                time.sleep(0.1)
        self.assertTrue(self.driver_removed)
        time.sleep(1.0)
        self.manager.removeWatcher(self.zwcallback)
        time.sleep(1.0)
        self.manager.destroy()
        time.sleep(1.0)
        self.manager = None
        

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
