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

import sys, os, shutil
import time
import unittest
from pprint import pprint
import datetime
import random
import socket
import libopenzwave
import re
import time
import sys
import six
if six.PY3:
    from pydispatch import dispatcher
else:
    from louie import dispatcher
import libopenzwave
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
from tests.common import pyozw_version
from tests.common import SLEEP
from tests.api.common import TestApi
from tests.common import TestPyZWave

class TestCommand(TestApi):

    def test_010_battery_item(self):
        ran = False
        for node in self.active_nodes:
            for val in self.active_nodes[node].get_battery_levels() :
                ran = True
                self.assertTrue(isinstance(self.active_nodes[node].get_battery_level(val),
                                           six.integer_types))
        if ran == False :
            self.skipTest("No battery found")

    def test_020_config_item(self):
        ran = False
        for node in self.active_nodes:
            for val in self.active_nodes[node].get_configs() :
                ran = True
                self.assertNotEqual(self.active_nodes[node].get_config(val), None)
        if ran == False :
            self.skipTest("No config param found")

    def test_030_door_locks(self):
        ran = False
        for node in self.active_nodes:
            for val in self.active_nodes[node].get_doorlocks() :
                ran = True
                self.assertNotEqual(self.active_nodes[node].get_usercodes(), None)
                self.assertNotEqual(self.active_nodes[node].get_doorlock_logs(), None)
        if ran == False :
            self.skipTest("No door_locks found")

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
