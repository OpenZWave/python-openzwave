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
import re
import six
if six.PY3:
    from pydispatch import dispatcher
else:
    from louie import dispatcher
from six import string_types, integer_types
import openzwave
from openzwave.node import ZWaveNode
from openzwave.group import ZWaveGroup
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import libopenzwave
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
        self.assertTrue(isinstance(self.network.nodes[node_id].node_id, integer_types))
        self.assertTrue(self.network.nodes[node_id].node_id > 0)

    def test_330_node_neighbors(self):
        node_id = max(self.network.nodes.keys())
        self.assertEqual(type(self.network.nodes[node_id].neighbors), type(set()))

    def test_340_node_baud_rate(self):
        node_id = max(self.network.nodes.keys())
        self.assertTrue(isinstance(self.network.nodes[node_id].max_baud_rate, integer_types))
        self.assertTrue(self.network.nodes[node_id].max_baud_rate > 0)

    def test_410_node_product(self):
        node_id = max(self.network.nodes.keys())
        self.assertTrue(isinstance(self.network.nodes[node_id].product_type, string_types))
        self.assertTrue(isinstance(self.network.nodes[node_id].product_id, string_types))

    def test_420_node_name(self):
        node_id = max(self.network.nodes.keys())
        name = "TestUnit name"
        self.network.nodes[node_id].name = name
        self.assertEqual(self.network.nodes[node_id].name, name)

    def test_421_node_name_accent(self):
        #~ self.wipTest()
        node_id = max(self.network.nodes.keys())
        name = "noeud éééé"
        self.network.nodes[node_id].name = name
        self.assertEqual(self.network.nodes[node_id].name, name)

    def test_430_node_location(self):
        node_id = max(self.network.nodes.keys())
        location = "TestUnit location"
        self.network.nodes[node_id].location = location
        self.assertEqual(self.network.nodes[node_id].location, location)

    def test_431_node_location_accent(self):
        #~ self.wipTest()
        node_id = max(self.network.nodes.keys())
        name = "location éééé"
        self.network.nodes[node_id].location = name
        self.assertEqual(self.network.nodes[node_id].location, name)

    def test_440_node_product_name(self):
        node_id = max(self.network.nodes.keys())
        name = "TestUnit product name"
        self.network.nodes[node_id].product_name = name
        self.assertEqual(self.network.nodes[node_id].product_name, name)

    def test_441_node_product_name_accent(self):
        #~ self.wipTest()
        node_id = max(self.network.nodes.keys())
        name = "product éééé"
        self.network.nodes[node_id].product_name = name
        self.assertEqual(self.network.nodes[node_id].product_name, name)

    def test_450_node_manufacturer_name(self):
        node_id = max(self.network.nodes.keys())
        self.assertTrue(isinstance(self.network.nodes[node_id].manufacturer_id, string_types))
        name = "TestUnit manufacturer name"
        self.network.nodes[node_id].manufacturer_name = name
        self.assertEqual(self.network.nodes[node_id].manufacturer_name, name)

    def test_451_node_manufacturer_name_accent(self):
        #~ self.wipTest()
        node_id = max(self.network.nodes.keys())
        name = "manufacturer_name éééé"
        self.network.nodes[node_id].manufacturer_name = name
        self.assertEqual(self.network.nodes[node_id].manufacturer_name, name)

    def test_510_node_group(self):
        node_id = max(self.network.nodes.keys())
        self.assertTrue(self.network.nodes[node_id].num_groups >= 0)
        self.assertEqual(type(self.network.nodes[node_id].groups), type(dict()))

    def test_520_node_group_associations(self):
        node_id = max(self.network.nodes.keys())
        self.assertTrue(self.network.nodes[node_id].num_groups >= 0)
        groups = self.network.nodes[node_id].groups
        self.assertEqual(type(groups), type(dict()))
        for grp in groups.keys():
            associations = groups[grp].associations
            for ass in associations:
                self.assertTrue(isinstance(ass, integer_types))
                self.assertTrue(0 <= ass <= 255)

    def test_530_node_group_associations_instances(self):
        node_id = max(self.network.nodes.keys())
        self.assertTrue(self.network.nodes[node_id].num_groups >= 0)
        groups = self.network.nodes[node_id].groups
        self.assertEqual(type(groups), type(dict()))
        for grp in groups.keys():
            associations = groups[grp].associations_instances
            for ass in associations:
                self.assertTrue(isinstance(ass[0], integer_types))
                self.assertTrue(isinstance(ass[1], integer_types))
                self.assertTrue(0 <= ass[0] <= 255)
                self.assertTrue(0 <= ass[1] <= 255)

    def test_550_request_all_config_params(self):
        node_id = max(self.network.nodes.keys())
        self.network.nodes[node_id].request_all_config_params()

    def test_580_node_command_class(self):
        node_id = max(self.network.nodes.keys())
        self.assertEqual(type(self.network.nodes[node_id].command_classes), type(set()))
        self.assertTrue(len(self.network.nodes[node_id].command_classes) >= 0)

    def test_610_node_is_awake(self):
        node_id = max(self.network.nodes.keys())
        self.assertEqual(type(self.network.nodes[node_id].is_awake), type(True))

    def test_615_node_is_ready(self):
        node_id = max(self.network.nodes.keys())
        self.assertEqual(type(self.network.nodes[node_id].is_ready), type(True))

    def test_620_node_is_failed(self):
        node_id = max(self.network.nodes.keys())
        self.assertEqual(type(self.network.nodes[node_id].is_failed), type(True))

    def test_625_node_is_zwave_plus(self):
        node_id = max(self.network.nodes.keys())
        self.assertEqual(type(self.network.nodes[node_id].is_zwave_plus), type(True))

    def test_630_node_is_info_received(self):
        node_id = max(self.network.nodes.keys())
        self.assertEqual(type(self.network.nodes[node_id].is_info_received), type(True))

    def test_680_node_query_stage(self):
        node_id = max(self.network.nodes.keys())
        self.assertTrue(isinstance(self.network.nodes[node_id].query_stage, string_types))

    def test_690_node_type(self):
        node_id = max(self.network.nodes.keys())
        self.assertTrue(isinstance(self.network.nodes[node_id].type, string_types))

    def test_691_node_device_type(self):
        node_id = max(self.network.nodes.keys())
        self.assertTrue(isinstance(self.network.nodes[node_id].device_type, string_types))

    def test_692_node_role(self):
        node_id = max(self.network.nodes.keys())
        self.assertTrue(isinstance(self.network.nodes[node_id].role, string_types))

    def test_710_node_test(self):
        node_id = max(self.network.nodes.keys())
        self.network.nodes[node_id].test()

    def test_720_node_heal(self):
        node_id = max(self.network.nodes.keys())
        self.network.nodes[node_id].heal()

    def test_730_node_assign_return_route(self):
        node_id = max(self.network.nodes.keys())
        ret=self.network.nodes[node_id].assign_return_route()
        self.assertEqual(ret, True)
        self.network.controller.kill_command()

    def test_740_node_refresh_info(self):
        node_id = max(self.network.nodes.keys())
        ret=self.network.nodes[node_id].refresh_info()
        self.assertEqual(ret, True)
        self.network.controller.kill_command()

    def test_745_node_send_information(self):
        node_id = max(self.network.nodes.keys())
        ret=self.network.nodes[node_id].send_information()
        self.assertEqual(ret, True)
        self.network.controller.kill_command()

    def test_750_node_network_update(self):
        node_id = max(self.network.nodes.keys())
        ret=self.network.nodes[node_id].network_update()
        self.assertEqual(ret, True)
        self.network.controller.kill_command()

    def test_760_node_neighbor_update(self):
        node_id = max(self.network.nodes.keys())
        ret=self.network.nodes[node_id].neighbor_update()
        self.assertEqual(ret, True)
        self.network.controller.kill_command()

    def test_770_node_request_state(self):
        node_id = max(self.network.nodes.keys())
        ret=self.network.nodes[node_id].request_state()
        self.assertEqual(ret, True)
        self.network.controller.kill_command()

    def test_810_node_values(self):
        node_id = max(self.network.nodes.keys())
        self.assertEqual(type(self.network.nodes[node_id].get_values()), type(dict()))

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
