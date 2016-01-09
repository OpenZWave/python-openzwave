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

import sys, os, shutil, stat
import time
import unittest
from pprint import pprint
import datetime
import random
import socket
import libopenzwave
from common import TestLib
import re
from tests.common import pyozw_version
from six import string_types

import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        """NullHandler logger for python 2.6"""
        def emit(self, record):
            pass
logger = logging.getLogger('test')


class TestInit(TestLib):

    SIGNAL_NETWORK_FAILED = 'NetworkFailed'
    SIGNAL_NETWORK_STARTED = 'NetworkStarted'
    SIGNAL_NETWORK_READY = 'NetworkReady'
    SIGNAL_NETWORK_STOPPED = 'NetworkStopped'
    SIGNAL_NETWORK_RESETTED = 'DriverResetted'
    SIGNAL_NETWORK_AWAKED = 'DriverAwaked'
    SIGNAL_DRIVER_FAILED = 'DriverFailed'
    SIGNAL_DRIVER_READY = 'DriverReady'
    SIGNAL_DRIVER_RESET = 'DriverReset'
    SIGNAL_DRIVER_REMOVED = 'DriverRemoved'
    SIGNAL_GROUP = 'Group'
    SIGNAL_NODE = 'Node'
    SIGNAL_NODE_ADDED = 'NodeAdded'
    SIGNAL_NODE_EVENT = 'NodeEvent'
    SIGNAL_NODE_NAMING = 'NodeNaming'
    SIGNAL_NODE_NEW = 'NodeNew'
    SIGNAL_NODE_PROTOCOL_INFO = 'NodeProtocolInfo'
    SIGNAL_NODE_READY = 'NodeReady'
    SIGNAL_NODE_REMOVED = 'NodeRemoved'
    SIGNAL_SCENE_EVENT = 'SceneEvent'
    SIGNAL_VALUE = 'Value'
    SIGNAL_VALUE_ADDED = 'ValueAdded'
    SIGNAL_VALUE_CHANGED = 'ValueChanged'
    SIGNAL_VALUE_REFRESHED = 'ValueRefreshed'
    SIGNAL_VALUE_REMOVED = 'ValueRemoved'
    SIGNAL_POLLING_ENABLED = 'PollingEnabled'
    SIGNAL_POLLING_DISABLED = 'PollingDisabled'
    SIGNAL_CREATE_BUTTON = 'CreateButton'
    SIGNAL_DELETE_BUTTON = 'DeleteButton'
    SIGNAL_BUTTON_ON = 'ButtonOn'
    SIGNAL_BUTTON_OFF = 'ButtonOff'
    SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE = 'EssentialNodeQueriesComplete'
    SIGNAL_NODE_QUERIES_COMPLETE = 'NodeQueriesComplete'
    SIGNAL_AWAKE_NODES_QUERIED = 'AwakeNodesQueried'
    SIGNAL_ALL_NODES_QUERIED = 'AllNodesQueried'
    SIGNAL_ALL_NODES_QUERIED_SOME_DEAD = 'AllNodesQueriedSomeDead'
    SIGNAL_MSG_COMPLETE = 'MsgComplete'
    SIGNAL_NOTIFICATION = 'Notification'
    SIGNAL_CONTROLLER_COMMAND = 'ControllerCommand'
    SIGNAL_CONTROLLER_WAITING = 'ControllerWaiting'

    STATE_STOPPED = 0
    STATE_FAILED = 1
    STATE_RESETTED = 3
    STATE_STARTED = 5
    STATE_AWAKED = 7
    STATE_READY = 10

    @classmethod
    def setUpClass(self):
        super(TestLib, self).setUpClass()
        self.options = libopenzwave.PyOptions(config_path="openzwave/config", \
            user_path=self.userpath, cmd_line="--logging false")
        self.options.lock()
        self.homeid = None
        self.ready = False
        time.sleep(1.0)
        self.manager = libopenzwave.PyManager()
        self.manager.create()
        self.manager.addWatcher(self.zwcallback)
        time.sleep(1.0)
        self.manager.addDriver(self.device)
        self.nodes = {}
        time.sleep(1.0)
        self.wait_for_ready()

    @classmethod
    def tearDownClass(self):
        self.manager.removeDriver(self.device)
        self.manager.removeWatcher(self.zwcallback)
        self.manager.destroy()
        self.options.destroy()
        super(TestLib, self).tearDownClass()

    @classmethod
    def zwcallback(self, args):
        logger.debug('zwcallback args=[%s]', args)
        try:
            notify_type = args['notificationType']
            if notify_type == self.SIGNAL_DRIVER_FAILED:
                self._handle_driver_failed(args)
            elif notify_type == self.SIGNAL_DRIVER_READY:
                self._handle_driver_ready(args)
            elif notify_type == self.SIGNAL_DRIVER_RESET:
                self._handle_driver_reset(args)
            elif notify_type == self.SIGNAL_NODE_ADDED:
                self._handle_node_added(args)
            elif notify_type == self.SIGNAL_NODE_EVENT:
                self._handle_node_event(args)
            elif notify_type == self.SIGNAL_NODE_NAMING:
                self._handle_node_naming(args)
            elif notify_type == self.SIGNAL_NODE_NEW:
                self._handle_node_new(args)
            elif notify_type == self.SIGNAL_NODE_PROTOCOL_INFO:
                self._handle_node_protocol_info(args)
            elif notify_type == self.SIGNAL_NODE_READY:
                self._handleNodeReady(args)
            elif notify_type == self.SIGNAL_NODE_REMOVED:
                self._handle_node_removed(args)
            elif notify_type == self.SIGNAL_GROUP:
                self._handle_group(args)
            elif notify_type == self.SIGNAL_SCENE_EVENT:
                self._handle_scene_event(args)
            elif notify_type == self.SIGNAL_VALUE_ADDED:
                self._handle_value_added(args)
            elif notify_type == self.SIGNAL_VALUE_CHANGED:
                self._handle_value_changed(args)
            elif notify_type == self.SIGNAL_VALUE_REFRESHED:
                self._handle_value_refreshed(args)
            elif notify_type == self.SIGNAL_VALUE_REMOVED:
                self._handle_value_removed(args)
            elif notify_type == self.SIGNAL_POLLING_DISABLED:
                self._handle_polling_disabled(args)
            elif notify_type == self.SIGNAL_POLLING_ENABLED:
                self._handle_polling_enabled(args)
            elif notify_type == self.SIGNAL_CREATE_BUTTON:
                self._handle_create_button(args)
            elif notify_type == self.SIGNAL_DELETE_BUTTON:
                self._handle_delete_button(args)
            elif notify_type == self.SIGNAL_BUTTON_ON:
                self._handle_button_on(args)
            elif notify_type == self.SIGNAL_BUTTON_OFF:
                self._handle_button_off(args)
            elif notify_type == self.SIGNAL_ALL_NODES_QUERIED:
                self._handle_all_nodes_queried(args)
            elif notify_type == self.SIGNAL_ALL_NODES_QUERIED_SOME_DEAD:
                self._handle_all_nodes_queried_some_dead(args)
            elif notify_type == self.SIGNAL_AWAKE_NODES_QUERIED:
                self._handle_awake_nodes_queried(args)
            elif notify_type == self.SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE:
                self._handle_essential_node_queries_complete(args)
            elif notify_type == self.SIGNAL_NODE_QUERIES_COMPLETE:
                self._handle_node_queries_complete(args)
            elif notify_type == self.SIGNAL_MSG_COMPLETE:
                self._handle_msg_complete(args)
            elif notify_type == self.SIGNAL_NOTIFICATION:
                self._handle_notification(args)
            elif notify_type == self.SIGNAL_DRIVER_REMOVED:
                self._handle_driver_removed(args)
            elif notify_type == self.SIGNAL_CONTROLLER_COMMAND:
                self._handle_controller_command(args)
            else:
                logger.warning('Skipping unhandled notification [%s]', args)
        except:
            import sys, traceback
            logger.error('Error in manager callback : %s', traceback.format_exception(*sys.exc_info()))

    @classmethod
    def wait_for_ready(self):
        for i in range(0,15):
            if self.ready == True:
                break
            else:
                time.sleep(1.0)

    @classmethod
    def _handle_driver_failed(self, args):
        logger.warning('Z-Wave Notification DriverFailed : %s', args)

    @classmethod
    def _handle_driver_ready(self, args):
        logger.debug('Z-Wave Notification DriverReady : %s', args)
        self.homeid = args['homeId']

    @classmethod
    def _handle_driver_reset(self, args):
        logger.debug('Z-Wave Notification DriverReset : %s', args)

    @classmethod
    def _handle_driver_removed(self, args):
        logger.debug('Z-Wave Notification DriverRemoved : %s', args)

    @classmethod
    def _handle_group(self, args):
        logger.debug('Z-Wave Notification Group : %s', args)

    @classmethod
    def _handle_node(self, node):
        logger.debug('Z-Wave Notification Node : %s', node)

    @classmethod
    def _handle_node_added(self, args):
        logger.debug('Z-Wave Notification NodeAdded : %s', args)
        self.nodes[args['nodeId']] = {}

    @classmethod
    def _handle_scene_event(self, args):
        logger.debug('Z-Wave Notification SceneEvent : %s', args)

    @classmethod
    def _handle_node_event(self, args):
        logger.debug('Z-Wave Notification NodeEvent : %s', args)

    @classmethod
    def _handle_node_naming(self, args):
        logger.debug('Z-Wave Notification NodeNaming : %s', args)
        self.nodes[args['nodeId']] = {'NodeNaming' : True }

    @classmethod
    def _handle_node_new(self, args):
        logger.debug('Z-Wave Notification NodeNew : %s', args)

    @classmethod
    def _handle_node_protocol_info(self, args):
        logger.debug('Z-Wave Notification NodeProtocolInfo : %s', args)

    @classmethod
    def _handle_node_removed(self, args):
        logger.debug('Z-Wave Notification NodeRemoved : %s', args)

    @classmethod
    def _handle_essential_node_queries_complete(self, args):
        logger.debug('Z-Wave Notification EssentialNodeQueriesComplete : %s', args)

    @classmethod
    def _handle_node_queries_complete(self, args):
        logger.debug('Z-Wave Notification NodeQueriesComplete : %s', args)

    @classmethod
    def _handle_all_nodes_queried(self, args):
        logger.debug('Z-Wave Notification AllNodesQueried : %s', args)
        self.ready = True

    @classmethod
    def _handle_all_nodes_queried_some_dead(self, args):
        logger.debug('Z-Wave Notification AllNodesQueriedSomeDead : %s', args)

    @classmethod
    def _handle_awake_nodes_queried(self, args):
        logger.debug('Z-Wave Notification AwakeNodesQueried : %s', args)

    @classmethod
    def _handle_polling_disabled(self, args):
        logger.debug('Z-Wave Notification PollingDisabled : %s', args)

    @classmethod
    def _handle_polling_enabled(self, args):
        logger.debug('Z-Wave Notification PollingEnabled : %s', args)

    @classmethod
    def _handle_create_button(self, args):
        logger.debug('Z-Wave Notification CreateButton : %s', args)

    @classmethod
    def _handle_delete_button(self, args):
        logger.debug('Z-Wave Notification DeleteButton : %s', args)

    @classmethod
    def _handle_button_on(self, args):
        logger.debug('Z-Wave Notification ButtonOn : %s', args)

    @classmethod
    def _handle_button_off(self, args):
        logger.debug('Z-Wave Notification ButtonOff : %s', args)

    @classmethod
    def _handle_value_added(self, args):
        logger.debug('Z-Wave Notification ValueAdded : %s', args)

    @classmethod
    def _handle_value_changed(self, args):
        logger.debug('Z-Wave Notification ValueChanged : %s', args)

    @classmethod
    def _handle_value_refreshed(self, args):
        logger.debug('Z-Wave Notification ValueRefreshed : %s', args)

    @classmethod
    def _handle_value_removed(self, args):
        logger.debug('Z-Wave Notification ValueRemoved : %s', args)

    @classmethod
    def _handle_notification(self, args):
        logger.debug('Z-Wave Notification : %s', args)

    @classmethod
    def _handle_controller_command(self, args):
        logger.debug('Z-Wave ControllerCommand : %s', args)

    @classmethod
    def _handle_msg_complete(self, args):
        logger.debug('Z-Wave Notification MsgComplete : %s', args)

    def test_100_controller_name(self):
        #~ oldname = self.manager.getNodeName(self.homeid, 1)
        #~ self.assertTrue(isinstance(oldname, string_types))
        self.manager.setNodeName(self.homeid, 1, "test lib name")
        newname = self.manager.getNodeName(self.homeid, 1)
        self.assertTrue(isinstance(newname, string_types))

    def test_101_controller_name_accent(self):
        oldname = self.manager.getNodeName(self.homeid, 1)
        self.assertTrue(isinstance(oldname, string_types))
        self.manager.setNodeName(self.homeid, 1, "test lib name éé")
        newname = self.manager.getNodeName(self.homeid, 1)
        self.assertTrue(isinstance(newname, string_types))

    def test_110_controller_name_notification(self):
        self.nodes[1]['NodeNaming'] = False
        self.manager.setNodeName(self.homeid, 1, "test lib name")
        time.sleep(1)
        self.assertTrue(self.nodes[1]['NodeNaming'])

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
