# -*- coding: utf-8 -*-
"""
.. module:: openzwave.network

This file is part of **python-openzwave** project http://code.google.com/p/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave wrapper

.. moduleauthor:: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>

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

from collections import namedtuple
import thread
import time
from louie import dispatcher, All
import logging
import libopenzwave
import openzwave
from openzwave.object import ZWaveException, ZwaveObject, NullLoggingHandler
from openzwave.controller import ZWaveController
from openzwave.node import ZWaveNode

logging.getLogger('openzwave').addHandler(logging.NullHandler())

class ZWaveNetwork(ZwaveObject):
    '''
    The network objet = homeid.
    It contains a reference to the manager
    '''
    SIGNAL_DRIVER_READY = 'driverReady'
    SIGNAL_NODE_ADDED = 'nodeAdded'
    SIGNAL_NODE_READY = 'nodeReady'
    SIGNAL_SYSTEM_READY = 'systemReady'
    SIGNAL_VALUE_CHANGED = 'valueChanged'

    ignoreSubsequent = True

    def __init__(self, networkId, devicePath="/dev/zwave", userPath="."\
        , configPath=None, log=None, options="--logging true"):
        '''
        Initialize zwave network

        :param networkId: ID of the network
        :type networkId: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork
        '''
        self._manager = libopenzwave.PyManager()

        self.log = log
        #if self.log is None:
        #    self.log = logging.getLogger(__name__)
        #    self.log.addHandler(NullLoggingHandler())

        super(ZWaveNetwork, self).__init__(networkId,self)

        self._controller = ZWaveController( self, 1, devicePath=devicePath, userPath=userPath\
        , configPath=configPath, options=options)

        logging.debug("Create object network")

        self._nodes = dict()

        self._started = False

        options = libopenzwave.PyOptions()
        options.create(self._controller.libraryConfigPath, self._controller.libraryUserPath,\
          self._controller.optionsManager)
        options.lock()

        self._manager = libopenzwave.PyManager()
        self._manager.create()
        self._manager.addWatcher(self.zwcallback)
        self._manager.addDriver(device)

    @property
    def homeId(self):
        """
        The homeId of the network.
        :rtype: int
        """
        return self._objectId

    @homeId.setter
    def homeId(self, value):
        """
        Set the homeId of the network.
        :rtype: int
        """
        self._objectId = value

    @property
    def manager(self):
        """
        The manager of the network.
        :rtype:
        """
        return self._manager

    @property
    def controller(self):
        """
        The controller of the network.
        :rtype:
        """
        return self._controller

    @controller.setter
    def controller(self, value):
        """
        The controller of the network.
        :rtype:
        """
        if type(value) == type(ZWaveController) or value == None:
            self._controller = value
        else:
            raise ZWaveException("Can't update controller. Bad object type %s" % type(value))

    @property
    def nodes(self):
        """
        The nodes of the network.
        :rtype: list()
        """
        return self._nodes

    @property
    def nodesCount(self):
        """
        The nodes count of the network.
        :rtype: int
        """
        return len(self.nodes)

    @property
    def sleepingNodesCount(self):
        """
        The count of sleeping nodes on the network.
        :rtype: int
        """
        retval = 0
        for node in self.nodes:
            if node.isSleeping:
                retval += 1
        return retval - 1 if retval > 0 else 0

    def zwcallback(self, args):
        try:
            return self._zwcallback(args)
        except:
            import sys, traceback
            logging.error(traceback.format_exception(*sys.exc_info()))
            raise

    def _zwcallback(self, args):
        '''
        Callback Handler

        @param args: callback dict
        '''

        notifyType = args['notificationType']
        logging.debug('\n%s\n%s (node %s)\n%s', '-' * 30, notifyType, args['nodeId'], '-' * 30)
        if notifyType == 'DriverReady':
            self._handleDriverReady(args)
        elif notifyType in ('NodeAdded', 'NodeNew'):
            self._handleNodeChanged(args)
        elif notifyType == 'ValueAdded':
            self._handleValueAdded(args)
        elif notifyType == 'ValueChanged':
            self._handleValueChanged(args)
        elif notifyType == 'NodeQueriesComplete':
            self._handleNodeQueryComplete(args)
        elif notifyType in ('AwakeNodesQueried', 'AllNodesQueried'):
            self._handleInitializationComplete(args)
        else:
            logging.debug('Skipping unhandled notification type [%s]', notifyType)

        # TODO: Optional command classes are not being reported via wrapper! Example: Node(2)::CommandClass 0x2b (COMMAND_CLASS_SCENE_ACTIVATION) - NOT REQUIRED
        # TODO: handle event
        # TODO: handle group change
        # TODO: handle value removed
        # TODO: handle node removed
        # TODO: handle config params

    def _handleDriverReady(self, args):
        '''
        Called once OZW has queried capabilities and determined startup values.  HomeID
        and NodeID of controller are known at this point.
        '''
        self.homeId = args['homeId']
        self._controller.node = ZWaveNode(args['nodeId'], network=self)
        self.nodes = list()
        self.nodes.append(self._controller.node)

        logging.info('Driver ready using library %s' % self._controller.libraryDescription )
        logging.info('homeId 0x%0.8x, controller node id is %d' % (self.homeId, self._controller.nodeId))

    def _handleNodeQueryComplete(self, args):
        '''
        Called when a node query is complete.
        '''
        self.nodes[args['nodeId']].outdated = True
        logging.info('Z-Wave Device Node %s is ready.' % (args['nodeId']))
        #dispatcher.send(self.SIGNAL_NODE_READY, **{'homeId': self._homeId, 'nodeId': args['nodeId']})

    def _handleNodeChanged(self, args):
        '''
        Called when a node is changed or added.
        '''
        if args['nodeId'] in self.nodes :
            self.nodes.outdated = True
        else :
            newnode = ZWaveNode(args['nodeId'], network=self)
            newnode.lastUpdate = datetime.datetime.today()
            self.nodes.append(newnode)
        #dispatcher.send(self.SIGNAL_NODE_ADDED, **{'homeId': args['homeId'], 'nodeId': args['nodeId']})

    def _getValueNode(self, homeId, nodeId, valueId):
        node = self._getNode(homeId, nodeId)
        if node is None:
            raise ZWaveWrapperException('Value notification received before node creation (homeId %.8x, nodeId %d)' % (homeId, nodeId))
        vid = valueId['id']
        if node._values.has_key(vid):
            retval = node._values[vid]
        else:
            retval = ZWaveValueNode(homeId, nodeId, valueId)
            self._log.debug('Created new value node with homeId %0.8x, nodeId %d, valueId %s', homeId, nodeId, valueId)
            node._values[vid] = retval
        return retval

    def _handleValueAdded(self, args):
        homeId = args['homeId']
        controllerNodeId = args['nodeId']
        valueId = args['valueId']
        node = self._fetchNode(homeId, controllerNodeId)
        node._lastUpdate = time.time()
        valueNode = self._getValueNode(homeId, controllerNodeId, valueId)
        valueNode.update(args)

    def _handleValueChanged(self, args):
        homeId = args['homeId']
        controllerNodeId = args['nodeId']
        valueId = args['valueId']
        node = self._fetchNode(homeId, controllerNodeId)
        node._sleeping = False
        node._lastUpdate = time.time()
        valueNode = self._getValueNode(homeId, controllerNodeId, valueId)
        valueNode.update(args)
        if self._initialized:
            dispatcher.send(self.SIGNAL_VALUE_CHANGED, **{'homeId': homeId, 'nodeId': controllerNodeId, 'valueId': valueId})

    def _updateNodeCommandClasses(self, node):
        '''Update node's command classes'''
        classSet = list()()
        for cls in PyManager.COMMAND_CLASS_DESC:
            if self._manager.getNodeClassInformation(node._homeId, node._nodeId, cls):
                classSet.add(cls)
        node._commandClasses = classSet
        self._log.debug('Node [%d] command classes are: %s', node._nodeId, node._commandClasses)
        # TODO: add command classes as string

    def _handleInitializationComplete(self, args):
        logging.debug('Controller capabilities are: %s', self.manager.controller.capabilities)
        logging.info("Initialization completed.  Found %s Z-Wave Device Nodes (%s sleeping)" % (self.nodesCount, self.sleepingNodesCount))
        self._initialized = True
        #dispatcher.send(self.SIGNAL_SYSTEM_READY, **{'homeId': self._homeId})
        self.manager.writeConfig(self._homeId)
        # TODO: write config on shutdown as well

    def setNodeOn(self, node):
        self._log.debug('Requesting setNodeOn for node {0}'.format(node.id))
        self._manager.setNodeOn(node.homeId, node.id)

    def setNodeOff(self, node):
        self._log.debug('Requesting setNodeOff for node {0}'.format(node.id))
        self._manager.setNodeOff(node.homeId, node.id)

    def setNodeLevel(self, node, level):
        self._log.debug('Requesting setNodeLevel for node {0} with new level {1}'.format(node.id, level))
        self._manager.setNodeLevel(node.homeId, node.id, level)

    def getCommandClassName(self, commandClassCode):
        return PyManager.COMMAND_CLASS_DESC[commandClassCode]

    def getCommandClassCode(self, commandClassName):
        for k, v in PyManager.COMMAND_CLASS_DESC.iteritems():
            if v == commandClassName:
                return k
        return None

# commands:
# - refresh node
# - request node state
# - request config param/request all config params
# - set node level
# - set node on/off
# - switch all on/off
# - add node, remove node (needs command support)

# editing:
# - add association, remove association
# - set config param
# - set node manufacturer name
# - set node name
# - set node location
# - set node product name
# - set poll interval
# - set wake up interval (needs command support)

# questions:
# - can powerlevel be queried directly? See PowerLevel.cpp in command classes
# - need more detail about notification events!
# - what is COMMAND_CLASS_HAIL used for?
# - what is COMMAND_CLASS_INDICATOR used for?
# - wake up duration sent via COMMAND_CLASS_WAKE_UP

#   initialization callback sequence:
#
#   [driverReady]
#
#   [nodeAdded] <-------------------------+ This cycle is extremely quick, well under one second.
#       [nodeProtocolInfo]                |
#       [nodeNaming]                      |
#       [valueAdded] <---------------+    |
#                                    |    |
#       {REPEATS FOR EACH VALUE} ----+    |
#                                         |
#       [group] <--------------------+    |
#                                    |    |
#       {REPEATS FOR EACH GROUP} ----+    |
#                                         |
#   {REPEATS FOR EACH NODE} --------------+
#
#   [? (no notification)] <---------------+ (no notification announces the beginning of this cycle)
#                                         |
#       [valueChanged] <-------------+    | This cycle can take some time, especially if some nodes
#                                    |    | are sleeping or slow to respond.
#       {REPEATS FOR EACH VALUE} ----+    |
#                                         |
#       [group] <--------------------+    |
#                                    |    |
#       {REPEATS FOR EACH GROUP} ----+    |
#                                         |
#   [nodeQueriesComplete]                 |
#                                         |
#   {REPEATS FOR EACH NODE} --------------+
#
#   [awakeNodesQueried] or [allNodesQueried] (with nodeId 255)
