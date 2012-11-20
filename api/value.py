# -*- coding: utf-8 -*-
"""
.. module:: openzwave.value

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
from collections import namedtuple
import thread
import time
import openzwave
import logging
from threading import Timer
from openzwave.object import ZWaveObject

logging.getLogger('openzwave').addHandler(logging.NullHandler())

# TODO: don't report controller node as sleeping
# TODO: allow value identification by device/index/instance
class ZWaveValue(ZWaveObject):
    '''
    Represents a single value.
    Must be updated to use the cachedObject facilities.
    '''
    def __init__(self, value_id, network=None, parent=None):
        '''
        Initialize value

        n['valueId'] = {'home_id' : v.GetHomeId(),
            * 'parent_id' : v.GetNodeId(),
            * 'commandClass' : PyManager.COMMAND_CLASS_DESC[v.GetCommandClassId()],
            * 'instance' : v.GetInstance(),
            * 'index' : v.GetIndex(),
            * 'id' : v.GetId(),
            * 'genre' : PyGenres[v.GetGenre()],
            * 'type' : PyValueTypes[v.GetType()],
            * #'value' : value.c_str(),
            * 'value' : getValueFromType(manager,v.GetId()),
            * 'label' : label.c_str(),
            * 'units' : units.c_str(),
            * 'readOnly': manager.IsValueReadOnly(v),
            }

        Cache management :
        We must developp a special mechanism for caching values.
        Values are updated or created by notifications and attached to nodes.

        Cache management in nodes : no cache for values.

        :param value_id: ID of the value
        :type value_id: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork
        :param parent_id: ID of parent (node or scene)
        :type parent_id: int

        '''
        ZWaveObject.__init__(self, value_id, network=network)
        logging.debug("Create object value (valueId:%s)" % (value_id))
        self._parent = parent
        self._poll_intensity = 0
        #self._command_class = command_class
        #self._type = type
        #print command_class
        #print self._network.manager
        #print self._network.manager.COMMAND_CLASS_DESC[command_class]
        #self._command_class = self._network.manager.COMMAND_CLASS_DESC[command_class]
        #self._value_data = value_data
        #self.n = valueId
        #self._values = dict()
        #self._label = None
        #self.cache_property("self.label")
        #self._help = None
        #self.cache_property("self.help")
        #self._min = None
        #self.cache_property("self.min")
        #self._max = None
        #self.cache_property("self.max")
        #self._units = None
        #self.cache_property("self.units")
        #self._poll_intensity = None
        #self.cache_property("self.poll_intensity")
        #self._data_as_string = None
        #self.cache_property("self.data_as_string")
        #self._data_items = None
        #self.cache_property("self.data_items")
        #self._data = None
        #self.cache_property("self.data")
        #self._type = None
        #self.cache_property("self.type")

    def __str__(self):
        """
        The string representation of the value.

        :rtype: str

        """
        return 'home_id: [%s] id: [%s] parent_id: [%s] label: [%s] data: [%s]' % \
          (self._network.home_id_str, self._object_id, self.parent_id, self.label, self.data)

    @property
    def parent_id(self):
        """
        The parent_id of the value.
        """
        return self._parent.object_id

    @property
    def value_id(self):
        """
        The value_id of the value.
        """
        return self._object_id

    @property
    def id_on_network(self):
        """
        Return an unique id for this value.
        The scenes use this to retrieve values
        <Scene id="1" label="scene1">
                <Value homeId="0x014d0ef5" nodeId="2" genre="user" commandClassId="38" instance="1" index="0" type="byte">54</Value>
        </Scene>
        The format is :
            home_id.node_id.commnand_class.instance.index

        """
        return "%0.8x.%s.%0.2x.%s.%s" % (self._network.home_id, self.parent_id, self.command_class, self.instance, self.index )

    @property
    def node(self):
        """
        The value_id of the value.
        """
        return self._parent

    @property
    def label(self):
        """
        The label of the value.

        :rtype: str

        """
#        if self.is_outdated("self.label"):
#            self._label = self._network.manager.getValueLabel(self.value_id)
#            self.update("self.label")
#        return self._label
        return self._network.manager.getValueLabel(self.value_id)

    @label.setter
    def label(self, value):
        """
        Set the label of the value.

        :param value: The new label value
        :type value: str

        """
        self._network.manager.setValueLabel(self.value_id, value)
#        self.outdate("self.label")

    @property
    def help(self):
        """
        The help of the value.

        :rtype: str

        """
#        if self.is_outdated("self.help"):
#            self._help = self._network.manager.getValueHelp(self.value_id)
#            self.update("self.help")
#        return self._help
        return self._network.manager.getValueHelp(self.value_id)

    @help.setter
    def help(self, value):
        """
        Set the help of the value.

        :param value: The new help value
        :type value: str

        """
        self._network.manager.setValueHelp(self.value_id, value)
#        self.outdate("self.help")

    @property
    def units(self):
        """
        The units of the value.

        :rtype: str

        """
#        if self.is_outdated("self.units"):
#            self._units = self._network.manager.getValueUnits(self.value_id)
#            self.update("self.units")
#        return self._units
        return self._network.manager.getValueUnits(self.value_id)

    @units.setter
    def units(self, value):
        """
        Set the units of the value.

        :param value: The new units value
        :type value: str

        """
        self._network.manager.setValueUnits(self.value_id, value)
#        self.outdate("self.units")

    @property
    def max(self):
        """
        The max of the value.

        :rtype: int

        """
#        if self.is_outdated("self.max"):
#            self._max = self._network.manager.getValueMax(self.value_id)
#            self.update("self.max")
#        return self._min
        return self._network.manager.getValueMax(self.value_id)

    @property
    def min(self):
        """
        The min of the value.

        :rtype: int

        """
#        if self.is_outdated("self.min"):
#            self._min = self._network.manager.getValueMin(self.value_id)
#            self.update("self.min")
#        return self._min
        return self._network.manager.getValueMin(self.value_id)

    @property
    def type(self):
        """
        Get the type of the value.  The type describes the data held by the value
        and enables the user to select the correct value accessor method in the
        Manager class.

        :return: type of the value
        :rtype: str

        """
#        if self.is_outdated("self.type"):
#            self._type = self._network.manager.getValueType(self.value_id)
#            self.update("self.type")
#        return self._type
        return self._network.manager.getValueType(self.value_id)

    @property
    def genre(self):
        """
        Get the genre of the value.  The genre classifies a value to enable
        low-level system or configuration parameters to be filtered out
        by the application

        :return: genre of the value (Basic, User, Config, System)
        :rtype: str

        """
        return self._network.manager.getValueGenre(self.value_id)

    @property
    def index(self):
        """
        Get the value index.  The index is used to identify one of multiple
        values created and managed by a command class.  In the case of configurable
        parameters (handled by the configuration command class), the index is the
        same as the parameter ID.

        :return: index of the value
        :rtype: int

        """
        return self._network.manager.getValueIndex(self.value_id)

    @property
    def instance(self):
        """
        Get the command class instance of this value.  It is possible for there to be
        multiple instances of a command class, although currently it appears that
        only the SensorMultilevel command class ever does this.

        :return: instance of the value
        :rtype: int

        """
        return self._network.manager.getValueInstance(self.value_id)

    @property
    def data(self):
        """
        The current data of the value.

        :return: The data of the value
        :rtype: depending of the type of the value

        """
#        if self.is_outdated("self.data"):
#            self._data = self._network.manager.getValue(self.value_id)
#            self.update("self.data")
#        return self._data
        return self._network.manager.getValue(self.value_id)

    @data.setter
    def data(self, value):
        """
        Set the data of the value.
        Use check_data before setting it.

        :param value: The new data value
        :type value: str

        """
        val = self.check_data(value)
        self._network.manager.setValue(self.value_id, val)
#        self.outdate("self.data")

    @property
    def data_as_string(self):
        """
        The value data as String.

        :rtype: str

        """
#        if self.is_outdated("self.data_as_string"):
#            self._as_string = self._network.manager.getValueAsString(self.value_id)
#            self.update("self.data_as_string")
#        return self._as_string
        return self._network.manager.getValueAsString(self.value_id)

    @property
    def data_items(self):
        """
        When type of value is list, data_items contains a list of valid values

        :return: The valid values
        :rtype: set()

        """
#        if self.is_outdated("self.data_items"):
#            self._data_items = self._network.manager.getValueListItems(self.value_id)
#            self.update("self.data_items")
#        return self._data_items
        if self.is_read_only :
            return "Read only"
        if self.type == "Bool":
            return "True or False"
        elif self.type == "Byte":
            return "A byte between %s and %s" % (self.min,self.max)
        elif self.type == "Decimal":
            return "A decimal"
        elif self.type == "Int":
            return "An integer between %s and %s" % (self.min,self.max)
        elif self.type == "Short":
            return "A short between %s and %s" % (self.min,self.max)
        elif self.type == "String":
            return "A string"
        elif self.type == "Button":
            return "True or False"
        elif self.type == "List":
            return self._network.manager.getValueListItems(self.value_id)
        else :
            return "Unknown"

    def check_data(self, data):
        """
        Check that data is correct for this value.
        Return the data in a correct type. None is data is incorrect.

        :return: A variable of the good type if the data is correct. None otherwise.
        :rtype: variable

        """
        if self.is_read_only :
            return None
        new_data = None
        logging.debug("check_data type :%s" % (self.type))
        if self.type == "Bool":
            new_data = data
            if type(data) == type("") :
                if data == "False" or data == "false" or data == "0":
                    new_data = False
                else :
                    new_data = True
        elif self.type == "Byte":
            try :
                new_data = int(data)
            except :
                new_data = None
            if new_data != None:
                if new_data < 0 :
                    new_data = 0
                elif new_data > 255 :
                    new_data = 255
        elif self.type == "Decimal":
            try :
                new_data = float(data)
            except :
                new_data = None
        elif self.type == "Int":
            try :
                new_data = int(data)
            except :
                new_data = None
            if new_data != None:
                if new_data < -2147483648 :
                    new_data = -2147483648
                elif new_data > 2147483647 :
                    new_data = 2147483647
        elif self.type == "Short":
            try :
                new_data = int(data)
            except :
                new_data = None
            if new_data != None:
                if new_data < -32768 :
                    new_data = -32768
                elif new_data > 32767 :
                    new_data = 32767
        elif self.type == "String":
                new_data = data
        elif self.type == "Button":
            new_data = data
            if type(data) == type("") :
                if data == "False" or data == "false" or data == "0":
                    new_data = False
                else :
                    new_data = True
        elif self.type == "List":
            if type(data) == type("") :
                if data in self.data_items:
                    new_data = data
                else :
                    new_data = None
        return new_data

    @property
    def is_set(self):
        """
        Test whether the value has been set.

        :return: True if the value has actually been set by a status message
        from the device, rather than simply being the default.
        :rtype: bool

        """
        return self._network.manager.isValueSet(self.value_id)

    @property
    def is_read_only(self):
        """
        Test whether the value is read-only.

        :return: True if the value cannot be changed by the user.
        :rtype: bool

        """
        return self._network.manager.isValueReadOnly(self.value_id)

    @property
    def is_write_only(self):
        """
        Test whether the value is write-only.

        :return: True if the value can only be written to and not read.
        :rtype: bool

        """
        return self._network.manager.isValueWriteOnly(self.value_id)

    def enable_poll(self, intensity=1):
        """
        Enable the polling of a device's state.

        :param intensity: The intensity of the poll
        :type intensity: int
        :return: True if polling was enabled.
        :rtype: bool

        """
        self._poll_intensity = intensity
        return self._network.manager.enablePoll(self.value_id, intensity)

    def disable_poll(self):
        """
        Disable poll off this value.

        :return: True if polling was disabled.
        :rtype: bool

        """
        self._poll_intensity = 0
        return self._network.manager.disablePoll(self.value_id)

    @property
    def poll_intensity(self):
        """
        The poll intensity of the value.

        :returns: 0=none, 1=every time through the list, 2-every other time, etc
        :rtype: int

        """
        return self._poll_intensity

    @property
    def is_polled(self):
        """
        Verify that the value is polled.

        :rtype: bool

        """
        ret = self._network.manager.isPolled(self.value_id)
        if ret == False:
            self._poll_intensity = 0
        return ret

    @property
    def command_class(self):
        """
        The commandclass of the value.

        :returns: The command class of this value
        :rtype: int

        """
        return self._network.manager.getValueCommandClass(self.value_id)

    def refresh(self):
        """
        Refresh the value.

        :returns: True if the command was transmitted to controller
        :rtype: bool

        """
#        if self.is_outdated("self.data_as_string"):
#            self._as_string = self._network.manager.getValueAsString(self.value_id)
#            self.update("self.data_as_string")
#        return self._as_string
        return self._network.manager.refreshValue(self.value_id)
