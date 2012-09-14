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

    def __init__(self, node_id, network ):
        '''
        Initialize zwave node

        :param node_id: ID of the node
        :type node_id: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork

        '''
        logging.debug("Create object node (node_id:%s)" % (node_id))
        super(ZWaveNode, self).__init__(node_id, network)
        self._command_classes = list()
        self.cache_property(self._command_classes)
        self._values = dict()

        self._is_sleeping = False
        self._is_locked = False
        self._name = None
        self.cache_property(lambda: self.name)
        self._location = None
        self.cache_property(lambda: self.location)
        self._product_name = None
        self.cache_property(lambda: self.product_name)
        self._manufacturer_id = None
        self.cache_property(lambda: self.manufacturer_id)
        self._manufacturer_name = None
        self.cache_property(lambda: self.manufacturer_name)
        self._product_id = None
        self.cache_property(lambda: self.product_id)
        self._product_type = None
        self.cache_property(lambda: self.product_type)
        self._is_routing_device = False
        self.cache_property(lambda: self.is_routing_device)
        self._is_listening_device = False
        self.cache_property(lambda: self.is_listening_device)
        self._is_frequent_listening_device = False
        self.cache_property(lambda: self.is_frequent_listening_device)
        self._is_security_device = False
        self.cache_property(lambda: self.is_node_security_device)
        self._is_beaming_device = False
        self.cache_property(lambda: self.is_beaming_device)
        self._generic = 0
        self.cache_property(lambda: self.generic)
        self._basic = 0
        self.cache_property(lambda: self.basic)
        self._specific = 0
        self.cache_property(lambda: self.specific)
        self._security = 0
        self.cache_property(lambda: self.security)
        self._version = 0
        self.cache_property(lambda: self.version)
        self._command_classes = list()
        self.cache_property(lambda: self.command_classes)
        self._neighbors = list()
        self.cache_property(lambda: self.neighbors)
        self._num_groups = list()
        self.cache_property(lambda: self.num_groups)
        self._groups = list()
        self.cache_property(lambda: self.groups)

    @property
    def name(self):
        """
        The name of the node.

        :rtype: str

        """
        if self.is_outdated(lambda: self.name):
            self._name = self._network.manager.getNodeName(self.home_id, self.object_id)
            self.update(lambda: self.name)
        return self._name

    @name.setter
    def name(self,value):
        """
        Set the name of the node.

        :param value: The new name of the node
        :type value: str

        """
        self._network.manager.setNodeName(self.home_id, self.object_id, value)
        self.outdate(lambda: self.name)

    @property
    def location(self):
        """
        The location of the node.

        :rtype: str

        """
        if self.is_outdated(lambda: self.location):
            self._location = self._network.manager.getNodeLocation(self.home_id, self.object_id)
            self.update(lambda: self.location)
        return self._location

    @location.setter
    def location(self,value):
        """
        Set the location of the node.

        :param value: The new location of the node
        :type value: str

        """
        self._network.manager.setNodeLocation(self.home_id, self.object_id, value)
        self.outdate(lambda: self.location)

    @property
    def product_name(self):
        """
        The product name of the node.

        :rtype: str

        """
        if self.is_outdated(lambda: self.product_name):
            self._product_name = self._network.manager.getNodeProductName(self.home_id, self.object_id)
            self.update(lambda: self.product_name)
        return self._product_name

    @productName.setter
    def product_name(self, value):
        """
        Set the product name of the node.

        :param value: The new name of the product
        :type value: str

        """
        self._network.manager.setNodeProductName(self.home_id, self.object_id, value)
        self.outdate(lambda: self.product_name)

    @property
    def product_type(self):
        """
        The product type of the node.

        :rtype: int

        """
        if self.is_outdated(lambda: self.product_type):
            self._product_type = self._network.manager.getNodeProductType(self.home_id, self.object_id)
            self.update(lambda: self.product_type)
        return self._product_type

    @property
    def product_id(self):
        """
        The product Id of the node.

        :rtype: int

        """
        if self.is_outdated(lambda: self.product_id):
            self._product_id = self._network.manager.product_id(self.home_id, self.object_id)
            self.update(lambda: self.product_id)
        return self._product_id

    @property
    def capabilities(self):
        """
        The capabilities of the node.

        :rtype: list()

        """
        caps = list()
        if self.is_routing_device(): caps.add('routing')
        if self.is_listening_device(): caps.add('listening')
        if self.is_frequent_listening_device(): caps.add('frequent')
        if self.is_security_device(): caps.add('security')
        if self.is_beaming_device(): caps.add('beaming')
        return caps

    @property
    def neighbors(self):
        """
        The neighbors of the node.

        :rtype: list()

        """
        if self.is_outdated(lambda: self.neighbors):
            self._neighbors = self._network.manager.getNodeNeighbors(self.home_id, self.object_id)
            self.update(lambda: self.neighbors)
        return self._neighbors

    @property
    def num_groups(self):
        """
        Gets the number of association groups reported by this node.

        :rtype: list()

        """
        if self.is_outdated(lambda: self.num_groups):
            self._num_groups = self._network.manager.getNodeNeighbors(self.home_id, self.object_id)
            self.update(lambda: self.num_groups)
        return self._num_groups

    @property
    def groups(self):
        """
        The groups of the node.

        :rtype: list()

        """
        node._groups = list()
        for i in range(0, self.num_groups()):
            node._groups.append(ZWaveGroup(i,network=self._network))
        return node._groups

    @property
    def command_classes(self):
        """
        The commandClasses of the node.

        :rtype: list()

        """
        if self.is_outdated(lambda: self.command_classes):
            self._command_classes = list()
            for cls in self._network.manager.COMMAND_CLASS_DESC:
                if self._network.manager.getNodeClassInformation(self.home_id, self.object_id, cls):
                    self._command_classes.add(cls)
            self.update(lambda: self.neighbors)
        return self._command_classes

    @property
    def command_classes_as_string(self):
        """
        Return the command classes of the node as string.

        :rtype: list()

        """
        if self.is_outdated(lambda: self.command_classes):
            self._command_classes = list()
            for cls in self._network.manager.COMMAND_CLASS_DESC:
                if self._network.manager.getNodeClassInformation(self.home_id, self.object_id, cls):
                    self._command_classes.add(cls)
            self.update(lambda: self.neighbors)
        return self._command_classes

    @property
    def values(self):
        """
        The values of the node.
        Todo

        :rtype: list()

        """

    def values_for_command_class(self, class_id):
        """
        Retrieve the list of values for a command class

        :param class_id: the COMMAND_CLASS to get values
        :type class_id: hexadecimal code
        :rtype: list() of classId

        """
        ret = list()
        for value in self._values:
            val = value.data
            if val and val.has_key('commandClass') and \
              val['commandClass'] == self._network.manager.COMMAND_CLASS_DESC[classId]:
                ret.append(value)
        return ret

    def has_command_class(self, class_id):
        """
        Check that this node use this commandClass.

        :param classId: the COMMAND_CLASS to check
        :type classId: hexadecimal code
        :rtype: bool

        """
        return class_id in self.command_classes

    @property
    def manufacturer_id(self):
        """
        The manufacturer id of the node.

        :rtype: int

        """
        if self.is_outdated(lambda: self.manufacturer_id):
            self._manufacturer_id = self._network.manager.getNodeManufacturerId(self.home_id, self.object_id)
            self.update(lambda: self.manufacturer_id)
        return self._manufacturer_id

    @property
    def manufacturer_name(self):
        """
        The manufacturer name of the node.

        :rtype: str

        """
        if self.is_outdated(lambda: self.manufacturer_name):
            self._manufacturer_name = \
                self._network.manager.getNodeManufacturerName(self.home_id, self.object_id)
            self.update(lambda: self.manufacturer_name)
        return self._manufacturer_name

    @manufacturer_name.setter
    def manufacturer_name(self, value):
        """
        Set the manufacturer name of the node.

        :param value: The new manufacturer name of the node
        :type value: str

        """
        self._network.manager.setNodeManufacturerName(self.home_id, self.object_id, value)
        self.outdate(lambda: self.manufacturer_name)

    @property
    def generic(self):
        """
        The generic type of the node.

        :rtype: int

        """
        if self.is_outdated(lambda: self.generic):
            self._generic = self._network.manager.getNodeGeneric(self.home_id, self.object_id)
            self.update(lambda: self.generic)
        return self._generic

    @property
    def basic(self):
        """
        The basic type of the node.

        :rtype: int

        """
        if self.is_outdated(lambda: self.basic):
            self._basic = self._network.manager.getNodeBasic(self.home_id, self.object_id)
            self.update(lambda: self.basic)
        return self._basic

    @property
    def specific(self):
        """
        The specific type of the node.

        :rtype: int

        """
        if self.is_outdated(lambda: self.specific):
            self._specific = self._network.manager.getNodeSpecific(self.home_id, self.object_id)
            self.update(lambda: self.specific)
        return self._specific

    @property
    def security(self):
        """
        The security type of the node.

        :rtype: int

        """
        if self.is_outdated(lambda: self.security):
            self._security = self._network.manager.getNodeSecurity(self.home_id, self.object_id)
            self.update(lambda: self.security)
        return self._security

    @property
    def version(self):
        """
        The version of the node.

        :rtype: int

        """
        if self.is_outdated(lambda: self.version):
            self._version = self._network.manager.getNodeVersion(self.home_id, self.object_id)
            self.update(lambda: self.version)
        return self._version

    @property
    def is_listening_device(self):
        """
        Is this node a listening device.

        :rtype: bool

        """
        if self.is_outdated(lambda: self.is_listening_device):
            self._is_listening_device = self._network.manager.isNodeListeningDevice(self.home_id, self.object_id)
            self.update(lambda: self.is_listening_device)
        return self._is_listening_device

    @property
    def isBeamingDevice(self):
        """
        Is this node a beaming device.

        :rtype: bool

        """
        if self.is_outdated(lambda: self.is_beaming_device):
            self._is_beaming_device = self._network.manager.isNodeBeamingDevice(self.home_id, self.object_id)
            self.update(lambda: self.is_beaming_device)
        return self._is_beaming_device

    @property
    def is_frequent_listening_device(self):
        """
        Is this node a frequent listening device.

        :rtype: bool

        """
        if self.is_outdated(lambda: self.is_frequent_listening_device):
            self._is_frequent_listening_device = \
                self._network.manager.isNodeFrequentListeningDevice(self.home_id, self.object_id)
            self.update(lambda: self.is_frequent_listening_device)
        return self._is_frequent_listening_device

    @property
    def is_security_device(self):
        """
        Is this node a security device.

        :rtype: bool

        """
        if self.is_outdated(lambda: self.is_security_device):
            self._is_security_device = self._network.manager.isNodeSecurityDevice(self.home_id, self.object_id)
            self.update(lambda: self.is_security_device)
        return self._is_security_device

    @property
    def is_routing_device(self):
        """
        Is this node a routing device.

        :rtype: bool

        """
        if self.is_outdated(lambda: self.is_routing_device):
            self._is_routing_device = self._network.manager.isNodeRoutingDevice(self.home_id, self.object_id)
            self.update(lambda: self.is_routing_device)
        return self._is_routing_device

    @property
    def is_primary_controller(self):
        """
        Is this node a primary controller of the network.

        :rtype: bool

        """
        if self.is_outdated(lambda: self.is_primary_controller):
            self._is_primary_controller = self._network.manager.is_primary_controller(self.home_id)
            self.update(lambda: self.is_primary_controller)
        return self._is_primary_controller

    @property
    def is_static_update_controller(self):
        """
        Is this controller a static update controller (SUC).

        :rtype: bool

        """
        if self.is_outdated(lambda: self.is_static_update_controller):
            self._is_static_update_controller = self._network.manager.is_static_update_controller(self.home_id)
            self.update(lambda: self.is_static_update_controller)
        return self._is_static_update_controller

    @property
    def is_bridge_controller(self):
        """
        Is this controller using the bridge controller library.

        :rtype: bool

        """
        if self.is_outdated(lambda: self.is_bridge_controller):
            self._is_bridge_controller = self._network.manager.is_bridge_controller(self.home_id)
            self.update(lambda: self.is_bridge_controller)
        return self._isBridgeController

    @property
    def is_locked(self):
        """
        Is this node locked.

        :rtype: bool

        """
        return self._isLocked

    @property
    def is_sleeping(self):
        """
        Is this node sleeping.

        :rtype: bool

        """
        return self._isSleeping

    @property
    def level(self):
        """
        The level of the node.
        Todo
        """
        values = self._getValuesForCommandClass(0x26)  # COMMAND_CLASS_SWITCH_MULTILEVEL
        if values:
            for value in values:
                vdic = value.value_data
                if vdic and vdic.has_key('type') and vdic['type'] == 'Byte' and vdic.has_key('value'):
                    return int(vdic['value'])
        return 0

    @property
    def is_on(self):
        """
        Is this node On.
        Todo
        """
        values = self._getValuesForCommandClass(0x25)  # COMMAND_CLASS_SWITCH_BINARY
        if values:
            for value in values:
                vdic = value.value_data
                if vdic and vdic.has_key('type') and vdic['type'] == 'Bool' and vdic.has_key('value'):
                    return vdic['value'] == 'True'
        return False

    @property
    def battery_level(self):
        """
        The battery level of this node.
        Todo
        """
        values = self._getValuesForCommandClass(0x80)  # COMMAND_CLASS_BATTERY
        if values:
            for value in values:
                vdic = value.value_data
                if vdic and vdic.has_key('type') and vdic['type'] == 'Byte' and vdic.has_key('value'):
                    return int(vdic['value'])
        return -1

    @property
    def signal_strength(self):
        """
        The signal strenght of this node.
        Todo
        """
        return 0

    def refresh_info(self):
        """
        Request a refresh for node.
        """
        self._network.manager.refreshNodeInfo(self.home_id, self.object_id)
        self.outdated = True

    def request_config(self):
        """
        Request config parameters for node.
        """
        logging.debug('Requesting config params for node [%d]', self.object_id)
        self._network.manager.requestAllConfigParams(self.home_id, self.object_id)
        self.outdated = True


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
#   [awakeNodesQueried] or [allNodesQueried] (with node_id 255)
