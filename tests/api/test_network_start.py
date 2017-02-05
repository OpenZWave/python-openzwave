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
import libopenzwave
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork, ZWaveNetworkSingleton
from openzwave.option import ZWaveOption, ZWaveOptionSingleton
from tests.common import pyozw_version
from tests.common import SLEEP
from tests.api.common import TestApi
from tests.common import TestPyZWave

class TestNetworkStartStop(TestPyZWave):

    @classmethod
    def setUpClass(self):
        super(TestNetworkStartStop, self).setUpClass()
        self.options = None
        self.network = None

    @classmethod
    def tearDownClass(self):
        if self.network is not None:
            self.network.stop()
            self.network.destroy()
            self.network = None
        super(TestNetworkStartStop, self).tearDownClass()

    def driver_ready_message(self, network):
        self.driver_ready = True

    def driver_removed_message(self, network):
        self.driver_removed = True

    def network_started_message(self, network):
        self.network_started = True

    def network_stopped_message(self, network):
        self.network_stopped = True

    def test_000_network_start_stop(self):
        self.driver_ready = False
        self.driver_removed = False
        self.network_started = False
        self.network_stopped = False
        self.options = ZWaveOption(device=self.device, user_path=self.userpath)
        self.options.set_log_file("OZW_Log.log")
        self.options.set_append_log_file(False)
        self.options.set_console_output(False)
        self.options.set_save_log_level("Debug")
        self.options.set_logging(True)
        self.options.lock()
        dispatcher.connect(self.driver_ready_message, ZWaveNetwork.SIGNAL_DRIVER_READY)
        dispatcher.connect(self.driver_removed_message, ZWaveNetwork.SIGNAL_DRIVER_REMOVED)
        dispatcher.connect(self.driver_ready_message, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
        dispatcher.connect(self.driver_removed_message, ZWaveNetwork.SIGNAL_DRIVER_REMOVED)
        self.network = ZWaveNetwork(self.options)
        for i in range(0, SLEEP):
            if self.network.state>=self.network.STATE_STARTED:
                break
            else:
                time.sleep(1.0)
        time.sleep(5.0)
        self.assertTrue(self.driver_ready)
        #~ time.sleep(5.0)
        #~ self.assertTrue(self.network_started)
        self.network.stop()
        for i in range(0, SLEEP):
            if self.network.state==self.network.STATE_STOPPED:
                break
            else:
                time.sleep(1.0)
        self.assertEqual(self.network.state, self.network.STATE_STOPPED)
        #~ self.assertTrue(self.network_stopped)
        #~ self.assertTrue(self.driver_removed)

    def test_010_network_start_stop_start_stop(self):
        self.driver_ready = False
        self.driver_removed = False
        self.options = ZWaveOption(device=self.device, user_path=self.userpath)
        self.options.set_log_file("OZW_Log.log")
        self.options.set_append_log_file(False)
        self.options.set_console_output(False)
        self.options.set_save_log_level("Debug")
        self.options.set_logging(True)
        self.options.lock()
        dispatcher.connect(self.driver_ready_message, ZWaveNetwork.SIGNAL_DRIVER_READY)
        dispatcher.connect(self.driver_removed_message, ZWaveNetwork.SIGNAL_DRIVER_REMOVED)
        dispatcher.connect(self.driver_ready_message, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
        dispatcher.connect(self.driver_removed_message, ZWaveNetwork.SIGNAL_DRIVER_REMOVED)
        self.network = ZWaveNetwork(self.options)
        for i in range(0, SLEEP):
            if self.network.state>=self.network.STATE_STARTED:
                break
            else:
                time.sleep(0.1)
        self.network.stop()
        for i in range(0, SLEEP*10):
            if self.network.state==self.network.STATE_STOPPED:
                break
            else:
                time.sleep(0.1)
        self.assertEqual(self.network.state, self.network.STATE_STOPPED)
        self.network.start()
        for i in range(0, SLEEP*10):
            if self.network.state>=self.network.STATE_STARTED:
                break
            else:
                time.sleep(0.1)
        self.network.stop()
        for i in range(0, SLEEP*10):
            if self.network.state==self.network.STATE_STOPPED:
                break
            else:
                time.sleep(0.1)
        self.assertEqual(self.network.state, self.network.STATE_STOPPED)
        #self.assertTrue(self.driver_removed)

    def test_100_network_start_stop_singleton(self):
        self.wipTest()
        self.driver_ready = False
        self.driver_removed = False
        self.options = ZWaveOptionSingleton(device=self.device, user_path=self.userpath)
        self.options.set_log_file("OZW_Log.log")
        self.options.set_append_log_file(False)
        self.options.set_console_output(False)
        self.options.set_save_log_level("Debug")
        self.options.set_logging(True)
        self.options.lock()
        dispatcher.connect(self.driver_ready_message, ZWaveNetwork.SIGNAL_DRIVER_READY)
        dispatcher.connect(self.driver_removed_message, ZWaveNetwork.SIGNAL_DRIVER_REMOVED)
        self.network = ZWaveNetworkSingleton(self.options)
        for i in range(0, SLEEP):
            if self.network.state>=self.network.STATE_AWAKED:
                break
            else:
                time.sleep(1.0)
        self.assertTrue(self.driver_ready)
        network2 = ZWaveNetworkSingleton(self.options, autostart=False)
        self.assertIs(self.network, network2)
        self.network.stop()
        for i in range(0, SLEEP):
            if self.network.state==self.network.STATE_STOPPED:
                break
            else:
                time.sleep(1.0)
        self.assertEqual(self.network.state, self.network.STATE_STOPPED)

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
