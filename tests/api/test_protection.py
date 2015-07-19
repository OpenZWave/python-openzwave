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
if sys.hexversion >= 0x3000000:
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

class TestProtection(TestApi):

    def test_010_protection_item(self):
        ran = False
        for node in self.network.nodes:
            for val in self.network.nodes[node].get_protections() :
                ran = True
                self.assertTrue(isinstance(self.network.nodes[node].get_protection_item(val), string_types))
        if not ran :
            self.skipTest("No Protection found")

    def test_020_protection_set_item_no_operation(self):
        ran = False
        for node in self.network.nodes:
            for val in self.network.nodes[node].get_protections() :
                ran = True
                old_value = self.network.nodes[node].get_protection_item(val)
                new_value = "No Operation Possible"
                self.network.nodes[node].set_protection(val, new_value)
                time.sleep(1)
                self.assertEqual(self.network.nodes[node].get_protection_item(val), new_value)
                self.network.nodes[node].set_protection(val, old_value)
                time.sleep(1)
        if not ran :
            self.skipTest("No Protection found")

    def test_030_protection_set_item_unprotected(self):
        ran = False
        for node in self.network.nodes:
            for val in self.network.nodes[node].get_protections() :
                ran = True
                old_value = self.network.nodes[node].get_protection_item(val)
                new_value = "Unprotected"
                self.network.nodes[node].set_protection(val, new_value)
                time.sleep(1)
                self.assertEqual(self.network.nodes[node].get_protection_item(val), new_value)
                self.network.nodes[node].set_protection(val, old_value)
                time.sleep(1)
        if not ran :
            self.skipTest("No Protection found")

    def test_050_protection_items(self):
        ran = False
        for node in self.network.nodes:
            for val in self.network.nodes[node].get_protections() :
                ran = True
                self.assertTrue(type(self.network.nodes[node].get_protection_items(val)) == type(set()) or isinstance(self.network.nodes[node].get_protection_items(val), string_types))
        if not ran :
            self.skipTest("No Protection found")

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
