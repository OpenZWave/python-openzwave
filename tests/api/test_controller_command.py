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
from tests.api.common import SLEEP
from tests.api.common import TestApi
from tests.common import TestPyZWave

class TestControllerCommand(TestApi):
    """
    Parent test class for api
    """

    @classmethod
    def tearDownClass(self):
        self.network.controller.cancel_command()
        super(TestControllerCommand, self).tearDownClass()

    def setUp(self):
        self.wait_for_network_state(self.network.STATE_READY, 1)
        self.wait_for_queue()
        self.ctrl_state_result = None
        dispatcher.connect(self.ctrl_message, ZWaveNetwork.SIGNAL_CONTROLLER_COMMAND)
        dispatcher.connect(self.ctrl_waiting, ZWaveNetwork.SIGNAL_CONTROLLER_WAITING)

    def tearDown(self):
        self.wait_for_queue()
        try:
            dispatcher.disconnect(self.ctrl_message)
        except :
            pass
        try:
            dispatcher.disconnect(self.ctrl_waiting)
        except :
            pass
        self.network.controller.cancel_command()
        self.ctrl_state_result = None

    def test_010_command_send_node_information_nodes(self):
        node_ids = [ k for k in self.network.nodes.keys() if k != self.network.controller.node_id ]
        for node_id in node_ids:
            node_id = max(self.network.nodes.keys())
            ret = self.network.controller.send_node_information(node_id)
            self.assertTrue(ret)
            current = None
            for i in range(0,SLEEP):
                #print("self.ctrl_state_result = %s" % self.ctrl_state_result)
                if self.ctrl_state_result != None and self.ctrl_state_result not in [self.network.controller.STATE_STARTING,
                        self.network.controller.STATE_WAITING, self.network.controller.STATE_INPROGRESS]:
                    current = self.ctrl_state_result
                    break
                else:
                    time.sleep(1.0)
            self.assertEqual(current, self.network.controller.STATE_COMPLETED)

    def test_015_command_send_node_information_controller(self):
        node_id = self.network.controller.node_id
        ret = self.network.controller.send_node_information(node_id)
        self.assertTrue(ret)
        current = None
        for i in range(0,SLEEP):
            #print("self.ctrl_state_result = %s" % self.ctrl_state_result)
            if self.ctrl_state_result != None and self.ctrl_state_result not in [self.network.controller.STATE_STARTING,
                    self.network.controller.STATE_WAITING, self.network.controller.STATE_INPROGRESS]:
                current = self.ctrl_state_result
                break
            else:
                time.sleep(1.0)
        self.assertEqual(current, self.network.controller.STATE_FAILED)

    def test_020_command_request_node_neighbor_update_nodes(self):
        self.wipTest()
        node_ids = [ k for k in self.network.nodes.keys() if k != self.network.controller.node_id ]
        for node_id in node_ids:
            ret = self.network.controller.request_node_neighbor_update(node_id)
            self.assertTrue(ret)
            current = None
            for i in range(0,SLEEP):
                #print("self.ctrl_state_result = %s" % self.ctrl_state_result)
                if self.ctrl_state_result != None and self.ctrl_state_result not in [self.network.controller.STATE_STARTING,
                        self.network.controller.STATE_WAITING, self.network.controller.STATE_INPROGRESS]:
                    current = self.ctrl_state_result
                    break
                else:
                    time.sleep(1.0)
            self.assertEqual(current, self.network.controller.STATE_COMPLETED)

    def test_025_command_request_node_neighbor_update_controller(self):
        self.wipTest()
        node_id = self.network.controller.node_id
        ret = self.network.controller.request_node_neighbor_update(node_id)
        self.assertTrue(ret)
        current = None
        for i in range(0,SLEEP):
            #print("self.ctrl_state_result = %s" % self.ctrl_state_result)
            if self.ctrl_state_result != None and self.ctrl_state_result not in [self.network.controller.STATE_STARTING,
                    self.network.controller.STATE_WAITING, self.network.controller.STATE_INPROGRESS]:
                current = self.ctrl_state_result
                break
            else:
                time.sleep(1.0)
        self.assertEqual(current, self.network.controller.STATE_COMPLETED)

    def test_030_command_request_network_update_nodes(self):
        node_ids = [ k for k in self.network.nodes.keys() if k != self.network.controller.node_id ]
        for node_id in node_ids:
            node_id = max(self.network.nodes.keys())
            ret = self.network.controller.request_network_update(node_id)
            self.assertTrue(ret)
            current = None
            for i in range(0,SLEEP):
                #print("self.ctrl_state_result = %s" % self.ctrl_state_result)
                if self.ctrl_state_result != None and self.ctrl_state_result not in [self.network.controller.STATE_STARTING,
                        self.network.controller.STATE_WAITING, self.network.controller.STATE_INPROGRESS]:
                    current = self.ctrl_state_result
                    break
                else:
                    time.sleep(1.0)
            self.assertEqual(current, self.network.controller.STATE_FAILED)

    def test_035_command_request_network_update_controller(self):
        node_id = self.network.controller.node_id
        ret = self.network.controller.request_network_update(node_id)
        self.assertTrue(ret)
        current = None
        for i in range(0,SLEEP):
            #print("self.ctrl_state_result = %s" % self.ctrl_state_result)
            if self.ctrl_state_result != None and self.ctrl_state_result not in [self.network.controller.STATE_STARTING,
                    self.network.controller.STATE_WAITING, self.network.controller.STATE_INPROGRESS]:
                current = self.ctrl_state_result
                break
            else:
                time.sleep(1.0)
        self.assertEqual(current, self.network.controller.STATE_FAILED)

    def test_040_command_delete_all_return_routes_nodes(self):
        node_ids = [ k for k in self.network.nodes.keys() if k != self.network.controller.node_id ]
        for node_id in node_ids:
            node_id = max(self.network.nodes.keys())
            ret = self.network.controller.delete_all_return_routes(node_id)
            self.assertTrue(ret)
            current = None
            for i in range(0,SLEEP):
                #print("self.ctrl_state_result = %s" % self.ctrl_state_result)
                if self.ctrl_state_result != None and self.ctrl_state_result not in [self.network.controller.STATE_STARTING,
                        self.network.controller.STATE_WAITING, self.network.controller.STATE_INPROGRESS]:
                    current = self.ctrl_state_result
                    break
                else:
                    time.sleep(1.0)
            self.assertEqual(current, self.network.controller.STATE_COMPLETED)

    def test_045_command_delete_all_return_routes_controller(self):
        node_id = self.network.controller.node_id
        ret = self.network.controller.delete_all_return_routes(node_id)
        self.assertTrue(ret)
        current = None
        for i in range(0,SLEEP):
            #print("self.ctrl_state_result = %s" % self.ctrl_state_result)
            if self.ctrl_state_result != None and self.ctrl_state_result not in [self.network.controller.STATE_STARTING,
                    self.network.controller.STATE_WAITING, self.network.controller.STATE_INPROGRESS]:
                current = self.ctrl_state_result
                break
            else:
                time.sleep(1.0)
        self.assertEqual(current, self.network.controller.STATE_FAILED)

    def test_050_command_assign_return_route_nodes(self):
        node_ids = [ k for k in self.network.nodes.keys() if k != self.network.controller.node_id ]
        for node_id in node_ids:
            node_id = max(self.network.nodes.keys())
            ret = self.network.controller.assign_return_route(node_id)
            self.assertTrue(ret)
            current = None
            for i in range(0,SLEEP):
                #print("self.ctrl_state_result = %s" % self.ctrl_state_result)
                if self.ctrl_state_result != None and self.ctrl_state_result not in [self.network.controller.STATE_STARTING,
                        self.network.controller.STATE_WAITING, self.network.controller.STATE_INPROGRESS]:
                    current = self.ctrl_state_result
                    break
                else:
                    time.sleep(1.0)
            self.assertEqual(current, self.network.controller.STATE_COMPLETED)

    def test_055_command_assign_return_route_controller(self):
        node_id = self.network.controller.node_id
        ret = self.network.controller.assign_return_route(node_id)
        self.assertTrue(ret)
        current = None
        for i in range(0,SLEEP):
            #print("self.ctrl_state_result = %s" % self.ctrl_state_result)
            if self.ctrl_state_result != None and self.ctrl_state_result not in [self.network.controller.STATE_STARTING,
                    self.network.controller.STATE_WAITING, self.network.controller.STATE_INPROGRESS]:
                current = self.ctrl_state_result
                break
            else:
                time.sleep(1.0)
        self.assertEqual(current, self.network.controller.STATE_FAILED)

    def test_060_command_has_node_failed_nodes(self):
        node_ids = [ k for k in self.network.nodes.keys() if k != self.network.controller.node_id ]
        for node_id in node_ids:
            node_id = max(self.network.nodes.keys())
            ret = self.network.controller.has_node_failed(node_id)
            self.assertTrue(ret)
            current = None
            for i in range(0,SLEEP):
                #print("self.ctrl_state_result = %s" % self.ctrl_state_result)
                if self.ctrl_state_result != None and self.ctrl_state_result not in [self.network.controller.STATE_STARTING,
                        self.network.controller.STATE_WAITING, self.network.controller.STATE_INPROGRESS]:
                    current = self.ctrl_state_result
                    break
                else:
                    time.sleep(1.0)
            self.assertEqual(current, self.network.controller.STATE_NODEOK)

    def test_070_command_remove_failed_node_nodes(self):
        node_ids = [ k for k in self.network.nodes.keys() if k != self.network.controller.node_id ]
        for node_id in node_ids:
            node_id = max(self.network.nodes.keys())
            ret = self.network.controller.remove_failed_node(node_id)
            self.assertTrue(ret)
            current = None
            for i in range(0,SLEEP):
                #print("self.ctrl_state_result = %s" % self.ctrl_state_result)
                if self.ctrl_state_result != None and self.ctrl_state_result not in [self.network.controller.STATE_STARTING,
                        self.network.controller.STATE_WAITING, self.network.controller.STATE_INPROGRESS]:
                    current = self.ctrl_state_result
                    break
                else:
                    time.sleep(1.0)
            self.assertEqual(current, self.network.controller.STATE_FAILED)

    def test_080_command_replace_failed_node_nodes(self):
        node_ids = [ k for k in self.network.nodes.keys() if k != self.network.controller.node_id ]
        for node_id in node_ids:
            node_id = max(self.network.nodes.keys())
            ret = self.network.controller.replace_failed_node(node_id)
            self.assertTrue(ret)
            current = None
            for i in range(0,SLEEP):
                #print("self.ctrl_state_result = %s" % self.ctrl_state_result)
                if self.ctrl_state_result != None and self.ctrl_state_result not in [self.network.controller.STATE_STARTING,
                        self.network.controller.STATE_WAITING, self.network.controller.STATE_INPROGRESS]:
                    current = self.ctrl_state_result
                    break
                else:
                    time.sleep(1.0)
            self.assertEqual(current, self.network.controller.STATE_FAILED)

    def test_080_command_replace_failed_node_nodes(self):
        node_ids = [ k for k in self.network.nodes.keys() if k != self.network.controller.node_id ]
        for node_id in node_ids:
            node_id = max(self.network.nodes.keys())
            ret = self.network.controller.replace_failed_node(node_id)
            self.assertTrue(ret)
            current = None
            for i in range(0,SLEEP):
                #print("self.ctrl_state_result = %s" % self.ctrl_state_result)
                if self.ctrl_state_result != None and self.ctrl_state_result not in [self.network.controller.STATE_STARTING,
                        self.network.controller.STATE_WAITING, self.network.controller.STATE_INPROGRESS]:
                    current = self.ctrl_state_result
                    break
                else:
                    time.sleep(1.0)
            self.assertEqual(current, self.network.controller.STATE_FAILED)

    def test_100_command_add_node_secure_off_and_wait_for_user(self):
        self.skipManualTest()
        nb_nodes = len(self.network.nodes)
        ret = self.network.controller.add_node(False)
        self.assertTrue(ret)
        current = None
        for i in range(0,SLEEP):
            #print("self.ctrl_state_result = %s" % self.ctrl_state_result)
            if self.ctrl_state_result != None and self.ctrl_state_result not in [self.network.controller.STATE_STARTING,
                    self.network.controller.STATE_WAITING, self.network.controller.STATE_INPROGRESS]:
                current = self.ctrl_state_result
                break
            else:
                time.sleep(1.0)
        self.network.controller.cancel_command()
        self.assertEqual(len(self.network.nodes), nb_nodes+1)

    def test_110_command_add_node_secure_on_and_wait_for_user(self):
        self.skipManualTest()
        nb_nodes = len(self.network.nodes)
        ret = self.network.controller.add_node(True)
        self.assertTrue(ret)
        current = None
        for i in range(0,SLEEP):
            #print("self.ctrl_state_result = %s" % self.ctrl_state_result)
            if self.ctrl_state_result != None and self.ctrl_state_result not in [self.network.controller.STATE_STARTING,
                    self.network.controller.STATE_WAITING, self.network.controller.STATE_INPROGRESS]:
                current = self.ctrl_state_result
                break
            else:
                time.sleep(1.0)
        self.network.controller.cancel_command()
        self.assertEqual(len(self.network.nodes), nb_nodes-1)

    def test_150_command_remove_node_and_wait_for_user(self):
        self.skipManualTest()
        nb_nodes = len(self.network.nodes)
        ret = self.network.controller.remove_node()
        self.assertTrue(ret)
        current = None
        for i in range(0,SLEEP):
            #print("self.ctrl_state_result = %s" % self.ctrl_state_result)
            if self.ctrl_state_result != None and self.ctrl_state_result not in [self.network.controller.STATE_STARTING,
                    self.network.controller.STATE_WAITING, self.network.controller.STATE_INPROGRESS]:
                current = self.ctrl_state_result
                break
            else:
                time.sleep(1.0)
        self.network.controller.cancel_command()
        self.assertEqual(len(self.network.nodes), nb_nodes-1)

    def test_200_command_create_new_primary(self):
        self.skipManualTest()
        nb_nodes = len(self.network.nodes)
        ret = self.network.controller.create_new_primary()
        self.assertTrue(ret)
        current = None
        for i in range(0,SLEEP):
            #print("self.ctrl_state_result = %s" % self.ctrl_state_result)
            if self.ctrl_state_result != None and self.ctrl_state_result not in [self.network.controller.STATE_STARTING,
                    self.network.controller.STATE_WAITING, self.network.controller.STATE_INPROGRESS]:
                current = self.ctrl_state_result
                break
            else:
                time.sleep(1.0)
        self.assertEqual(current, self.network.controller.STATE_COMPLETED)

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
