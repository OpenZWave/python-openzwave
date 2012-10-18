# -*- coding: utf-8 -*-
"""
.. module:: openzwave.node

This file is part of **python-openzwave** project http://code.google.com/p/python-openzwave.
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
import libopenzwave
from collections import namedtuple
import thread
import time
import logging
from openzwave.object import ZWaveException, ZWaveCommandClassException
from openzwave.object import ZWaveObject, NullLoggingHandler, ZWaveNodeInterface
from openzwave.group import ZWaveGroup
from openzwave.value import ZWaveValue
from openzwave.command import ZWaveNodeBasic, ZWaveNodeSwitch, ZWaveNodeSensor

logging.getLogger('openzwave').addHandler(logging.NullHandler())

class ZWaveNode( ZWaveObject,
                 ZWaveNodeBasic, ZWaveNodeSwitch,
                 ZWaveNodeSensor
                 ):
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
        ZWaveObject.__init__(self, node_id, network)
        #No cache management for values in nodes
        self.values = dict()
        self._is_sleeping = False
        self._is_locked = False
        #self._name = None
        #self.cache_property("self.name")
        #self._location = None
        #self.cache_property("self.location")
        #self._manufacturer_id = None
        #self.cache_property("self.manufacturer_id")
        #self._manufacturer_name = None
        #self.cache_property("self.manufacturer_name")
        #self._product_id = None
        #self.cache_property("self.product_id")
        #self._product_type = None
        #self.cache_property("self.product_type")
        #self._product_name = None
        #self.cache_property("self.product_name")
        #self._is_routing_device = False
        #self.cache_property("self.is_routing_device")
        #self._is_listening_device = False
        #self.cache_property("self.is_listening_device")
        #self._is_frequent_listening_device = False
        #self.cache_property("self.is_frequent_listening_device")
        #self._is_security_device = False
        #self.cache_property("self.is_security_device")
        #self._is_beaming_device = False
        #self.cache_property("self.is_beaming_device")

        #self._is_primary_controller = False
        #self.cache_property("self.is_primary_controller")
        #self._is_bridge_controller = False
        #self.cache_property("self.is_bridge_controller")
        #self._is_static_update_controller = False
        #self.cache_property("self.is_static_update_controller")

        #self._is_polled = False
        #self.cache_property("self.is_polled")
        #self._generic = 0
        #self.cache_property("self.generic")
        #self._basic = 0
        #self.cache_property("self.basic")
        #self._specific = 0
        #self.cache_property("self.specific")
        #self._security = 0
        #self.cache_property("self.security")
        #self._version = 0
        #self.cache_property("self.version")

        #self._command_classes = set()
        #self.cache_property("self.command_classes")
        #self._neighbors = set()
        #self.cache_property("self.neighbors")
        #self._num_groups = int
        #self.cache_property("self.num_groups")
        #self._groups = dict()
        #self.cache_property("self.groups")

        #self._max_baud_rate = None
        #self.cache_property("self.max_baud_rate")
        #self._signal_strength = None
        #self.cache_property("self.signal_strength")
        #self._battery_level = None
        #self.cache_property("self.battery_level")

    @property
    def node_id(self):
        """
        The id of the node.

        :rtype: int

        """
        return self._object_id

    @property
    def name(self):
        """
        The name of the node.

        :rtype: str

        """
#        if self.is_outdated("self.name"):
#            #print "No cache"
#            self._name = self._network.manager.getNodeName(self.home_id, self.object_id)
#            self.update("self.name")
#        #print "self._name"
#        return self._name
        return self._network.manager.getNodeName(self.home_id, self.object_id)

    @name.setter
    def name(self, value):
        """
        Set the name of the node.

        :param value: The new name of the node
        :type value: str

        """
        self._network.manager.setNodeName(self.home_id, self.object_id, value)
#        self.outdate("self.name")

    @property
    def location(self):
        """
        The location of the node.

        :rtype: str

        """
#        if self.is_outdated("self.location"):
#            self._location = self._network.manager.getNodeLocation(self.home_id, self.object_id)
#            self.update("self.location")
#        return self._location
        return self._network.manager.getNodeLocation(self.home_id, self.object_id)

    @location.setter
    def location(self, value):
        """
        Set the location of the node.

        :param value: The new location of the node
        :type value: str

        """
        self._network.manager.setNodeLocation(self.home_id, self.object_id, value)
#        self.outdate("self.location")

    @property
    def product_name(self):
        """
        The product name of the node.

        :rtype: str

        """
#        if self.is_outdated("self.product_name"):
#            self._product_name = self._network.manager.getNodeProductName(self.home_id, self.object_id)
#            self.update("self.product_name")
#        return self._product_name
        return self._network.manager.getNodeProductName(self.home_id, self.object_id)

    @product_name.setter
    def product_name(self, value):
        """
        Set the product name of the node.

        :param value: The new name of the product
        :type value: str

        """
        self._network.manager.setNodeProductName(self.home_id, self.object_id, value)
#        self.outdate("self.product_name")

    @property
    def product_type(self):
        """
        The product type of the node.

        :rtype: int

        """
#        if self.is_outdated("self.product_type"):
#            self._product_type = self._network.manager.getNodeProductType(self.home_id, self.object_id)
#            self.update("self.product_type")
#        return self._product_type
        return self._network.manager.getNodeProductType(self.home_id, self.object_id)

    @property
    def product_id(self):
        """
        The product Id of the node.

        :rtype: int

        """
#        if self.is_outdated("self.product_id"):
#            self._product_id = self._network.manager.getNodeProductId(self.home_id, self.object_id)
#            self.update("self.product_id")
#        return self._product_id
        return self._network.manager.getNodeProductId(self.home_id, self.object_id)

    @property
    def capabilities(self):
        """
        The capabilities of the node.

        :rtype: set()

        """
        caps = set()
        if self.is_routing_device:
            caps.add('routing')
        if self.is_listening_device:
            caps.add('listening')
        if self.is_frequent_listening_device:
            caps.add('frequent')
        if self.is_security_device:
            caps.add('security')
        if self.is_beaming_device:
            caps.add('beaming')
        return caps

    @property
    def neighbors(self):
        """
        The neighbors of the node.

        :rtype: set()

        """
#        if self.is_outdated("self.neighbors"):
#            self._neighbors = self._network.manager.getNodeNeighbors(self.home_id, self.object_id)
#            self.update("self.neighbors")
#        return self._neighbors
        return self._network.manager.getNodeNeighbors(self.home_id, self.object_id)

    @property
    def num_groups(self):
        """
        Gets the number of association groups reported by this node.

        :rtype: int

        """
#        if self.is_outdated("self.num_groups"):
#            self._num_groups = self._network.manager.getNumGroups(self.home_id, self.object_id)
#            self.update("self.num_groups")
#        return self._num_groups
        return self._network.manager.getNumGroups(self.home_id, self.object_id)

    @property
    def groups(self):
        """
        The groups of the node.
        to do

        :rtype: dict()

        """
#        if self.is_outdated("self.groups"):
#            self._groups = dict()
#            for i in range(0, self.num_groups):
#                self._groups[i] = ZWaveGroup(i, network=self._network, node_id=self.node_id)
#        return self._groups
        groups = dict()
        nbgroups = self.num_groups
        for i in range(0, nbgroups):
            groups[i] = ZWaveGroup(i, network=self._network, node_id=self.node_id)
        return groups

    @property
    def command_classes(self):
        """
        The commandClasses of the node.

        :rtype: set()

        """
#        if self.is_outdated("self.command_classes"):
#            #print "no cache"
#            self._command_classes = set()
#            for cls in self._network.manager.COMMAND_CLASS_DESC:
#                if self._network.manager.getNodeClassInformation(self.home_id, self.object_id, cls):
#                    self._command_classes.add(cls)
#            self.update("self.command_classes")
#        #print "command_classes : ",self._command_classes
#        return self._command_classes
        command_classes = set()
        for cls in self._network.manager.COMMAND_CLASS_DESC:
            if self._network.manager.getNodeClassInformation(self.home_id, self.object_id, cls):
                command_classes.add(cls)
        #print "command_classes : ",self._command_classes
        return command_classes

    @property
    def command_classes_as_string(self):
        """
        Return the command classes of the node as string.

        :rtype: set()

        """
        commands = self.command_classes
        command_str = set()
        for cls in commands :
            command_str.add(self._network.manager.COMMAND_CLASS_DESC[cls])
        return command_str

    def get_command_class_as_string(self, class_id):
        """
        Return the command class representation as string.

        :param class_id: the COMMAND_CLASS to get string representation
        :type class_id: hexadecimal code
        :rtype: str

        """
        return self._network.manager.COMMAND_CLASS_DESC[class_id]

#    @property
#    def values(self):
#        """
#        The values of the node.
#        Todo
#
#        :rtype: set()
#
#        """
#        return self._values

    def get_values_by_command_classes(self, genre='All', \
        type='All', readonly='All', writeonly='All'):
        """
        Retrieve values in a dict() of dicts(). The dict is indexed on the COMMAND_CLASS.
        This allows to browse values grouped by the COMMAND_CLASS.You can optionnaly filter for a command class,
        a genre and/or a type. You can also filter readonly and writeonly params.

        This method always filter the values.
        If you wan't to get all the node's values, use the property self.values instead.

        :param genre: the genre of value
        :type genre: 'All' or PyGenres
        :param type: the type of value
        :type type: 'All' or PyValueTypes
        :param readonly: Is this value readonly
        :type readonly: 'All' or True or False
        :param writeonly: Is this value writeonly
        :type writeonly: 'All' or True or False
        :rtype: dict(command_class : dict(valueids))

        """
        values = dict()
        for val in self.values :
            if (genre == 'All' or self.values[value].genre == genre) and \
              (type == 'All' or self.values[value].type == type) and \
              (readonly == 'All' or self.values[value].is_read_only == readonly) and \
              (writeonly == 'All' or self.values[value].is_write_only == writeonly):
                if self.values[val].command_class not in values :
                    values[self.values[val].command_class] = dict()
                values[self.values[val].command_class][value] = self.values[value]
        return values

    def get_values_for_command_class(self, class_id):
        """
        Retrieve the set of values for a command class.
        Deprecated
        For backward compatibility only.
        Use get_values instead

        :param class_id: the COMMAND_CLASS to get values
        :type class_id: hexadecimal code or string
        :type writeonly: 'All' or True or False
        :rtype: set() of classId

        """
        #print class_id
        return self.get_values(class_id=class_id)

    def get_values(self, class_id='All', genre='All', \
        type='All', readonly='All', writeonly='All'):
        """
        Retrieve the set of values. You can optionnaly filter for a command class,
        a genre and/or a type. You can also filter readonly and writeonly params.

        This method always filter the values.
        If you wan't to get all the node's values, use self.values instead.

        :param class_id: the COMMAND_CLASS to get values
        :type class_id: hexadecimal code or string
        :param genre: the genre of value
        :type genre: 'All' or PyGenres
        :param type: the type of value
        :type type: 'All' or PyValueTypes
        :param readonly: Is this value readonly
        :type readonly: 'All' or True or False
        :param writeonly: Is this value writeonly
        :type writeonly: 'All' or True or False
        :rtype: set() of Values

        """
        ret = dict()
        for value in self.values:
            #print "self.values[value].command_class= ",self.values[value].command_class
            #print "class_id= ",class_id
            if (class_id == 'All' or self.values[value].command_class == \
                self._network.manager.COMMAND_CLASS_DESC[class_id]) and \
              (genre == 'All' or self.values[value].genre == genre) and \
              (type == 'All' or self.values[value].type == type) and \
              (readonly == 'All' or self.values[value].is_read_only == readonly) and \
              (writeonly == 'All' or self.values[value].is_write_only == writeonly):
                ret[value] = self.values[value]
#        for value in self._values:
#            print "type(class_id)= ",type(class_id)
#            if type(class_id)==type(''):
#                for cls in self._network.manager.COMMAND_CLASS_DESC :
#                    if self._network.manager.COMMAND_CLASS_DESC[cls]==class_id:
#                        if self.values[value].command_class==cls:
#                            ret.add(self.values[value])
#            elif type(class_id)==type(0):
#                if self.values[value].command_class==class_id:
#                    ret.add(self.values[value])
        #if len(ret) == 0:
        #   return None
        #else :
        return ret

    def add_value(self, value_id, command_class):
        """
        Add a value to the node

        :param value_id: The id of the value to add
        :type value_id: int
        :rtype: bool

        """
        value = ZWaveValue(value_id, network=self.network, parent_id=self.node_id, command_class=command_class)
        self.values[value_id] = value
        #self.values[value_id].oudated = True

    def change_value(self, value_id):
        """
        Change a value of the node. Todo

        :param value_id: The id of the value to change
        :type value_id: int
        :rtype: bool

        """
#        self.values[value_id].oudated = True
        pass

    def refresh_value(self, value_id):
        """
        Change a value of the node. Todo

        :param value_id: The id of the value to change
        :type value_id: int
        :rtype: bool

        """
#        self.values[value_id].oudated = True
        pass

    def remove_value(self, value_id):
        """
        Change a value of the node. Todo

        :param value_id: The id of the value to change
        :type value_id: int
        :rtype: bool

        """
        del(self.values[value_id])

    def set_field(self, field, value):
        """
        A helper to set a writable field : name, location, product_name, ...

        :param field: The field to set : name, location, product_name, manufacturer_name
        :type field: str
        :param value: The value to set
        :type value: str
        :rtype: bool

        """
        if field == "name":
            self.name=value
        elif field == "location":
            self.location=value
        elif field == "product_name":
            self.product_name=value
        elif field == "manufacturer_name":
            self.manufacturer_name=value

    def has_command_class(self, class_id):
        """
        Check that this node use this commandClass.

        :param classId: the COMMAND_CLASS to check
        :type classId: hexadecimal code
        :rtype: bool

        """
        return class_id in self.command_classes

    def handle_command_class(self, class_id):
        """
        Check that this node use this commandClass and the method is implemented.

        :param classId: the COMMAND_CLASS to check
        :type classId: hexadecimal code
        :rtype: bool or None (if class_id is supported but not implemented).

        """
        if self.has_command_class(class_id) :
            try :
                eval("self.command_class_%s()" % class_id)
                return True
            except AttributeError:
                logging.error("CommandCLass %s not supported by API (Report a bug to developpers.)." % class_id)
                return None
        return False

    @property
    def manufacturer_id(self):
        """
        The manufacturer id of the node.

        :rtype: int

        """
#        if self.is_outdated("self.manufacturer_id"):
#            #print "No cache"
#            self._manufacturer_id = self._network.manager.getNodeManufacturerId(self.home_id, self.object_id)
#            self.update("self.manufacturer_id")
#        return self._manufacturer_id
        return self._network.manager.getNodeManufacturerId(self.home_id, self.object_id)

    @property
    def manufacturer_name(self):
        """
        The manufacturer name of the node.

        :rtype: str

        """
#        if self.is_outdated("self.manufacturer_name"):
#            #print "No cache"
#            self._manufacturer_name = \
#                self._network.manager.getNodeManufacturerName(self.home_id, self.object_id)
#            self.update("self.manufacturer_name")
#        return self._manufacturer_name
        return self._network.manager.getNodeManufacturerName(self.home_id, self.object_id)

    @manufacturer_name.setter
    def manufacturer_name(self, value):
        """
        Set the manufacturer name of the node.

        :param value: The new manufacturer name of the node
        :type value: str

        """
        self._network.manager.setNodeManufacturerName(self.home_id, self.object_id, value)
#        self.outdate("self.manufacturer_name")

    @property
    def generic(self):
        """
        The generic type of the node.

        :rtype: int

        """
#        if self.is_outdated("self.generic"):
#            self._generic = self._network.manager.getNodeGeneric(self.home_id, self.object_id)
#            self.update("self.generic")
#        return self._generic
        return self._network.manager.getNodeGeneric(self.home_id, self.object_id)

    @property
    def basic(self):
        """
        The basic type of the node.

        :rtype: int

        """
#        if self.is_outdated("self.basic"):
#            self._basic = self._network.manager.getNodeBasic(self.home_id, self.object_id)
#            self.update("self.basic")
#        return self._basic
        return self._network.manager.getNodeBasic(self.home_id, self.object_id)

    @property
    def specific(self):
        """
        The specific type of the node.

        :rtype: int

        """
#        if self.is_outdated("self.specific"):
#            self._specific = self._network.manager.getNodeSpecific(self.home_id, self.object_id)
#            self.update("self.specific")
#        return self._specific
        return self._network.manager.getNodeSpecific(self.home_id, self.object_id)

    @property
    def security(self):
        """
        The security type of the node.

        :rtype: int

        """
#        if self.is_outdated("self.security"):
#            self._security = self._network.manager.getNodeSecurity(self.home_id, self.object_id)
#            self.update("self.security")
#        return self._security
        return self._network.manager.getNodeSecurity(self.home_id, self.object_id)

    @property
    def version(self):
        """
        The version of the node.

        :rtype: int

        """
#        if self.is_outdated("self.version"):
#            self._version = self._network.manager.getNodeVersion(self.home_id, self.object_id)
#            self.update("self.version")
#        return self._version
        return self._network.manager.getNodeVersion(self.home_id, self.object_id)

    @property
    def is_listening_device(self):
        """
        Is this node a listening device.

        :rtype: bool

        """
#        if self.is_outdated("self.is_listening_device"):
#            self._is_listening_device = self._network.manager.isNodeListeningDevice(self.home_id, self.object_id)
#            self.update("self.is_listening_device")
#        return self._is_listening_device
        return self._network.manager.isNodeListeningDevice(self.home_id, self.object_id)

    @property
    def is_beaming_device(self):
        """
        Is this node a beaming device.

        :rtype: bool

        """
#        if self.is_outdated("self.is_beaming_device"):
#            self._is_beaming_device = self._network.manager.isNodeBeamingDevice(self.home_id, self.object_id)
#            self.update("self.is_beaming_device")
#        return self._is_beaming_device
        return self._network.manager.isNodeBeamingDevice(self.home_id, self.object_id)

    @property
    def is_frequent_listening_device(self):
        """
        Is this node a frequent listening device.

        :rtype: bool

        """
#        if self.is_outdated("self.is_frequent_listening_device"):
#            self._is_frequent_listening_device = \
#                self._network.manager.isNodeFrequentListeningDevice(self.home_id, self.object_id)
#            self.update("self.is_frequent_listening_device")
#        return self._is_frequent_listening_device
        return self._network.manager.isNodeFrequentListeningDevice(self.home_id, self.object_id)

    @property
    def is_security_device(self):
        """
        Is this node a security device.

        :rtype: bool

        """
#        if self.is_outdated("self.is_security_device"):
#            self._is_security_device = self._network.manager.isNodeSecurityDevice(self.home_id, self.object_id)
#            self.update("self.is_security_device")
#        return self._is_security_device
        return self._network.manager.isNodeSecurityDevice(self.home_id, self.object_id)

    @property
    def is_routing_device(self):
        """
        Is this node a routing device.

        :rtype: bool

        """
#        if self.is_outdated("self.is_routing_device"):
#            self._is_routing_device = self._network.manager.isNodeRoutingDevice(self.home_id, self.object_id)
#            self.update("self.is_routing_device")
#        return self._is_routing_device
        return self._network.manager.isNodeRoutingDevice(self.home_id, self.object_id)

    @property
    def is_primary_controller(self):
        """
        Is this node a primary controller of the network.

        :rtype: bool

        """
#        if self.is_outdated("self.is_primary_controller"):
#            self._is_primary_controller = self._network.manager.isPrimaryController(self.home_id)
#            self.update("self.is_primary_controller")
#        return self._is_primary_controller
        return self._network.manager.isPrimaryController(self.home_id)

    @property
    def is_static_update_controller(self):
        """
        Is this controller a static update controller (SUC).

        :rtype: bool

        """
#        if self.is_outdated("self.is_static_update_controller"):
#            self._is_static_update_controller = self._network.manager.isStaticUpdateController(self.home_id)
#            self.update("self.is_static_update_controller")
#        return self._is_static_update_controller
        return self._network.manager.isStaticUpdateController(self.home_id)

    @property
    def is_bridge_controller(self):
        """
        Is this controller using the bridge controller library.

        :rtype: bool

        """
#        if self.is_outdated("self.is_bridge_controller"):
#            self._is_bridge_controller = self._network.manager.isBridgeController(self.home_id)
#            self.update("self.is_bridge_controller")
#        return self._is_bridge_controller
        return self._network.manager.isBridgeController(self.home_id)

    @property
    def is_locked(self):
        """
        Is this node locked.

        :rtype: bool

        """
        return self.is_locked

    @property
    def is_sleeping(self):
        """
        Is this node sleeping.

        :rtype: bool

        """
        return self.is_sleeping

#    @property
#    def level(self):
#        """
#        The level of the node.
#        Todo
#        """
#        values = self._getValuesForCommandClass(0x26)  # COMMAND_CLASS_SWITCH_MULTILEVEL
#        if values:
#            for value in values:
#                vdic = value.value_data
#                if vdic and vdic.has_key('type') and vdic['type'] == 'Byte' and vdic.has_key('value'):
#                    return int(vdic['value'])
#        return 0

#    @property
#    def is_on(self):
#        """
#        Is this node On.
#        Todo
#        """
#        values = self._getValuesForCommandClass(0x25)  # COMMAND_CLASS_SWITCH_BINARY
#        if values:
#            for value in values:
#                vdic = value.value_data
#                if vdic and vdic.has_key('type') and vdic['type'] == 'Bool' and vdic.has_key('value'):
#                    return vdic['value'] == 'True'
#        return False

#    @property
#    def signal_strength(self):
#        """
#        The signal strenght of this node.
#        Todo
#        """
#        return 0

    @property
    def max_baud_rate(self):
        """
        Get the maximum baud rate of a nodes communications
        """
#        if self.is_outdated("self.max_baud_rate"):
#            self._max_baud_rate = self._network.manager.getNodeMaxBaudRate(self.home_id, self.object_id)
#            self.update("self.max_baud_rate")
#        return self._max_baud_rate
#        self.outdated = True
        return self._network.manager.getNodeMaxBaudRate(self.home_id, self.object_id)

    def refresh_info(self):
        """
        Request a refresh for node.
        """
        self._network.manager.refreshNodeInfo(self.home_id, self.object_id)
#        self.outdated = True

    def request_config(self):
        """
        Request config parameters for node.
        """
        logging.debug('Requesting config params for node [%d]', self.object_id)
        self._network.manager.requestAllConfigParams(self.home_id, self.object_id)
#        self.outdated = True

#    def setNodeOn(self, node):
#        """
#        """
#        self._log.debug('Requesting setNodeOn for node {0}'.format(node.id))
#        self._manager.setNodeOn(node.home_id, node.id)

#    def setNodeOff(self, node):
#        """
#        """
#        self._log.debug('Requesting setNodeOff for node {0}'.format(node.id))
#        self._manager.setNodeOff(node.home_id, node.id)

#    def setNodeLevel(self, node, level):
#        """
#        """
#        self._log.debug('Requesting setNodeLevel for node {0} with new level {1}'.format(node.id, level))
#        self._manager.setNodeLevel(node.home_id, node.id, level)
