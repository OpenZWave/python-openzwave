# -*- coding: utf-8 -*-

"""
.. module:: tests

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave API

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

import sys, os
import time
import unittest
import threading
import logging
import json as mjson
import shutil
from nose.plugins.skip import SkipTest
import libopenzwave
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
#from openzwave.network import ZWaveNetworkSingleton as ZWaveNetwork
from openzwave.option import ZWaveOption
#from openzwave.option import ZWaveOptionSingleton as ZWaveOption

import sys
if sys.hexversion >= 0x3000000:
    from pydispatch import dispatcher
else:
    from louie import dispatcher

from tests.common import SLEEP
from tests.common import TestPyZWave

class TestApi(TestPyZWave):
    """
    Parent test class for api
    """

    @classmethod
    def setUpClass(self):
        super(TestApi, self).setUpClass()
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
        super(TestApi, self).tearDownClass()
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

    def ctrl_message(self, network, controller, node, node_id,
            state_int, state, state_full,
            error_int, error, error_full,):
        self.ctrl_command_result = state
        print "catched"

    def node_update(self, network, node):
        self.node_result = node


