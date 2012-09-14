# -*- coding: utf-8 -*-
"""
.. module:: openzwave.value

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
import libopenzwave
import openzwave
import logging
from openzwave.object import ZwaveObject

logging.getLogger('openzwave').addHandler(logging.NullHandler())

# TODO: don't report controller node as sleeping
# TODO: allow value identification by device/index/instance
class ZWaveValue(ZwaveObject):
    '''
    Represents a single value.
    Must be updated to use the cachedObject facilities.
    '''
    def __init__(self, value_id, network=None, node_id=None):
        '''
        Initialize value

        n['valueId'] = {'home_id' : v.GetHomeId(),
                'node_id' : v.GetNodeId(),
                'commandClass' : PyManager.COMMAND_CLASS_DESC[v.GetCommandClassId()],
                'instance' : v.GetInstance(),
                'index' : v.GetIndex(),
                'id' : v.GetId(),
                'genre' : PyGenres[v.GetGenre()],
                'type' : PyValueTypes[v.GetType()],
#                    'value' : value.c_str(),
                'value' : getValueFromType(manager,v.GetId()),
                'label' : label.c_str(),
                'units' : units.c_str(),
                'readOnly': manager.IsValueReadOnly(v),
                }

        :param valueId: ID of the value
        :type valueId: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork
        :param nodeid: ID of node
        :type nodeid: int

        '''
        ZwaveObject.__init__(value_id, network)
        logging.debug("Create object value (valueId:%s)" % (value_id))
        self._node_id = node_id
        #self._value_data = value_data
        #self.n = valueId
        #self._values = dict()
        self._label = None
        self.cache_property(lambda: self.label)
        self._help = None
        self.cache_property(lambda: self.help)
        self._min = None
        self.cache_property(lambda: self.min)
        self._max = None
        self.cache_property(lambda: self.max)
        self._units = None
        self.cache_property(lambda: self.units)
        self._poll_intensity = None
        self.cache_property(lambda: self.poll_intensity)
        self._as_string = None
        self.cache_property(lambda: self.as_string)
        self._data = None
        self.cache_property(lambda: self.data)

    @property
    def node_id(self):
        """
        The node_id of the value.
        """
        return self._node_id

    @property
    def label(self):
        """
        The label of the value.

        :rtype: str

        """
        if self.is_outdated(lambda: self.label):
            self._label = self._network.manager.getValueLabel(self.object_id)
            self.update(lambda: self.label)
        return self._label

    @label.setter
    def label(self, value):
        """
        Set the label of the value.

        :param value: The new label value
        :type value: str

        """
        self._network.manager.setValueLabel(self.object_id, value)
        self.outdate(lambda: self.label)

    @property
    def help(self):
        """
        The help of the value.

        :rtype: str

        """
        if self.is_outdated(lambda: self.help):
            self._help = self._network.manager.getValueHelp(self.object_id)
            self.update(lambda: self.help)
        return self._help

    @help.setter
    def help(self, value):
        """
        Set the help of the value.

        :param value: The new help value
        :type value: str

        """
        self._network.manager.setValueHelp(self.object_id, value)
        self.outdate(lambda: self.help)

    @property
    def units(self):
        """
        The units of the value.

        :rtype: str

        """
        if self.is_outdated(lambda: self.units):
            self._units = self._network.manager.getValueUnits(self.object_id)
            self.update(lambda: self.units)
        return self._units

    @units.setter
    def units(self, value):
        """
        Set the units of the value.

        :param value: The new units value
        :type value: str

        """
        self._network.manager.setValueUnits(self.object_id, value)
        self.outdate(lambda: self.units)

    @property
    def max(self):
        """
        The max of the value.

        :rtype: int

        """
        if self.is_outdated(lambda: self.max):
            self._max = self._network.manager.getValueMax(self.object_id)
            self.update(lambda: self.max)
        return self._min

    @property
    def min(self):
        """
        The min of the value.

        :rtype: int

        """
        if self.is_outdated(lambda: self.min):
            self._min = self._network.manager.getValueMin(self.object_id)
            self.update(lambda: self.min)
        return self._min

    @property
    def as_string(self):
        """
        The value as String.

        :rtype: str

        """
        if self.is_outdated(lambda: self.asString):
            self._as_string = self._network.manager.getValueAsString(self.object_id)
            self.update(lambda: self.as_string)
        return self._as_string

    @property
    def data(self):
        """
        The data of the value.

        :rtype: depending of the type of the value

        """
        if self.is_outdated(lambda: self.data):
            self._data = self._network.manager.getValue(self.object_id)
            self.update(lambda: self.data)
        return self._data

    @data.setter
    def data(self, value):
        """
        Set the data of the value.

        :param value: The new data value
        :type value: str

        """
        self._network.manager.setValue(self.object_id, value)
        self.outdate(lambda: self.data)

    @property
    def poll_intensity(self):
        """
        The poll intensity of the value.

        :rtype: int (0=none, 1=every time through the list, 2-every other time, etc)

        """
        return self._poll_intensity

    @data.setter
    def poll_intensity(self, value):
        """
        Set the poll intensity of the value (0=none, 1=every time through the list, 2-every other time, etc)

        :param value: The new poll intensity of the value
        :type value: int

        """
        self._poll_intensity = value
        self._network.manager.SetPollIntensity(self.object_id, value)

    def is_polled(self):
        """
        Verify that the value is polled.

        :rtype: bool

        """
        return self._network.manager.isPolled(self.object_id)

    def get_value(self, key):
        """
        The value_data of the value.

        :param key: The key to check
        :type value: int

        """
        return self.value_data[key] if self._value_data.has_key(key) else None

    def __str__(self):
        return 'home_id: [{0}]  node_id: [{1}]  value_data: {2}'.format(self._home_id, self._node_id, self._value_data)
