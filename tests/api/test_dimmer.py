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

class TestDimmer(TestApi):

    def test_010_dimmer_level(self):
        ran = False
        for node in self.network.nodes:
            for val in self.network.nodes[node].get_dimmers() :
                ran = True
                self.assertTrue(self.network.nodes[node].get_dimmer_level(val) in range(0,256))
        if not ran :
            self.skipTest("No Dimmer found")

    def test_110_dimmer_on_off(self):
        ran = False
        for node in self.network.nodes:
            for val in self.network.nodes[node].get_dimmers() :
                ran = True
                level = 80
                self.network.nodes[node].set_dimmer(val,level)
                time.sleep(1)
                if self.network.nodes[node].get_dimmer_level(val) not in range(level-5,level+5):
                    time.sleep(5)
                self.assertTrue(self.network.nodes[node].get_dimmer_level(val) in range(level-5,level+5))
                self.network.nodes[node].set_dimmer(val,0)
                time.sleep(2)
                if self.network.nodes[node].get_dimmer_level(val) != 0:
                    time.sleep(5)
                self.assertEqual(self.network.nodes[node].get_dimmer_level(val), 0)
        if not ran :
            self.skipTest("No Dimmer found")

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
