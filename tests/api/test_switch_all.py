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
from six import string_types

class TestSwitchAll(TestApi):

    def test_010_switch_all_item(self):
        ran = False
        for node in self.network.nodes:
            for val in self.network.nodes[node].get_switches_all() :
                ran = True
                self.assertTrue(isinstance(self.network.nodes[node].get_switch_all_item(val), string_types))
        if not ran :
            self.skipTest("No Switch_All found")

    def test_015_switch_all_set_item(self):
        ran = False
        for node in self.network.nodes:
            for val in self.network.nodes[node].get_switches_all() :
                self.wait_for_queue()
                ran = True
                old_value = self.network.nodes[node].get_switch_all_item(val)
                new_value = "Disabled"
                self.network.nodes[node].set_switch_all(val, new_value)
                time.sleep(1)
                self.wait_for_queue()
                self.assertEqual(self.network.nodes[node].get_switch_all_item(val), new_value)
                self.network.nodes[node].set_switch_all(val, old_value)
                time.sleep(1)
        if not ran :
            self.skipTest("No Switch_All found")

    def test_020_switch_all_items(self):
        ran = False
        for node in self.network.nodes:
            for val in self.network.nodes[node].get_switches_all() :
                ran = True
                self.assertTrue(isinstance(self.network.nodes[node].get_switch_all_item(val), string_types) or type(self.network.nodes[node].get_switch_all_items(val)) == type(""))
        if not ran :
            self.skipTest("No Switch_All found")

    def test_110_switch_all_on(self):
        #~ self.wipTest()
        self.wait_for_queue()
        time.sleep(2)
        ran = False
        self.network.switch_all(True)
        time.sleep(3)
        self.wait_for_queue()
        for node in self.network.nodes:
            for val in self.network.nodes[node].get_switches_all() :
                item = self.network.nodes[node].get_switch_all_item(val)
                if item == "On and Off Enabled" or item == "On Enabled":
                    ran = True
                    print "Node/State : %s/%s" % (node, self.network.nodes[node].get_switch_all_state(val))
                    self.assertTrue(self.network.nodes[node].get_switch_all_state(val))
        if not ran :
            self.skipTest("No Switch_All with 'On and Off Enabled' or 'On Enabled' found")

    def test_120_switch_all_off(self):
        #~ self.wipTest()
        self.wait_for_queue()
        time.sleep(2)
        ran = False
        self.network.switch_all(False)
        time.sleep(3)
        self.wait_for_queue()
        for node in self.network.nodes:
            for val in self.network.nodes[node].get_switches_all() :
                item = self.network.nodes[node].get_switch_all_item(val)
                if item == "On and Off Enabled" or item == "Off Enabled":
                    ran = True
                    print "Node/State : %s/%s" % (node, self.network.nodes[node].get_switch_all_state(val))
                    self.assertFalse(self.network.nodes[node].get_switch_all_state(val))
        if not ran :
            self.skipTest("No Switch_All with 'On and Off Enabled' or 'Off Enabled' found")

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
