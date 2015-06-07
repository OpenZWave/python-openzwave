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
from tests.api.common import SLEEP
from tests.api.common import TestApi
from tests.common import TestPyZWave

class TestControllerCommand(TestPyZWave):
    """
    Parent test class for api
    """

    @classmethod
    def setUpClass(self):
        super(TestPyZWave, self).setUpClass()
        self.options = ZWaveOption(device=self.device, user_path=self.userpath)
        self.options.set_log_file("OZW_Log.log")
        self.options.set_append_log_file(False)
        self.options.set_console_output(False)
        self.options.set_save_log_level("Debug")
        self.options.set_logging(True)
        self.options.lock()
        self.node_result = None
        dispatcher.connect(self.node_update, ZWaveNetwork.SIGNAL_NODE)
        self.network = ZWaveNetwork(self.options)
        self.ctrl_command_result = None
        dispatcher.connect(self.ctrl_message, ZWaveNetwork.SIGNAL_CONTROLLER_COMMAND)
        time.sleep(1.0)

    @classmethod
    def tearDownClass(self):
        self.network.stop()
        time.sleep(2.0)
        super(TestPyZWave, self).tearDownClass()
        self.network=None

    def setUp(self):
        self.wait_for_network_state(self.network.STATE_AWAKED, 1)

    def wait_for_queue(self):
        for i in range(0,60):
            if self.network.controller.send_queue_count <= 0:
                break
            else:
                time.sleep(0.5)

    def wait_for_network_state(self, state, multiply=1):
        for i in range(0,SLEEP*multiply):
            if self.network.state>=state:
                break
            else:
                #sys.stdout.write(".")
                #sys.stdout.flush()
                time.sleep(1.0)

    def ctrl_message(self, network, controller, node, node_id, state, command, message):
        self.ctrl_command_result = state
        print "catched"

    def node_update(self, network, node):
        self.node_result = node



    #~ def setUp(self):
        #~ self.max_delay = 30
        #~ self.ctrl_command_result = None
        #~ dispatcher.connect(self.ctrl_message, ZWaveController.SIGNAL_CONTROLLER)
        #~ self.node_result = None
        #~ dispatcher.connect(self.node_update, ZWaveNetwork.SIGNAL_NODE)
#~
    #~ def tearDown(self):
        #~ self.network.controller.cancel_command()
        #~ dispatcher.disconnect(self.ctrl_message, ZWaveController.SIGNAL_CONTROLLER)
        #~ dispatcher.disconnect(self.node_update, ZWaveNetwork.SIGNAL_NODE)

    def test_010_command_send_node_information_nodeid(self):
        self.wait_for_network_state(self.network.STATE_READY, 1)
        self.wait_for_queue()
        print self.network.state_str
        node_id = max(self.network.nodes.keys())
        print node_id
        #ret = self.network.controller.send_node_information(node_id)
        #self.assertTrue(ret)
        current = None
        for i in range(0,SLEEP):
            print self.ctrl_command_result
            #print("self.ctrl_command_result = %s" % self.ctrl_command_result)
            if self.ctrl_command_result != None and self.ctrl_command_result != "InProgress":
                current = self.ctrl_command_result
                print(current)
                self.ctrl_command_result = None
                break
            else:
                time.sleep(1.0)
        self.assertEqual(current, "Completed")

    #~ def test_020_command_send_node_information_nodeid_controller(self):
        #~ self.wipTest()
        #~ node_id = self.network.controller.node_id
        #~ ret = self.network.controller.begin_command_send_node_information(node_id)
        #~ self.assertTrue(ret)
        #~ current = None
        #~ for i in range(0,SLEEP*2):
            #~ #print("self.ctrl_command_result = %s" % self.ctrl_command_result)
            #~ if self.ctrl_command_result != None and self.ctrl_command_result != "InProgress":
                #~ current = self.ctrl_command_result
                #~ #print(current)
                #~ self.ctrl_command_result = None
                #~ break
            #~ else:
                #~ time.sleep(1.0)
        #~ self.assertEqual(current, "Failed")
#~
    #~ def test_110_command_request_network_update(self):
        #~ self.wipTest()
        #~ ret = self.network.controller.begin_command_request_network_update()
        #~ self.assertTrue(ret)
        #~ current = None
        #~ for i in range(0,SLEEP*2):
            #~ #print("self.ctrl_command_result = %s" % self.ctrl_command_result)
            #~ if self.ctrl_command_result != None and self.ctrl_command_result != "InProgress":
                #~ current = self.ctrl_command_result
                #~ #print(current)
                #~ self.ctrl_command_result = None
                #~ break
            #~ else:
                #~ time.sleep(1.0)
        #~ self.assertEqual(current, "Completed")
#~
    #~ def test_210_command_request_node_neigbhor_update_node(self):
        #~ self.wipTest()
        #~ node_id = max(self.network.nodes.keys())
        #~ ret = self.network.controller.begin_command_request_node_neigbhor_update(node_id)
        #~ self.assertTrue(ret)
        #~ current = None
        #~ for i in range(0,SLEEP*2):
            #~ #print("self.ctrl_command_result = %s" % self.ctrl_command_result)
            #~ if self.ctrl_command_result != None and self.ctrl_command_result != "InProgress":
                #~ current = self.ctrl_command_result
                #~ print(current)
                #~ self.ctrl_command_result = None
                #~ break
            #~ else:
                #~ time.sleep(1.0)
        #~ self.assertEqual(current, "Completed")
#~
    #~ def test_220_command_request_node_neigbhor_update_controller(self):
        #~ self.wipTest()
        #~ node_id = self.network.controller.node_id
        #~ ret = self.network.controller.begin_command_request_node_neigbhor_update(node_id)
        #~ self.assertTrue(ret)
        #~ current = None
        #~ for i in range(0,SLEEP*2):
            #~ #print("self.ctrl_command_result = %s" % self.ctrl_command_result)
            #~ if self.ctrl_command_result != None and self.ctrl_command_result != "InProgress":
                #~ current = self.ctrl_command_result
                #~ #print(current)
                #~ self.ctrl_command_result = None
                #~ break
            #~ else:
                #~ time.sleep(1.0)
        #~ self.assertEqual(current, "Completed")
#~
    #~ def test_910_command_command_replication_send(self):
        #~ self.wipTest()
        #~ node_id = max(self.network.nodes.keys())
        #~ ret = self.network.controller.begin_command_replication_send(node_id)
        #~ self.assertTrue(ret)
        #~ current = None
        #~ for i in range(0,SLEEP*2):
            #~ #print("self.ctrl_command_result = %s" % self.ctrl_command_result)
            #~ if self.ctrl_command_result != None and self.ctrl_command_result != "InProgress":
                #~ current = self.ctrl_command_result
                #~ print(current)
                #~ self.ctrl_command_result = None
                #~ break
            #~ else:
                #~ time.sleep(1.0)
        #~ self.assertEqual(current, "Completed")
#~
    #~ def test_920_command_command_replication_send_controller(self):
        #~ self.wipTest()
        #~ node_id = self.network.controller.node_id
        #~ ret = self.network.controller.begin_command_replication_send(node_id)
        #~ self.assertTrue(ret)
        #~ current = None
        #~ for i in range(0,SLEEP*2):
            #~ #print("self.ctrl_command_result = %s" % self.ctrl_command_result)
            #~ if self.ctrl_command_result != None and self.ctrl_command_result != "InProgress":
                #~ current = self.ctrl_command_result
                #~ print(current)
                #~ self.ctrl_command_result = None
                #~ break
            #~ else:
                #~ time.sleep(1.0)
        #~ self.assertEqual(current, "Completed")

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
