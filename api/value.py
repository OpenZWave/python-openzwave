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
from openzwave.object import ZWaveObject

logging.getLogger('openzwave').addHandler(logging.NullHandler())

# TODO: don't report controller node as sleeping
# TODO: allow value identification by device/index/instance
class ZWaveValue(ZWaveObject):
    '''
    Represents a single value.
    Must be updated to use the cachedObject facilities.
    '''
    def __init__(self, value_id, network=None, parent_id=None, \
            command_class=0):
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
        self._parent_id = parent_id
        self._command_class = command_class
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

    @property
    def parent_id(self):
        """
        The parent_id of the value.
        """
        return self._parent_id

    @property
    def value_id(self):
        """
        The value_id of the value.
        """
        return self._object_id

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
        The type of the value.

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
        The genre of the value.

        :return: genre of the value (Basic, User, Config, System)
        :rtype: str

        """
#        if self.is_outdated("self.type"):
#            self._type = self._network.manager.getValueType(self.value_id)
#            self.update("self.type")
#        return self._type
        return self._network.manager.getValueGenre(self.value_id)

    @property
    def data(self):
        """
        The current data of the value.

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

        :param value: The new data value
        :type value: str

        """
        self._network.manager.setValue(self.value_id, value)
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

        :returns: The valid values
        :rtype: set()

        """
#        if self.is_outdated("self.data_items"):
#            self._data_items = self._network.manager.getValueListItems(self.value_id)
#            self.update("self.data_items")
#        return self._data_items
        return self._network.manager.getValueListItems(self.value_id)

    def check_data(self):
        """
        Check that data is correct for this value.
        Must be called

        :returns: The valid values
        :rtype: set()

        """
#        if self.is_outdated("self.data_items"):
#            self._data_items = self._network.manager.getValueListItems(self.value_id)
#            self.update("self.data_items")
#        return self._data_items
        return self._network.manager.getValueListItems(self.value_id)


#    @property
#    def poll_intensity(self):
#        """
#        The poll intensity of the value.
#
#        :rtype: int (0=none, 1=every time through the list, 2-every other time, etc)
#
#        """
#        return self._poll_intensity

    @property
    def is_polled(self):
        """
        Verify that the value is polled.

        :rtype: bool

        """
        return self._network.manager.isPolled(self.value_id)

    @property
    def is_set(self):
        """
        Test whether the value has been set.

        :returns: True if the value has actually been set by a status message
        from the device, rather than simply being the default.
        :rtype: bool

        """
        return self._network.manager.isValueSet(self.value_id)

    @property
    def is_read_only(self):
        """
        Test whether the value is read-only.

        :returns: True if the value cannot be changed by the user.
        :rtype: bool

        """
        return self._network.manager.isValueReadOnly(self.value_id)

    @property
    def is_write_only(self):
        """
        Test whether the value is write-only.

        :returns: True if the value can only be written to and not read.
        :rtype: bool

        """
        return self._network.manager.isValueWriteOnly(self.value_id)

    def enable_poll(self, intensity):
        """
        Enable poll off this value.

        :rtype: bool

        """
#        self._poll_intensity = intensity
        return self._network.manager.enablePoll(self.value_id, intensity)

    def disable_poll(self, intensity):
        """
        Disable poll off this value.

        :rtype: bool

        """
#        self._poll_intensity = 0
        return self._network.manager.disablePoll(self.value_id)

    @property
    def value_id(self):
        """
        The id of the value.

        :rtype: int

        """
        return self._object_id

    @property
    def command_class(self):
        """
        The commandclass of the value.

        :rtype: int

        """
        return self._command_class

    @command_class.setter
    def command_class(self, value):
        """
        Set the command_class of the value.

        :param value: The new command_class value
        :type value: int

        """
        self._command_class = value

#    def get_value(self, key):
#        """
#        The value_data of the value.
#
#        :param key: The key to check
#        :type value: int
#
#        """
#        return self.value_data[key] if self._value_data.has_key(key) else None

    def __str__(self):
        return 'home_id: [{0}]  parent_id: [{1}]  value_data: {2}'.format(self.home_id, self._parent_id, self._value_data)
