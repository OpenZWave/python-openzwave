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
from louie import dispatcher, All
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


class TestController(TestApi):

    def test_010_controller(self):
        self.assertEqual(type(self.network.controller.name), type(""))
        self.assertEqual(type(self.network.controller.ozw_library_version), type(""))
        self.assertEqual(type(self.network.controller.python_library_version), type(""))
        self.assertEqual(type(self.network.controller.library_description), type(""))

    def test_020_controller_capabilities(self):
        self.assertEqual(type(self.network.controller.capabilities), type(set()))

    def test_030_controller_send_queue(self):
        self.assertEqual(type(self.network.controller.send_queue_count), type(0))
        self.assertTrue(self.network.controller.send_queue_count >= 0)

    def test_040_controller_stats(self):
        self.assertEqual(type(self.network.controller.stats), type(dict()))

    def test_110_controller_soft_reset(self):
        time.sleep(5)
        self.network.controller.soft_reset()
        self.assertTrue(self.network.controller.node.refresh_info())

    def test_310_controller_node(self):
        self.assertEqual(type(self.network.controller.node.node_id), type(0))
        self.assertTrue(self.network.controller.node.node_id > 0)
        self.assertEqual(type(self.network.controller.node.version), type(0))
        self.assertTrue(self.network.controller.node.version > 0)

    def test_320_controller_node_capabilities(self):
        self.assertEqual(type(self.network.controller.node.capabilities), type(set()))

    def test_330_controller_node_neighbors(self):
        self.assertEqual(type(self.network.controller.node.neighbors), type(set()))

    def test_340_controller_node_baud_rate(self):
        self.assertTrue(type(self.network.controller.node.max_baud_rate) in [type(long()), type(int())])
        self.assertTrue(self.network.controller.node.max_baud_rate > 0)

    def test_410_controller_node_product(self):
        self.assertEqual(type(self.network.controller.node.product_type), type(""))
        self.assertEqual(type(self.network.controller.node.product_id), type(""))

    def test_420_controller_node_name(self):
        name = "TestUnit name"
        self.network.controller.node.name = name
        self.assertEqual(self.network.controller.node.name, name)

    def test_430_controller_node_product_location(self):
        location = "TestUnit location"
        self.network.controller.node.location = location
        self.assertEqual(self.network.controller.node.location, location)

    def test_440_controller_node_product_name(self):
        name = "TestUnit product name"
        self.network.controller.node.product_name = name
        self.assertEqual(self.network.controller.node.product_name, name)

    def test_510_controller_node_group(self):
        self.assertTrue(self.network.controller.node.num_groups >= 0)
        self.assertEqual(type(self.network.controller.node.groups), type(dict()))

    def test_610_controller_node_command_class(self):
        self.assertEqual(type(self.network.controller.node.command_classes), type(set()))
        self.assertTrue(len(self.network.controller.node.command_classes) >= 0)

    def test_710_controller_node_manufacturer_name(self):
        self.assertEqual(type(self.network.controller.node.manufacturer_id), type(""))
        name = "TestUnit manufacturer name"
        self.network.controller.node.manufacturer_name = name
        self.assertEqual(self.network.controller.node.manufacturer_name, name)

    def test_760_controller_stats_label(self):
        self.assertEqual(type(self.network.controller.get_stats_label('retries')), type(""))

    def test_810_controller_node_values(self):
        self.assertEqual(type(self.network.controller.node.get_values()), type(dict()))

    def test_820_controller_node_generic(self):
        self.assertEqual(type(self.network.controller.node.generic), type(0))
        self.assertTrue(self.network.controller.node.generic > 0)
        self.assertEqual(type(self.network.controller.node.basic), type(0))
        self.assertTrue(self.network.controller.node.basic > 0)
        self.assertEqual(type(self.network.controller.node.specific), type(0))
        self.assertTrue(self.network.controller.node.specific >= 0)
        self.assertEqual(type(self.network.controller.node.security), type(0))
        self.assertTrue(self.network.controller.node.security >= 0)

    def notest_910_controller_node_refresh(self):
        #self.wait_for_queue()
        self.assertTrue(self.network.controller.node.refresh_info())

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
