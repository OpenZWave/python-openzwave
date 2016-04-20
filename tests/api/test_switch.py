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

import os, shutil
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

class TestSwitch(TestApi):

    def test_010_switch_state(self):
        ran = False
        for node in self.network.nodes:
            for val in self.network.nodes[node].get_switches() :
                ran = True
                self.assertTrue(self.network.nodes[node].get_switch_state(val) in [True, False])
        if not ran :
            self.skipTest("No Switch found")

    def test_020_switch_rgb_state(self):
        ran = False
        for node in self.network.nodes:
            for val in self.network.nodes[node].get_rgbbulbs() :
                ran = True
                self.assertTrue(self.network.nodes[node].get_switch_state(val) in [True, False])
        if not ran :
            self.skipTest("No RGB bulb found")

    def test_110_switch_on_off(self):
        ran = False
        for node in self.network.nodes:
            for val in self.network.nodes[node].get_switches() :
                ran = True
                time.sleep(1)
                self.network.nodes[node].set_switch(val,True)
                #self.wait_for_queue()
                time.sleep(1)
                if self.network.nodes[node].get_switch_state(val) == False :
                    time.sleep(5)
                self.assertTrue(self.network.nodes[node].get_switch_state(val))
                self.network.nodes[node].set_switch(val,False)
                #self.wait_for_queue()
                time.sleep(1)
                if self.network.nodes[node].get_switch_state(val) == True :
                    time.sleep(5)
                self.assertFalse(self.network.nodes[node].get_switch_state(val))
        if not ran :
            self.skipTest("No Switch found")

    def test_120_switch_rgbbulbs(self):
        ran = False
        for node in self.network.nodes:
            for val in self.network.nodes[node].get_rgbbulbs() :
                ran = True
                time.sleep(1)
                self.network.nodes[node].set_switch(val,True)
                #self.wait_for_queue()
                time.sleep(1)
                if self.network.nodes[node].get_switch_state(val) == False :
                    time.sleep(5)
                self.assertTrue(self.network.nodes[node].get_switch_state(val))

                oldrgbw = self.network.nodes[node].get_rgbw(val)
                rgbw = 114
                self.network.nodes[node].set_rgbw(val,rgbw)
                #self.wait_for_queue()
                time.sleep(1)
                if self.network.nodes[node].get_rgbw(val) != rgbw :
                    time.sleep(5)
                self.assertEqual(rgbw, self.network.nodes[node].get_rgbw(val))
                self.network.nodes[node].set_rgbw(val,oldrgbw)
                #self.wait_for_queue()
                time.sleep(1)
                if self.network.nodes[node].get_rgbw(val) != rgbw :
                    time.sleep(5)
                self.assertEqual(oldrgbw, self.network.nodes[node].get_rgbw(val))

                self.network.nodes[node].set_switch(val,False)
                #self.wait_for_queue()
                time.sleep(1)
                if self.network.nodes[node].get_switch_state(val) == True :
                    time.sleep(5)
                self.assertFalse(self.network.nodes[node].get_switch_state(val))
        if not ran :
            self.skipTest("No RGB bulb found")

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
