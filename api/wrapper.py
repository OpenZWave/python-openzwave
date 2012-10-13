# -*- coding: utf-8 -*-
"""
.. module:: openzwave.wrapper

This file is part of **py-openzwave** project https://github.com/maartendamen/py-openzwave.
    :platform: Unix, Windows
    :sinopsis: openzwave wrapper

.. moduleauthor: maartendamen
.. moduleauthor: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>

License : GPL(v3)

**py-openzwave** is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

**py-openzwave** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with py-openzwave. If not, see http://www.gnu.org/licenses.

"""

import libopenzwave
from libopenzwave import PyManager
import openzwave
from openzwave import wrapper_singleton
from collections import namedtuple
import thread
import time
from louie import dispatcher, All
import logging

NamedPair = namedtuple('NamedPair', ['id', 'name'])
NodeInfo = namedtuple('NodeInfo', ['generic','basic','specific','security','version'])
GroupInfo = namedtuple('GroupInfo', ['index','label','max_associations','members'])

class ZWaveWrapperException(Exception):
    '''Exception class for ZWave Wrapper'''
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr(self.value)

# TODO: don't report controller node as sleeping
# TODO: allow value identification by device/index/instance
class ZWaveValueNode:
    '''Represents a single value for an OZW node element'''
    def __init__(self, home_id, node_id, value_data):
        '''
        Initialize value node
        @param homeid: ID of home/driver
        @param nodeid: ID of node
        @param value_data: valueId dict (see libopenzwave.pyx)
        '''
        self.home_id = home_id
        self._node_id = node_id
        self._value_data = value_data
        self._lastUpdate = None

    home_id = property(lambda self: self.home_id)
    node_id = property(lambda self: self._node_id)
    lastUpdate = property(lambda self: self._lastUpdate)
    value_data = property(lambda self: self._value_data)

    def getValue(self, key):
        return self.value_data[key] if self._value_data.has_key(key) else None

    def update(self, args):
        '''Update node value from callback arguments'''
        self._value_data = args['valueId']
        self._lastUpdate = time.time()

    def __str__(self):
        return 'home_id: [{0}]  node_id: [{1}]  value_data: {2}'.format(self.home_id, self._node_id, self._value_data)


class ZWaveNode:
    '''Represents a single device within the Z-Wave Network'''

    def __init__(self, home_id, node_id):
        '''
        Initialize zwave node
        @param home_id: ID of home/driver
        @param node_id: ID of node
        '''
        self._lastUpdate = None
        self.home_id = home_id
        self._node_id = node_id
        self._capabilities = set()
        self._commandClasses = set()
        self._neighbors = set()
        self._values = dict()
        self._name = ''
        self._location = ''
        self._manufacturer = None
        self._product = None
        self._productType = None
        self._groups = list()
        self._sleeping = True

    id = property(lambda self: self._node_id)
    name = property(lambda self: self._name)
    location = property(lambda self: self._location)
    product = property(lambda self: self._product.name if self._product else '')
    productType = property(lambda self: self._productType.name if self._productType else '')
    lastUpdate = property(lambda self: self._lastUpdate)
    home_id = property(lambda self: self.home_id)
    node_id = property(lambda self: self._node_id)
    capabilities = property(lambda self: ', '.join(self._capabilities))
    commandClasses = property(lambda self: self._commandClasses)
    neighbors = property(lambda self:self._neighbors)
    values = property(lambda self:self._values)
    manufacturer = property(lambda self: self._manufacturer.name if self._manufacturer else '')
    groups = property(lambda self:self._groups)
    isSleeping = property(lambda self: self._sleeping)
    is_locked = property(lambda self: self._getIsLocked())
    level = property(lambda self: self._getLevel())
    isOn = property(lambda self: self._getIsOn())
    batteryLevel = property(lambda self: self._getBatteryLevel())
    signalStrength = property(lambda self: self._getSignalStrength())

    def _getIsLocked(self):
        return False

    def _getValuesForCommandClass(self, classId):
        retval = list()
        classStr = PyManager.COMMAND_CLASS_DESC[classId]
        for value in self._values.itervalues():
            vdic = value.value_data
            if vdic and vdic.has_key('commandClass') and vdic['commandClass'] == classStr:
                retval.append(value)
        return retval

    def _getLevel(self):
        values = self._getValuesForCommandClass(0x26)  # COMMAND_CLASS_SWITCH_MULTILEVEL
        if values:
            for value in values:
                vdic = value.value_data
                if vdic and vdic.has_key('type') and vdic['type'] == 'Byte' and vdic.has_key('value'):
                    return int(vdic['value'])
        return 0

    def _getBatteryLevel(self):
        values = self._getValuesForCommandClass(0x80)  # COMMAND_CLASS_BATTERY
        if values:
            for value in values:
                vdic = value.value_data
                if vdic and vdic.has_key('type') and vdic['type'] == 'Byte' and vdic.has_key('value'):
                    return int(vdic['value'])
        return -1

    def _getSignalStrength(self):
        return 0

    def _getIsOn(self):
        values = self._getValuesForCommandClass(0x25)  # COMMAND_CLASS_SWITCH_BINARY
        if values:
            for value in values:
                vdic = value.value_data
                if vdic and vdic.has_key('type') and vdic['type'] == 'Bool' and vdic.has_key('value'):
                    return vdic['value'] == 'True'
        return False

    def hasCommandClass(self, commandClass):
        return commandClass in self._commandClasses

        # decorator?
        #self._batteryLevel = None # if COMMAND_CLASS_BATTERY
        #self._level = None # if COMMAND_CLASS_SWITCH_MULTILEVEL - maybe state? off - ramped - on?
        #self._powerLevel = None # hmm...
        # sensor multilevel?  instance/index
        # meter?
        # sensor binary?

class NullHandler(logging.Handler):
    '''A Null Logging Handler'''
    def emit(self, record):
        pass

class ZWaveWrapper(wrapper_singleton.Singleton):
    '''
        The purpose of this wrapper is to eliminate some of the tedium of working with
        the underlying API, which is extremely fine-grained.

        Wrapper provides a single, cohesive set of python objects representing the
        current state of the underlying ZWave network.  It is kept in sync with OZW and
        the network via callback hooks.

        Note: This version only handles a single Driver/Controller.  Modifications will
        be required in order to support more complex ZWave deployments.
    '''
    SIGNAL_DRIVER_READY = 'driverReady'
    SIGNAL_NODE_ADDED = 'nodeAdded'
    SIGNAL_NODE_READY = 'nodeReady'
    SIGNAL_SYSTEM_READY = 'systemReady'
    SIGNAL_VALUE_CHANGED = 'valueChanged'

    ignoreSubsequent = True

    def __init__(self, device, config, log=None):
        self._log = log
        if self._log is None:
            self._log = logging.getLogger(__name__)
            self._log.addHandler(NullHandler())
        self._initialized = False
        self.home_id = None
        self._controllerNodeId = None
        self._controller = None
        self._nodes = dict()
        self._library_type_name = 'Unknown'
        self._library_version = 'Unknown'
        self._device = device
        options = libopenzwave.PyOptions()
        options.create(config, '', '--logging false')
        options.lock()
        self._manager = libopenzwave.PyManager()
        self._manager.create()
        self._manager.addWatcher(self.zwcallback)
        self._manager.addDriver(device)

    controllerDescription = property(lambda self: self._getControllerDescription())
    nodeCount = property(lambda self: len(self._nodes))
    nodeCountDescription = property(lambda self: self._getNodeCountDescription())
    sleepingNodeCount = property(lambda self: self._getSleepingNodeCount())
    home_id = property(lambda self: self.home_id)
    controllerNode = property(lambda self: self._controller)
    controllerNodeId = property(lambda self: self._controllerNodeId)
    library_description = property(lambda self: self._getLibraryDescription())
    library_type_name = property(lambda self: self._library_type_name)
    library_version = property(lambda self: self._library_version)
    initialized = property(lambda self: self._initialized)
    nodes = property(lambda self: self._nodes)
    device = property(lambda self: self._device)

    def _getSleepingNodeCount(self):
        retval = 0
        for node in self._nodes.itervalues():
            if node.isSleeping:
                retval += 1
        return retval - 1 if retval > 0 else 0

    def _getLibraryDescription(self):
        if self._library_type_name and self._library_version:
            return '{0} Library Version {1}'.format(self._library_type_name, self._library_version)
        else:
            return 'Unknown'

    def _getNodeCountDescription(self):
        retval = '{0} Nodes'.format(self.nodeCount)
        sleepCount = self.sleepingNodeCount
        if sleepCount:
            retval = '{0} ({1} sleeping)'.format(retval, sleepCount)
        return retval

    def _getControllerDescription(self):
        if self._controllerNodeId:
            node = self._getNode(self.home_id, self._controllerNodeId)
            if node and node._product:
                return node._product.name
        return 'Unknown Controller'

    def zwcallback(self, args):
        try:
            return self._zwcallback(args)
        except:
            import sys, traceback
            print '\n'.join(traceback.format_exception(*sys.exc_info()))
            raise

    def _zwcallback(self, args):
        '''
        Callback Handler

        @param args: callback dict
        '''

        notifyType = args['notificationType']
        self._log.debug('\n%s\n%s (node %s)\n%s', '-' * 30, notifyType, args['node_id'], '-' * 30)
        if notifyType == 'DriverReady':
            self._handle_driver_ready(args)
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
            self._log.debug('Skipping unhandled notification type [%s]', notifyType)

        # TODO: Optional command classes are not being reported via wrapper! Example: Node(2)::CommandClass 0x2b (COMMAND_CLASS_SCENE_ACTIVATION) - NOT REQUIRED
        # TODO: handle event
        # TODO: handle group change
        # TODO: handle value removed
        # TODO: handle node removed
        # TODO: handle config params

    def _handle_driver_ready(self, args):
        '''
        Called once OZW has queried capabilities and determined startup values.  HomeID
        and NodeID of controller are known at this point.
        '''
        self.home_id = args['home_id']
        self._controllerNodeId = args['node_id']
        self._controller = self._fetchNode(self.home_id, self._controllerNodeId)
        self._library_version = self._manager.getLibraryVersion(self.home_id)
        self._library_type_name = self._manager.getLibraryTypeName(self.home_id)
        self._log.info('Driver ready.  home_id is 0x%0.8x, controller node id is %d, using %s library version %s', self.home_id, self._controllerNodeId, self._library_type_name, self._library_version)
        self._log.info('OpenZWave Initialization Begins.')
        self._log.info('The initialization process could take several minutes.  Please be patient.')
        dispatcher.send(self.SIGNAL_DRIVER_READY, **{'home_id': self.home_id, 'node_id': self._controllerNodeId})

    def _handleNodeQueryComplete(self, args):
        node = self._getNode(self.home_id, args['node_id'])
        self._updateNodeCapabilities(node)
        self._updateNodeCommandClasses(node)
        self._updateNodeNeighbors(node)
        self._updateNodeInfo(node)
        self._updateNodeGroups(node)
        self._log.info('Z-Wave Device Node {0} is ready.'.format(node.id))
        dispatcher.send(self.SIGNAL_NODE_READY, **{'home_id': self.home_id, 'node_id': args['node_id']})

    def _getNode(self, home_id, node_id):
        return self._nodes[node_id] if self._nodes.has_key(node_id) else None

    def _fetchNode(self, home_id, node_id):
        '''
        Build a new node and store it in nodes dict
        '''
        retval = self._getNode(home_id, node_id)
        if retval is None:
            retval = ZWaveNode(home_id, node_id)
            self._log.debug('Created new node with home_id 0x%0.8x, node_id %d', home_id, node_id)
            self._nodes[node_id] = retval
        return retval

    def _handleNodeChanged(self, args):
        node = self._fetchNode(args['home_id'], args['node_id'])
        node._lastUpdate = time.time()
        dispatcher.send(self.SIGNAL_NODE_ADDED, **{'home_id': args['home_id'], 'node_id': args['node_id']})

    def _getValueNode(self, home_id, node_id, valueId):
        node = self._getNode(home_id, node_id)
        if node is None:
            raise ZWaveWrapperException('Value notification received before node creation (home_id %.8x, node_id %d)' % (home_id, node_id))
        vid = valueId['id']
        if node._values.has_key(vid):
            retval = node._values[vid]
        else:
            retval = ZWaveValueNode(home_id, node_id, valueId)
            self._log.debug('Created new value node with home_id %0.8x, node_id %d, valueId %s', home_id, node_id, valueId)
            node._values[vid] = retval
        return retval

    def _handleValueAdded(self, args):
        home_id = args['home_id']
        controllerNodeId = args['node_id']
        valueId = args['valueId']
        node = self._fetchNode(home_id, controllerNodeId)
        node._lastUpdate = time.time()
        valueNode = self._getValueNode(home_id, controllerNodeId, valueId)
        valueNode.update(args)

    def _handleValueChanged(self, args):
        home_id = args['home_id']
        controllerNodeId = args['node_id']
        valueId = args['valueId']
        node = self._fetchNode(home_id, controllerNodeId)
        node._sleeping = False
        node._lastUpdate = time.time()
        valueNode = self._getValueNode(home_id, controllerNodeId, valueId)
        valueNode.update(args)
        if self._initialized:
            dispatcher.send(self.SIGNAL_VALUE_CHANGED, **{'home_id': home_id, 'node_id': controllerNodeId, 'valueId': valueId})

    def _updateNodeCapabilities(self, node):
        '''Update node's capabilities set'''
        nodecaps = set()
        if self._manager.isNodeListeningDevice(node._home_id, node._node_id): nodecaps.add('listening')
        if self._manager.isNodeRoutingDevice(node._home_id, node._node_id): nodecaps.add('routing')

        node._capabilities = nodecaps
        self._log.debug('Node [%d] capabilities are: %s', node._node_id, node._capabilities)

    def _updateNodeCommandClasses(self, node):
        '''Update node's command classes'''
        classSet = set()
        for cls in PyManager.COMMAND_CLASS_DESC:
            if self._manager.getNodeClassInformation(node._home_id, node._node_id, cls):
                classSet.add(cls)
        node._commandClasses = classSet
        self._log.debug('Node [%d] command classes are: %s', node._node_id, node._commandClasses)
        # TODO: add command classes as string

    def _updateNodeNeighbors(self, node):
        '''Update node's neighbor list'''
        # TODO: I believe this is an OZW bug, but sleeping nodes report very odd (and long) neighbor lists
        neighborstr = str(self._manager.getNodeNeighbors(node._home_id, node._node_id))
        if neighborstr is None or neighborstr == 'None':
            node._neighbors = None
        else:
            node._neighbors = sorted([int(i) for i in filter(None, neighborstr.strip('()').split(','))])

        if node.isSleeping and node._neighbors is not None and len(node._neighbors) > 10:
            self._log.warning('Probable OZW bug: Node [%d] is sleeping and reports %d neighbors; marking neighbors as none.', node.id, len(node._neighbors))
            node._neighbors = None

        self._log.debug('Node [%d] neighbors are: %s', node._node_id, node._neighbors)

    def _updateNodeInfo(self, node):
        '''Update general node information'''
        node._name = self._manager.getNodeName(node._home_id, node._node_id)
        node._location = self._manager.getNodeLocation(node._home_id, node._node_id)
        node._manufacturer = NamedPair(id=self._manager.getNodeManufacturerId(node._home_id, node._node_id), name=self._manager.getNodeManufacturerName(node._home_id, node._node_id))
        node._product = NamedPair(id=self._manager.getNodeProductId(node._home_id, node._node_id), name=self._manager.getNodeProductName(node._home_id, node._node_id))
        node._productType = NamedPair(id=self._manager.getNodeProductType(node._home_id, node._node_id), name=self._manager.getNodeType(node._home_id, node._node_id))
        node._nodeInfo = NodeInfo(
            generic = self._manager.getNodeGeneric(node._home_id, node._node_id),
            basic = self._manager.getNodeBasic(node._home_id, node._node_id),
            specific = self._manager.getNodeSpecific(node._home_id, node._node_id),
            security = self._manager.getNodeSecurity(node._home_id, node._node_id),
            version = self._manager.getNodeVersion(node._home_id, node._node_id)
        )

    def _updateNodeGroups(self, node):
        '''Update node group/association information'''
        groups = list()
        for i in range(0, self._manager.getNumGroups(node._home_id, node._node_id)):
            groups.append(GroupInfo(
                index = i,
                label = self._manager.getGroupLabel(node._home_id, node._node_id, i),
                max_associations = self._manager.getMaxAssociations(node._home_id, node._node_id, i),
                members = self._manager.getAssociations(node._home_id, node._node_id, i)
            ))
        node._groups = groups
        self._log.debug('Node [%d] groups are: %s', node._node_id, node._groups)

    def _updateNodeConfig(self, node):
        self._log.debug('Requesting config params for node [%d]', node._node_id)
        self._manager.requestAllConfigParams(node._home_id, node._node_id)

    def _handleInitializationComplete(self, args):
        controllercaps = set()
        if self._manager.is_primary_controller(self.home_id): controllercaps.add('primaryController')
        if self._manager.is_static_update_controller(self.home_id): controllercaps.add('staticUpdateController')
        if self._manager.is_bridge_controller(self.home_id): controllercaps.add('bridgeController')
        self._controllerCaps = controllercaps
        self._log.debug('Controller capabilities are: %s', controllercaps)
        for node in self._nodes.values():
            self._updateNodeCapabilities(node)
            self._updateNodeCommandClasses(node)
            self._updateNodeNeighbors(node)
            self._updateNodeInfo(node)
            self._updateNodeGroups(node)
            self._updateNodeConfig(node)
        self._initialized = True
        self._log.info("OpenZWave initialization is complete.  Found {0} Z-Wave Device Nodes ({1} sleeping)".format(self.nodeCount, self.sleepingNodeCount))
        dispatcher.send(self.SIGNAL_SYSTEM_READY, **{'home_id': self.home_id})
        self._manager.writeConfig(self.home_id)
        # TODO: write config on shutdown as well

    def refresh(self, node):
        self._log.debug('Requesting refresh for node {0}'.format(node.id))
        self._manager.refreshNodeInfo(node.home_id, node.id)

    def setNodeOn(self, node):
        self._log.debug('Requesting setNodeOn for node {0}'.format(node.id))
        self._manager.setNodeOn(node.home_id, node.id)

    def setNodeOff(self, node):
        self._log.debug('Requesting setNodeOff for node {0}'.format(node.id))
        self._manager.setNodeOff(node.home_id, node.id)

    def setNodeLevel(self, node, level):
        self._log.debug('Requesting setNodeLevel for node {0} with new level {1}'.format(node.id, level))
        self._manager.setNodeLevel(node.home_id, node.id, level)

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
#   [awakeNodesQueried] or [allNodesQueried] (with node_id 255)
