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


class TestNode(TestApi):

    def test_020_node_capabilities(self):
        node_id = max(self.network.nodes.keys())
        self.assertEqual(type(self.network.nodes[node_id].capabilities), type(set()))

    def test_310_node(self):
        node_id = max(self.network.nodes.keys())
        self.assertEqual(type(self.network.nodes[node_id].node_id), type(0))
        self.assertTrue(self.network.nodes[node_id].node_id > 0)

    def test_330_controller_node_neighbors(self):
        node_id = max(self.network.nodes.keys())
        self.assertEqual(type(self.network.nodes[node_id].neighbors), type(set()))

    def test_340_controller_node_baud_rate(self):
        node_id = max(self.network.nodes.keys())
        self.assertTrue(type(self.network.nodes[node_id].max_baud_rate) in [type(long()), type(int())])
        self.assertTrue(self.network.nodes[node_id].max_baud_rate > 0)

    def test_410_controller_node_product(self):
        node_id = max(self.network.nodes.keys())
        self.assertEqual(type(self.network.nodes[node_id].product_type), type(""))
        self.assertEqual(type(self.network.nodes[node_id].product_id), type(""))

    def test_420_controller_node_name(self):
        node_id = max(self.network.nodes.keys())
        name = "TestUnit name"
        self.network.nodes[node_id].name = name
        self.assertEqual(self.network.nodes[node_id].name, name)

    def test_421_controller_node_name_accent(self):
        node_id = max(self.network.nodes.keys())
        name = "Contrôleur"
        self.network.nodes[node_id].name = name
        self.assertEqual(self.network.nodes[node_id].name, name)

    def test_430_controller_node_product_location(self):
        node_id = max(self.network.nodes.keys())
        location = "TestUnit location"
        self.network.nodes[node_id].location = location
        self.assertEqual(self.network.nodes[node_id].location, location)

    def test_440_controller_node_product_name(self):
        node_id = max(self.network.nodes.keys())
        name = "TestUnit product name"
        self.network.nodes[node_id].product_name = name
        self.assertEqual(self.network.nodes[node_id].product_name, name)

    def test_510_controller_node_group(self):
        node_id = max(self.network.nodes.keys())
        self.assertTrue(self.network.nodes[node_id].num_groups >= 0)
        self.assertEqual(type(self.network.nodes[node_id].groups), type(dict()))

    def test_610_controller_node_command_class(self):
        node_id = max(self.network.nodes.keys())
        self.assertEqual(type(self.network.nodes[node_id].command_classes), type(set()))
        self.assertTrue(len(self.network.nodes[node_id].command_classes) >= 0)

    def test_710_controller_node_manufacturer_name(self):
        node_id = max(self.network.nodes.keys())
        self.assertEqual(type(self.network.nodes[node_id].manufacturer_id), type(""))
        name = "TestUnit manufacturer name"
        self.network.nodes[node_id].manufacturer_name = name
        self.assertEqual(self.network.nodes[node_id].manufacturer_name, name)

    def test_810_controller_node_values(self):
        node_id = max(self.network.nodes.keys())
        self.assertEqual(type(self.network.nodes[node_id].get_values()), type(dict()))

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
