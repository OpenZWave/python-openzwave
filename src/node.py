# -*- coding: utf-8 -*-
"""
.. module:: openzwave.node

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

import libopenzwave
from collections import namedtuple
import thread
import time
import logging
from openzwave.object import ZwaveObject
from openzwave.group import ZWaveGroup

logging.getLogger('openzwave').addHandler(logging.NullHandler())

class ZWaveNode(ZwaveObject):
    '''
    Represents a single Node within the Z-Wave Network
    '''

    def __init__(self, nodeId, network ):
        '''
        Initialize zwave node

        :param nodeId: ID of the node
        :type nodeId: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork
        '''
        logging.debug("Create object node (nodeId:%s)" % (nodeId))
        super(ZWaveNode, self).__init__(nodeId, network)
        self._commandClasses = list()
        self.cacheProperty(self._commandClasses)
        self._values = dict()

        self._isSleeping = False
        self._isLocked = False

        self._name = None
        self.cacheProperty(lambda: self.name)
        self._location = None
        self.cacheProperty(lambda: self.location)
        self._productName = None
        self.cacheProperty(lambda: self.productName)
        self._manufacturerId = None
        self.cacheProperty(lambda: self.manufacturerId)
        self._manufacturerName = None
        self.cacheProperty(lambda: self.manufacturerName)
        self._productId = None
        self.cacheProperty(lambda: self.productId)
        self._productType = None
        self.cacheProperty(lambda: self.productType)

        self._isNodeRoutingDevice = False
        self.cacheProperty(lambda: self.isNodeRoutingDevice)
        self._isNodeListeningDevice = False
        self.cacheProperty(lambda: self.isNodeListeningDevice)
        self._isNodeFrequentListeningDevice = False
        self.cacheProperty(lambda: self.isNodeFrequentListeningDevice)
        self._isNodeSecurityDevice = False
        self.cacheProperty(lambda: self.isNodeSecurityDevice)
        self._isNodeBeamingDevice = False
        self.cacheProperty(lambda: self.isNodeBeamingDevice)

        self._generic = 0
        self.cacheProperty(lambda: self.generic)
        self._basic = 0
        self.cacheProperty(lambda: self.basic)
        self._specific = 0
        self.cacheProperty(lambda: self.specific)
        self._security = 0
        self.cacheProperty(lambda: self.security)
        self._version = 0
        self.cacheProperty(lambda: self.version)

        self._commandClasses = list()
        self.cacheProperty(lambda: self.commandClasses)
        self._neighbors = list()
        self.cacheProperty(lambda: self.neighbors)
        self._numGroups = list()
        self.cacheProperty(lambda: self.numGroups)
        self._groups = list()
        self.cacheProperty(lambda: self.groups)

    @property
    def name(self):
        """
        The name of the node.
        :rtype: str
        """
        if self.isOutdated(lambda: self.name):
            self._name = self._network.manager.getNodeName(self.homeId, self.objectId)
            self.update(lambda: self.name)
        return self._name

    @name.setter
    def name(self,value):
        """
        Set the name of the node.
        """
        self._network.manager.setNodeName(self.homeId, self.objectId, value)
        self.outdate(lambda: self.name)

    @property
    def location(self):
        """
        The location of the node.
        :rtype: str
        """
        if self.isOutdated(lambda: self.location):
            self._location = self._network.manager.getNodeLocation(self.homeId, self.objectId)
            self.update(lambda: self.location)
        return self._location

    @location.setter
    def location(self,value):
        """
        Set the location of the node.
        :param value: The new location of the node
        :type value: str
        """
        self._network.manager.setNodeLocation(self.homeId, self.objectId, value)
        self.outdate(lambda: self.location)

    @property
    def productName(self):
        """
        The product name of the node.
        :rtype: str
        """
        if self.isOutdated(lambda: self.productName):
            self._productName = self._network.manager.getNodeProductName(self.homeId, self.objectId)
            self.update(lambda: self.productName)
        return self._productName

    @productName.setter
    def productName(self, value):
        """
        Set the product name of the node.
        :param value: The new name of the product
        :type value: str
        """
        self._network.manager.setNodeProductName(self.homeId, self.objectId, value)
        self.outdate(lambda: self.productName)

    @property
    def productType(self):
        """
        The product type of the node.
        :rtype: int
        """
        if self.isOutdated(lambda: self.productType):
            self._productType = self._network.manager.getNodeProductType(self.homeId, self.objectId)
            self.update(lambda: self.productType)
        return self._productType

    @property
    def productId(self):
        """
        The product Id of the node.
        :rtype: int
        """
        if self.isOutdated(lambda: self.productId):
            self._productId = self._network.manager.productId(self.homeId, self.objectId)
            self.update(lambda: self.productId)
        return self._productId

    @property
    def capabilities(self):
        """
        The capabilities of the node.
        :rtype: list()
        """
        caps = list()
        if self.isNodeRoutingDevice(): caps.add('routing')
        if self.isNodeListeningDevice(): caps.add('listening')
        if self.isNodeFrequentListeningDevice(): caps.add('frequent')
        if self.isNodeSecurityDevice(): caps.add('security')
        if self.isNodeBeamingDevice(): caps.add('beaming')
        return caps

    @property
    def commandClasses(self):
        """
        The commandClasses of the node.
        :rtype: list()
        """
        self._commandClasses = list()
        if self.isOutdated(lambda: self.commandClasses):
            for cls in self._network.manager.COMMAND_CLASS_DESC:
                if self._network.manager.getNodeClassInformation(self.homeId, self.objectId, cls):
                    self._commandClasses.add(cls)
            self.update(lambda: self.neighbors)
        return self._commandClasses

    @property
    def neighbors(self):
        """
        The neighbors of the node.
        :rtype: list()
        """
        if self.isOutdated(lambda: self.neighbors):
            self._neighbors = self._network.manager.getNodeNeighbors(self.homeId, self.objectId)
            self.update(lambda: self.neighbors)
        return self._neighbors

    @property
    def numGroups(self):
        """
        Gets the number of association groups reported by this node.
        :rtype: list()
        """
        if self.isOutdated(lambda: self.numGroups):
            self._numGroups = self._network.manager.getNodeNeighbors(self.homeId, self.objectId)
            self.update(lambda: self.numGroups)
        return self._numGroups

    @property
    def groups(self):
        """
        The groups of the node.
        :rtype: list()
        """
        node._groups = list()
        for i in range(0, self.numGroups()):
            node._groups.append(ZWaveGroup(i,network=self._network))
        return node._groups

    @property
    def values(self):
        """
        The values of the node.
        :rtype: list()()
        """

    @property
    def manufacturerId(self):
        """
        The manufacturer id of the node.
        :rtype: int
        """
        if self.isOutdated(lambda: self.manufacturerId):
            self._manufacturerId = self._network.manager.getNodeManufacturerId(self.homeId, self.objectId)
            self.update(lambda: self.manufacturerId)
        return self._manufacturerId

    @property
    def manufacturerName(self):
        """
        The manufacturer name of the node.
        :rtype: str
        """
        if self.isOutdated(lambda: self.manufacturerName):
            self._manufacturerName = self._network.manager.getNodeManufacturerName(self.homeId, self.objectId)
            self.update(lambda: self.manufacturerName)
        return self._manufacturerName

    @manufacturerName.setter
    def manufacturerName(self,value):
        """
        Set the manufacturer name of the node.
        :param value: The new manufacturer name of the node
        :type value: str
        """
        self._network.manager.setNodeManufacturerName(self.homeId, self.objectId, value)
        self.outdate(lambda: self.manufacturerName)

    @property
    def generic(self):
        """
        The generic type of the node.
        :rtype: int
        """
        if self.isOutdated(lambda: self.generic):
            self._generic = self._network.manager.getNodeGeneric(self.homeId, self.objectId)
            self.update(lambda: self.generic)
        return self._generic

    @property
    def basic(self):
        """
        The basic type of the node.
        :rtype: int
        """
        if self.isOutdated(lambda: self.basic):
            self._basic = self._network.manager.getNodeBasic(self.homeId, self.objectId)
            self.update(lambda: self.basic)
        return self._basic

    @property
    def specific(self):
        """
        The specific type of the node.
        :rtype: int
        """
        if self.isOutdated(lambda: self.specific):
            self._specific = self._network.manager.getNodeSpecific(self.homeId, self.objectId)
            self.update(lambda: self.specific)
        return self._specific

    @property
    def security(self):
        """
        The security type of the node.
        :rtype: int
        """
        if self.isOutdated(lambda: self.security):
            self._security = self._network.manager.getNodeSecurity(self.homeId, self.objectId)
            self.update(lambda: self.security)
        return self._security

    @property
    def version(self):
        """
        The version of the node.
        :rtype: int
        """
        if self.isOutdated(lambda: self.version):
            self._version = self._network.manager.getNodeVersion(self.homeId, self.objectId)
            self.update(lambda: self.version)
        return self._version

    @property
    def isListeningDevice(self):
        """
        Is this node a listening device.
        :rtype: bool
        """
        if self.isOutdated(lambda: self.isListeningDevice):
            self._isListeningDevice = self._network.manager.isNodeListeningDevice(self.homeId, self.objectId)
            self.update(lambda: self.isListeningDevice)
        return self._isListeningDevice

    @property
    def isBeamingDevice(self):
        """
        Is this node a beaming device.
        :rtype: bool
        """
        if self.isOutdated(lambda: self.isBeamingDevice):
            self._isBeamingDevice = self._network.manager.isNodeBeamingDevice(self.homeId, self.objectId)
            self.update(lambda: self.isBeamingDevice)
        return self._isBeamingDevice

    @property
    def isFrequentListeningDevice(self):
        """
        Is this node a frequent listening device.
        :rtype: bool
        """
        if self.isOutdated(lambda: self.isFrequentListeningDevice):
            self._isFrequentListeningDevice = self._network.manager.isNodeFrequentListeningDevice(self.homeId, self.objectId)
            self.update(lambda: self.isFrequentListeningDevice)
        return self._isFrequentListeningDevice

    @property
    def isSecurityDevice(self):
        """
        Is this node a security device.
        :rtype: bool
        """
        if self.isOutdated(lambda: self.isSecurityDevice):
            self._isSecurityDevice = self._network.manager.isNodeSecurityDevice(self.homeId, self.objectId)
            self.update(lambda: self.isSecurityDevice)
        return self._isSecurityDevice

    @property
    def isRoutingDevice(self):
        """
        Is this node a routing device.
        :rtype: bool
        """
        if self.isOutdated(lambda: self.isRoutingDevice):
            self._isRoutingDevice = self._network.manager.isNodeRoutingDevice(self.homeId, self.objectId)
            self.update(lambda: self.isRoutingDevice)
        return self._isRoutingDevice

    @property
    def isPrimaryController(self):
        """
        Is this node a primary controller of the network.
        :rtype: bool
        """
        if self.isOutdated(lambda: self.isPrimaryController):
            self._isPrimaryController = self._network.manager.isPrimaryController(self.homeId)
            self.update(lambda: self.isPrimaryController)
        return self._isPrimaryController

    @property
    def isStaticUpdateController(self):
        """
        Is this controller a static update controller (SUC).
        :rtype: bool
        """
        if self.isOutdated(lambda: self.isStaticUpdateController):
            self._isStaticUpdateController = self._network.manager.isStaticUpdateController(self.homeId)
            self.update(lambda: self.isStaticUpdateController)
        return self._isStaticUpdateController

    @property
    def isBridgeController(self):
        """
        Is this controller using the bridge controller library.
        :rtype: bool
        """
        if self.isOutdated(lambda: self.isBridgeController):
            self._isBridgeController = self._network.manager.isBridgeController(self.homeId)
            self.update(lambda: self.isBridgeController)
        return self._isBridgeController

    @property
    def isLocked(self):
        """
        Is this node locked.
        :rtype: bool
        """
        return self._isLocked

    @isLocked.setter
    def isLocked(self, value):
        """
        Set if this node is locked.
        :rtype: bool
        """
        self._isLocked = value

    @property
    def isSleeping(self):
        """
        Is this node sleeping.
        :rtype: bool
        """
        return self._isSleeping

    @isSleeping.setter
    def isSleeping(self, value):
        """
        Set if this node is sleeping.
        :rtype: bool
        """
        self._isSleeping = value

    @property
    def level(self):
        """
        The level of the node.
        Todo
        """
        values = self._getValuesForCommandClass(0x26)  # COMMAND_CLASS_SWITCH_MULTILEVEL
        if values:
            for value in values:
                vdic = value.valueData
                if vdic and vdic.has_key('type') and vdic['type'] == 'Byte' and vdic.has_key('value'):
                    return int(vdic['value'])
        return 0

    @property
    def isOn(self):
        """
        Is this node On.
        Todo
        """
        values = self._getValuesForCommandClass(0x25)  # COMMAND_CLASS_SWITCH_BINARY
        if values:
            for value in values:
                vdic = value.valueData
                if vdic and vdic.has_key('type') and vdic['type'] == 'Bool' and vdic.has_key('value'):
                    return vdic['value'] == 'True'
        return False

    @property
    def batteryLevel(self):
        """
        The battery level of this node.
        Todo
        """
        values = self._getValuesForCommandClass(0x80)  # COMMAND_CLASS_BATTERY
        if values:
            for value in values:
                vdic = value.valueData
                if vdic and vdic.has_key('type') and vdic['type'] == 'Byte' and vdic.has_key('value'):
                    return int(vdic['value'])
        return -1

    @property
    def signalStrength(self):
        """
        The signal strenght of this node.
        Todo
        """
        return 0

    def refreshInfo(self, node):
        """
        Request a refresh for node.
        """
        self._network.manager.refreshNodeInfo(self.homeId, self.objectId)
        self.outdated = True

    def requestConfig(self):
        """
        Request config parameters for node.
        """
        logging.debug('Requesting config params for node [%d]', self.objectId)
        self._network.manager.requestAllConfigParams(self.homeId, self.objectId)
        self.outdated = True

    def _getValuesForCommandClass(self, classId):
        """
        Get values from a command class.
        Todo
        """
        retval = list()
        classStr = PyManager.COMMAND_CLASS_DESC[classId]
        for value in self._values.itervalues():
            vdic = value.valueData
            if vdic and vdic.has_key('commandClass') and vdic['commandClass'] == classStr:
                retval.append(value)
        return retval

    def hasCommandClass(self, commandClass):
        """
        Check that this node use this commandClass.
        Todo
        """
        return commandClass in self._commandClasses

        # decorator?
        #self._batteryLevel = None # if COMMAND_CLASS_BATTERY
        #self._level = None # if COMMAND_CLASS_SWITCH_MULTILEVEL - maybe state? off - ramped - on?
        #self._powerLevel = None # hmm...
        # sensor multilevel?  instance/index
        # meter?
        # sensor binary?


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
