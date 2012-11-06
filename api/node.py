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

    def __str__(self):
        """
        The string representation of the node.

        :rtype: str

        """
        return 'home_id: [%s] id: [%s] name: [%s] model: [%s]' % \
          (self._network.home_id_str, self._object_id, self.name, self.product_name)

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
        Get the association groups reported by this node

        In Z-Wave, groups are numbered starting from one.  For example, if a call to
        GetNumGroups returns 4, the _groupIdx value to use in calls to GetAssociations
        AddAssociation and RemoveAssociation will be a number between 1 and 4.

        :rtype: dict()

        """
#        if self.is_outdated("self.groups"):
#            self._groups = dict()
#            for i in range(0, self.num_groups):
#                self._groups[i] = ZWaveGroup(i, network=self._network, node_id=self.node_id)
#        return self._groups
        groups = dict()
        nbgroups = self.num_groups
        for i in range(1, nbgroups+1):
            groups[i] = ZWaveGroup(i, network=self._network, node_id=self.node_id)
        return groups

#    def add_group(self, target_node_id):
#        """
#        Add a new group containing the target node target_node_id.
#        to do
#
#        :param target_node_id: Identifier for the node that will be added to the association group.
#        :type target_node_id: int
#
#        """
#        self._network.manager.addAssociation(self.home_id, self.node_id, self.num_groups+1, target_node_id)

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
                #logging.debug("node.command_classes : type = %s, values = %s)" % (type(cls), command_classes))
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
        for value in self.values :
            if (genre == 'All' or self.values[value].genre == genre) and \
              (type == 'All' or self.values[value].type == type) and \
              (readonly == 'All' or self.values[value].is_read_only == readonly) and \
              (writeonly == 'All' or self.values[value].is_write_only == writeonly):
                if self.values[value].command_class not in values :
                    values[self.values[value].command_class] = dict()
                values[self.values[value].command_class][value] = self.values[value]
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
            if (class_id == 'All' or self.values[value].command_class == class_id) and \
              (genre == 'All' or self.values[value].genre == genre) and \
              (type == 'All' or self.values[value].type == type) and \
              (readonly == 'All' or self.values[value].is_read_only == readonly) and \
              (writeonly == 'All' or self.values[value].is_write_only == writeonly):
                ret[value] = self.values[value]
                #logging.debug("value.command_classes : type = %s" % (type(class_id)))
        return ret

    def add_value(self, value_id):
        """
        Add a value to the node

        :param value_id: The id of the value to add
        :type value_id: int
        :param command_class: The command_class of the value
        :type command_class: str
        :rtype: bool

        """
        value = ZWaveValue(value_id, network=self.network, parent=self)
        self.values[value_id] = value
        logging.debug("Add value : %s" % value)
        #self.values[value_id].oudated = True

    def change_value(self, value_id):
        """
        Change a value of the node.

        :param value_id: The id of the value to change
        :type value_id: int

        """
        logging.debug("Change value : %s" % self.values[value_id])

    def refresh_value(self, value_id):
        """
        Refresh a value of the node.

        :param value_id: The id of the value to change
        :type value_id: int

        """
        logging.debug("Refresh value : %s" % self.values[value_id])

    def remove_value(self, value_id):
        """
        Change a value of the node. Todo

        :param value_id: The id of the value to change
        :type value_id: int
        :return: The result of the operation
        :rtype: bool

        """
        if value_id in self.values :
            logging.debug("Remove value : %s" % self.values[value_id])
            del(self.values[value_id])
            return True
        return False

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

        :return: The specific type of the node
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

        :return: The security type of the node
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

        :return: The version of the node
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
        return self._is_locked

    @property
    def is_sleeping(self):
        """
        Is this node sleeping.

        :rtype: bool

        """
        return self._is_sleeping

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
        Get the maximum baud rate of a node

        """
#        if self.is_outdated("self.max_baud_rate"):
#            self._max_baud_rate = self._network.manager.getNodeMaxBaudRate(self.home_id, self.object_id)
#            self.update("self.max_baud_rate")
#        return self._max_baud_rate
#        self.outdated = True
        return self._network.manager.getNodeMaxBaudRate(self.home_id, self.object_id)

    def refresh_info(self):
        """
        Trigger the fetching of fixed data about a node.

        Causes the nodes data to be obtained from the Z-Wave network in the same way
        as if it had just been added.  This method would normally be called
        automatically by OpenZWave, but if you know that a node has been changed,
        calling this method will force a refresh of the data held by the library.  This
        can be especially useful for devices that were asleep when the application was
        first run.

        """
        self._network.manager.refreshNodeInfo(self.home_id, self.object_id)
#        self.outdated = True

    def request_all_config_params(self):
        """
        Request the values of all known configurable parameters from a device.

        """
        logging.debug('Requesting config params for node [%d]', self.object_id)
        self._network.manager.requestAllConfigParams(self.home_id, self.object_id)
#        self.outdated = True

    def request_config_param(self, param):
        """
        Request the value of a configurable parameter from a device.

        Some devices have various parameters that can be configured to control the
        device behaviour.  These are not reported by the device over the Z-Wave network
        but can usually be found in the devices user manual.  This method requests
        the value of a parameter from the device, and then returns immediately,
        without waiting for a response.  If the parameter index is valid for this
        device, and the device is awake, the value will eventually be reported via a
        ValueChanged notification callback.  The ValueID reported in the callback will
        have an index set the same as _param and a command class set to the same value
        as returned by a call to Configuration::StaticGetCommandClassId.

        :param param: The param of the node.
        :type param:

        """
        logging.debug('Requesting config param %s for node [%d]', (param, self.object_id))
        self._network.manager.requestConfigParam(self.home_id, self.object_id, param)
#        self.outdated = True

    def set_config_param(self, param, value):
        """
        Set the value of a configurable parameter in a device.

        Some devices have various parameters that can be configured to control the
        device behaviour.  These are not reported by the device over the Z-Wave network
        but can usually be found in the devices user manual.  This method returns
        immediately, without waiting for confirmation from the device that the change
        has been made.

        :param param: The param of the node.
        :type param:
        :param value: The value of the param.
        :type value:
        :return:
        :rtype: bool

        """
        logging.debug('Set config param %s for node [%d]', (param, self.object_id))
        return self._network.manager.setConfigParam(self.home_id, self.object_id, param, value)

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
